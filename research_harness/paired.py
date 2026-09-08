"""Matched conditions with fresh state, an explicit order, and persistent pair status."""
from __future__ import annotations
import copy
import json
import tempfile
import uuid
from pathlib import Path
from .session import RunSession, write_json
from .model_gateway import MockTransport, RunStopped, utc_now
from .demo_transport import DemoTransport, StressTransport
from .hashing import sha256_file
from .live import Budget, request_bound, verify_route
from .analysis import rows

ROOT=Path(__file__).resolve().parents[1]


def catalog():
    return json.loads((ROOT/'data/demo/catalog.json').read_text())


def verify_freeze():
    frozen=json.loads((ROOT/'research/a0_a1_freeze_manifest.json').read_text())
    checks={frozen['scenario']['path']:frozen['scenario']['sha256'],
            frozen['skill']['provider_neutral_path']:frozen['skill']['provider_neutral_sha256']}
    checks.update({value['config_path']:value['config_sha256'] for value in frozen['conditions'].values()})
    for path, digest in checks.items():
        if sha256_file(ROOT/path)!=digest:raise RunStopped(f'Frozen file changed: {path}')
    from .runner import render_prompt
    from sim import pm_bench as PM
    scenario = json.loads((ROOT/frozen['scenario']['path']).read_text())
    for condition, item in frozen['conditions'].items():
        cfg = json.loads((ROOT/item['config_path']).read_text())
        _, metadata = render_prompt(ROOT/cfg['prompt']['base_path'], ROOT/cfg['prompt']['addendum_path'] if cfg['prompt'].get('addendum_path') else None, PM.list_state_channels(scenario), False)
        if metadata['effective_prompt_sha256'] != item['effective_prompt_sha256']:
            raise RunStopped('Frozen effective prompt changed: '+condition)
    from scripts.verify_benchmark_integrity import verify_manifest
    errors=verify_manifest(ROOT/'research/protected_hashes.json')
    if errors:raise RunStopped('Protected integrity failed: '+errors[0])
    for manifest_name in ['pilot_freeze_v1.json','demo_freeze_v1.json']:
        manifest=json.loads((ROOT/'research'/manifest_name).read_text())
        for path,digest in manifest['files'].items():
            if sha256_file(ROOT/path)!=digest:raise RunStopped(f'Frozen input changed: {path}')
    return frozen


def configs(suite='development', scenario_id=None, mode='MOCK'):
    verify_freeze()
    spec=next((s for s in catalog() if s['id']==scenario_id),None) if suite=='demo' else None
    if suite=='demo' and not spec:raise ValueError('Choose an existing demo scenario.')
    result={}
    for condition in ['A0','A1']:
        prefix='pilot' if suite=='pilot' else 'dev'
        cfg=json.loads((ROOT/f'configs/{prefix}_{condition.lower()}_deepseek_v31.yaml').read_text())
        if spec:
            cfg['scenario']=spec['path'];cfg['benchmark_split']='educational-demo-v1-not-held-out'
            cfg['benchmark_commit']='not-applicable-codex-authored-demo'
            cfg['experiment_id']=f'demo-{scenario_id}-{condition.lower()}-v1'
        if mode=='MOCK':
            cfg['model'].update(provider='mock',route='local-scripted',model_id='mock/educational-script-v1' if spec else 'mock/noop-v1')
            cfg['execution']['allow_paid']=False
        result[condition]=cfg
    a,b=copy.deepcopy(result['A0']),copy.deepcopy(result['A1'])
    for cfg in [a,b]:
        for key in ['condition','experiment_id']:cfg.pop(key)
        cfg['prompt'].pop('addendum_path')
    if a!=b:raise RunStopped('A0/A1 settings differ beyond the intervention and bookkeeping.')
    return result,spec


def estimate_pair(configurations):
    prices=configurations['A0']['model']['pricing_usd_per_million_tokens']
    total=0.0;attempts=0
    with tempfile.TemporaryDirectory(prefix='kiodai-preflight-') as temp:
        temp=Path(temp)
        for condition,cfg in configurations.items():
            mock=copy.deepcopy(cfg);mock['model']['provider']='mock';mock['execution']['allow_paid']=False
            file=temp/f'{condition}.json';write_json(file,mock)
            session=RunSession(file,output_root=temp/'runs',transport=StressTransport())
            while session.status=='running':session.advance()
            if not session.status.startswith('completed'):raise RunStopped('Offline cost preflight interrupted.')
            for call in rows(session.run_dir/'raw_model_calls.jsonl'):
                request=call['request'];request['provider']='openrouter'
                total+=request_bound(request,prices);attempts+=1
    return {'conservative_pair_estimate_usd':total,'maximum_attempts':attempts,
            'estimator':'padded request bytes/4 * 1.6 input tokens; 256 output tokens every attempt; one tool query and one malformed retry per interaction',
            'billable':False,'guaranteed_billing_cap':False}


class Pair:
    def __init__(self, *, suite='demo', scenario_id='time', mode='MOCK', output_root=None,
                 live=False, budget_usd=None, budget=None, repeat=0):
        if mode not in ['MOCK','LIVE']:raise ValueError('New pairs must be MOCK or LIVE.')
        if mode=='LIVE' and not live:raise RunStopped('LIVE requires explicit --live opt-in.')
        cfgs,spec=configs(suite,scenario_id,mode)
        root=Path(output_root or ROOT/'results/kiodai').resolve()
        self.pair_id=f'{mode.lower()}-pair-{uuid.uuid4().hex[:12]}'
        self.path=root/self.pair_id;self.path.mkdir(parents=True,exist_ok=False)
        self.mode=mode;self.repeat=repeat;self.index=0;self.sessions={}
        self.order=['A0','A1'] if repeat%2==0 else ['A1','A0']
        self.plan={'schema_version':2,'pair_id':self.pair_id,'mode':mode,'suite':suite,
                   'scenario_id':scenario_id if spec else 'first-development-day-pilot-v1' if suite=='pilot' else 'frozen-development-v1',
                   'provenance':spec['provenance'] if spec else 'Recovered frozen development suite, authored during prior implementation; not blind OOD.',
                   'scenario_sha256':sha256_file(ROOT/cfgs['A0']['scenario']),
                   'freeze_manifest_sha256':sha256_file(ROOT/'research/a0_a1_freeze_manifest.json'),
                   'repeat':repeat,'seed':cfgs['A0']['sampling'].get('seed'),'order':self.order,
                   'execution_schedule':'A0/A1 interleaved one scheduled step at a time; alternate first condition by repeat',
                   'started_at_utc':utc_now(),'status':'preparing','runs':{},'completed_timeline_steps':0,
                   'budget_ceiling_usd':budget_usd if mode=='LIVE' else 0.0,
                   'analysis_plan':'Official trajectory Set-F1; paired differences; average repeats within scenario before averaging scenarios. No step-level independent samples. Include failures; label incomplete pairs.',
                   'stopping_rules':'Reserve full paired stress estimate before inference. At most one corrective retry per interaction; separate one transport retry; stop pair on repeated transport failure, route mismatch, exhausted budget, reset, or interruption.',
                   'runtime_configurations':cfgs}
        self.save()
        try:
            route=None
            if mode=='LIVE':
                budget=budget or Budget(budget_usd,cfgs['A0']['model']['pricing_usd_per_million_tokens'])
                estimate=estimate_pair(cfgs);self.plan['preflight']=estimate;self.save()
                budget.require(estimate['conservative_pair_estimate_usd'])
                route=verify_route(cfgs['A0']);self.plan['route_preflight']=route;self.save()
            for condition in self.order:
                file=self.path/f'{condition}-config.json';write_json(file,cfgs[condition])
                transport=(DemoTransport(spec['script']) if spec else MockTransport()) if mode=='MOCK' else None
                session=RunSession(file,allow_paid=live,output_root=self.path,transport=transport,
                                   budget=budget,budget_usd=budget_usd,pair_id=self.pair_id,repeat=repeat,route_preflight=route)
                self.sessions[condition]=session;self.plan['runs'][condition]=session.run_dir.name
            self.plan['status']='running';self.save()
        except (Exception,KeyboardInterrupt) as exc:
            from .model_gateway import safe_error
            self.interrupt(safe_error(exc));raise

    def save(self):write_json(self.path/'pair.json',self.plan)

    def advance(self):
        if self.plan['status']!='running':return
        for condition in self.order:
            session=self.sessions[condition]
            session.advance()
            if session.status=='interrupted':
                self.interrupt(session.manifest.get('interruption_reason','Run interrupted'));return
        self.index+=1;self.plan['completed_timeline_steps']=self.index
        if all(s.status.startswith('completed') for s in self.sessions.values()):
            self.plan['status']='completed';self.plan['finished_at_utc']=utc_now()
        self.save()

    def interrupt(self,reason='User reset'):
        for session in self.sessions.values():session.interrupt(reason)
        if self.plan['status']!='completed':
            self.plan.update(status='interrupted',interruption_reason=reason,finished_at_utc=utc_now())
        self.save()

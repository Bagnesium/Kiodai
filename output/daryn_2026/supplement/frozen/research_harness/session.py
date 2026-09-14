"""One incremental runner used by CLI and dashboard; evaluator artifacts stay separate."""
from __future__ import annotations
import json
import subprocess
import sys
import importlib.metadata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from .config import load_config, validate_runtime_config
from .hashing import sha256_file
from .model_gateway import ActionSelector, RunStopped, safe_error, utc_now
from . import runner
from sim import pm_bench as PM


def write_json(path, value):
    temp = path.with_suffix(path.suffix + '.tmp')
    temp.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n')
    temp.replace(path)


def append_json(path, value):
    with path.open('a') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + '\n')


class RunSession:
    def __init__(self, config_path, *, allow_paid=False, output_root=None, transport=None,
                 budget_usd=None, budget=None, pair_id=None, repeat=0, route_preflight=None):
        self.config_path = Path(config_path).resolve()
        self.config, self.hashes = load_config(self.config_path, runner.PROJECT_ROOT)
        validate_runtime_config(self.config, allow_paid)
        self.mode = 'MOCK' if self.config['model']['provider'] == 'mock' else 'LIVE'
        self.budget = budget
        if self.mode == 'LIVE':
            from .live import Budget, BudgetedTransport, verify_route
            if transport is not None:
                raise RunStopped('LIVE does not accept injected or mock transports.')
            self.budget = budget or Budget(budget_usd, self.config['model']['pricing_usd_per_million_tokens'])
            route_preflight = route_preflight or verify_route(self.config)
            transport = BudgetedTransport(self.config, self.budget)
        else:
            transport = transport or runner.build_transport(self.config)
        self.transport = transport
        self.scenario_path = Path(self.config['scenario'])
        self.scenario = PM.load_scenario(str(self.scenario_path))
        self.channels = PM.list_state_channels(self.scenario)
        prompt = self.config['prompt']
        self.system_prompt, self.prompt_metadata = runner.render_prompt(
            Path(prompt['base_path']), Path(prompt['addendum_path']) if prompt.get('addendum_path') else None,
            self.channels, self.config['execution'].get('show_task_legend', False))
        self.run_id = f"{self.mode.lower()}-{self.config['condition']}-{datetime.now(timezone.utc):%Y%m%dT%H%M%S}-{uuid.uuid4().hex[:8]}"
        self.run_dir = Path(output_root or self.config['output']['root']).resolve() / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=False)
        self.manifest_path = self.run_dir / 'manifest.json'
        for name in ['raw_model_calls.jsonl', 'failures.jsonl', 'actions.jsonl', 'steps.jsonl', 'evaluator.jsonl']:
            (self.run_dir / name).touch()
        # Save exact local inputs; no private manuscript enters a run.
        (self.run_dir / 'scenario.json').write_bytes(self.scenario_path.read_bytes())
        write_json(self.run_dir / 'config.json', self.config)
        (self.run_dir / 'system_prompt.txt').write_text(self.system_prompt)
        (self.run_dir / 'baseline_template.txt').write_bytes(Path(prompt['base_path']).read_bytes())
        if prompt.get('addendum_path'):
            (self.run_dir / 'addendum.txt').write_bytes(Path(prompt['addendum_path']).read_bytes())
        commit, dirty = runner._git_state(runner.PROJECT_ROOT)
        git_status = subprocess.check_output(['git','status','--porcelain'], cwd=runner.PROJECT_ROOT, text=True)
        source_hashes = {str(p.relative_to(runner.PROJECT_ROOT)): sha256_file(p)
                         for folder in ['research_harness','demo','scripts']
                         for p in (runner.PROJECT_ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in p.parts}
        try:
            sdk_version = importlib.metadata.version('openai')
        except importlib.metadata.PackageNotFoundError:
            sdk_version = None
        self.manifest = {
            'runtime': {'python':sys.version, 'openai_sdk':sdk_version},
            'schema_version': 2, 'mode': self.mode, 'experiment_id': self.config['experiment_id'],
            'run_id': self.run_id, 'pair_id': pair_id, 'repeat': repeat, 'condition': self.config['condition'],
            'git_commit': commit, 'git_dirty': dirty, 'git_status': git_status, 'implementation_hashes': source_hashes,
            'benchmark_commit': self.config.get('benchmark_commit'), 'benchmark_hash': sha256_file(self.scenario_path),
            'evaluator_hash': sha256_file(runner.PROJECT_ROOT/'sim/pm_bench.py'),
            'configuration_hash': self.hashes['config_file_sha256'],
            'resolved_configuration_hash': self.hashes['resolved_config_sha256'],
            'prompt_hash': self.prompt_metadata['effective_prompt_sha256'], 'prompt': self.prompt_metadata,
            'model_provider': self.config['model']['provider'], 'provider_route': self.config['model'].get('route'),
            'provider_quantizations': self.config['model'].get('quantizations', []),
            'route_fallbacks_allowed': self.config['model'].get('allow_route_fallbacks', False),
            'provider_require_parameters': self.config['model'].get('require_parameters', False),
            'exact_model_id': self.config['model']['model_id'], 'generation_parameters': self.config['sampling'],
            'temperature': self.config['sampling'].get('temperature'), 'top_p': self.config['sampling'].get('top_p'),
            'maximum_output_tokens': self.config['limits']['max_output_tokens'],
            'context_limit': self.config['limits']['max_context_tokens'], 'random_seed': self.config['sampling'].get('seed'),
            'retry_settings': {'max_retries': min(1,self.config['limits']['max_retries']), 'total_attempts_per_call': min(1,self.config['limits']['max_retries'])+1, 'transport': 'retry once without corrective message; interrupt on repeated transport failure', 'malformed': 'one schema-only corrective retry, then empty action set'},
            'timeout_seconds': self.config['limits']['timeout_seconds'],
            'tool_permissions': {'state_query_channels': self.channels, 'max_tool_calls_per_step': self.config['limits']['max_tool_calls_per_step'], 'network_enabled': self.mode == 'LIVE'},
            'heartbeat_enabled': False, 'benchmark_split': self.config['benchmark_split'],
            'scenario_ids': [{'day': d['name'], 'step_ids':[s['id'] for s in d['steps']]} for d in self.scenario['days']],
            'started_at_utc': utc_now(), 'finished_at_utc': None,
            'route_preflight': route_preflight, 'excluded_run_count': 0, 'exclusion_reasons': [],
            'raw_output_locations': {key: str(self.run_dir / filename) for key,filename in {'actions':'actions.jsonl','raw_model_calls':'raw_model_calls.jsonl','failures':'failures.jsonl','score':'score.json','manifest':'manifest.json','evaluator':'evaluator.jsonl','steps':'steps.jsonl'}.items()},
        }
        self.status = 'running'
        self.actions = []
        self.steps = []
        self.total_steps = sum(len(d['steps']) for d in self.scenario['days'])
        self.selector = ActionSelector(transport, self.run_dir/'raw_model_calls.jsonl', self.config['model'], self.config['sampling'], self.config['limits'])
        self.iterator = runner.iter_environment(scenario=self.scenario, system_prompt=self.system_prompt,
            selector=self.selector, config=self.config, allowed_channels=self.channels,
            state_visibility=PM.normalize_state_visibility(self.scenario), state_channels=PM.normalize_state_channels(self.scenario),
            failure_path=self.run_dir/'failures.jsonl')
        self.save()

    def advance(self):
        if self.status != 'running':
            return None
        try:
            step = next(self.iterator)
            self.actions.append(step['action'])
            evaluator = step.pop('evaluator')
            evaluator.update({'mode':self.mode,'day':step['day'],'step_id':step['step_id']})
            step['mode'] = self.mode
            self.steps.append(step)
            append_json(self.run_dir/'actions.jsonl', step['action'])
            append_json(self.run_dir/'steps.jsonl', step)
            append_json(self.run_dir/'evaluator.jsonl', evaluator)
            if len(self.actions) == self.total_steps:
                self.status = 'completed_with_failures' if (self.run_dir/'failures.jsonl').stat().st_size else 'completed'
            self.save()
            return step
        except (Exception, KeyboardInterrupt) as exc:
            self.status = 'interrupted'
            self.manifest['interruption_reason'] = safe_error(exc)
            self.save()
            return None

    def interrupt(self, reason='Stopped/reset by user'):
        if self.status == 'running':
            self.status = 'interrupted'
            self.manifest['interruption_reason'] = reason
            self.save()

    def save(self):
        from .analysis import accounting, score_artifacts
        self.manifest.update({'status':self.status,'completed_steps':len(self.actions),'total_steps':self.total_steps})
        if self.status != 'running':
            self.manifest['finished_at_utc'] = utc_now()
        counts = accounting(self.run_dir/'raw_model_calls.jsonl', self.mode, self.config['model'].get('pricing_usd_per_million_tokens', {}))
        failures = [json.loads(s) for s in (self.run_dir/'failures.jsonl').read_text().splitlines()]
        self.manifest.update(counts)
        self.manifest.update({'failed_run_count':int(bool(failures) or self.status=='interrupted'), 'failed_action_count':len(failures), 'failure_records':failures, 'budget':self.budget.snapshot() if self.budget else None})
        if self.status.startswith('completed'):
            score = score_artifacts(self.run_dir)
            write_json(self.run_dir/'score.json', score)
            self.manifest['aggregate_metrics'] = score['summary']
        else:
            self.manifest['aggregate_metrics'] = None
        self.manifest['artifact_sha256'] = {p.name:sha256_file(p) for p in self.run_dir.iterdir() if p.is_file() and p.name != 'manifest.json' and not p.name.endswith('.tmp')}
        write_json(self.manifest_path, self.manifest)

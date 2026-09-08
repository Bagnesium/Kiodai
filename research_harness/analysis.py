"""Deterministic reconstruction; no inference and no mock/live pooling."""
from __future__ import annotations
import json
from pathlib import Path
from statistics import mean
from sim import pm_bench as PM
from .hashing import sha256_file


def rows(path):
    return [json.loads(s) for s in Path(path).read_text().splitlines() if s.strip()]


def rates(summary):
    tp, fp, fn = (summary[k] for k in ['set_tp','set_fp','set_fn'])
    return {'precision':tp/(tp+fp) if tp+fp else None,
            'recall':tp/(tp+fn) if tp+fn else None,
            'set_f1':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}


def accounting(path, mode, prices):
    calls = rows(path)
    def total(key):
        if mode == 'MOCK' or not calls or any(c.get('usage',{}).get(key) is None for c in calls):
            return None
        return sum(c['usage'][key] for c in calls)
    inputs, outputs = total('input_tokens'), total('output_tokens')
    costs = [(c.get('provider_metadata') or {}).get('cost_usd_reported') for c in calls]
    reported = 0.0 if mode == 'MOCK' else sum(costs) if calls and all(isinstance(c,(int,float)) for c in costs) else None
    estimated = 0.0 if mode == 'MOCK' else ((inputs*prices['input']+outputs*prices['output'])/1e6 if inputs is not None and outputs is not None and prices else None)
    return {'token_usage': {'input_tokens': inputs, 'output_tokens': outputs, 'total_tokens':inputs+outputs if inputs is not None and outputs is not None else None, 'model_call_attempts':len(calls)},
            'mock_token_estimates': {'input_tokens':sum((c.get('usage') or {}).get('input_tokens',0) for c in calls),'output_tokens':sum((c.get('usage') or {}).get('output_tokens',0) for c in calls)} if mode=='MOCK' else None,
            'estimated_cost_usd':estimated, 'reported_cost_usd':reported,
            'model_reported_versions':sorted({c['reported_model'] for c in calls if c.get('reported_model')}),
            'invalid_attempt_count':sum(bool(c.get('parse_error')) for c in calls),
            'transport_error_count':sum(bool(c.get('transport_error')) for c in calls),
            'retry_count':sum(c['attempt']>1 for c in calls),
            'model_latency_seconds':sum(c['latency_seconds'] for c in calls) if mode=='LIVE' and calls else None,
            'transport_latency_seconds':sum(c['latency_seconds'] for c in calls)}


def score_artifacts(run_dir):
    run_dir = Path(run_dir)
    scenario = json.loads((run_dir/'scenario.json').read_text())
    actions = rows(run_dir/'actions.jsonl')
    summary, days, n = PM.score_log(scenario, actions)
    return {'summary':summary,'per_day':days,'summary_steps':n,'rates':rates(summary),
            'official_evaluator':'sim.pm_bench.score_log',
            'zero_denominator':'unavailable (official display: n/a); never coerce to zero or one'}


def verify_run(run_dir):
    run_dir = Path(run_dir)
    manifest = json.loads((run_dir/'manifest.json').read_text())
    for name, digest in manifest.get('artifact_sha256', {}).items():
        if Path(name).name != name or sha256_file(run_dir/name) != digest:
            raise ValueError('Saved artifact hash mismatch: '+name)
    if sha256_file(run_dir/'scenario.json') != manifest['benchmark_hash']:
        raise ValueError('Saved scenario hash mismatch')
    if sha256_file(run_dir/'system_prompt.txt') != manifest['prompt_hash']:
        raise ValueError('Saved prompt hash mismatch')
    if sha256_file(Path(__file__).resolve().parents[1]/'sim/pm_bench.py') != manifest['evaluator_hash']:
        raise ValueError('Scorer hash mismatch')
    if manifest['status'].startswith('completed'):
        score = score_artifacts(run_dir)
        if score != json.loads((run_dir/'score.json').read_text()):
            raise ValueError('Saved score differs from official reconstruction')
        if score['summary'] != manifest['aggregate_metrics']:
            raise ValueError('Manifest metrics differ from reconstruction')
    return manifest


def analyze(root, mode='LIVE'):
    root = Path(root)
    manifests=[]
    for path in sorted(root.rglob('manifest.json')):
        data=json.loads(path.read_text())
        if data.get('schema_version')==2 and data.get('mode')==mode:
            manifest=verify_run(path.parent)
            manifest['_path']=str(path)
            manifests.append(manifest)
    groups={}
    for m in manifests:
        if m.get('pair_id'):
            groups.setdefault(m['pair_id'],[]).append(m)
    paired=[]; incomplete=[]
    for path in sorted(root.rglob('pair.json')):
        plan=json.loads(path.read_text())
        if plan.get('mode')==mode and plan.get('pair_id') not in groups:
            incomplete.append(plan['pair_id'])
    for pair_id, members in sorted(groups.items()):
        conditions={m['condition']:m for m in members}
        if len(members)!=2 or set(conditions)!={'A0','A1'} or any(not m['status'].startswith('completed') for m in members):
            incomplete.append(pair_id);continue
        a,b=conditions['A0'],conditions['A1']
        if a['benchmark_hash']!=b['benchmark_hash']:
            raise ValueError('Pair scenario mismatch')
        shared=['exact_model_id','model_provider','provider_route','provider_quantizations','route_fallbacks_allowed','provider_require_parameters','generation_parameters','maximum_output_tokens','context_limit','random_seed','retry_settings','timeout_seconds','tool_permissions','heartbeat_enabled','benchmark_split','evaluator_hash']
        if any(a.get(k)!=b.get(k) for k in shared):
            raise ValueError('Pair experimental controls differ')
        if a['prompt']['base_prompt_file_sha256']!=b['prompt']['base_prompt_file_sha256'] or a['prompt']['addendum_present'] or not b['prompt']['addendum_present']:
            raise ValueError('Pair intervention mismatch')
        f0,f1=rates(a['aggregate_metrics'])['set_f1'],rates(b['aggregate_metrics'])['set_f1']
        paired.append({'pair_id':pair_id,'scenario_sha256':a['benchmark_hash'],'repeat':a['repeat'],
                       'a0_f1':f0,'a1_f1':f1,'difference':f1-f0 if f1 is not None and f0 is not None else None})
    by_scenario={}
    for pair in paired:
        by_scenario.setdefault(pair['scenario_sha256'],[]).append(pair)
    averaged=[{'scenario_sha256':key,'paired_repeats':len(value),
               'mean_difference':mean([p['difference'] for p in value]) if all(p['difference'] is not None for p in value) else None}
              for key,value in sorted(by_scenario.items())]
    differences=[s['mean_difference'] for s in averaged]
    return {'mode':mode,'runs':manifests,'pairs':paired,'incomplete_pairs':incomplete,
            'unpaired_runs':[m['run_id'] for m in manifests if not m.get('pair_id')],
            'scenario_averages':averaged,'mean_paired_difference':mean(differences) if differences and all(d is not None for d in differences) else None,
            'analysis_unit':'whole scenario/trajectory; average repeats within scenarios first; days and steps are not independent samples'}


def report(result):
    mode=result['mode']
    lines=[f'# Kiodai results — {mode}', '',
           'Scripted software demonstration only. These are NOT measured model-performance results.' if mode=='MOCK' else 'Genuine saved inference artifacts only; no mock data included.', '']
    if not result['runs']:
        lines += ['Live A0/A1 evaluation has not yet run. No measured effect, token usage, latency, or billed cost is available.', '']
    else:
        lines+=['| Mode | Condition | Status | TP | FP | FN | Precision | Recall | Set-F1 | Invalid | Retries | Tools | Reported USD |', '|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|']
        for m in result['runs']:
            s=m.get('aggregate_metrics');r=rates(s) if s else {}
            def fmt(x): return 'unavailable' if x is None else f'{x:.4f}'
            fields=[mode,m['condition'],m['status']]+[str(s[k]) if s else 'unavailable' for k in ['set_tp','set_fp','set_fn']]+[fmt(r.get(k)) for k in ['precision','recall','set_f1']]+[str(m['invalid_attempt_count']),str(m['retry_count']),str(s['state_query_calls']) if s else 'unavailable',fmt(m['reported_cost_usd'])]
            lines.append('| '+' | '.join(fields)+' |')
        lines += ['', '| Condition | Cancellation/update violations | Duplicates (commission) | Late actions | Tokens | Model latency s | Estimated USD |', '|---|---:|---:|---:|---|---|---|']
        for m in result['runs']:
            s=m.get('aggregate_metrics') or {}
            cells=[m['condition'],s.get('update_violation'),s.get('commission'),s.get('late'),m['token_usage']['total_tokens'],m['model_latency_seconds'],m['estimated_cost_usd']]
            lines.append('| '+' | '.join('unavailable' if c is None else str(c) for c in cells)+' |')
        lines+=['','Run artifacts:']+[f"- `{m['_path']}`" for m in result['runs']]
    lines+=['',f"Complete pairs: {len(result['pairs'])}. Incomplete pairs: {len(result['incomplete_pairs'])}.",
            f"Mean scenario-level paired Set-F1 difference: {result['mean_paired_difference'] if result['mean_paired_difference'] is not None else 'unavailable'}.",
            '',result['analysis_unit']+'.',
            'No confidence intervals or significance claims for this tiny pilot. Missing and zero-denominator values remain unavailable.',
            'Official detailed scores include lifecycle violations, late actions, duplicates (commission), and per-day counts. Token, latency and cost details are in each manifest. Mock token values are estimates, not measurements.', '']
    return '\n'.join(lines)

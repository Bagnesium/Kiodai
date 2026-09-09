"""Post-selection, evaluator-side analysis from immutable saved records."""
import json
from pathlib import Path
from sim import pm_bench as PM
from .common import dump, rows
from .runner import verify_case


def metrics(tp, fp, fn):
    return {'tp': tp, 'fp': fp, 'fn': fn,
            'precision': tp/(tp+fp) if tp+fp else None,
            'recall': tp/(tp+fn) if tp+fn else None,
            'set_f1': 2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else None}


def analyze_case(folder):
    folder = Path(folder)
    manifest = verify_case(folder)
    scenario = json.loads((folder/'scenario.json').read_text())
    official = PM.score_log(scenario, rows(folder/'actions.jsonl'))
    if json.loads(json.dumps(official)) != json.loads((folder/'score.json').read_text()):
        raise ValueError('Saved official score does not reproduce')
    summary = official[0]
    calls = [r for r in rows(folder/'calls.jsonl') if r['event'] == 'response']
    requests = [r for r in rows(folder/'calls.jsonl') if r['event'] == 'request']
    steps = rows(folder/'steps.jsonl')
    trace = rows(folder/'agent.jsonl')
    native_false = []
    for step in steps:
        states = {r['id']: r for r in step['evaluator']['tasks']}
        for identifier in step['evaluator']['false']:
            state = states.get(identifier, {})
            native_false.append({'checkpoint': step['checkpoint'], 'task_id_evaluator_only': identifier,
                                 'status': state.get('status'), 'updated': state.get('updated')})
    hidden = []
    for step in steps:
        day = next(d for d in scenario['days'] if d['name'] == step['day'])
        current_step = next(s for s in day['steps'] if s['id'] == step['step_id'])
        records = [r for r in trace if r['checkpoint'] == step['checkpoint']]
        for task in day['tasks']:
            channel = task.get('cue_channel', 'narrative')
            if channel == 'narrative' or scenario.get('state_visibility', {}).get(channel, False):
                continue
            identifier = task['id']
            due = identifier in step['evaluator']['due_task_ids']
            selected = identifier in step['evaluator']['selected_task_ids']
            if not due and not selected:
                continue
            event_texts = [e['text'] for s in day['steps'] for e in s.get('state_events', {}).get(channel, []) if isinstance(e, dict) and e.get('id') == task.get('cue_id')]
            queried = [t for t in step['tools'] if t['channel'] == channel]
            query_supported = any(t in q['observation'] for q in queried for t in event_texts)
            visible_supported = any(t in current_step['text'] for t in event_texts)
            category = ('false_action' if not due else 'missed_action' if not selected else
                        'query_supported_hit' if query_supported else 'visible_supported_hit' if visible_supported else 'hit_without_identifiable_support')
            hidden.append({'checkpoint': step['checkpoint'], 'day': step['day'], 'step_id': step['step_id'],
                           'task_id_evaluator_only': identifier, 'channel': channel, 'due': due,
                           'selected': selected, 'category': category, 'queries': queried,
                           'visible_scene': current_step['text'],
                           'agent_trace_record_indices': [i+1 for i,r in enumerate(trace) if r in records]})
    def complete_sum(key):
        values = [(r.get('usage') or {}).get(key) for r in calls]
        return sum(values) if values and len(calls) == len(requests) and all(v is not None for v in values) else None
    costs = [(r.get('provider') or {}).get('cost_usd_reported') for r in calls]
    return {'path': str(folder), 'method': manifest['method'], 'mode': manifest['mode'],
            'status': manifest['status'], 'completed_steps': len(steps), 'planned_steps': manifest['planned_steps'],
            **metrics(summary['set_tp'], summary['set_fp'], summary['set_fn']),
            'official_metrics': summary, 'hidden_opportunities': hidden,
            'native_false_action_diagnostics': native_false,
            'canceled_actions': sum(r['status']=='canceled' for r in native_false),
            'false_actions_on_updated_tasks': sum(bool(r['updated']) for r in native_false),
            'superseded_versions_executed': 0 if manifest['method'] in ('A2','B_ledger') else None,
            'duplicate_side_effects_native': None,
            'premature_actions_native': summary['commission'],
            'lifecycle_note': 'Superseded-version exclusion is an enforced code invariant. Native commission follows the official scorer. Native duplicate side effects are unidentifiable because completed handles disappear. Separate local lifecycle tests establish only simulator idempotency.',
            'hidden_due_opportunities': sum(h['due'] for h in hidden),
            'hidden_hits': sum(h['due'] and h['selected'] for h in hidden),
            'model_calls': len(requests), 'invalid_responses': sum(bool(r['validation_error']) for r in calls),
            'transport_errors': sum(bool(r['transport_error']) for r in calls),
            'interrupted_requests': len(requests)-len(calls),
            'retries': sum(r['attempt'] > 1 for r in requests),
            'tool_queries': sum(len(s['tools']) for s in steps),
            'input_tokens': complete_sum('input_tokens'), 'output_tokens': complete_sum('output_tokens'),
            'latency_seconds': sum(r['latency_seconds'] for r in calls),
            'api_response_cost_usd': sum(costs) if costs and len(requests) == len(calls) and all(c is not None for c in costs) else None,
            'verified_billed_cost_usd': None,
            'execution_receipts': [e for s in steps for e in s['execution']],
            'lifecycle_outcomes': [item['status'] for item in json.loads((folder/'memory.json').read_text()).values()]}


def report(study_dir):
    root = Path(study_dir)
    study = json.loads((root/'study.json').read_text())
    cases = []
    pairs = []
    for item in study['runs']:
        folder = root/item['folder']
        if not (folder/'manifest.json').exists():
            continue
        result = analyze_case(folder)
        result.update(trajectory=item['trajectory'], family=item['family'])
        cases.append(result)
    for trajectory in dict.fromkeys(c['trajectory'] for c in cases):
        matched = {r['method']: r for r in cases if r['trajectory'] == trajectory and r['status'] == 'completed'}
        if not all(method in matched for method in study['methods']):
            continue
        for comparator in ('A0', 'B_ledger'):
            if comparator in matched and 'A2' in matched:
                pairs.append({'trajectory': trajectory, 'comparison': 'A2 minus '+comparator,
                              'difference': {k: matched['A2'][k]-matched[comparator][k] if matched['A2'][k] is not None and matched[comparator][k] is not None else None
                                             for k in ('tp','fp','fn','precision','recall','set_f1','model_calls','tool_queries','input_tokens','output_tokens','api_response_cost_usd')}})
    aggregate = {}
    for method in study['methods']:
        selected = [r for r in cases if r['method'] == method]
        counts = [sum(r[k] for r in selected) for k in ('tp','fp','fn')]
        aggregate[method] = {**metrics(*counts), 'completed_trajectories': sum(r['status']=='completed' for r in selected),
                             'model_calls': sum(r['model_calls'] for r in selected),
                             'tool_queries': sum(r['tool_queries'] for r in selected),
                             'invalid_responses': sum(r['invalid_responses'] for r in selected)}
    result = {'mode': study['mode'], 'study_status': study['status'], 'cases': cases, 'matched_differences': pairs,
              'descriptive_micro_aggregate': aggregate,
              'interpretation': ('MOCK verifies mechanics only; these are not model-performance results. ' + study.get('scope','') if study['mode'] == 'MOCK' else
                                 'Real local development smoke on an exposed trajectory; not the frozen OpenRouter comparison.' if study['mode']=='LOCAL_MODEL' else
                                 'Exploratory same-process synthetic development evaluation; four template families; no intrinsic-memory claim.'),
              'aggregation': 'Primary: each full trajectory and paired differences. Micro totals are descriptive. Sequential steps and model calls are not replications. Undefined denominators remain null.',
              'budget': study.get('budget'), 'verified_billed_cost_usd': None}
    dump(root/'report.json', result)
    lines = ['# Kiodai v2 saved-artifact report', '', result['interpretation'], '', result['aggregation'], '',
             '| Trajectory | Method | TP | FP | FN | Precision | Recall | Set-F1 | Calls | Queries |',
             '|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in cases:
        values = [row['trajectory'], row['method']] + [row[k] for k in ('tp','fp','fn','precision','recall','set_f1','model_calls','tool_queries')]
        lines.append('| ' + ' | '.join(f'{v:.4f}' if type(v) is float else str(v) for v in values) + ' |')
    lines += ['', 'Full diagnostics, paired differences, resource accounting and trace paths: `report.json`.',
              'API costs and tokens are unavailable for MOCK. No verified billing record was obtained.',
              'Native PM-Bench removes completed handles. Execution failure, uncertainty and duplicate protection are separately tested local lifecycle mechanics.']
    (root/'report.md').write_text('\n'.join(lines)+'\n')
    return result

#!/usr/bin/env python3
"""Post-run comparison diagnostics and manual semantic review, outside agent code."""
import argparse
import json
import sqlite3
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import dump, rows
from kiodai_v2.report import analyze_case, metrics
from sim import pm_bench as PM


def read(path):
    return json.loads(Path(path).read_text())


def obligation_diagnostics(scenario, steps):
    """Replay only recorded actions through unchanged public evaluator helpers.

    Blocking counts trigger opportunities suppressed by an unmet prerequisite.
    These diagnostics never change the official due sets or primary score.
    """
    updates = PM.build_updates_by_day(scenario)
    saved = {(s['day'], s['step_id']): s for s in steps}
    obligations = []
    for day in scenario['days']:
        states = {t['id']: PM.init_task_state(t) for t in day['tasks']}
        active = set()
        for t in day['tasks']:
            if PM.normalize_encoding(t['encoding'])[0] == 'start':
                active.add(t['id']); states[t['id']]['active'] = True
        change = updates.get(day['name'], {'pre': [], 'by_step': {}})
        for update in change['pre']:
            PM.apply_task_update(states[update['task_id']], update, task_states=states)
        due_checkpoints = {t: [] for t in states}
        blocked_checkpoints = {t: [] for t in states}
        start_minutes = PM.build_day_start_minutes(day)
        for index, step in enumerate(day['steps']):
            record = saved.get((day['name'], step['id']))
            if record is None:
                break  # Never infer outcomes beyond the recorded prefix.
            for update in change['by_step'].get(step['id'], []):
                PM.apply_task_update(states[update['task_id']], update, task_states=states)
            for task in day['tasks']:
                encoding, at = PM.normalize_encoding(task['encoding'])
                if encoding == 'step' and at == step['id']:
                    active.add(task['id']); states[task['id']]['active'] = True
            minutes = PM.time_to_minutes(step['time'])
            for identifier, state in states.items():
                dependency = state['task'].get('depends_on')
                if not state['active'] or state['completed'] or state['canceled'] or not dependency:
                    continue
                current = state['current']
                triggered = ((current['type'] == 'time' and PM.is_due_time(current, step)) or
                             (current['type'] == 'event' and PM.is_due_event(current, step)) or
                             (current['type'] == 'time_check' and
                              PM.timecheck_status(current, minutes, start_minutes) == 'on_time'))
                if triggered and not states[dependency]['completed']:
                    blocked_checkpoints[identifier].append(record['checkpoint'])
            due = PM.compute_due_now(states, active, step, index, minutes, start_minutes)
            if due != set(record['evaluator']['due_task_ids']):
                raise ValueError('Recorded due sets disagree with unchanged evaluator replay')
            for identifier in due:
                due_checkpoints[identifier].append(record['checkpoint'])
            PM.apply_runtime_completions(states, record['action']['task_ids'], due,
                                         step, index, minutes, start_minutes)
        for identifier, state in states.items():
            obligations.append({'day': day['name'], 'task_id_evaluator_only': identifier,
                'action': PM.runtime_task_action_text(state), 'depends_on': state['task'].get('depends_on'),
                'due_checkpoints': due_checkpoints[identifier],
                'first_due_checkpoint': next(iter(due_checkpoints[identifier]), None),
                'dependency_blocked_trigger_checkpoints': blocked_checkpoints[identifier],
                'completed': state['completed'], 'canceled': state['canceled'], 'active_at_last_observed': state['active']})
    complete = len(steps) == sum(len(d['steps']) for d in scenario['days'])
    return {'coverage': 'complete' if complete else 'recorded prefix only',
        'total_instructed_obligations': len(obligations),
        'unique_obligations_ever_due': sum(bool(t['due_checkpoints']) for t in obligations),
        'unique_obligations_blocked_at_trigger': sum(bool(t['dependency_blocked_trigger_checkpoints']) for t in obligations),
        'completed_obligations': sum(t['completed'] for t in obligations),
        'unfinished_including_canceled': sum(not t['completed'] for t in obligations) if complete else None,
        'unfinished_not_canceled': sum(not t['completed'] and not t['canceled'] for t in obligations) if complete else None,
        'canceled_obligations': sum(t['canceled'] for t in obligations), 'obligations': obligations}


def diagnostics(folder, base):
    steps = rows(folder/'steps.jsonl')
    calls = rows(folder/'calls.jsonl')
    responses = [r for r in calls if r['event'] == 'response']
    trace = rows(folder/'agent.jsonl')
    connection = sqlite3.connect((folder/'memory.sqlite').resolve().as_uri()+'?mode=ro&immutable=1', uri=True)
    try:
        events = [{'seq': i, **json.loads(b)} for i, b in connection.execute('SELECT seq,body FROM events ORDER BY seq')]
    finally:
        connection.close()
    failures = Counter((r['kind'], r.get('validation_stage')) for r in responses if r['validation_error'])
    obligations = obligation_diagnostics(read(folder/'scenario.json'), steps)
    quarantined = [{'checkpoint': s['checkpoint'], 'id': k, 'version': v['version']}
                   for s in steps for k, v in s['intentions_after_receipt'].items() if v['status'] == 'quarantined']
    hidden = base['hidden_opportunities']
    query_table = []
    for step in steps:
        for query in step['tools']:
            hits = [h for h in hidden if h['checkpoint'] == step['checkpoint'] and
                    h['channel'] == query['channel'] and h['category'] == 'query_supported_hit']
            query_table.append({'checkpoint': step['checkpoint'], **query,
                                'same_checkpoint_supported_hits': len(hits), 'necessity': 'manual_review_required'})
    return {'obligations': obligations, 'queries': query_table,
        'hidden_categories': dict(Counter(h['category'] for h in hidden)),
        'queries_without_same_checkpoint_hidden_hit': sum(not q['same_checkpoint_supported_hits'] for q in query_table),
        'query_necessity_note': 'This proxy is not an unnecessary-query count. Negative checks, clocks and information useful later need separate manual review.',
        'validation_failures': [{'kind': k, 'stage': s, 'count': n} for (k, s), n in sorted(failures.items())],
        'extraction_accepted_empty_updates': sum(r.get('outcome') == 'accepted_empty_update' for r in responses),
        'extraction_accepted_operation_responses': sum(r.get('outcome') == 'accepted_operations' for r in responses),
        'fail_closed_checkpoints': [s['checkpoint'] for s in steps if s['action']['invalid_response_failure']],
        'task_executions': sum(len(s['execution']) for s in steps),
        'successful_simulator_receipts': sum(e['outcome'] == 'simulator_completed' for s in steps for e in s['execution']),
        'failed_simulator_receipts': sum(e['outcome'] != 'simulator_completed' for s in steps for e in s['execution']),
        'quarantined_snapshots': quarantined,
        'final_unresolved_intentions': sum(v['status'] == 'quarantined' for v in read(folder/'memory.json').values()),
        'ledger_changes': [e for e in events if e['kind'] in ('create', 'revise', 'cancel', 'ambiguous')],
        'semantic_review': {'status': 'not_applicable' if base['method'] == 'A0' else 'pending_manual_review',
            'error_count': None, 'source_paths': [str(folder.name+'/'+n) for n in ('scenario.json','calls.jsonl','agent.jsonl','steps.jsonl')],
            'note': 'Schema acceptance and exact quotations do not establish semantics. Review all declared obligations and all accepted/rejected drafts, including missing intentions.'},
        'binding_audit': [{'checkpoint': r['checkpoint'], 'bindings': r['decision'].get('bindings', [])}
                          for r in trace if r['decision'].get('bindings')],
        'known_uncertainty': 'Native completed handles disappear; independent duplicate side effects are unidentifiable. Superseded ledger versions are code-level, semantic stale instructions require review.'}


def group_summary(cases, planned, completed):
    by_id = {(c['trajectory'], c['method']): c for c in cases}
    comparisons = {}
    for comparator in ('B_ledger', 'A0'):
        differences = []
        for trajectory in planned:
            a, b = by_id[(trajectory, 'A2')], by_id[(trajectory, comparator)]
            valid = all(c.get('primary_usable') and c.get('set_f1') is not None for c in (a, b))
            differences.append({'trajectory': trajectory, 'difference': a['set_f1']-b['set_f1'] if valid else None})
        valid = [r['difference'] for r in differences if r['difference'] is not None]
        comparisons['A2 minus '+comparator] = {
            'planned_pairs': len(planned), 'usable_pairs': len(valid), 'per_trajectory': differences,
            'declared_mean_difference': sum(valid)/len(planned) if completed and len(valid) == len(planned) else None,
            'available_pair_mean_diagnostic_only': sum(valid)/len(valid) if valid else None}
    totals = {}
    for method in ('A0', 'B_ledger', 'A2'):
        all_cases = [c for c in cases if c['method'] == method]
        usable = [c for c in all_cases if c.get('primary_usable')]
        sums = [sum(c[k] for c in usable) for k in ('tp', 'fp', 'fn')]
        rates = metrics(*sums) if usable else {k: None for k in ('tp','fp','fn','precision','recall','set_f1')}
        totals[method] = {'planned_trajectories': len(planned), 'usable_trajectories': len(usable),
            'complete_declared_group': len(usable) == len(planned),
            'complete_case_micro_totals': rates,
            'coverage_note': 'Sum unchanged official TP/FP/FN across complete cases only; incomplete totals are descriptive and never the headline.',
            'observed_model_calls': sum(c.get('model_calls', 0) for c in all_cases),
            'observed_tool_queries': sum(c.get('tool_queries', 0) for c in all_cases)}
    return {'comparisons': comparisons, 'micro_aggregates': totals}


SEMANTIC_CATEGORIES = ('missing_prerequisite', 'missing_required_field', 'incorrect_trigger',
                       'incorrect_binding', 'unsupported_intention', 'missing_intention',
                       'quarantined_unresolved', 'other')


def review_template(report):
    return {'scope': 'Manual post-run review only; never an agent input or replacement scorer.',
        'instructions': 'For every ledger case review all instructions, checkpoints, accepted/rejected drafts and action bindings. An empty findings list means zero only after review_status=reviewed with reviewer and notes. Record repaired defects too. Use evaluator obligation keys only here.',
        'categories': SEMANTIC_CATEGORIES,
        'finding_fields': {'category': 'one listed category', 'intention_id': 'ledger ID or null for missing',
            'obligation': 'day/task_id or null for unsupported intention', 'first_checkpoint': 'integer',
            'repair_checkpoint': 'integer or null', 'source_refs': ['ref/quote or raw file:line'], 'notes': 'required explanation'},
        'cases': [{'trajectory': c['trajectory'], 'method': c['method'], 'review_status': 'pending',
                   'reviewer': None, 'notes': None, 'findings': [],
                   'query_necessity_review': {'status': 'pending', 'unnecessary_checkpoints': [], 'notes': None}}
                  for c in report['cases'] if c['method'] != 'A0']}


def apply_reviews(report, annotations):
    index = {(c['trajectory'], c['method']): c for c in report['cases'] if c['method'] != 'A0'}
    seen = set()
    for review in annotations['cases']:
        key = (review['trajectory'], review['method'])
        if key not in index or key in seen:
            raise ValueError('Unknown or duplicate semantic-review case')
        seen.add(key)
        case = index[key]
        if review['review_status'] == 'pending':
            continue
        if review['review_status'] != 'reviewed' or not review.get('reviewer') or not review.get('notes'):
            raise ValueError('Completed semantic review needs reviewer and notes')
        if not case.get('primary_usable'):
            raise ValueError('An incomplete trajectory cannot be marked fully reviewed')
        known = {r['day']+'/'+r['task_id_evaluator_only']: r for r in case['diagnostics']['obligations']['obligations']}
        findings = []
        for original in review['findings']:
            finding = dict(original)
            start, repair = finding['first_checkpoint'], finding['repair_checkpoint']
            if (finding['category'] not in SEMANTIC_CATEGORIES or not finding.get('notes') or not finding.get('source_refs')
                    or type(start) is not int or not 1 <= start <= case['planned_steps']
                    or repair is not None and (type(repair) is not int or not start <= repair <= case['planned_steps'])):
                raise ValueError('Incomplete or invalid semantic finding')
            obligation = finding['obligation']
            if obligation is not None and obligation not in known:
                raise ValueError('Unknown reviewed obligation')
            due = known[obligation]['first_due_checkpoint'] if obligation else None
            finding.update(first_official_due_checkpoint=due,
                repaired_before_first_due_checkpoint=repair < due if repair is not None and due is not None else None,
                repaired_by_first_due_decision=repair <= due if repair is not None and due is not None else None)
            findings.append(finding)
        case['diagnostics']['semantic_review'] = {**review, 'status': 'reviewed', 'findings': findings,
            'error_count': len(findings), 'timing_note': 'Due time is endogenous to this run. Never-due obligations have null repair-before-due, not success.'}
    if seen != set(index):
        raise ValueError('Annotations must retain all 24 ledger cases, even pending ones')


def analyze(root, annotations=None):
    root = Path(root).resolve()
    study = read(root/'study.json')
    spec = read(root/'comparison_specification.json')
    cases = []
    for block in spec['schedule']:
        for method in block['methods']:
            folder = root/block['trajectory']/method
            identity = {'trajectory': block['trajectory'], 'family': block['family'],
                        'method': method, 'prior_network_smoke': block['prior_network_smoke']}
            if not (folder/'manifest.json').exists():
                cases.append({**identity, 'status': 'not_started' if not folder.exists() else 'setup_incomplete',
                    'primary_usable': False, **{k: None for k in ('tp','fp','fn','precision','recall','set_f1')},
                    'diagnostics': {'semantic_review': {'status': 'not_applicable' if method == 'A0' else 'unavailable', 'error_count': None}}})
                continue
            try:
                base = analyze_case(folder)
                detail = diagnostics(folder, base)
            except (ValueError, KeyError, OSError, sqlite3.Error) as exc:
                cases.append({**identity, 'status': 'artifact_invalid', 'primary_usable': False,
                    **{k: None for k in ('tp','fp','fn','precision','recall','set_f1')},
                    'artifact_error': str(exc),
                    'diagnostics': {'semantic_review': {'status': 'unavailable', 'error_count': None}}})
                continue
            cases.append({**base, **identity, 'diagnostics': detail})
    planned = [b['trajectory'] for b in spec['schedule']]
    result = {'identifier': spec['identifier'], 'mode': study['mode'], 'status': study['status'],
        'interpretation': 'MOCK software verification only; no model-effectiveness measurements.' if study['mode'] == 'MOCK' else
                         'Exploratory comparison on exposed synthetic development cases; four template families.',
        'primary_contrast': spec['primary_contrast'], 'cases': cases,
        'overall': group_summary(cases, planned, study['status'] == 'completed'),
        'families': {}, 'smoke_overlap': {}, 'budget': study.get('budget'), 'verified_billed_cost_usd': None,
        'analysis_policy': spec['analysis_policy']}
    for field, target in (('family', 'families'), ('prior_network_smoke', 'smoke_overlap')):
        for value in dict.fromkeys(c[field] for c in cases):
            subset = [c for c in cases if c[field] == value]
            names = list(dict.fromkeys(c['trajectory'] for c in subset))
            result[target][str(value)] = group_summary(subset, names, study['status'] == 'completed')
    if annotations:
        apply_reviews(result, read(annotations))
    return result


def write_report(root, annotations=None):
    root = Path(root)
    result = analyze(root, annotations)
    # Derived reports only; original engine report, case files and manifests stay intact.
    suffix = '_reviewed' if annotations else ''
    dump(root/('comparison_report'+suffix+'.json'), result)
    lines = ['# '+result['identifier'], '', result['interpretation'], '',
             'Primary: A2 minus B_ledger. Secondary: A2 minus A0. '+result['analysis_policy']['headline'], '',
             '| Trajectory | Family | Method | Status | TP | FP | FN | Precision | Recall | Set-F1 | Calls | Queries |',
             '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for c in result['cases']:
        lines.append('| '+' | '.join(str(c.get(k)) for k in ('trajectory','family','method','status','tp','fp','fn','precision','recall','set_f1','model_calls','tool_queries'))+' |')
    lines += ['', '## Declared paired comparisons', '', '| Group | Contrast | Usable/planned pairs | Declared mean |', '|---|---|---:|---:|']
    groups = {'all': result['overall'], **{'family:'+k:v for k,v in result['families'].items()},
              **{'prior-network-smoke:'+k:v for k,v in result['smoke_overlap'].items()}}
    for group, summary in groups.items():
        for contrast, value in summary['comparisons'].items():
            lines.append(f'| {group} | {contrast} | {value["usable_pairs"]}/{value["planned_pairs"]} | {value["declared_mean_difference"]} |')
    lines += ['', 'Null means undefined or unavailable, never zero. Descriptive micro totals, obligation/dependency diagnostics, hidden evidence categories, costs and manual-review status are in the JSON report.',
              'Semantic correctness is unmeasured until manual review; A0 extraction is not applicable. Queries without an immediate hit are not automatically unnecessary.',
              'No independent replication, significance or equivalence claim. MOCK tokens/API cost remain unavailable.']
    (root/('comparison_report'+suffix+'.md')).write_text('\n'.join(lines)+'\n')
    template = root/'semantic_review_template.json'
    if not template.exists():
        dump(template, review_template(result))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study', type=Path, required=True)
    parser.add_argument('--annotations', type=Path)
    args = parser.parse_args()
    write_report(args.study, args.annotations)
    print(args.study/'comparison_report.json')

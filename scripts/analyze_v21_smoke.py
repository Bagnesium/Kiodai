#!/usr/bin/env python3
"""Read-only, post-run analysis of the two recorded DeepSeek development smokes.

Prints JSON to stdout. Does not call a model, regenerate original reports, restore
missing evidence, or open a writable database. Scenario-specific trace selection
and action-identity diagnostics here are evaluator-side post-hoc analysis only.
"""
import json
import sqlite3
import sys
import zipfile
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest, rows
from kiodai_v2.dashboard import Viewer
from kiodai_v2.report import analyze_case
from scripts.run_v21_smoke import preflight
from scripts.verify_saved_smoke import equal_number, require, verify_accounting

ROOT = Path(__file__).resolve().parents[1]
CURRENT = Path('results/v2_1/deepseek-smoke-v1')
PREVIOUS = Path('results/v2/deepseek-smoke-v1')


def read_json(path):
    return json.loads(path.read_text())


def preserved_files():
    inventory = read_json(ROOT/'research/v2_1/live_smoke_v1_inventory.json')
    archive = ROOT/inventory['archive']
    require(digest(archive.read_bytes()) == inventory['archive_sha256'], 'Archive changed')
    with zipfile.ZipFile(archive) as saved:
        require(len(saved.namelist()) == len(set(saved.namelist())), 'Duplicate archive member')
        require(set(saved.namelist()) == set(inventory['files']), 'Archive membership changed')
        for name, expected in inventory['files'].items():
            path = (ROOT/name).resolve()
            require(path.is_relative_to((ROOT/CURRENT).resolve()), 'Evidence outside run scope')
            require(digest(saved.read(name)) == expected, 'Archived evidence changed: '+name)
            require(digest(path.read_bytes()) == expected, 'Recorded evidence changed: '+name)
    require((ROOT/CURRENT/'freeze.json').read_bytes() ==
            (ROOT/'research/v2_1/smoke_v1.json').read_bytes(), 'Smoke manifest changed')
    require(read_json(ROOT/CURRENT/'study.json')['code_commit'] == inventory['execution_commit'],
            'Recorded execution commit mismatch')
    return inventory


def ledger_events(folder):
    db = sqlite3.connect((folder/'memory.sqlite').as_uri()+'?mode=ro&immutable=1', uri=True)
    try:
        return [{'seq': seq, **json.loads(body)} for seq, body in
                db.execute('SELECT seq,body FROM events ORDER BY seq')]
    finally:
        db.close()


def inspect_run(relative):
    root = ROOT/relative
    study = read_json(root/'study.json')
    require(study['methods'] == ['A2'] and study['repeat'] == 1 and len(study['runs']) == 1,
            'Expected one A2-only trajectory')
    folder = root/study['runs'][0]['folder']
    case = analyze_case(folder)  # Includes immutable case hashes and official rescoring.
    saved = read_json(root/'report.json')
    require(saved['matched_differences'] == [] and len(saved['cases']) == 1, 'Comparison scope changed')
    for key, value in case.items():
        if key != 'path':
            require(value == saved['cases'][0][key], 'Original report does not reproduce: '+key)
    accounting = verify_accounting(root, folder)
    calls = rows(folder/'calls.jsonl')
    responses = [(line, r) for line, r in enumerate(calls, 1) if r['event'] == 'response']
    requests = [r for r in calls if r['event'] == 'request']
    events = ledger_events(folder)
    steps = rows(folder/'steps.jsonl')
    memory = read_json(folder/'memory.json')
    instruction = json.loads(requests[0]['request']['messages'][-1]['content'])['observations']['m1']['text']
    # This fixed development story delegates only in its initial visible header.
    # This identity check is NOT a general semantic validator or runtime filter.
    unsupported = []
    accepted_ops = Counter()
    empties = []
    call_table = []
    for line, response in responses:
        value = json.loads(response['raw_text'])
        accepted = not response['validation_error'] and not response['transport_error']
        if response['kind'] == 'extract':
            operations = value['operations']
            if accepted:
                accepted_ops.update(op['kind'] for op in operations)
                if not operations:
                    empties.append(response['checkpoint'])
            for op in operations:
                action = (op.get('record') or {}).get('action', '')
                if action and action not in instruction:
                    unsupported.append({'checkpoint': response['checkpoint'], 'calls_line': line,
                                        'action': action, 'accepted': accepted, 'sources': op['sources']})
        stage = response.get('validation_stage')
        if response['validation_error'] and stage is None:
            # Historical logs predate explicit stage fields; these exact errors
            # are application errors confirmed at the original execution commit.
            if response['validation_error'] in (
                'ValueError: Missing intention content',
                'ValueError: Intention is stale, canceled, unresolved or dependency-blocked',
            ):
                stage = 'application (historical classification)'
            else:
                stage = 'unclassified historical failure'
        call_table.append({
            'calls_line': line, 'request_id': response.get('request_id'),
            'response_id': response['raw_response']['id'], 'checkpoint': response['checkpoint'],
            'kind': response['kind'], 'attempt': response['attempt'],
            'outcome': response.get('outcome'), 'accepted': accepted,
            'validation_error': response['validation_error'], 'validation_stage': stage,
            'finish_reason': response['raw_response']['choices'][0]['finish_reason'],
            'usage': response['usage'], 'api_response_cost_usd': response['provider']['cost_usd_reported'],
        })
    creates = [e for e in events if e['kind'] == 'create']
    require(len(creates) == accepted_ops['create'], 'Accepted creates disagree with ledger')
    require(sum(e['kind'] == 'revise' for e in events) == accepted_ops['revise'], 'Revision count mismatch')
    selected = [e for e in events if e['kind'] == 'selected']
    attempts = [e['execution_id'] for e in events if e['kind'] == 'attempted']
    receipts = [e for e in events if e['kind'] == 'receipt']
    require([e['execution_id'] for e in selected] == attempts, 'Execution attempt mismatch')
    require(len(attempts) == sum(len(s['execution']) for s in steps), 'Simulator execution mismatch')
    require({e['execution_id'] for e in receipts} == set(attempts), 'Unreceipted execution')
    require(sum(e['outcome'] == 'success' for e in receipts) ==
            sum(r['status'] == 'completed' for r in memory.values()), 'Receipt/lifecycle mismatch')
    keys = ('completed_steps', 'planned_steps', 'primary_usable', 'tp', 'fp', 'fn', 'precision',
            'recall', 'set_f1', 'model_calls', 'retries', 'tool_queries', 'input_tokens',
            'output_tokens', 'latency_seconds', 'transport_errors', 'interrupted_requests',
            'hidden_due_opportunities', 'hidden_hits')
    metrics = {k: case[k] for k in keys}
    metrics.update({
        'unique_intentions_stored': len(creates), 'accepted_operations': dict(accepted_ops),
        'extraction_responses': sum(r['kind'] == 'extract' for _, r in responses),
        'accepted_empty_updates': len(empties), 'accepted_empty_checkpoints': empties,
        'extraction_validation_failures': sum(r['kind'] == 'extract' and bool(r['validation_error']) for _, r in responses),
        'selection_validation_failures': sum(r['kind'] == 'select' and bool(r['validation_error']) for _, r in responses),
        'validation_failures_by_stage': dict(Counter(r['validation_stage'] for r in call_table if r['validation_error'])),
        'unsupported_action_proposals': len(unsupported),
        'unsupported_action_proposals_accepted': sum(r['accepted'] for r in unsupported),
        'task_executions': len(attempts), 'successful_receipts': sum(e['outcome'] == 'success' for e in receipts),
        'completed_intentions': sum(r['status'] == 'completed' for r in memory.values()),
        'fail_closed_checkpoints': sum(s['action']['invalid_response_failure'] for s in steps),
        'finish_reasons': dict(Counter(r['finish_reason'] for r in call_table)),
        'total_tokens': sum(r['usage']['total_tokens'] for _, r in responses), **accounting,
    })
    checkpoints = [{
        'checkpoint': s['checkpoint'], 'time': s['time'], 'queries': s['tools'],
        'raw_handles': s['action']['selected_handles_raw'],
        'validated_handles': s['action']['selected_handles_validated'],
        'receipts': s['execution'], 'tp': s['evaluator']['tp'],
        'fp': s['evaluator']['fp'], 'fn': s['evaluator']['fn'],
        'ledger': {identifier: {k: r[k] for k in
                   ('action', 'version', 'status', 'trigger', 'condition', 'channel', 'dependencies')}
                   for identifier, r in s['intentions_after_receipt'].items()},
    } for s in steps]
    return {'path': str(relative), 'execution_commit': study['code_commit'], 'metrics': metrics,
            'calls': call_table, 'checkpoints': checkpoints, 'unsupported_proposals': unsupported}, events


def analyze():
    inventory = preserved_files()
    _, checks = preflight()  # Offline only; includes previous archives and frozen source checks.
    current, events = inspect_run(CURRENT)
    previous, _ = inspect_run(PREVIOUS)
    equal_number(current['metrics']['api_response_cost_usd'],
                 inventory['accounting']['api_response_cost_usd'], 'Inventory cost mismatch')
    require((ROOT/CURRENT/'v2_hidden_91320/A2/scenario.json').read_bytes() ==
            (ROOT/PREVIOUS/'v2_hidden_91320/A2/scenario.json').read_bytes(), 'Scenario changed')
    archive_id = next(e['id'] for e in events if e['kind'] == 'create' and e['record']['action'].startswith('Archive '))
    create = next(e for e in events if e['kind'] == 'create' and e['id'] == archive_id)
    selection = next(e for e in events if e['kind'] == 'selected' and e['id'] == archive_id)
    execution_id = selection['execution_id']
    trace = {'instruction': create['record']['update_evidence'], 'stored': create,
             'monitoring': [e for e in events if e['kind'] in ('monitor', 'query_received')],
             'selection': selection,
             'attempt_and_receipt': [e for e in events if e.get('execution_id') == execution_id],
             'selection_call': next(r for r in current['calls'] if r['checkpoint'] == selection['checkpoint'] and r['kind'] == 'select'),
             'final_state': read_json(ROOT/CURRENT/'v2_hidden_91320/A2/memory.json')[archive_id]}
    viewer = Viewer(ROOT/CURRENT)
    require(viewer.catalog()['mode'] == 'RECORDED', 'Viewer mode incorrect')
    for index in range(current['metrics']['completed_steps']):
        view = viewer.inspect('v2_hidden_91320', 'A2', index)
        require(not view['inference_enabled'] and 'evaluator' not in view, 'Viewer isolation failed')
        require('evaluator' in viewer.inspect('v2_hidden_91320', 'A2', index, True), 'Evaluator reveal unavailable')
    return {
        'analysis_type': 'post-hoc, offline, recorded evidence; no model calls',
        'preservation': {'original_run_files': len(inventory['files']), 'archive_sha256': inventory['archive_sha256'],
                         'v21_frozen_sources': len(checks['hashes']), 'previous_archive_files': checks['historical_archive_files'],
                         'previous_frozen_sources': checks['historical_source_files'], 'same_scenario_bytes': True},
        'current': current, 'previous': previous, 'complete_trace': trace, 'dashboard': viewer.catalog(),
        'interpretation_limits': [
            'One exposed development trajectory per revision; no A0 or B_ledger comparator.',
            'Action-identity audit is specific to this story; it is not a general semantic validator.',
            'Sealing dependencies omitted at checkpoint 1; known trigger fields dropped at checkpoint 2; restored at checkpoint 4.',
            'Checkpoint 3 accepted empty update retained an unresolved sealing record; empties do not prove adequate extraction.',
            'Score denominator differs because registration success makes dependent sealing due under unchanged scoring.',
            'API schema acceptance observed; server enforcement of each keyword is not independently established.',
            'API-response cost is reconciled; independently verified billing is unavailable.',
        ],
    }


if __name__ == '__main__':
    print(json.dumps(analyze(), ensure_ascii=False, indent=2, sort_keys=True))

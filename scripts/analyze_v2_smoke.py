#!/usr/bin/env python3
"""Offline diagnostics from the one saved LIVE smoke; never sends requests."""
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import rows, dump, parse, digest
from kiodai_v2.report import report
from kiodai_v2.store import EXTRACTION
from scripts.run_v2_smoke import ROOT, LIVE_ROOT


def analyze():
    study = json.loads((LIVE_ROOT/'study.json').read_text())
    if study['status'] not in ('completed', 'interrupted'):
        raise ValueError('Wait until the one frozen invocation ends')
    # Preserve the original generic renderer output before correcting its scope label.
    for suffix in ('json', 'md'):
        source, saved = LIVE_ROOT/f'report.{suffix}', LIVE_ROOT/f'report.engine.{suffix}'
        if source.exists() and not saved.exists():
            saved.write_bytes(source.read_bytes())
    result = report(LIVE_ROOT)  # verifies hashes and reuses the protected official scorer
    result['interpretation'] = 'One exposed synthetic hidden-state A2 development trajectory; one repeat; no comparator or reliability estimate.'
    result['complete_study_paired_means'] = {}
    result['report_scope_correction'] = 'Generic frozen renderer mentions four families and planned comparator pairs; neither applies to this A2-only smoke. Numeric case metrics are unchanged.'
    dump(LIVE_ROOT/'report.json', result)
    path = LIVE_ROOT/'report.md'
    text = path.read_text().replace(
        'Exploratory same-process synthetic development evaluation; four template families; no intrinsic-memory claim.', result['interpretation'])
    path.write_text(text)
    case = result['cases'][0]
    folder = Path(case['path'])
    calls = rows(folder/'calls.jsonl')
    requests = {(r['checkpoint'], r['kind'], r['attempt']): r for r in calls if r['event'] == 'request'}
    responses = [r for r in calls if r['event'] == 'response']
    attempts = []
    for r in responses:
        if r['kind'] != 'extract':
            continue
        structural = None
        payload = None
        try:
            payload = parse(r['raw_text'], EXTRACTION)
        except (ValueError, TypeError) as exc:
            structural = str(exc)
        req = requests[(r['checkpoint'], r['kind'], r['attempt'])]
        observations = json.loads(req['request']['messages'][1]['content'])['observations']
        bad_citations = []
        def walk(value, location=''):
            if isinstance(value, dict):
                if set(value) == {'ref', 'quote'}:
                    source = observations.get(value['ref'])
                    if not source or not value['quote'] or value['quote'] not in source['text']:
                        bad_citations.append({'path': location, **value})
                for key, item in value.items():
                    walk(item, location+'/'+key)
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    walk(item, location+'/'+str(i))
        if payload:
            walk(payload)
        accepted = structural is None and not r['validation_error'] and not r['transport_error']
        attempts.append({'checkpoint': r['checkpoint'], 'attempt': r['attempt'],
            'json_schema_valid': structural is None, 'schema_error': structural,
            'validator_error': r['validation_error'], 'transport_error': r['transport_error'],
            'accepted': accepted, 'operations': payload['operations'] if payload else None,
            'accepted_operation_count': len(payload['operations']) if accepted else 0,
            'accepted_empty_operation_list': accepted and not payload['operations'],
            'invalid_citations': bad_citations,
            'finish_reason': (r.get('raw_response') or {}).get('choices', [{}])[0].get('finish_reason'),
            'usage': r['usage']})
    trace = rows(folder/'agent.jsonl')
    checkpoints = []
    for step in rows(folder/'steps.jsonl'):
        checkpoint = step['checkpoint']
        public = [r for r in trace if r['checkpoint'] == checkpoint]
        checkpoints.append({'checkpoint': checkpoint, 'time': step['time'],
            'extraction': [r for r in attempts if r['checkpoint'] == checkpoint],
            'received_observations': public[-1]['frame']['observations'] if public else {},
            'tool_queries': step['tools'], 'decisions': [r['decision'] for r in public],
            'receipts': step['execution'], 'intentions_after_receipt': step['intentions_after_receipt'],
            'evaluator_only': step['evaluator']})
    blocked = Counter(r['decision'].get('blocked') for r in trace if r['decision'].get('blocked'))
    summary = {'processed_checkpoints': len(checkpoints), 'extraction_attempts': len(attempts),
        'schema_valid_extraction_responses': sum(r['json_schema_valid'] for r in attempts),
        'accepted_extraction_responses': sum(r['accepted'] for r in attempts),
        'accepted_empty_updates': sum(r['accepted_empty_operation_list'] for r in attempts),
        'accepted_operations': sum(r['accepted_operation_count'] for r in attempts),
        'rejected_extractions': sum(not r['accepted'] for r in attempts),
        'fail_closed_decisions_by_reason': dict(blocked),
        'selection_validation_failures': sum(bool(r['validation_error']) for r in responses if r['kind'] == 'select'),
        'extraction_truncations': sum(r['finish_reason'] == 'length' for r in attempts),
        'transport_failures': sum(bool(r['transport_error']) for r in responses)}
    audit = {'purpose': 'post-hoc only; never passed to agent decisions', 'summary': summary,
        'case_metrics': case, 'checkpoints': checkpoints,
        'raw_artifact_hashes': {p.name: digest(p.read_bytes()) for p in folder.iterdir() if p.is_file()}}
    dump(LIVE_ROOT/'behavior_audit.json', audit)
    project(responses, requests)
    print(json.dumps({'summary': summary, 'metrics': {k: case[k] for k in ('status', 'primary_usable', 'tp', 'fp', 'fn', 'precision', 'recall', 'set_f1', 'model_calls', 'tool_queries', 'input_tokens', 'output_tokens', 'api_response_cost_usd', 'latency_seconds')}}, indent=2))


def project(responses, requests):
    prior = json.loads((ROOT/'research/v2/cost_projection.json').read_text())
    calibration = {}
    for kind, floor in (('extract', 750), ('select', 256)):
        observed = [r for r in responses if r['kind'] == kind]
        complete = bool(observed) and all(r['usage'] is not None for r in observed)
        first = [r for r in observed if r['attempt'] == 1]
        if not complete or not first:
            calibration[kind] = {'available': False}
            continue
        input_tokens = sum(r['usage']['input_tokens'] for r in observed)
        request_bytes = sum(len(json.dumps(requests[(r['checkpoint'], kind, r['attempt'])]['request'], ensure_ascii=False).encode()) for r in observed)
        # Size complete nonempty extraction proposals even when rejected. Empty retries
        # are not evidence that a functioning extraction pipeline would cost eight tokens.
        output_samples = []
        for r in observed:
            if kind == 'extract':
                try:
                    if not json.loads(r['raw_text']).get('operations'):
                        continue
                except (ValueError, TypeError):
                    pass
            output_samples.append(r['usage']['output_tokens'])
        calibration[kind] = {'available': True, 'tokens_per_request_byte': input_tokens/request_bytes,
            'retry_rate_per_initial_call': sum(r['attempt'] > 1 for r in observed)/len(first),
            'observed_output_sample_mean': sum(output_samples)/len(output_samples) if output_samples else None,
            'planning_output_tokens_per_attempt': max(floor, sum(output_samples)/len(output_samples) if output_samples else floor),
            'prior_output_floor': floor}
    revised = {'source': 'one actual A2 hidden-state smoke; planning sensitivity, not a validated forecast',
        'calibration': calibration, 'methods': {}, 'old_expected_usd': prior['usage_informed_projection_usd'],
        'unchanged_full_conservative_allowance_usd': 19.95251712, 'full_authorized_for_execution': False,
        'assumptions': ['Retain 35% input padding and full-study successful MOCK request sizes to represent growing histories.',
            'Retain output floors of 750 extraction and 256 selection tokens; empty updates cannot justify reducing functioning-pipeline allowance.',
            'Apply observed phase retry rates to A2 and, as an explicit untested transfer assumption, B_ledger.',
            'Retain original A0 projection and three extra B_ledger query/selection cycles.',
            'Each retry includes preceding planned output as added input with 35% padding; no cache discount.',
            'One hidden family does not represent revision, visible-event or cross-day families; extraction failure makes extrapolation especially uncertain.']}
    revised['methods']['A0'] = prior['methods']['A0']
    if all(c.get('available') for c in calibration.values()):
        for method in ('B_ledger', 'A2'):
            items = [r for p in (ROOT/'results/v2/mock-verification-v2').glob('*/'+method+'/calls.jsonl') for r in rows(p) if r['event'] == 'request']
            expected = prior['methods'][method]['projected_calls'] - (3 if method == 'B_ledger' else 0)
            if len(items) != expected:
                raise ValueError('Full-study sizing artifacts missing; first run scripts/restore_v2_artifacts.py. No zero-cost projection substituted.')
            inputs = outputs = attempts = 0
            for r in items:
                c = calibration[r['kind']]
                amount = len(json.dumps(r['request'], ensure_ascii=False).encode()) * c['tokens_per_request_byte'] * 1.35
                out, retry = c['planning_output_tokens_per_attempt'], c['retry_rate_per_initial_call']
                inputs += amount*(1+retry) + retry*out*1.35
                outputs += out*(1+retry)
                attempts += 1+retry
            if method == 'B_ledger':
                c = calibration['select']; retry = c['retry_rate_per_initial_call']; out = c['planning_output_tokens_per_attempt']
                inputs += 3*(12000*c['tokens_per_request_byte']*1.35*(1+retry)+retry*out*1.35)
                outputs += 3*out*(1+retry); attempts += 3*(1+retry)
            revised['methods'][method] = {'projected_calls': attempts, 'projected_input_tokens': inputs,
                'projected_output_tokens': outputs, 'projected_uncached_cost_usd': (inputs*.27+outputs)/1e6}
        revised['planning_projection_usd'] = sum(m['projected_uncached_cost_usd'] for m in revised['methods'].values())
    else:
        revised['planning_projection_usd'] = None
        revised['reason'] = 'Complete phase usage unavailable; no fabricated full-study extrapolation.'
    dump(LIVE_ROOT/'full_study_usage_projection.json', revised)


if __name__ == '__main__':
    analyze()

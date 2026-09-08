"""Rebuild the completed pilot report from immutable LIVE artifacts; no inference."""
from pathlib import Path
from datetime import datetime, timezone
from decimal import Decimal
import hashlib
import json
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research_harness.analysis import analyze, report, rows, verify_run, score_artifacts
from research_harness.paired import configs

PAIR = ROOT / 'results/kiodai/live-pair-42433e00474b'


def total(values):
    return None if not values or any(v is None for v in values) else sum(values)


def money(values):
    return None if not values or any(v is None for v in values) else float(sum(Decimal(str(v)) for v in values))


def main():
    configs('pilot', None, 'LIVE')
    plan = json.loads((PAIR / 'pair.json').read_text())
    assert plan['mode'] == 'LIVE' and plan['status'] == 'completed'
    assert plan['repeat'] == 0 and plan['order'] == ['A0', 'A1']
    result = analyze(ROOT / 'results/kiodai', 'LIVE')
    assert len(result['pairs']) == 1
    conditions, trajectories = {}, {}
    for condition, folder in plan['runs'].items():
        path = PAIR / folder
        manifest = verify_run(path)
        score = score_artifacts(path)
        calls = rows(path / 'raw_model_calls.jsonl')
        steps, evaluations = rows(path / 'steps.jsonl'), rows(path / 'evaluator.jsonl')
        assert manifest['completed_steps'] == 8 and len(steps) == len(evaluations) == 8
        assert all(c['reported_model'] == 'deepseek/deepseek-chat-v3.1' and
                   c['provider_metadata']['provider_reported'] == 'Novita' for c in calls)
        summary = score['summary']
        conditions[condition] = {
            'manifest_path': str(path / 'manifest.json'),
            'tp': summary['set_tp'], 'fp': summary['set_fp'], 'fn': summary['set_fn'],
            **score['rates'], 'completed_steps': len(steps),
            'model_attempts': len(calls), 'tool_queries': summary['state_query_calls'],
            'invalid_responses': manifest['invalid_attempt_count'], 'retries': manifest['retry_count'],
            'transport_errors': manifest['transport_error_count'],
            'input_tokens': manifest['token_usage']['input_tokens'],
            'output_tokens': manifest['token_usage']['output_tokens'],
            'total_tokens': manifest['token_usage']['total_tokens'],
            'provider_reported_cached_input_tokens': total([
                c['raw_response']['usage'].get('prompt_tokens_details', {}).get('cached_tokens') for c in calls]),
            'model_latency_seconds': manifest['model_latency_seconds'],
            'list_price_usage_estimate_usd': manifest['estimated_cost_usd'],
            'provider_reported_cost_usd': money([c['provider_metadata'].get('cost_usd_reported') for c in calls]),
            'verified_billed_cost_usd': None,
        }
        trajectories[condition] = [
            {'step_id': s['step_id'], 'time': s['time'],
             'selected_task_ids': e['selected_task_ids'], 'due_task_ids': e['due_task_ids'],
             'ongoing_choice': s['action']['choice'], 'tp': e['tp'], 'fp': e['fp'], 'fn': e['fn'],
             'missed': e['missed'], 'false': e['false'], 'execution': s['execution']}
            for s, e in zip(steps, evaluations)]
    differences = {}
    for key in ['tp', 'fp', 'fn', 'precision', 'recall', 'set_f1', 'model_attempts', 'tool_queries',
                'invalid_responses', 'retries', 'input_tokens', 'output_tokens', 'total_tokens',
                'model_latency_seconds', 'provider_reported_cost_usd']:
        a, b = conditions['A0'][key], conditions['A1'][key]
        differences[key] = None if a is None or b is None else float(Decimal(str(b)) - Decimal(str(a)))
    old = json.loads((ROOT / 'artifacts/verification/pilot-retry-audit-20260908T163833Z.json').read_text())
    for previous in old['previous_attempts']:
        for file, digest in previous['files_sha256'].items():
            assert hashlib.sha256((ROOT / file).read_bytes()).hexdigest() == digest
    details = {
        'generated_at_utc': datetime.now(timezone.utc).isoformat(),
        'pair_path': str(PAIR), 'analysis_unit': 'one scenario/trajectory, one repeat; not eight independent samples',
        'conditions': conditions, 'a1_minus_a0': differences, 'trajectories': trajectories,
        'complete_pairs': len(result['pairs']), 'incomplete_pairs': result['incomplete_pairs'],
        'task_selections_identical': all(a['selected_task_ids'] == b['selected_task_ids']
                                        for a, b in zip(trajectories['A0'], trajectories['A1'])),
        'prior_startup_failures': old['previous_attempts'],
        'prior_startup_failure_classification': 'TLS infrastructure failure before model requests; no performance score',
        'preflight_pair_estimate_usd': plan['preflight']['conservative_pair_estimate_usd'],
        'provider_reported_cost_total_usd': money([c['provider_reported_cost_usd'] for c in conditions.values()]),
        'list_price_usage_estimate_total_usd': money([c['list_price_usage_estimate_usd'] for c in conditions.values()]),
        'verified_billed_cost_usd': None,
        'cost_source': 'sum of saved OpenRouter response usage.cost values, corroborated by upstream_inference_cost; no billing statement queried',
        'artifact_sha256': {str(f.relative_to(ROOT)): hashlib.sha256(f.read_bytes()).hexdigest()
                           for f in sorted(PAIR.rglob('*')) if f.is_file()},
    }
    (ROOT / 'artifacts/verification/live-pilot-analysis-20260908.json').write_text(json.dumps(details, indent=2) + '\n')
    (ROOT / 'RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    lines = [report(result), '## Completed frozen pilot', '',
             f'Pair: `{PAIR}`. Executed {plan["started_at_utc"]}–{plan["finished_at_utc"]}.', '',
             'One development scenario, one repeat, two complete eight-step trajectories; 16 genuine model calls total. '
             'Both selected all five due task actions correctly and matched all eight step-level due sets. '
             'All task selections were identical. A0 chose ongoing option B and A1 option A at 08:30; '
             'this ongoing-task choice is not scored by the prospective-memory metric.', '',
             '| Measure | A0 | A1 | A1 minus A0 |', '|---|---:|---:|---:|']
    for key in ['tp', 'fp', 'fn', 'precision', 'recall', 'set_f1', 'model_attempts', 'tool_queries',
                'invalid_responses', 'retries', 'input_tokens', 'output_tokens', 'total_tokens',
                'model_latency_seconds', 'provider_reported_cost_usd']:
        lines.append(f'| {key} | {conditions["A0"][key]} | {conditions["A1"][key]} | {differences[key]} |')
    lines += ['', 'Aggregation sums TP/FP/FN over each whole trajectory, then computes precision, recall and Set-F1. '
              'The paired difference is A1 minus A0 for that trajectory. With one scenario and one repeat, '
              'the scenario-mean difference equals this single difference. Steps are not independent experimental units. '
              'No confidence interval, p-value or equivalence claim is warranted.', '',
              '## Cost sources', '',
              '| Cost measure | USD | Interpretation |', '|---|---:|---|',
              '| Prospective stress estimate | 0.13677592 | Both conditions, maximum queries/retries, 256 output tokens per attempt; heuristic, not a bill |',
              f'| Usage × frozen uncached list prices | {details["list_price_usage_estimate_total_usd"]:.8f} | Computed from actual tokens, ignores cache discounts |',
              f'| Provider-reported total | {details["provider_reported_cost_total_usd"]:.8f} | Sum of all 16 saved response costs |',
              '| Verified billed total | unavailable | No billing statement or account ledger was inspected |', '',
              'Provider responses report 4,672 cached input tokens for A0 and 8,640 for A1. '
              'At the advertised half-price cache-read rate, these account for the difference between the uncached estimate '
              'and reported response costs. Caching was provider-reported; no application answer cache or shared condition memory was added. '
              'Do not infer a general latency/cost effect from this single ordered pair. '
              'Budget snapshots are cumulative and must not be summed across conditions; the last A1 snapshot reserves '
              '$0.01924624 for the actual 16 requests. Remaining balance was not spent.', '',
              '## Concrete successes and failures', '',
              '- At 09:40 both logged humidity and ignored the blue-circle lure for a task requiring a blue hexagon.',
              '- At 10:50 both released the sample envelope on the correct cue and did not recycle the canceled proof.',
              '- At the superseded 11:00 deadline both selected no task action; at 11:20 both inspected the pressure gauge and sent the corrected status note.',
              '- There were no observed task-performance failures, malformed responses, transport errors, retries or tool queries in the completed pair. No failed model example can honestly be supplied.', '',
              'The two earlier infrastructure failures remain in the dataset:', '']
    for previous in old['previous_attempts']:
        lines.append(f'- `{ROOT / previous["path"]}`: certificate verification failed in the free route lookup; no condition sessions or model requests. Preserved byte-for-byte.')
    lines += ['', '## Interpretation and limitations', '',
              'This is an exploratory development pilot with a ceiling result in both conditions. '
              'It found no task-accuracy improvement from the frozen P1 instruction; it does not establish general equivalence or general superiority. '
              'A1 used 5,360 more input tokens and its response-reported cost was $0.00091152 higher in this pair. '
              'No hidden-state query, cross-day retention, real tool-failure recovery or autonomous monitoring was demonstrated.', '',
              'Frozen P1 assumes completion after selection; it does not robustly confirm successful execution. '
              'PM-Bench removes completed handles, so duplicate prevention is not independently attributable to the prompt. '
              'Heartbeat was disabled in both conditions. Software tests and MOCK demonstrations are separate from this live model evidence.', '',
              'Replay: `python3 -m research_harness.dashboard`, then choose **RECORDED** and '
              '**first-development-day-pilot-v1 · live-pair-42433e00474b**. Replay makes no inference calls.', '',
              'Rebuild this full report: `python3 artifacts/verification/analyze_live_pilot_20260908.py`. '
              'Machine-readable detailed analysis and all source-file hashes: `artifacts/verification/live-pilot-analysis-20260908.json`.', '']
    (ROOT / 'RESULTS.md').write_text('\n'.join(lines))
    print(json.dumps({k: details[k] for k in ['complete_pairs', 'incomplete_pairs', 'task_selections_identical',
                                            'provider_reported_cost_total_usd', 'verified_billed_cost_usd']}))


if __name__ == '__main__':
    main()

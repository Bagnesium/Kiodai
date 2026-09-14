#!/usr/bin/env python3
"""Reconstruct the completed frozen follow-up from saved LIVE files; no inference."""
import json
import sys
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research_harness.analysis import analyze, rows, score_artifacts, verify_run
from research_harness.hashing import sha256_file

OUT = ROOT / 'artifacts/verification/followup-live-20260909'


def total(values):
    return None if not values or any(v is None for v in values) else sum(values)


def money(values):
    return None if not values or any(v is None for v in values) else float(sum(Decimal(str(v)) for v in values))


def difference(a, b):
    return {k: None if a[k] is None or b[k] is None else float(Decimal(str(b[k])) - Decimal(str(a[k])))
            for k in a if isinstance(a[k], (int, float)) or a[k] is None}


def metrics(evaluations, calls, steps):
    tp, fp, fn = (sum(e[k] for e in evaluations) for k in ['tp', 'fp', 'fn'])
    inputs = total([c.get('usage', {}).get('input_tokens') for c in calls])
    outputs = total([c.get('usage', {}).get('output_tokens') for c in calls])
    return {'tp': tp, 'fp': fp, 'fn': fn,
            'precision': tp / (tp + fp) if tp + fp else None,
            'recall': tp / (tp + fn) if tp + fn else None,
            'set_f1': 2 * tp / (2 * tp + fp + fn) if 2 * tp + fp + fn else None,
            'steps': len(steps), 'model_calls': len(calls),
            'invalid_responses': sum(bool(c.get('parse_error')) for c in calls),
            'retries': sum(c['attempt'] > 1 for c in calls),
            'transport_errors': sum(bool(c.get('transport_error')) for c in calls),
            'tool_queries': sum(len(s['tools']) for s in steps),
            'input_tokens': inputs, 'output_tokens': outputs,
            'total_tokens': inputs + outputs if inputs is not None and outputs is not None else None,
            'cached_input_tokens_reported': total([c['raw_response'].get('usage', {}).get('prompt_tokens_details', {}).get('cached_tokens') for c in calls]),
            'model_latency_seconds': total([c.get('latency_seconds') for c in calls]),
            'api_response_cost_usd': money([(c.get('provider_metadata') or {}).get('cost_usd_reported') for c in calls]),
            'usage_uncached_price_estimate_usd': (inputs * .27 + outputs) / 1e6 if inputs is not None and outputs is not None else None,
            'verified_billed_cost_usd': None}


def write_report(details, plan):
    a, b, delta = details['conditions']['A0'], details['conditions']['A1'], details['a1_minus_a0']
    pair = Path(details['pair_path'])
    lines = ['# Frozen follow-up results — completed 9 September 2026', '',
        '**One usable matched pair, one repeat, one complete three-day trajectory per condition.** '
        'Both conditions achieved TP=11, FP=0, FN=1; Set-F1=22/23=0.956522. '
        'A1−A0=0: no observed accuracy improvement. Both missed the hidden cooling event; all task selections matched. '
        'The run is genuine LIVE inference, not a mock demonstration.', '',
        f'Execution: {details["started_at_utc"]}–{details["finished_at_utc"]} (UTC), '
        '18:19–18:21 on 9 September in Almaty. The exact authorized command completed once. '
        'There were no infrastructure failures, invalid responses, retries, interrupted attempts, exclusions, '
        'prompt edits, replacements or protocol deviations. Experimental development is finished.', '',
        '## Primary result: whole three-day trajectory', '',
        '| Measure | A0 | A1 | A1 minus A0 |', '|---|---:|---:|---:|']
    metric_names = [('tp','TP'),('fp','FP'),('fn','FN'),('precision','Precision'),('recall','Recall'),('set_f1','Set-F1'),
        ('steps','Completed steps'),('model_calls','Model calls'),('invalid_responses','Invalid responses'),('retries','Retries'),
        ('transport_errors','Transport errors'),('tool_queries','Executed tool queries'),('input_tokens','Input tokens'),
        ('output_tokens','Output tokens'),('total_tokens','Total tokens'),('model_latency_seconds','Sum of model-call latency, seconds'),
        ('api_response_cost_usd','API-response-reported cost, USD')]
    for key, label in metric_names:
        digits = 8 if 'cost' in key else 6 if key in ['precision','recall','set_f1','model_latency_seconds'] else 0
        lines.append('| ' + label + ' | ' + ' | '.join(f'{v:.{digits}f}' for v in [a[key], b[key], delta[key]]) + ' |')
    lines += ['', 'TP/FP/FN are summed across each complete trajectory before calculating Precision=TP/(TP+FP), '
        'Recall=TP/(TP+FN), and Set-F1=2TP/(2TP+FP+FN). The primary difference compares those two trajectory scores. '
        'With one scenario and one repeat, no averaging across replications is possible. Model calls, days and steps '
        'are not independent experimental replications. No significance, general equivalence or superiority claim is supported.', '',
        '## Descriptive breakdown — does not replace the primary result', '',
        '| Portion | Condition | Steps | TP | FP | FN | Precision | Recall | Set-F1 |', '|---|---|---:|---:|---:|---:|---:|---:|---:|']
    for portion, label in [('overlapping_Monday','Overlapping Monday'),('additional_12_steps','Additional Tuesday + Wednesday')]:
        for condition in ['A0','A1']:
            m=details['descriptive_portions'][condition][portion]
            lines.append(f'| {label} | {condition} | {m["steps"]} | {m["tp"]} | {m["fp"]} | {m["fn"]} | {m["precision"]:.6f} | {m["recall"]:.6f} | {m["set_f1"]:.6f} |')
    lines += ['', 'A1−A0 is zero for all six accuracy measures in both portions. These descriptive counts use '
        'the saved per-step evaluator records from the intact full-context run. Neither portion was rerun or evaluated '
        'as a sliced scenario. The additional 12 steps have 7 due actions: Tuesday 4 TP/0 FP/1 FN, Wednesday 2 TP/0 FP/0 FN in each condition. '
        'Monday overlaps pilot 1 and must not be pooled with it as independent evidence. Follow-up planning occurred after observing the pilot.', '',
        '| Portion | Condition | Queries / calls | Input / output tokens | API-reported USD |', '|---|---|---:|---:|---:|']
    for portion, label in [('overlapping_Monday','Monday'),('additional_12_steps','Additional 12 steps')]:
        for condition in ['A0','A1']:
            m=details['descriptive_portions'][condition][portion]
            lines.append(f'| {label} | {condition} | {m["tool_queries"]} / {m["model_calls"]} | {m["input_tokens"]} / {m["output_tokens"]} | {m["api_response_cost_usd"]:.8f} |')
    lines += ['', '## Hidden-condition audit: all seven Tuesday opportunities', '',
        'Both conditions received the instruction to acknowledge cooling **only when the sensor board reports fully stable cooling**, '
        'the same action menu, and permission to query `sensor_board` once per scheduled step. Clock time was already visible. '
        'Only the sensor-board condition was hidden. Neither condition ever selected the cooling action.', '',
        '| Step / simulated time | Relevant visible information | A0 query / information before choice | A1 query / information before choice | Cooling score |',
        '|---|---|---|---|---|',
        '| dev_t_s1 / 07:30 | Initial conditional instruction; routine checks, no positive state | None; no sensor observation | None; no sensor observation | Correctly no action due; no FP |',
        '| dev_t_s2 / 08:00 | Manifest override; no cooling confirmation | None; no sensor observation | None; no sensor observation | Correctly no action due; no FP |',
        '| dev_t_s3 / 09:00 | Vignette explicitly says nearly stable, not fully stable; safety chime | None; visible negative statement available | None; visible negative statement available | Correctly withheld cooling; both locked chamber, TP=1 |',
        '| dev_t_s4 / 11:30 | Unrelated notices; no changed trigger | Queries sensor_board; receives nearly stable / final stabilization not complete, then chooses no task | No query; earlier visible negative statement retained | Correctly no action due; no FP |',
        '| dev_t_s5 / 13:00 | Review window opens; cooling continues out of sight | No new query; previous negative sensor observation remains in history | No query; no positive sensor observation | Both omit due cooling action: FN=1 each; both sign record, TP=1 |',
        '| dev_t_s6 / 15:00 | Violet approval; placard cancellation | No query; no newer sensor evidence | No query; no positive sensor evidence | Cooling no longer in timely due set; no later cooling selection. Both publish, TP=1 |',
        '| dev_t_s7 / 16:00 | Calibration time, canceled placard cue, Wednesday note | No query; no newer sensor evidence | No query; no positive sensor evidence | No later cooling selection. Both call calibration, TP=1; canceled action withheld |', '',
        'At `dev_t_s4`, A0 raw-call line 12 requests `sensor_board` and finishes at **13:20:53.490 UTC**. '
        'The local simulator returns `State [sensor_board]: Cooling is nearly stable; final stabilization is not complete.` '
        'That exact observation is in the next request (line 13), which starts at **13:20:53.492 UTC**, before the empty selection. '
        'There is no separately timestamped tool-delivery event; ordering and the following saved request establish that delivery preceded selection. '
        'The response is the negative state originating at simulated 09:00, returned at 11:30.', '',
        'At simulated 13:00 the hidden environment event is `Cooling is now fully stable.` **Neither agent retrieved it.** '
        'It appears in the saved scenario/evaluator context, not as an observation in either final selection request. '
        'A0 raw-call line 14 and A1 line 13 both select only `task_14` (signing the chamber record), supported by '
        'the visible review-window cue and earlier lock selection at 09:00. Both miss `dev_t_ack_cooling`; '
        'the evaluator reports TP=1, FP=0, FN=1 at steps/evaluator line 13.', '',
        '**Query-supported hidden hits: A0=0, A1=0. Correct cooling selections without relevant query evidence: A0=0, A1=0.** '
        'There is no correct hidden selection to label as a guess. Withholding at 09:00 was supported by a legitimate visible negative observation. '
        'The shared miss is task performance in obtaining/acting on the newly available hidden condition, not an infrastructure or format failure. '
        'The records do not reveal why either model failed to query at 13:00. One negative query does not establish successful monitoring.', '',
        '## Cross-day and concrete behavioral evidence', '',
        '- The Monday 08:00 message instructs filing the blue archive card on Wednesday when the brass cabinet clicks. '
        'The Tuesday 16:00 message instructs hanging the visitor badge when the east gate opens on Wednesday. '
        'Both original notes are present in the saved final requests at every Wednesday step; Wednesday’s header says only that there are no immediate intentions.',
        '- At Wednesday 10:00 (`dev_w_s2`, steps line 17), the cabinet scrapes without clicking and the gate stays closed. Both select no task.',
        '- At Wednesday 12:00 (`dev_w_s3`, line 18), the gate visibly opens and both select `task_11` (visitor badge), TP=1. '
        'The relevant raw-call lines are A0=19 and A1=18.',
        '- At Wednesday 15:00 (`dev_w_s4`, line 19), the cabinet visibly clicks and both select `task_8` (archive card), TP=1. '
        'The raw-call lines are A0=20 and A1=19. Neither condition has a cross-day failure in this trajectory.',
        '- The observed between-condition difference is the single negative sensor query by A0 at Tuesday 11:30; A1 directly chooses no task. '
        'This changes call count and context but produces no task-score difference. Both preserve the cancellation, rescheduling and prerequisite behavior.', '',
        'These are successes with complete prior conversation and action-text menus still available, not proof of an independent memory store '
        'or an explanation of internal reasoning. The 20 task selections match exactly; there is no observed accuracy advantage.', '',
        '## Cost and overhead — different sources kept separate', '',
        '| Quantity / source | USD | Meaning |', '|---|---:|---|',
        '| Pre-run usage-informed projection | 0.03935938 | Pilot-calibrated full-history estimate; assumed 44 calls and no retries/cache discount |',
        '| Pre-run conservative allowance | 0.63708409 | Up to 160 attempts including both conditions, queries, retries and output allowances; heuristic |',
        '| Authorized cumulative ceiling | 0.70000000 | Applies only to this follow-up |',
        f'| Actual tokens × frozen uncached prices | {details["usage_uncached_price_estimate_total_usd"]:.8f} | Calculation, not a bill |',
        f'| Sum of all saved API response costs | {details["api_response_cost_total_usd"]:.8f} | Provider-reported inference costs for 41 calls |',
        f'| Final cumulative request reservations | {details["final_cumulative_budget"]["reserved_estimate_usd"]:.8f} | Budget guard’s retained estimates, not charges |',
        '| Independently verified billing | unavailable | No account ledger or billing statement inspected |', '',
        'The free public route GET was the only provider preflight; there were **zero billable preflight requests** and '
        'zero unreported model attempts. All responses reported the pinned DeepSeek V3.1 / Novita route. '
        'API-reported costs were A0 $0.01454109 and A1 $0.01593485: A1 used 9,800 more input tokens (+16.56%), '
        '34 fewer output tokens and one fewer model call, but cost $0.00139376 more (+9.58%). '
        'These are observed differences for this ordered pair, not a general cost or speed effect.', '',
        'The responses report 15,808 cached input tokens for A0 and 24,832 for A1. At the saved route’s $0.135/M cache-read rate, '
        'these reconcile the uncached-price estimate with the API-reported costs. No application answer cache was introduced. '
        'Provider caching, differing query histories and fixed A0-first order confound attribution of the entire cost/latency difference to prompt length. '
        'Summed request latencies are 68.270222 s and 68.147285 s; they are not independent timing trials or the same as total study wall time. '
        'Budget snapshots are cumulative and must not be summed. The run was not restarted and unused budget was not spent.', '',
        '## Original pilot and limitations', '',
        'Pilot 1 remains unchanged in `RESULTS.md`: one eight-step pair, both 5/0/0 and Set-F1=1.00; '
        'A1 used 5,360 extra input tokens; saved API cost $0.00765034. The follow-up was planned after that result '
        'and includes the same Monday portion. Report both separately; they are not two independent replications.', '',
        'This is an exploratory development evaluation, not blind or independently held out. It has one pair, one repeat, '
        'one hidden positive event, two cross-day intentions, full histories, action-text menus and some explicit near-match/obsolete-cue wording. '
        'Frozen P1 assumes completion after selection; PM-Bench removes completed handles, so independent prompt-driven duplicate prevention '
        'and robust execution confirmation are not established. Heartbeat/background calls are disabled; querying during a supplied step '
        'is not autonomous monitoring. MOCK and local tests validate software behavior, not model superiority. '
        'No additional experimental development or inference follows this evaluation.', '',
        '## Artifacts and offline replay', '',
        f'- Study ledger: `{pair.parent / "study.json"}`.',
        f'- Frozen executed snapshot: `{pair.parent / "protocol_snapshot.json"}`.',
        f'- Pair: `{pair / "pair.json"}`.']
    for c, name in plan['runs'].items():
        lines.append(f'- {c}: `{pair / name}`; requests/responses in `raw_model_calls.jsonl`, visible observations/tools in `steps.jsonl`, scores in `score.json`, separate evaluator records in `evaluator.jsonl`, and all input hashes/settings in `manifest.json`.')
    lines += [f'- Machine-readable audit, including exact JSONL line references: `{OUT / "analysis.json"}`.',
        f'- Preserved raw study archive: `{ROOT / "artifacts/verification/followup-live-20260909.zip"}`.',
        f'- Recorded dashboard export and replay verification: `{OUT / "recorded-export.zip"}` and `{OUT / "replay-check.json"}`.', '',
        'Regenerate the numeric audit without inference:', '',
        '```bash', f'cd {ROOT}', 'python3 scripts/analyze_followup_saved.py', '```', '',
        'Replay using the unchanged dashboard (LIVE disabled):', '',
        '```bash', f'cd {ROOT}', 'python3 -m research_harness.dashboard --output-root results/followup_v1 --port 8766', '```', '',
        'Open http://127.0.0.1:8766, choose **RECORDED**, select **frozen-development-v1 · live-pair-bdf241965f35**, '
        'then **Start run** and **Advance timeline**. At steps 12 and 13 inspect the query and shared miss; '
        'at steps 18 and 19 inspect the cross-day hits. **Reveal this step** displays evaluator information separately. '
        'Replay and export make no model calls. The original pilot remains available under its original output root.', '']
    (ROOT / 'FOLLOWUP_RESULTS.md').write_text('\n'.join(lines))


def main():
    study_root = ROOT / 'results/followup_v1'
    study = json.loads((study_root / 'study.json').read_text())
    assert study['status'] == 'completed', 'Incomplete study: do not present full-trajectory results.'
    pair = study_root / study['pair_id']
    assert study['pair_id'] == 'live-pair-bdf241965f35'
    plan = json.loads((pair / 'pair.json').read_text())
    frozen = json.loads((study_root / 'protocol_snapshot.json').read_text())
    assert plan['mode'] == 'LIVE' and plan['status'] == 'completed'
    assert plan['repeat'] == 0 and plan['order'] == ['A0', 'A1']
    result = analyze(study_root, 'LIVE')
    assert len(result['pairs']) == 1 and not result['incomplete_pairs']
    conditions, portions, trajectories, hidden, cross_day = {}, {}, {}, {}, {}
    for condition, directory in plan['runs'].items():
        path = pair / directory
        manifest = verify_run(path)
        official = score_artifacts(path)
        calls, steps, evaluations = (rows(path / name) for name in ['raw_model_calls.jsonl', 'steps.jsonl', 'evaluator.jsonl'])
        assert len(steps) == len(evaluations) == manifest['completed_steps'] == 20
        assert manifest['prompt_hash'] == frozen['conditions'][condition]['effective_prompt_sha256']
        assert all(c['reported_model'] == frozen['model']['model_id'] and c['provider_metadata']['provider_reported'] == 'Novita' for c in calls)
        expected = {'model': frozen['model']['model_id'], 'provider': 'openrouter', 'provider_route': 'novita',
            'provider_quantizations': ['fp8'], 'provider_require_parameters': True, 'route_fallbacks_allowed': False,
            'reasoning': frozen['model']['reasoning'], 'max_tokens': frozen['limits']['max_output_tokens'], **frozen['sampling']}
        assert all(all(c['request'][k] == v for k, v in expected.items()) for c in calls)
        assert all(c['request']['messages'][0]['content'] == (path / 'system_prompt.txt').read_text() for c in calls)
        measured = metrics(evaluations, calls, steps)
        for k in ['tp', 'fp', 'fn']:
            assert measured[k] == official['summary']['set_' + k]
        assert measured['tool_queries'] == official['summary']['state_query_calls']
        assert measured['set_f1'] == official['rates']['set_f1']
        assert measured['api_response_cost_usd'] == money([manifest['reported_cost_usd']]) or abs(measured['api_response_cost_usd'] - manifest['reported_cost_usd']) < 1e-12
        conditions[condition] = measured
        portions[condition] = {}
        for label, days in [('overlapping_Monday', {'Monday'}), ('additional_12_steps', {'Tuesday', 'Wednesday'}), ('Tuesday', {'Tuesday'}), ('Wednesday', {'Wednesday'})]:
            portions[condition][label] = metrics([e for e in evaluations if e['day'] in days],
                [c for c in calls if c['call_context']['day'] in days], [s for s in steps if s['day'] in days])
        trajectories[condition], hidden[condition], cross_day[condition] = [], [], []
        for line, (step, evaluation) in enumerate(zip(steps, evaluations), 1):
            assert step['step_id'] == evaluation['step_id']
            step_calls = [(n, c) for n, c in enumerate(calls, 1) if c['call_context']['step_id'] == step['step_id'] and c['call_context']['day'] == step['day']]
            choose_calls = [(n, c) for n, c in step_calls if (c.get('parsed_action') or {}).get('action') == 'choose' and not c.get('parse_error')]
            final = choose_calls[-1][1] if choose_calls else None
            messages = final['request']['messages'] if final else []
            selected, due = set(evaluation['selected_task_ids']), set(evaluation['due_task_ids'])
            trajectories[condition].append({'line': line, 'step_id': step['step_id'], 'day': step['day'], 'time': step['time'],
                'selected': sorted(selected), 'due': sorted(due), 'tp': evaluation['tp'], 'fp': evaluation['fp'], 'fn': evaluation['fn'],
                'missed': evaluation['missed'], 'false': evaluation['false'], 'ongoing_choice': step['action']['choice'], 'tools': step['tools'], 'execution': step['execution']})
            if step['day'] == 'Tuesday':
                relevant = [m['content'] for m in messages if m['role'] == 'user' and m['content'].startswith('State [sensor_board]:')]
                observed_positive = any('Cooling is now fully stable.' in m for m in relevant)
                task = 'dev_t_ack_cooling'
                hidden[condition].append({'step_id': step['step_id'], 'simulated_time': step['time'], 'steps_and_evaluator_line': line,
                    'visible_before_any_query': step['agent_messages'][-1]['content'],
                    'queries': [{'raw_call_line': n, 'channel': c['parsed_action']['channel'], 'query_decision_finished_at_utc': c['finished_at_utc']}
                                for n, c in step_calls if (c.get('parsed_action') or {}).get('action') in ['query_state', 'check_time']],
                    'tool_responses': step['tools'], 'sensor_observations_in_final_request': relevant,
                    'final_choose_raw_call_line': choose_calls[-1][0] if choose_calls else None,
                    'final_choose_started_at_utc': final['started_at_utc'] if final else None,
                    'positive_sensor_fact_observed_before_selection': observed_positive,
                    'cooling_selected': task in selected, 'cooling_due': task in due,
                    'cooling_hit': task in selected & due, 'cooling_false_selection': task in selected - due,
                    'cooling_missed': task in due - selected,
                    'query_supported_hit': task in selected & due and observed_positive,
                    'correct_selection_without_sensor_query_evidence': task in selected & due and not observed_positive})
            if step['day'] == 'Wednesday':
                texts = [m['content'] for m in messages if m['role'] == 'user']
                cross_day[condition].append({'step_id': step['step_id'], 'time': step['time'], 'steps_and_evaluator_line': line,
                    'final_choose_raw_call_line': choose_calls[-1][0] if choose_calls else None,
                    'visible_current': step['agent_messages'][-1]['content'],
                    'monday_archive_note_present': any('On Wednesday, File the blue archive card when the brass cabinet clicks.' in t for t in texts),
                    'tuesday_badge_note_present': any('On Wednesday, Hang the visitor badge when the east gate opens.' in t for t in texts),
                    'wednesday_header': next((t for t in texts if t.startswith('=== Wednesday ===')), None),
                    'selected': sorted(selected), 'due': sorted(due), 'tp': evaluation['tp'], 'fp': evaluation['fp'], 'fn': evaluation['fn']})
    a, b = conditions['A0'], conditions['A1']
    differences = difference(a, b)
    details = {'status': 'completed', 'mode': 'LIVE', 'pair_id': plan['pair_id'], 'pair_path': str(pair),
        'started_at_utc': study['started_at_utc'], 'finished_at_utc': study['finished_at_utc'],
        'complete_matched_pairs': 1, 'repeats': 1, 'analysis_unit': 'one full three-day paired trajectory; no independent step/day replication or pooling with pilot 1',
        'conditions': conditions, 'a1_minus_a0': differences, 'descriptive_portions': portions,
        'trajectories': trajectories, 'hidden_condition_audit': hidden, 'cross_day_audit': cross_day,
        'task_selections_identical': all(x['selected'] == y['selected'] for x, y in zip(trajectories['A0'], trajectories['A1'])),
        'usage_informed_pre_run_estimate_usd': frozen['usage_informed_estimate']['total_usd'],
        'conservative_pre_run_allowance_usd': frozen['conservative_allowance_usd'],
        'api_response_cost_total_usd': money([a['api_response_cost_usd'], b['api_response_cost_usd']]),
        'usage_uncached_price_estimate_total_usd': money([a['usage_uncached_price_estimate_usd'], b['usage_uncached_price_estimate_usd']]),
        'verified_billed_cost_usd': None, 'final_cumulative_budget': study['budget'],
        'billable_preflight_requests': 0, 'experimental_deviations': [],
        'artifact_sha256': {str(f.relative_to(ROOT)): sha256_file(f) for f in sorted(study_root.rglob('*')) if f.is_file()}}
    assert details['api_response_cost_total_usd'] <= .70
    assert abs(details['api_response_cost_total_usd'] - study['budget']['reported_cost_usd']) < 1e-12
    OUT.mkdir(exist_ok=True)
    (OUT / 'analysis.json').write_text(json.dumps(details, indent=2, ensure_ascii=False) + '\n')
    (ROOT / 'FOLLOWUP_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    write_report(details, plan)
    print(json.dumps({k: v for k, v in details.items() if k not in ['artifact_sha256', 'trajectories', 'hidden_condition_audit', 'cross_day_audit', 'descriptive_portions']}, indent=2))


if __name__ == '__main__':
    main()

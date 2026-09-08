# Kiodai results — LIVE

Genuine saved inference artifacts only; no mock data included.

| Mode | Condition | Status | TP | FP | FN | Precision | Recall | Set-F1 | Invalid | Retries | Tools | Reported USD |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| LIVE | A0 | completed | 5 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 0 | 0.0034 |
| LIVE | A1 | completed | 5 | 0 | 0 | 1.0000 | 1.0000 | 1.0000 | 0 | 0 | 0 | 0.0043 |

| Condition | Cancellation/update violations | Duplicates (commission) | Late actions | Tokens | Model latency s | Estimated USD |
|---|---:|---:|---:|---|---|---|
| A0 | 0 | 0 | 0 | 14088 | 26.383078 | 0.00400013 |
| A1 | 0 | 0 | 0 | 19448 | 26.248401 | 0.00544733 |

Run artifacts:
- `/Users/bagnesium/Documents/GitHub/Kiodai/results/kiodai/live-pair-42433e00474b/live-A0-20260908T164420-7848b46b/manifest.json`
- `/Users/bagnesium/Documents/GitHub/Kiodai/results/kiodai/live-pair-42433e00474b/live-A1-20260908T164420-2fdeb6e6/manifest.json`

Complete pairs: 1. Incomplete pairs: 2.
Mean scenario-level paired Set-F1 difference: 0.0.

whole scenario/trajectory; average repeats within scenarios first; days and steps are not independent samples.
No confidence intervals or significance claims for this tiny pilot. Missing and zero-denominator values remain unavailable.
Official detailed scores include lifecycle violations, late actions, duplicates (commission), and per-day counts. Token, latency and cost details are in each manifest. Mock token values are estimates, not measurements.

## Completed frozen pilot

Pair: `/Users/bagnesium/Documents/GitHub/Kiodai/results/kiodai/live-pair-42433e00474b`. Executed 2026-09-08T16:44:19.395Z–2026-09-08T16:45:13.556Z.

One development scenario, one repeat, two complete eight-step trajectories; 16 genuine model calls total. Both selected all five due task actions correctly and matched all eight step-level due sets. All task selections were identical. A0 chose ongoing option B and A1 option A at 08:30; this ongoing-task choice is not scored by the prospective-memory metric.

| Measure | A0 | A1 | A1 minus A0 |
|---|---:|---:|---:|
| tp | 5 | 5 | 0.0 |
| fp | 0 | 0 | 0.0 |
| fn | 0 | 0 | 0.0 |
| precision | 1.0 | 1.0 | 0.0 |
| recall | 1.0 | 1.0 | 0.0 |
| set_f1 | 1.0 | 1.0 | 0.0 |
| model_attempts | 8 | 8 | 0.0 |
| tool_queries | 0 | 0 | 0.0 |
| invalid_responses | 0 | 0 | 0.0 |
| retries | 0 | 0 | 0.0 |
| input_tokens | 13819 | 19179 | 5360.0 |
| output_tokens | 269 | 269 | 0.0 |
| total_tokens | 14088 | 19448 | 5360.0 |
| model_latency_seconds | 26.383078 | 26.248401 | -0.134677 |
| provider_reported_cost_usd | 0.00336941 | 0.00428093 | 0.00091152 |

Aggregation sums TP/FP/FN over each whole trajectory, then computes precision, recall and Set-F1. The paired difference is A1 minus A0 for that trajectory. With one scenario and one repeat, the scenario-mean difference equals this single difference. Steps are not independent experimental units. No confidence interval, p-value or equivalence claim is warranted.

## Cost sources

| Cost measure | USD | Interpretation |
|---|---:|---|
| Prospective stress estimate | 0.13677592 | Both conditions, maximum queries/retries, 256 output tokens per attempt; heuristic, not a bill |
| Usage × frozen uncached list prices | 0.00944746 | Computed from actual tokens, ignores cache discounts |
| Provider-reported total | 0.00765034 | Sum of all 16 saved response costs |
| Verified billed total | unavailable | No billing statement or account ledger was inspected |

Provider responses report 4,672 cached input tokens for A0 and 8,640 for A1. At the advertised half-price cache-read rate, these account for the difference between the uncached estimate and reported response costs. Caching was provider-reported; no application answer cache or shared condition memory was added. Do not infer a general latency/cost effect from this single ordered pair. Budget snapshots are cumulative and must not be summed across conditions; the last A1 snapshot reserves $0.01924624 for the actual 16 requests. Remaining balance was not spent.

## Concrete successes and failures

- At 09:40 both logged humidity and ignored the blue-circle lure for a task requiring a blue hexagon.
- At 10:50 both released the sample envelope on the correct cue and did not recycle the canceled proof.
- At the superseded 11:00 deadline both selected no task action; at 11:20 both inspected the pressure gauge and sent the corrected status note.
- There were no observed task-performance failures, malformed responses, transport errors, retries or tool queries in the completed pair. No failed model example can honestly be supplied.

The two earlier infrastructure failures remain in the dataset:

- `/Users/bagnesium/Documents/GitHub/Kiodai/results/kiodai/live-pair-8eafb0fb7cc2/pair.json`: certificate verification failed in the free route lookup; no condition sessions or model requests. Preserved byte-for-byte.
- `/Users/bagnesium/Documents/GitHub/Kiodai/results/kiodai/live-pair-c13c57cee05d/pair.json`: certificate verification failed in the free route lookup; no condition sessions or model requests. Preserved byte-for-byte.

## Interpretation and limitations

This is an exploratory development pilot with a ceiling result in both conditions. It found no task-accuracy improvement from the frozen P1 instruction; it does not establish general equivalence or general superiority. A1 used 5,360 more input tokens and its response-reported cost was $0.00091152 higher in this pair. No hidden-state query, cross-day retention, real tool-failure recovery or autonomous monitoring was demonstrated.

Frozen P1 assumes completion after selection; it does not robustly confirm successful execution. PM-Bench removes completed handles, so duplicate prevention is not independently attributable to the prompt. Heartbeat was disabled in both conditions. Software tests and MOCK demonstrations are separate from this live model evidence.

Replay: `python3 -m research_harness.dashboard`, then choose **RECORDED** and **first-development-day-pilot-v1 · live-pair-42433e00474b**. Replay makes no inference calls.

Rebuild this full report: `python3 artifacts/verification/analyze_live_pilot_20260908.py`. Machine-readable detailed analysis and all source-file hashes: `artifacts/verification/live-pilot-analysis-20260908.json`.

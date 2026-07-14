# PM-Bench score report

## Summary

Hit: 40 | Late: 4 | Miss: 37 | False alarms: 35 | Commission: 0 | Wrong-content: 11 | Dependency violations: 0 | Overkill steps: 28 | state query calls: 9 | check_time calls: 9 | Actions: 79
Exact-set: matches 22 | mismatches 58 | reward -36
Set micro: TP 40 | FP 39 | FN 41
Cross-day: hit 0 | late 1 | miss 6 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 16
Rates: hit 49.4% | late 4.9% | miss 45.7% | false alarm/step 43.8% | commission 0.0% | wrong-content 13.6% | dependency/step 0.0% | overkill/step 35.0% | cross-day miss 85.7% | update miss 66.7% | precision_hit 50.6% | precision_any 55.7% | exact-set match rate 27.5% | exact-set avg reward -0.450 | set_precision 50.6% | set_recall 49.4% | set_f1 50.0%
Hit rates (by modality): event 54.4% | time 37.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:26:53.432Z |
| Finished (UTC) | 2026-03-28T22:28:00.890Z |
| Duration | 1m 7.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 40 |
| Late | 4 |
| Miss | 37 |
| False alarms | 35 |
| Commission | 0 |
| Wrong-content | 11 |
| Dependency violations | 0 |
| Overkill steps | 28 |
| State query calls | 9 |
| Check_time calls | 9 |
| Actions | 79 |
| Exact-set matches | 22 |
| Exact-set mismatches | 58 |
| Exact-set reward | -36 |
| Set TP | 40 |
| Set FP | 39 |
| Set FN | 41 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 9 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 49.4% |
| Late rate | 4.9% |
| Miss rate | 45.7% |
| False alarm/step | 43.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 13.6% |
| Dependency/step | 0.0% |
| Overkill/step | 35.0% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 50.6% |
| Precision any | 55.7% |
| Exact-set match rate | 27.5% |
| Exact-set avg reward | -0.450 |
| Set precision | 50.6% |
| Set recall | 49.4% |
| Set F1 | 50.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 31 | 57 | 54.4% |
| Time (time + time_check) | 9 | 24 | 37.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 1 | 10 | 42 | 73.8% | 76.2% |
| proactive_monitoring_required | 9 | 3 | 27 | 39 | 23.1% | 30.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 9 | 2 | 13 | 24 | 37.5% | 45.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 53.8% | 30.8% | 55.6% | 33.3% | 83.3% | 16.7% | 38.5% | -0.231 | 46.2% | 50.0% | 48.0% |
| Tuesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 38.5% | 38.5% | 57.1% | 50.0% | 100.0% | 28.6% | 30.8% | -0.385 | 50.0% | 54.5% | 52.2% |
| Wednesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 50.0% | 40.0% | 33.3% | 50.0% | 50.0% | 20.0% | 20.0% | -0.600 | 40.0% | 36.4% | 38.1% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 36.4% | 36.4% | 66.7% | 33.3% | 75.0% | 25.0% | 36.4% | -0.273 | 63.6% | 58.3% | 60.9% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 50.0% | 41.7% | 50.0% | 50.0% | 66.7% | 33.3% | 16.7% | -0.667 | 50.0% | 50.0% | 50.0% |
| Saturday | 6 | 1 | 7 | 42.9% | 7.1% | 50.0% | 30.0% | 20.0% | 50.0% | 25.0% | 62.5% | 16.7% | 20.0% | -0.600 | 60.0% | 42.9% | 50.0% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 45.5% | 36.4% | 80.0% | 25.0% | 100.0% | 20.0% | 27.3% | -0.455 | 45.5% | 55.6% | 50.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 1 |
| Friday | clock | 2 |
| Saturday | clock | 1 |
| Sunday | clock | 1 |

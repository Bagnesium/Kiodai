# PM-Bench score report

## Summary

Hit: 48 | Late: 1 | Miss: 32 | False alarms: 19 | Commission: 0 | Wrong-content: 7 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 0 | check_time calls: 0 | Actions: 68
Exact-set: matches 42 | mismatches 38 | reward 4
Set micro: TP 48 | FP 20 | FN 33
Cross-day: hit 4 | late 0 | miss 3 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 7
Rates: hit 59.3% | late 1.2% | miss 39.5% | false alarm/step 23.8% | commission 0.0% | wrong-content 8.6% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 42.9% | update miss 55.6% | precision_hit 70.6% | precision_any 72.1% | exact-set match rate 52.5% | exact-set avg reward 0.050 | set_precision 70.6% | set_recall 59.3% | set_f1 64.4%
Hit rates (by modality): event 63.2% | time 50.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-26T21:47:42.731Z |
| Finished (UTC) | 2026-03-26T21:49:35.571Z |
| Duration | 1m 52.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 48 |
| Late | 1 |
| Miss | 32 |
| False alarms | 19 |
| Commission | 0 |
| Wrong-content | 7 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 68 |
| Exact-set matches | 42 |
| Exact-set mismatches | 38 |
| Exact-set reward | 4 |
| Set TP | 48 |
| Set FP | 20 |
| Set FN | 33 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 59.3% |
| Late rate | 1.2% |
| Miss rate | 39.5% |
| False alarm/step | 23.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.6% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 42.9% |
| Update miss rate | 55.6% |
| Precision hit | 70.6% |
| Precision any | 72.1% |
| Exact-set match rate | 52.5% |
| Exact-set avg reward | 0.050 |
| Set precision | 70.6% |
| Set recall | 59.3% |
| Set F1 | 64.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 36 | 57 | 63.2% |
| Time (time + time_check) | 12 | 24 | 50.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 36 | 0 | 6 | 42 | 85.7% | 85.7% |
| proactive_monitoring_required | 12 | 1 | 26 | 39 | 30.8% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 12 | 1 | 11 | 24 | 50.0% | 54.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 23.1% | 7.7% | 44.4% | 33.3% | 66.7% | 16.7% | 53.8% | 0.077 | 55.6% | 41.7% | 47.6% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 7.7% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 87.5% | 63.6% | 73.7% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 20.0% | 10.0% | 55.6% | 50.0% | 83.3% | 20.0% | 60.0% | 0.200 | 75.0% | 54.5% | 63.2% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 18.2% | 88.9% | 33.3% | 100.0% | 25.0% | 63.6% | 0.273 | 81.8% | 75.0% | 78.3% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 50.0% | 41.7% | 50.0% | 25.0% | 66.7% | 16.7% | 8.3% | -0.833 | 45.5% | 41.7% | 43.5% |
| Saturday | 10 | 0 | 4 | 71.4% | 0.0% | 28.6% | 30.0% | 20.0% | 70.0% | 75.0% | 87.5% | 50.0% | 50.0% | 0.000 | 76.9% | 71.4% | 74.1% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 18.2% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | (none) | 0 |
| Tuesday | (none) | 0 |
| Wednesday | (none) | 0 |
| Thursday | (none) | 0 |
| Friday | (none) | 0 |
| Saturday | (none) | 0 |
| Sunday | (none) | 0 |

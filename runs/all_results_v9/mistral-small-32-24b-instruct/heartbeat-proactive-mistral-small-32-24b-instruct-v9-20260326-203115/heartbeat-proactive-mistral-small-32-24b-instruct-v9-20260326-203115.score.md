# PM-Bench score report

## Summary

Hit: 35 | Late: 2 | Miss: 44 | False alarms: 14 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 13 | state query calls: 0 | check_time calls: 0 | Actions: 51
Exact-set: matches 34 | mismatches 46 | reward -12
Set micro: TP 35 | FP 16 | FN 46
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 5
Rates: hit 43.2% | late 2.5% | miss 54.3% | false alarm/step 17.5% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 16.2% | cross-day miss 71.4% | update miss 88.9% | precision_hit 68.6% | precision_any 72.5% | exact-set match rate 42.5% | exact-set avg reward -0.150 | set_precision 68.6% | set_recall 43.2% | set_f1 53.0%
Hit rates (by modality): event 47.4% | time 33.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:31:15.800Z |
| Finished (UTC) | 2026-03-27T03:32:34.709Z |
| Duration | 1m 18.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 35 |
| Late | 2 |
| Miss | 44 |
| False alarms | 14 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 13 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 51 |
| Exact-set matches | 34 |
| Exact-set mismatches | 46 |
| Exact-set reward | -12 |
| Set TP | 35 |
| Set FP | 16 |
| Set FN | 46 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 43.2% |
| Late rate | 2.5% |
| Miss rate | 54.3% |
| False alarm/step | 17.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 16.2% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 88.9% |
| Precision hit | 68.6% |
| Precision any | 72.5% |
| Exact-set match rate | 42.5% |
| Exact-set avg reward | -0.150 |
| Set precision | 68.6% |
| Set recall | 43.2% |
| Set F1 | 53.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 27 | 57 | 47.4% |
| Time (time + time_check) | 8 | 24 | 33.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 27 | 2 | 13 | 42 | 64.3% | 69.0% |
| proactive_monitoring_required | 8 | 0 | 31 | 39 | 20.5% | 20.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 8 | 0 | 16 | 24 | 33.3% | 33.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 23.1% | 7.7% | 44.4% | 66.7% | 66.7% | 33.3% | 53.8% | 0.077 | 66.7% | 50.0% | 57.1% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 15.4% | 15.4% | 57.1% | 50.0% | 100.0% | 28.6% | 53.8% | 0.077 | 75.0% | 54.5% | 63.2% |
| Wednesday | 2 | 2 | 7 | 18.2% | 18.2% | 63.6% | 20.0% | 30.0% | 22.2% | 0.0% | 33.3% | 0.0% | 20.0% | -0.600 | 33.3% | 18.2% | 23.5% |
| Thursday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 27.3% | 27.3% | 44.4% | 33.3% | 50.0% | 25.0% | 36.4% | -0.273 | 62.5% | 41.7% | 50.0% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 16.7% | 16.7% | 50.0% | 25.0% | 66.7% | 16.7% | 33.3% | -0.333 | 71.4% | 41.7% | 52.6% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 10.0% | 10.0% | 50.0% | 25.0% | 62.5% | 16.7% | 40.0% | -0.200 | 85.7% | 42.9% | 57.1% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 9.1% | 9.1% | 80.0% | 25.0% | 100.0% | 20.0% | 54.5% | 0.091 | 83.3% | 55.6% | 66.7% |

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

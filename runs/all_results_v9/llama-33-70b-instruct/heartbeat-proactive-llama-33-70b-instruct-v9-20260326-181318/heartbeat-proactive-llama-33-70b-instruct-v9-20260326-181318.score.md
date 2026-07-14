# PM-Bench score report

## Summary

Hit: 49 | Late: 2 | Miss: 30 | False alarms: 12 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 10 | state query calls: 13 | check_time calls: 11 | Actions: 63
Exact-set: matches 44 | mismatches 36 | reward 8
Set micro: TP 49 | FP 14 | FN 32
Cross-day: hit 3 | late 0 | miss 4 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 8
Rates: hit 60.5% | late 2.5% | miss 37.0% | false alarm/step 15.0% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 12.5% | cross-day miss 57.1% | update miss 66.7% | precision_hit 77.8% | precision_any 81.0% | exact-set match rate 55.0% | exact-set avg reward 0.100 | set_precision 77.8% | set_recall 60.5% | set_f1 68.1%
Hit rates (by modality): event 61.4% | time 58.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T01:13:18.102Z |
| Finished (UTC) | 2026-03-27T01:15:42.242Z |
| Duration | 2m 24.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 49 |
| Late | 2 |
| Miss | 30 |
| False alarms | 12 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 10 |
| State query calls | 13 |
| Check_time calls | 11 |
| Actions | 63 |
| Exact-set matches | 44 |
| Exact-set mismatches | 36 |
| Exact-set reward | 8 |
| Set TP | 49 |
| Set FP | 14 |
| Set FN | 32 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 11 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 60.5% |
| Late rate | 2.5% |
| Miss rate | 37.0% |
| False alarm/step | 15.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 12.5% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 66.7% |
| Precision hit | 77.8% |
| Precision any | 81.0% |
| Exact-set match rate | 55.0% |
| Exact-set avg reward | 0.100 |
| Set precision | 77.8% |
| Set recall | 60.5% |
| Set F1 | 68.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 35 | 57 | 61.4% |
| Time (time + time_check) | 14 | 24 | 58.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 35 | 0 | 7 | 42 | 83.3% | 83.3% |
| proactive_monitoring_required | 14 | 2 | 23 | 39 | 35.9% | 41.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 14 | 2 | 8 | 24 | 58.3% | 66.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 1 | 5 | 50.0% | 8.3% | 41.7% | 23.1% | 7.7% | 44.4% | 66.7% | 66.7% | 33.3% | 53.8% | 0.077 | 60.0% | 50.0% | 54.5% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 15.4% | 15.4% | 57.1% | 75.0% | 100.0% | 42.9% | 53.8% | 0.077 | 77.8% | 63.6% | 70.0% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 44.4% | 100.0% | 66.7% | 40.0% | 70.0% | 0.400 | 100.0% | 54.5% | 70.6% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 6 | 1 | 5 | 50.0% | 8.3% | 41.7% | 16.7% | 25.0% | 50.0% | 50.0% | 66.7% | 33.3% | 33.3% | -0.333 | 66.7% | 50.0% | 57.1% |
| Saturday | 10 | 0 | 4 | 71.4% | 0.0% | 28.6% | 30.0% | 20.0% | 70.0% | 75.0% | 87.5% | 50.0% | 50.0% | 0.000 | 76.9% | 71.4% | 74.1% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 9.1% | 9.1% | 80.0% | 25.0% | 100.0% | 20.0% | 54.5% | 0.091 | 83.3% | 55.6% | 66.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 1 |
| Thursday | clock | 3 |
| Friday | clock | 2 |
| Saturday | (none) | 0 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 1 |

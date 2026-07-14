# PM-Bench score report

## Summary

Hit: 50 | Late: 2 | Miss: 29 | False alarms: 5 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 4 | state query calls: 9 | check_time calls: 6 | Actions: 57
Exact-set: matches 52 | mismatches 28 | reward 24
Set micro: TP 50 | FP 7 | FN 31
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 5 | late 1 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 61.7% | late 2.5% | miss 35.8% | false alarm/step 6.2% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 5.0% | cross-day miss 14.3% | update miss 33.3% | precision_hit 87.7% | precision_any 91.2% | exact-set match rate 65.0% | exact-set avg reward 0.300 | set_precision 87.7% | set_recall 61.7% | set_f1 72.5%
Hit rates (by modality): event 66.7% | time 50.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T04:04:42.012Z |
| Finished (UTC) | 2026-03-27T04:08:04.906Z |
| Duration | 3m 22.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 50 |
| Late | 2 |
| Miss | 29 |
| False alarms | 5 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 4 |
| State query calls | 9 |
| Check_time calls | 6 |
| Actions | 57 |
| Exact-set matches | 52 |
| Exact-set mismatches | 28 |
| Exact-set reward | 24 |
| Set TP | 50 |
| Set FP | 7 |
| Set FN | 31 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 6 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 61.7% |
| Late rate | 2.5% |
| Miss rate | 35.8% |
| False alarm/step | 6.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 5.0% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 87.7% |
| Precision any | 91.2% |
| Exact-set match rate | 65.0% |
| Exact-set avg reward | 0.300 |
| Set precision | 87.7% |
| Set recall | 61.7% |
| Set F1 | 72.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 57 | 66.7% |
| Time (time + time_check) | 12 | 24 | 50.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
| proactive_monitoring_required | 12 | 2 | 25 | 39 | 30.8% | 35.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 12 | 1 | 11 | 24 | 50.0% | 54.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 66.7% | 66.7% | 100.0% | 33.3% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 0.0% | 0.0% | 55.6% | 50.0% | 83.3% | 20.0% | 70.0% | 0.400 | 100.0% | 54.5% | 70.6% |
| Thursday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 9.1% | 18.2% | 77.8% | 33.3% | 87.5% | 25.0% | 63.6% | 0.273 | 80.0% | 66.7% | 72.7% |
| Friday | 7 | 1 | 4 | 58.3% | 8.3% | 33.3% | 16.7% | 8.3% | 62.5% | 50.0% | 83.3% | 33.3% | 58.3% | 0.167 | 70.0% | 58.3% | 63.6% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 0.0% | 0.0% | 80.0% | 25.0% | 100.0% | 16.7% | 60.0% | 0.200 | 100.0% | 64.3% | 78.3% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 18.2% | 9.1% | 60.0% | 50.0% | 75.0% | 40.0% | 54.5% | 0.091 | 71.4% | 55.6% | 62.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 2 |
| Wednesday | bank_balance | 1 |
| Thursday | clock | 1 |
| Thursday | shipment_status | 1 |
| Friday | clock | 1 |
| Saturday | (none) | 0 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 1 |

# PM-Bench score report

## Summary

Hit: 8 | Late: 0 | Miss: 73 | False alarms: 3 | Commission: 1 | Wrong-content: 2 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 237 | check_time calls: 80 | Actions: 12
Exact-set: matches 33 | mismatches 47 | reward -14
Set micro: TP 8 | FP 4 | FN 73
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 0 | late 0 | miss 9 | canceled 2 | total 11 | violations 1
Rates: hit 9.9% | late 0.0% | miss 90.1% | false alarm/step 3.8% | commission 1.2% | wrong-content 2.5% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 100.0% | update miss 100.0% | precision_hit 66.7% | precision_any 66.7% | exact-set match rate 41.2% | exact-set avg reward -0.175 | set_precision 66.7% | set_recall 9.9% | set_f1 17.2%
Hit rates (by modality): event 10.5% | time 8.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T05:03:17.801Z |
| Finished (UTC) | 2026-03-28T05:03:17.801Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 8 |
| Late | 0 |
| Miss | 73 |
| False alarms | 3 |
| Commission | 1 |
| Wrong-content | 2 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 237 |
| Check_time calls | 80 |
| Actions | 12 |
| Exact-set matches | 33 |
| Exact-set mismatches | 47 |
| Exact-set reward | -14 |
| Set TP | 8 |
| Set FP | 4 |
| Set FN | 73 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 50 |
| bank_balance | 5 |
| calendar | 36 |
| clock | 80 |
| email | 20 |
| laundry_status | 1 |
| library_hold | 40 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 9.9% |
| Late rate | 0.0% |
| Miss rate | 90.1% |
| False alarm/step | 3.8% |
| Commission rate | 1.2% |
| Wrong-content rate | 2.5% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 100.0% |
| Precision hit | 66.7% |
| Precision any | 66.7% |
| Exact-set match rate | 41.2% |
| Exact-set avg reward | -0.175 |
| Set precision | 66.7% |
| Set recall | 9.9% |
| Set F1 | 17.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 6 | 57 | 10.5% |
| Time (time + time_check) | 2 | 24 | 8.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 6 | 0 | 36 | 42 | 14.3% | 14.3% |
| proactive_monitoring_required | 2 | 0 | 37 | 39 | 5.1% | 5.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 2 | 0 | 22 | 24 | 8.3% | 8.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 0.0% | 0.0% | 11.1% | 0.0% | 16.7% | 0.0% | 38.5% | -0.231 | 100.0% | 8.3% | 15.4% |
| Tuesday | 2 | 0 | 9 | 18.2% | 0.0% | 81.8% | 0.0% | 0.0% | 14.3% | 25.0% | 25.0% | 14.3% | 61.5% | 0.231 | 66.7% | 18.2% | 28.6% |
| Wednesday | 1 | 0 | 10 | 9.1% | 0.0% | 90.9% | 20.0% | 10.0% | 11.1% | 0.0% | 16.7% | 0.0% | 40.0% | -0.200 | 33.3% | 9.1% | 14.3% |
| Thursday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 0.0% | 0.0% | 11.1% | 33.3% | 12.5% | 25.0% | 45.5% | -0.091 | 100.0% | 16.7% | 28.6% |
| Friday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 0.0% | 0.0% | 12.5% | 0.0% | 16.7% | 0.0% | 41.7% | -0.167 | 100.0% | 8.3% | 15.4% |
| Saturday | 1 | 0 | 13 | 7.1% | 0.0% | 92.9% | 10.0% | 10.0% | 10.0% | 0.0% | 12.5% | 0.0% | 20.0% | -0.600 | 50.0% | 7.1% | 12.5% |
| Sunday | 0 | 0 | 9 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 36.4% | -0.273 | n/a | 0.0% | 0.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 7 |
| Monday | clock | 13 |
| Monday | email | 6 |
| Monday | library_hold | 6 |
| Tuesday | calendar | 11 |
| Tuesday | clock | 13 |
| Tuesday | email | 2 |
| Tuesday | library_hold | 6 |
| Wednesday | bank_balance | 3 |
| Wednesday | calendar | 7 |
| Wednesday | clock | 10 |
| Thursday | appointment_portal | 10 |
| Thursday | bank_balance | 2 |
| Thursday | clock | 11 |
| Thursday | shipment_status | 5 |
| Friday | appointment_portal | 12 |
| Friday | clock | 12 |
| Friday | email | 11 |
| Friday | laundry_status | 1 |
| Friday | library_hold | 7 |
| Saturday | appointment_portal | 10 |
| Saturday | calendar | 7 |
| Saturday | clock | 10 |
| Saturday | email | 1 |
| Saturday | library_hold | 10 |
| Sunday | appointment_portal | 11 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |
| Sunday | library_hold | 11 |

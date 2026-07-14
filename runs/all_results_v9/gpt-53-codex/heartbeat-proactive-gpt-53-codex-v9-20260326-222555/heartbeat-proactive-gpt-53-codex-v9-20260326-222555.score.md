# PM-Bench score report

## Summary

Hit: 59 | Late: 5 | Miss: 17 | False alarms: 9 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 46 | check_time calls: 23 | Actions: 73
Exact-set: matches 52 | mismatches 28 | reward 24
Set micro: TP 59 | FP 14 | FN 22
Cross-day: hit 5 | late 0 | miss 2 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 72.8% | late 6.2% | miss 21.0% | false alarm/step 11.2% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 28.6% | update miss 22.2% | precision_hit 80.8% | precision_any 87.7% | exact-set match rate 65.0% | exact-set avg reward 0.300 | set_precision 80.8% | set_recall 72.8% | set_f1 76.6%
Hit rates (by modality): event 70.2% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T05:25:55.855Z |
| Finished (UTC) | 2026-03-27T05:36:12.548Z |
| Duration | 10m 16.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 59 |
| Late | 5 |
| Miss | 17 |
| False alarms | 9 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 46 |
| Check_time calls | 23 |
| Actions | 73 |
| Exact-set matches | 52 |
| Exact-set mismatches | 28 |
| Exact-set reward | 24 |
| Set TP | 59 |
| Set FP | 14 |
| Set FN | 22 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 4 |
| calendar | 3 |
| clock | 23 |
| course_portal | 1 |
| email | 8 |
| laundry_status | 1 |
| library_hold | 2 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 72.8% |
| Late rate | 6.2% |
| Miss rate | 21.0% |
| False alarm/step | 11.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 22.2% |
| Precision hit | 80.8% |
| Precision any | 87.7% |
| Exact-set match rate | 65.0% |
| Exact-set avg reward | 0.300 |
| Set precision | 80.8% |
| Set recall | 72.8% |
| Set F1 | 76.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 20 | 5 | 14 | 39 | 51.3% | 64.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 19 | 1 | 4 | 24 | 79.2% | 83.3% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 7.7% | 7.7% | 66.7% | 100.0% | 100.0% | 50.0% | 69.2% | 0.385 | 81.8% | 75.0% | 78.3% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 15.4% | 15.4% | 71.4% | 75.0% | 100.0% | 57.1% | 61.5% | 0.231 | 72.7% | 72.7% | 72.7% |
| Wednesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 0.0% | 10.0% | 55.6% | 100.0% | 83.3% | 40.0% | 60.0% | 0.200 | 87.5% | 63.6% | 73.7% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 77.8% | 66.7% | 87.5% | 50.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 16.7% | 8.3% | 62.5% | 100.0% | 83.3% | 66.7% | 66.7% | 0.333 | 75.0% | 75.0% | 75.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 30.0% | 20.0% | 80.0% | 75.0% | 100.0% | 50.0% | 50.0% | 0.000 | 78.6% | 78.6% | 78.6% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 3 |
| Monday | email | 2 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 3 |
| Tuesday | email | 3 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 1 |
| Wednesday | course_portal | 1 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | laundry_status | 1 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 2 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |

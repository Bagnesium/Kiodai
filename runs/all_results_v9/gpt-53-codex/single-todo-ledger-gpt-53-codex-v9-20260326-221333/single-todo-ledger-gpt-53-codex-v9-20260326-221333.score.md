# PM-Bench score report

## Summary

Hit: 55 | Late: 4 | Miss: 22 | False alarms: 7 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 42 | check_time calls: 33 | Actions: 66
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 55 | FP 11 | FN 26
Cross-day: hit 3 | late 0 | miss 4 | total 7
Updates: hit 5 | late 1 | miss 3 | canceled 2 | total 11 | violations 4
Rates: hit 67.9% | late 4.9% | miss 27.2% | false alarm/step 8.8% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 57.1% | update miss 33.3% | precision_hit 83.3% | precision_any 89.4% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 83.3% | set_recall 67.9% | set_f1 74.8%
Hit rates (by modality): event 66.7% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T05:13:33.876Z |
| Finished (UTC) | 2026-03-27T05:25:55.631Z |
| Duration | 12m 21.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 4 |
| Miss | 22 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 42 |
| Check_time calls | 33 |
| Actions | 66 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 55 |
| Set FP | 11 |
| Set FN | 26 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| calendar | 1 |
| clock | 33 |
| course_portal | 1 |
| email | 2 |
| library_hold | 2 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 67.9% |
| Late rate | 4.9% |
| Miss rate | 27.2% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 33.3% |
| Precision hit | 83.3% |
| Precision any | 89.4% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 83.3% |
| Set recall | 67.9% |
| Set F1 | 74.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 57 | 66.7% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 37 | 0 | 5 | 42 | 88.1% | 88.1% |
| proactive_monitoring_required | 18 | 4 | 17 | 39 | 46.2% | 56.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 17 | 3 | 4 | 24 | 70.8% | 83.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 7.7% | 7.7% | 55.6% | 100.0% | 83.3% | 50.0% | 69.2% | 0.385 | 88.9% | 66.7% | 76.2% |
| Tuesday | 9 | 0 | 2 | 81.8% | 0.0% | 18.2% | 15.4% | 15.4% | 71.4% | 100.0% | 100.0% | 71.4% | 69.2% | 0.385 | 81.8% | 81.8% | 81.8% |
| Wednesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 10.0% | 10.0% | 44.4% | 50.0% | 66.7% | 20.0% | 50.0% | 0.000 | 71.4% | 45.5% | 55.6% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 0.0% | 9.1% | 77.8% | 66.7% | 87.5% | 50.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 20.0% | 10.0% | 70.0% | 25.0% | 87.5% | 16.7% | 60.0% | 0.200 | 80.0% | 57.1% | 66.7% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 4 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 6 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 4 |
| Wednesday | course_portal | 1 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 1 |
| Friday | clock | 6 |
| Friday | email | 1 |
| Friday | library_hold | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |

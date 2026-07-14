# PM-Bench score report

## Summary

Hit: 55 | Late: 3 | Miss: 23 | False alarms: 8 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 47 | check_time calls: 31 | Actions: 66
Exact-set: matches 52 | mismatches 28 | reward 24
Set micro: TP 55 | FP 11 | FN 26
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 67.9% | late 3.7% | miss 28.4% | false alarm/step 10.0% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 71.4% | update miss 33.3% | precision_hit 83.3% | precision_any 87.9% | exact-set match rate 65.0% | exact-set avg reward 0.300 | set_precision 83.3% | set_recall 67.9% | set_f1 74.8%
Hit rates (by modality): event 63.2% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T05:45:44.815Z |
| Finished (UTC) | 2026-03-27T05:55:41.323Z |
| Duration | 9m 56.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 3 |
| Miss | 23 |
| False alarms | 8 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 47 |
| Check_time calls | 31 |
| Actions | 66 |
| Exact-set matches | 52 |
| Exact-set mismatches | 28 |
| Exact-set reward | 24 |
| Set TP | 55 |
| Set FP | 11 |
| Set FN | 26 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 2 |
| calendar | 2 |
| clock | 31 |
| course_portal | 1 |
| email | 4 |
| library_hold | 3 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 67.9% |
| Late rate | 3.7% |
| Miss rate | 28.4% |
| False alarm/step | 10.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 33.3% |
| Precision hit | 83.3% |
| Precision any | 87.9% |
| Exact-set match rate | 65.0% |
| Exact-set avg reward | 0.300 |
| Set precision | 83.3% |
| Set recall | 67.9% |
| Set F1 | 74.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 36 | 57 | 63.2% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 36 | 0 | 6 | 42 | 85.7% | 85.7% |
| proactive_monitoring_required | 19 | 3 | 17 | 39 | 48.7% | 56.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 19 | 0 | 5 | 24 | 79.2% | 79.2% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 7.7% | 7.7% | 55.6% | 100.0% | 83.3% | 50.0% | 69.2% | 0.385 | 88.9% | 66.7% | 76.2% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 15.4% | 23.1% | 57.1% | 100.0% | 100.0% | 57.1% | 53.8% | 0.077 | 72.7% | 72.7% | 72.7% |
| Wednesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 0.0% | 10.0% | 44.4% | 100.0% | 66.7% | 40.0% | 60.0% | 0.200 | 85.7% | 54.5% | 66.7% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 9.1% | 9.1% | 77.8% | 33.3% | 87.5% | 25.0% | 72.7% | 0.455 | 88.9% | 66.7% | 76.2% |
| Friday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 8.3% | 8.3% | 62.5% | 75.0% | 83.3% | 50.0% | 58.3% | 0.167 | 80.0% | 66.7% | 72.7% |
| Saturday | 10 | 0 | 4 | 71.4% | 0.0% | 28.6% | 20.0% | 10.0% | 70.0% | 75.0% | 87.5% | 50.0% | 60.0% | 0.200 | 83.3% | 71.4% | 76.9% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | library_hold | 1 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 4 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 1 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 7 |

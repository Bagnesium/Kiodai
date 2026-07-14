# PM-Bench score report

## Summary

Hit: 55 | Late: 4 | Miss: 22 | False alarms: 6 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 42 | check_time calls: 28 | Actions: 65
Exact-set: matches 51 | mismatches 29 | reward 22
Set micro: TP 55 | FP 10 | FN 26
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 67.9% | late 4.9% | miss 27.2% | false alarm/step 7.5% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 0.0% | update miss 33.3% | precision_hit 84.6% | precision_any 90.8% | exact-set match rate 63.7% | exact-set avg reward 0.275 | set_precision 84.6% | set_recall 67.9% | set_f1 75.3%
Hit rates (by modality): event 66.7% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T02:04:22.212Z |
| Finished (UTC) | 2026-03-27T02:07:47.063Z |
| Duration | 3m 24.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 4 |
| Miss | 22 |
| False alarms | 6 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 42 |
| Check_time calls | 28 |
| Actions | 65 |
| Exact-set matches | 51 |
| Exact-set mismatches | 29 |
| Exact-set reward | 22 |
| Set TP | 55 |
| Set FP | 10 |
| Set FN | 26 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 1 |
| bank_balance | 2 |
| calendar | 2 |
| clock | 28 |
| course_portal | 2 |
| email | 3 |
| library_hold | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 67.9% |
| Late rate | 4.9% |
| Miss rate | 27.2% |
| False alarm/step | 7.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 84.6% |
| Precision any | 90.8% |
| Exact-set match rate | 63.7% |
| Exact-set avg reward | 0.275 |
| Set precision | 84.6% |
| Set recall | 67.9% |
| Set F1 | 75.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 57 | 66.7% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 1 | 3 | 42 | 90.5% | 92.9% |
| proactive_monitoring_required | 17 | 3 | 19 | 39 | 43.6% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 1 | 6 | 24 | 70.8% | 75.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 7.7% | 15.4% | 55.6% | 100.0% | 83.3% | 50.0% | 61.5% | 0.231 | 80.0% | 66.7% | 72.7% |
| Tuesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 15.4% | 15.4% | 57.1% | 75.0% | 100.0% | 42.9% | 53.8% | 0.077 | 70.0% | 63.6% | 66.7% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 10.0% | 10.0% | 55.6% | 50.0% | 83.3% | 20.0% | 60.0% | 0.200 | 85.7% | 54.5% | 66.7% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 77.8% | 33.3% | 87.5% | 25.0% | 81.8% | 0.636 | 100.0% | 66.7% | 80.0% |
| Friday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 8.3% | 8.3% | 75.0% | 100.0% | 100.0% | 66.7% | 75.0% | 0.500 | 90.9% | 83.3% | 87.0% |
| Saturday | 10 | 1 | 3 | 71.4% | 7.1% | 21.4% | 10.0% | 10.0% | 70.0% | 75.0% | 87.5% | 50.0% | 50.0% | 0.000 | 83.3% | 71.4% | 76.9% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 0.0% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 85.7% | 66.7% | 75.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 4 |
| Monday | library_hold | 3 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 4 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 2 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Friday | library_hold | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 6 |

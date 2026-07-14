# PM-Bench score report

## Summary

Hit: 55 | Late: 8 | Miss: 18 | False alarms: 11 | Commission: 0 | Wrong-content: 8 | Dependency violations: 0 | Overkill steps: 14 | state query calls: 43 | check_time calls: 24 | Actions: 74
Exact-set: matches 47 | mismatches 33 | reward 14
Set micro: TP 55 | FP 19 | FN 26
Cross-day: hit 5 | late 0 | miss 2 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 5
Rates: hit 67.9% | late 9.9% | miss 22.2% | false alarm/step 13.8% | commission 0.0% | wrong-content 9.9% | dependency/step 0.0% | overkill/step 17.5% | cross-day miss 28.6% | update miss 22.2% | precision_hit 74.3% | precision_any 85.1% | exact-set match rate 58.8% | exact-set avg reward 0.175 | set_precision 74.3% | set_recall 67.9% | set_f1 71.0%
Hit rates (by modality): event 68.4% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T05:36:12.729Z |
| Finished (UTC) | 2026-03-27T05:45:44.635Z |
| Duration | 9m 31.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 8 |
| Miss | 18 |
| False alarms | 11 |
| Commission | 0 |
| Wrong-content | 8 |
| Dependency violations | 0 |
| Overkill steps | 14 |
| State query calls | 43 |
| Check_time calls | 24 |
| Actions | 74 |
| Exact-set matches | 47 |
| Exact-set mismatches | 33 |
| Exact-set reward | 14 |
| Set TP | 55 |
| Set FP | 19 |
| Set FN | 26 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 4 |
| calendar | 2 |
| clock | 24 |
| course_portal | 1 |
| email | 5 |
| library_hold | 3 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 67.9% |
| Late rate | 9.9% |
| Miss rate | 22.2% |
| False alarm/step | 13.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 9.9% |
| Dependency/step | 0.0% |
| Overkill/step | 17.5% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 22.2% |
| Precision hit | 74.3% |
| Precision any | 85.1% |
| Exact-set match rate | 58.8% |
| Exact-set avg reward | 0.175 |
| Set precision | 74.3% |
| Set recall | 67.9% |
| Set F1 | 71.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
| proactive_monitoring_required | 17 | 8 | 14 | 39 | 43.6% | 64.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 16 | 3 | 5 | 24 | 66.7% | 79.2% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 2 | 2 | 66.7% | 16.7% | 16.7% | 30.8% | 30.8% | 66.7% | 66.7% | 83.3% | 50.0% | 53.8% | 0.077 | 57.1% | 66.7% | 61.5% |
| Tuesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 7.7% | 23.1% | 57.1% | 75.0% | 100.0% | 42.9% | 46.2% | -0.077 | 70.0% | 63.6% | 66.7% |
| Wednesday | 6 | 2 | 3 | 54.5% | 18.2% | 27.3% | 0.0% | 10.0% | 55.6% | 50.0% | 83.3% | 20.0% | 60.0% | 0.200 | 75.0% | 54.5% | 63.2% |
| Thursday | 7 | 1 | 4 | 58.3% | 8.3% | 33.3% | 18.2% | 27.3% | 66.7% | 33.3% | 75.0% | 25.0% | 54.5% | 0.091 | 70.0% | 58.3% | 63.6% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 8.3% | 8.3% | 75.0% | 75.0% | 100.0% | 50.0% | 66.7% | 0.333 | 81.8% | 75.0% | 78.3% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 20.0% | 20.0% | 80.0% | 75.0% | 100.0% | 50.0% | 50.0% | 0.000 | 84.6% | 78.6% | 81.5% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 3 |
| Monday | library_hold | 2 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 3 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 1 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 4 |
| Friday | email | 3 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 5 |

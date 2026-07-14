# PM-Bench score report

## Summary

Hit: 56 | Late: 5 | Miss: 20 | False alarms: 10 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 10 | state query calls: 51 | check_time calls: 30 | Actions: 71
Exact-set: matches 50 | mismatches 30 | reward 20
Set micro: TP 56 | FP 15 | FN 25
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 69.1% | late 6.2% | miss 24.7% | false alarm/step 12.5% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 12.5% | cross-day miss 14.3% | update miss 33.3% | precision_hit 78.9% | precision_any 85.9% | exact-set match rate 62.5% | exact-set avg reward 0.250 | set_precision 78.9% | set_recall 69.1% | set_f1 73.7%
Hit rates (by modality): event 68.4% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:13:26.533Z |
| Finished (UTC) | 2026-03-27T03:17:08.024Z |
| Duration | 3m 41.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 5 |
| Miss | 20 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 10 |
| State query calls | 51 |
| Check_time calls | 30 |
| Actions | 71 |
| Exact-set matches | 50 |
| Exact-set mismatches | 30 |
| Exact-set reward | 20 |
| Set TP | 56 |
| Set FP | 15 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 2 |
| calendar | 2 |
| clock | 30 |
| course_portal | 1 |
| email | 6 |
| library_hold | 5 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 6.2% |
| Miss rate | 24.7% |
| False alarm/step | 12.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 12.5% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 33.3% |
| Precision hit | 78.9% |
| Precision any | 85.9% |
| Exact-set match rate | 62.5% |
| Exact-set avg reward | 0.250 |
| Set precision | 78.9% |
| Set recall | 69.1% |
| Set F1 | 73.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
| proactive_monitoring_required | 18 | 5 | 16 | 39 | 46.2% | 59.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 1 | 6 | 24 | 70.8% | 75.0% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 23.1% | 23.1% | 66.7% | 100.0% | 83.3% | 66.7% | 61.5% | 0.231 | 69.2% | 75.0% | 72.0% |
| Tuesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 15.4% | 15.4% | 57.1% | 75.0% | 100.0% | 42.9% | 53.8% | 0.077 | 70.0% | 63.6% | 66.7% |
| Wednesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 10.0% | 20.0% | 55.6% | 50.0% | 83.3% | 20.0% | 50.0% | 0.000 | 75.0% | 54.5% | 63.2% |
| Thursday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 88.9% | 66.7% | 100.0% | 50.0% | 90.9% | 0.818 | 100.0% | 83.3% | 90.9% |
| Friday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 0.0% | 0.0% | 62.5% | 75.0% | 83.3% | 50.0% | 75.0% | 0.500 | 88.9% | 66.7% | 76.2% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 20.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 84.6% | 78.6% | 81.5% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 18.2% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 62.5% | 55.6% | 58.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 5 |
| Monday | library_hold | 3 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 2 |
| Wednesday | course_portal | 1 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 3 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 5 |

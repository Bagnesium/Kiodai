# PM-Bench score report

## Summary

Hit: 52 | Late: 7 | Miss: 22 | False alarms: 10 | Commission: 0 | Wrong-content: 8 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 53 | check_time calls: 29 | Actions: 69
Exact-set: matches 47 | mismatches 33 | reward 14
Set micro: TP 52 | FP 17 | FN 29
Cross-day: hit 4 | late 1 | miss 2 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 2
Rates: hit 64.2% | late 8.6% | miss 27.2% | false alarm/step 12.5% | commission 0.0% | wrong-content 9.9% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 28.6% | update miss 33.3% | precision_hit 75.4% | precision_any 85.5% | exact-set match rate 58.8% | exact-set avg reward 0.175 | set_precision 75.4% | set_recall 64.2% | set_f1 69.3%
Hit rates (by modality): event 59.6% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:21:21.555Z |
| Finished (UTC) | 2026-03-27T03:25:12.541Z |
| Duration | 3m 51.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 7 |
| Miss | 22 |
| False alarms | 10 |
| Commission | 0 |
| Wrong-content | 8 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 53 |
| Check_time calls | 29 |
| Actions | 69 |
| Exact-set matches | 47 |
| Exact-set mismatches | 33 |
| Exact-set reward | 14 |
| Set TP | 52 |
| Set FP | 17 |
| Set FN | 29 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 3 |
| bank_balance | 3 |
| calendar | 3 |
| clock | 29 |
| course_portal | 2 |
| email | 6 |
| library_hold | 5 |
| shipment_status | 2 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 64.2% |
| Late rate | 8.6% |
| Miss rate | 27.2% |
| False alarm/step | 12.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 9.9% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 33.3% |
| Precision hit | 75.4% |
| Precision any | 85.5% |
| Exact-set match rate | 58.8% |
| Exact-set avg reward | 0.175 |
| Set precision | 75.4% |
| Set recall | 64.2% |
| Set F1 | 69.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 34 | 57 | 59.6% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 34 | 2 | 6 | 42 | 81.0% | 85.7% |
| proactive_monitoring_required | 18 | 5 | 16 | 39 | 46.2% | 59.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 18 | 1 | 5 | 24 | 75.0% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 38.5% | 15.4% | 44.4% | 100.0% | 66.7% | 50.0% | 61.5% | 0.231 | 58.3% | 58.3% | 58.3% |
| Tuesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 7.7% | 23.1% | 57.1% | 75.0% | 100.0% | 42.9% | 46.2% | -0.077 | 70.0% | 63.6% | 66.7% |
| Wednesday | 4 | 2 | 5 | 36.4% | 18.2% | 45.5% | 10.0% | 30.0% | 33.3% | 50.0% | 50.0% | 20.0% | 30.0% | -0.400 | 57.1% | 36.4% | 44.4% |
| Thursday | 7 | 1 | 4 | 58.3% | 8.3% | 33.3% | 0.0% | 9.1% | 55.6% | 66.7% | 62.5% | 50.0% | 72.7% | 0.455 | 87.5% | 58.3% | 70.0% |
| Friday | 10 | 1 | 1 | 83.3% | 8.3% | 8.3% | 0.0% | 0.0% | 75.0% | 100.0% | 100.0% | 66.7% | 83.3% | 0.667 | 90.9% | 83.3% | 87.0% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 20.0% | 20.0% | 80.0% | 75.0% | 100.0% | 50.0% | 50.0% | 0.000 | 84.6% | 78.6% | 81.5% |
| Sunday | 6 | 1 | 2 | 66.7% | 11.1% | 22.2% | 9.1% | 9.1% | 80.0% | 50.0% | 100.0% | 40.0% | 63.6% | 0.273 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 4 |
| Monday | library_hold | 3 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 2 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 1 |
| Thursday | clock | 4 |
| Thursday | shipment_status | 2 |
| Friday | clock | 5 |
| Friday | email | 4 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 4 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |

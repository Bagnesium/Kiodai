# PM-Bench score report

## Summary

Hit: 56 | Late: 4 | Miss: 21 | False alarms: 9 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 10 | state query calls: 75 | check_time calls: 40 | Actions: 69
Exact-set: matches 50 | mismatches 30 | reward 20
Set micro: TP 56 | FP 13 | FN 25
Cross-day: hit 5 | late 0 | miss 2 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 3
Rates: hit 69.1% | late 4.9% | miss 25.9% | false alarm/step 11.2% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 12.5% | cross-day miss 28.6% | update miss 55.6% | precision_hit 81.2% | precision_any 87.0% | exact-set match rate 62.5% | exact-set avg reward 0.250 | set_precision 81.2% | set_recall 69.1% | set_f1 74.7%
Hit rates (by modality): event 70.2% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:17:08.219Z |
| Finished (UTC) | 2026-03-27T03:21:21.332Z |
| Duration | 4m 13.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 56 |
| Late | 4 |
| Miss | 21 |
| False alarms | 9 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 10 |
| State query calls | 75 |
| Check_time calls | 40 |
| Actions | 69 |
| Exact-set matches | 50 |
| Exact-set mismatches | 30 |
| Exact-set reward | 20 |
| Set TP | 56 |
| Set FP | 13 |
| Set FN | 25 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 5 |
| bank_balance | 4 |
| calendar | 5 |
| clock | 40 |
| course_portal | 2 |
| email | 8 |
| library_hold | 7 |
| shipment_status | 4 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 69.1% |
| Late rate | 4.9% |
| Miss rate | 25.9% |
| False alarm/step | 11.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 12.5% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 55.6% |
| Precision hit | 81.2% |
| Precision any | 87.0% |
| Exact-set match rate | 62.5% |
| Exact-set avg reward | 0.250 |
| Set precision | 81.2% |
| Set recall | 69.1% |
| Set F1 | 74.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 37 | 0 | 5 | 42 | 88.1% | 88.1% |
| proactive_monitoring_required | 19 | 4 | 16 | 39 | 48.7% | 59.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 1 | 1 | 3 | 33.3% | 66.7% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 16 | 0 | 8 | 24 | 66.7% | 66.7% |
| course_portal | 0 | 1 | 0 | 1 | 0.0% | 100.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 23.1% | 30.8% | 66.7% | 66.7% | 66.7% | 66.7% | 46.2% | -0.077 | 66.7% | 66.7% | 66.7% |
| Tuesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 7.7% | 15.4% | 71.4% | 75.0% | 100.0% | 57.1% | 61.5% | 0.231 | 80.0% | 72.7% | 76.2% |
| Wednesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 10.0% | 10.0% | 44.4% | 50.0% | 66.7% | 20.0% | 50.0% | 0.000 | 71.4% | 45.5% | 55.6% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 18.2% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 81.8% | 75.0% | 78.3% |
| Friday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 0.0% | 0.0% | 62.5% | 75.0% | 83.3% | 50.0% | 75.0% | 0.500 | 88.9% | 66.7% | 76.2% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 9.1% | 80.0% | 75.0% | 100.0% | 60.0% | 72.7% | 0.455 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 4 |
| Monday | clock | 7 |
| Monday | library_hold | 4 |
| Tuesday | calendar | 3 |
| Tuesday | clock | 6 |
| Tuesday | email | 4 |
| Wednesday | bank_balance | 2 |
| Wednesday | clock | 4 |
| Wednesday | course_portal | 2 |
| Wednesday | library_hold | 2 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 4 |
| Friday | clock | 6 |
| Friday | email | 4 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 2 |
| Saturday | clock | 5 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 7 |

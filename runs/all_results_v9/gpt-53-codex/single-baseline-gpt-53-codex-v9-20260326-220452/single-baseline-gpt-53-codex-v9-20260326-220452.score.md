# PM-Bench score report

## Summary

Hit: 60 | Late: 3 | Miss: 18 | False alarms: 8 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 7 | state query calls: 55 | check_time calls: 34 | Actions: 71
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 60 | FP 11 | FN 21
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 0
Rates: hit 74.1% | late 3.7% | miss 22.2% | false alarm/step 10.0% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 8.8% | cross-day miss 14.3% | update miss 22.2% | precision_hit 84.5% | precision_any 88.7% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 84.5% | set_recall 74.1% | set_f1 78.9%
Hit rates (by modality): event 70.2% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T05:04:52.101Z |
| Finished (UTC) | 2026-03-27T05:13:33.643Z |
| Duration | 8m 41.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 60 |
| Late | 3 |
| Miss | 18 |
| False alarms | 8 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 7 |
| State query calls | 55 |
| Check_time calls | 34 |
| Actions | 71 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 60 |
| Set FP | 11 |
| Set FN | 21 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 3 |
| calendar | 2 |
| clock | 34 |
| course_portal | 2 |
| email | 7 |
| laundry_status | 1 |
| library_hold | 1 |
| shipment_status | 3 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 74.1% |
| Late rate | 3.7% |
| Miss rate | 22.2% |
| False alarm/step | 10.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 8.8% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 22.2% |
| Precision hit | 84.5% |
| Precision any | 88.7% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 84.5% |
| Set recall | 74.1% |
| Set F1 | 78.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 39 | 0 | 3 | 42 | 92.9% | 92.9% |
| proactive_monitoring_required | 21 | 3 | 15 | 39 | 53.8% | 61.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 20 | 0 | 4 | 24 | 83.3% | 83.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 15.4% | 7.7% | 55.6% | 100.0% | 83.3% | 50.0% | 61.5% | 0.231 | 72.7% | 66.7% | 69.6% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 7.7% | 15.4% | 71.4% | 100.0% | 100.0% | 71.4% | 69.2% | 0.385 | 81.8% | 81.8% | 81.8% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 20.0% | 20.0% | 55.6% | 50.0% | 83.3% | 20.0% | 50.0% | 0.000 | 75.0% | 54.5% | 63.2% |
| Thursday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 0.0% | 0.0% | 88.9% | 66.7% | 100.0% | 50.0% | 81.8% | 0.636 | 100.0% | 83.3% | 90.9% |
| Friday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 8.3% | 8.3% | 62.5% | 100.0% | 83.3% | 66.7% | 66.7% | 0.333 | 81.8% | 75.0% | 78.3% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 10.0% | 10.0% | 80.0% | 75.0% | 100.0% | 50.0% | 60.0% | 0.200 | 91.7% | 78.6% | 84.6% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 9.1% | 0.0% | 80.0% | 75.0% | 100.0% | 60.0% | 81.8% | 0.636 | 87.5% | 77.8% | 82.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 1 |
| Monday | clock | 6 |
| Monday | email | 2 |
| Tuesday | calendar | 1 |
| Tuesday | clock | 5 |
| Tuesday | email | 3 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 3 |
| Wednesday | course_portal | 2 |
| Thursday | clock | 5 |
| Thursday | shipment_status | 3 |
| Friday | clock | 5 |
| Friday | email | 2 |
| Friday | laundry_status | 1 |
| Friday | library_hold | 1 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 1 |
| Saturday | clock | 3 |
| Sunday | bank_balance | 2 |
| Sunday | clock | 7 |

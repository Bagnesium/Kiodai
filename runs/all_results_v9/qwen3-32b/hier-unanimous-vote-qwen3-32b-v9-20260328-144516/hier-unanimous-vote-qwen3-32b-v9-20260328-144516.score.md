# PM-Bench score report

## Summary

Hit: 8 | Late: 0 | Miss: 73 | False alarms: 8 | Commission: 1 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 169 | check_time calls: 80 | Actions: 17
Exact-set: matches 26 | mismatches 54 | reward -28
Set micro: TP 8 | FP 9 | FN 73
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 5
Rates: hit 9.9% | late 0.0% | miss 90.1% | false alarm/step 10.0% | commission 1.2% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 100.0% | update miss 66.7% | precision_hit 47.1% | precision_any 47.1% | exact-set match rate 32.5% | exact-set avg reward -0.350 | set_precision 47.1% | set_recall 9.9% | set_f1 16.3%
Hit rates (by modality): event 1.8% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:06:37.755Z |
| Finished (UTC) | 2026-03-28T22:06:37.755Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 8 |
| Late | 0 |
| Miss | 73 |
| False alarms | 8 |
| Commission | 1 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 169 |
| Check_time calls | 80 |
| Actions | 17 |
| Exact-set matches | 26 |
| Exact-set mismatches | 54 |
| Exact-set reward | -28 |
| Set TP | 8 |
| Set FP | 9 |
| Set FN | 73 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 47 |
| calendar | 18 |
| clock | 80 |
| email | 1 |
| laundry_status | 9 |
| library_hold | 14 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 9.9% |
| Late rate | 0.0% |
| Miss rate | 90.1% |
| False alarm/step | 10.0% |
| Commission rate | 1.2% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 66.7% |
| Precision hit | 47.1% |
| Precision any | 47.1% |
| Exact-set match rate | 32.5% |
| Exact-set avg reward | -0.350 |
| Set precision | 47.1% |
| Set recall | 9.9% |
| Set F1 | 16.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 1 | 57 | 1.8% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 1 | 0 | 41 | 42 | 2.4% | 2.4% |
| proactive_monitoring_required | 7 | 0 | 32 | 39 | 17.9% | 17.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 7 | 0 | 17 | 24 | 29.2% | 29.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 23.1% | 15.4% | 11.1% | 33.3% | 16.7% | 16.7% | 23.1% | -0.538 | 40.0% | 16.7% | 23.5% |
| Tuesday | 1 | 0 | 10 | 9.1% | 0.0% | 90.9% | 7.7% | 7.7% | 0.0% | 25.0% | 0.0% | 14.3% | 38.5% | -0.231 | 50.0% | 9.1% | 15.4% |
| Wednesday | 1 | 0 | 10 | 9.1% | 0.0% | 90.9% | 0.0% | 0.0% | 0.0% | 50.0% | 0.0% | 20.0% | 50.0% | 0.000 | 100.0% | 9.1% | 16.7% |
| Thursday | 0 | 0 | 12 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 36.4% | -0.273 | n/a | 0.0% | 0.0% |
| Friday | 0 | 0 | 12 | 0.0% | 0.0% | 100.0% | 8.3% | 8.3% | 0.0% | 0.0% | 0.0% | 0.0% | 33.3% | -0.333 | 0.0% | 0.0% | 0.0% |
| Saturday | 3 | 0 | 11 | 21.4% | 0.0% | 78.6% | 20.0% | 10.0% | 0.0% | 75.0% | 0.0% | 50.0% | 20.0% | -0.600 | 50.0% | 21.4% | 30.0% |
| Sunday | 1 | 0 | 8 | 11.1% | 0.0% | 88.9% | 9.1% | 9.1% | 0.0% | 25.0% | 0.0% | 20.0% | 27.3% | -0.455 | 50.0% | 11.1% | 18.2% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 12 |
| Monday | clock | 13 |
| Monday | library_hold | 6 |
| Tuesday | appointment_portal | 13 |
| Tuesday | clock | 13 |
| Wednesday | appointment_portal | 10 |
| Wednesday | clock | 10 |
| Thursday | appointment_portal | 11 |
| Thursday | clock | 11 |
| Friday | appointment_portal | 1 |
| Friday | clock | 12 |
| Friday | email | 1 |
| Friday | laundry_status | 8 |
| Friday | library_hold | 7 |
| Saturday | calendar | 7 |
| Saturday | clock | 10 |
| Saturday | laundry_status | 1 |
| Saturday | library_hold | 1 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |

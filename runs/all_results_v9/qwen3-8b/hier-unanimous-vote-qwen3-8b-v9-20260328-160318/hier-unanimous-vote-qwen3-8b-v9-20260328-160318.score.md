# PM-Bench score report

## Summary

Hit: 8 | Late: 0 | Miss: 73 | False alarms: 14 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 135 | check_time calls: 69 | Actions: 22
Exact-set: matches 24 | mismatches 56 | reward -32
Set micro: TP 8 | FP 14 | FN 73
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 7
Rates: hit 9.9% | late 0.0% | miss 90.1% | false alarm/step 17.5% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 100.0% | update miss 88.9% | precision_hit 36.4% | precision_any 36.4% | exact-set match rate 30.0% | exact-set avg reward -0.400 | set_precision 36.4% | set_recall 9.9% | set_f1 15.5%
Hit rates (by modality): event 5.3% | time 20.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T23:07:25.104Z |
| Finished (UTC) | 2026-03-28T23:07:25.104Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 8 |
| Late | 0 |
| Miss | 73 |
| False alarms | 14 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 135 |
| Check_time calls | 69 |
| Actions | 22 |
| Exact-set matches | 24 |
| Exact-set mismatches | 56 |
| Exact-set reward | -32 |
| Set TP | 8 |
| Set FP | 14 |
| Set FN | 73 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 8 |
| calendar | 22 |
| clock | 69 |
| course_portal | 1 |
| email | 8 |
| laundry_status | 4 |
| library_hold | 7 |
| reservation_waitlist | 4 |
| shipment_status | 12 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 9.9% |
| Late rate | 0.0% |
| Miss rate | 90.1% |
| False alarm/step | 17.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 88.9% |
| Precision hit | 36.4% |
| Precision any | 36.4% |
| Exact-set match rate | 30.0% |
| Exact-set avg reward | -0.400 |
| Set precision | 36.4% |
| Set recall | 9.9% |
| Set F1 | 15.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 3 | 57 | 5.3% |
| Time (time + time_check) | 5 | 24 | 20.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 3 | 0 | 39 | 42 | 7.1% | 7.1% |
| proactive_monitoring_required | 5 | 0 | 34 | 39 | 12.8% | 12.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 5 | 0 | 19 | 24 | 20.8% | 20.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 30.8% | 7.7% | 0.0% | 66.7% | 0.0% | 33.3% | 30.8% | -0.385 | 33.3% | 16.7% | 22.2% |
| Tuesday | 2 | 0 | 9 | 18.2% | 0.0% | 81.8% | 7.7% | 7.7% | 14.3% | 25.0% | 25.0% | 14.3% | 38.5% | -0.231 | 66.7% | 18.2% | 28.6% |
| Wednesday | 0 | 0 | 11 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 40.0% | -0.200 | n/a | 0.0% | 0.0% |
| Thursday | 0 | 0 | 12 | 0.0% | 0.0% | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 36.4% | -0.273 | n/a | 0.0% | 0.0% |
| Friday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 33.3% | 16.7% | 0.0% | 25.0% | 0.0% | 16.7% | 25.0% | -0.500 | 20.0% | 8.3% | 11.8% |
| Saturday | 1 | 0 | 13 | 7.1% | 0.0% | 92.9% | 20.0% | 10.0% | 10.0% | 0.0% | 12.5% | 0.0% | 10.0% | -0.800 | 33.3% | 7.1% | 11.8% |
| Sunday | 2 | 0 | 7 | 22.2% | 0.0% | 77.8% | 27.3% | 27.3% | 20.0% | 25.0% | 25.0% | 20.0% | 27.3% | -0.455 | 40.0% | 22.2% | 28.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 6 |
| Monday | calendar | 4 |
| Monday | clock | 8 |
| Monday | library_hold | 4 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 10 |
| Tuesday | email | 2 |
| Tuesday | reservation_waitlist | 1 |
| Wednesday | calendar | 3 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 1 |
| Wednesday | email | 2 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 11 |
| Friday | clock | 9 |
| Friday | email | 3 |
| Friday | laundry_status | 4 |
| Friday | library_hold | 3 |
| Friday | shipment_status | 5 |
| Saturday | calendar | 1 |
| Saturday | clock | 10 |
| Saturday | email | 1 |
| Saturday | shipment_status | 7 |
| Sunday | calendar | 1 |
| Sunday | clock | 11 |
| Sunday | reservation_waitlist | 3 |

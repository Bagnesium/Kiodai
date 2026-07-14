# PM-Bench score report

## Summary

Hit: 19 | Late: 1 | Miss: 61 | False alarms: 43 | Commission: 6 | Wrong-content: 25 | Dependency violations: 0 | Overkill steps: 24 | state query calls: 135 | check_time calls: 69 | Actions: 69
Exact-set: matches 13 | mismatches 67 | reward -54
Set micro: TP 19 | FP 50 | FN 62
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 2 | late 1 | miss 6 | canceled 2 | total 11 | violations 14
Rates: hit 23.5% | late 1.2% | miss 75.3% | false alarm/step 53.8% | commission 7.4% | wrong-content 30.9% | dependency/step 0.0% | overkill/step 30.0% | cross-day miss 100.0% | update miss 66.7% | precision_hit 27.5% | precision_any 29.0% | exact-set match rate 16.2% | exact-set avg reward -0.675 | set_precision 27.5% | set_recall 23.5% | set_f1 25.3%
Hit rates (by modality): event 14.0% | time 45.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T23:07:25.103Z |
| Finished (UTC) | 2026-03-28T23:07:25.103Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 19 |
| Late | 1 |
| Miss | 61 |
| False alarms | 43 |
| Commission | 6 |
| Wrong-content | 25 |
| Dependency violations | 0 |
| Overkill steps | 24 |
| State query calls | 135 |
| Check_time calls | 69 |
| Actions | 69 |
| Exact-set matches | 13 |
| Exact-set mismatches | 67 |
| Exact-set reward | -54 |
| Set TP | 19 |
| Set FP | 50 |
| Set FN | 62 |

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
| Hit rate | 23.5% |
| Late rate | 1.2% |
| Miss rate | 75.3% |
| False alarm/step | 53.8% |
| Commission rate | 7.4% |
| Wrong-content rate | 30.9% |
| Dependency/step | 0.0% |
| Overkill/step | 30.0% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 66.7% |
| Precision hit | 27.5% |
| Precision any | 29.0% |
| Exact-set match rate | 16.2% |
| Exact-set avg reward | -0.675 |
| Set precision | 27.5% |
| Set recall | 23.5% |
| Set F1 | 25.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 8 | 57 | 14.0% |
| Time (time + time_check) | 11 | 24 | 45.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 8 | 0 | 34 | 42 | 19.0% | 19.0% |
| proactive_monitoring_required | 11 | 1 | 27 | 39 | 28.2% | 30.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 11 | 1 | 12 | 24 | 45.8% | 50.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 3 | 0 | 9 | 25.0% | 0.0% | 75.0% | 69.2% | 30.8% | 11.1% | 66.7% | 16.7% | 33.3% | 15.4% | -0.692 | 25.0% | 25.0% | 25.0% |
| Tuesday | 3 | 1 | 7 | 27.3% | 9.1% | 63.6% | 23.1% | 30.8% | 28.6% | 25.0% | 50.0% | 14.3% | 23.1% | -0.538 | 27.3% | 27.3% | 27.3% |
| Wednesday | 3 | 0 | 8 | 27.3% | 0.0% | 72.7% | 50.0% | 20.0% | 22.2% | 50.0% | 33.3% | 20.0% | 30.0% | -0.400 | 33.3% | 27.3% | 30.0% |
| Thursday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 63.6% | 36.4% | 0.0% | 66.7% | 0.0% | 50.0% | 9.1% | -0.818 | 22.2% | 16.7% | 19.0% |
| Friday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 58.3% | 33.3% | 0.0% | 50.0% | 0.0% | 33.3% | 16.7% | -0.667 | 22.2% | 16.7% | 19.0% |
| Saturday | 2 | 0 | 12 | 14.3% | 0.0% | 85.7% | 70.0% | 20.0% | 10.0% | 25.0% | 12.5% | 16.7% | 0.0% | -1.000 | 22.2% | 14.3% | 17.4% |
| Sunday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 45.5% | 36.4% | 40.0% | 50.0% | 50.0% | 40.0% | 18.2% | -0.636 | 40.0% | 44.4% | 42.1% |

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

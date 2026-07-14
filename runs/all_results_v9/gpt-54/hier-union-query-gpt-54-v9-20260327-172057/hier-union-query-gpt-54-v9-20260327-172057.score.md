# PM-Bench score report

## Summary

Hit: 39 | Late: 2 | Miss: 40 | False alarms: 16 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 15 | state query calls: 300 | check_time calls: 79 | Actions: 57
Exact-set: matches 37 | mismatches 43 | reward -6
Set micro: TP 39 | FP 18 | FN 42
Cross-day: hit 0 | late 1 | miss 6 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 3
Rates: hit 48.1% | late 2.5% | miss 49.4% | false alarm/step 20.0% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 18.8% | cross-day miss 85.7% | update miss 88.9% | precision_hit 68.4% | precision_any 71.9% | exact-set match rate 46.2% | exact-set avg reward -0.075 | set_precision 68.4% | set_recall 48.1% | set_f1 56.5%
Hit rates (by modality): event 42.1% | time 62.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T00:20:57.547Z |
| Finished (UTC) | 2026-03-28T00:42:31.194Z |
| Duration | 21m 33.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 39 |
| Late | 2 |
| Miss | 40 |
| False alarms | 16 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 15 |
| State query calls | 300 |
| Check_time calls | 79 |
| Actions | 57 |
| Exact-set matches | 37 |
| Exact-set mismatches | 43 |
| Exact-set reward | -6 |
| Set TP | 39 |
| Set FP | 18 |
| Set FN | 42 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 41 |
| bank_balance | 21 |
| calendar | 39 |
| clock | 79 |
| course_portal | 11 |
| email | 45 |
| laundry_status | 8 |
| library_hold | 35 |
| reservation_waitlist | 1 |
| shipment_status | 20 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 48.1% |
| Late rate | 2.5% |
| Miss rate | 49.4% |
| False alarm/step | 20.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 18.8% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 88.9% |
| Precision hit | 68.4% |
| Precision any | 71.9% |
| Exact-set match rate | 46.2% |
| Exact-set avg reward | -0.075 |
| Set precision | 68.4% |
| Set recall | 48.1% |
| Set F1 | 56.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 24 | 57 | 42.1% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 22 | 1 | 19 | 42 | 52.4% | 54.8% |
| proactive_monitoring_required | 17 | 1 | 21 | 39 | 43.6% | 46.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 15 | 1 | 8 | 24 | 62.5% | 66.7% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 1 | 4 | 58.3% | 8.3% | 33.3% | 15.4% | 15.4% | 55.6% | 66.7% | 66.7% | 50.0% | 53.8% | 0.077 | 70.0% | 58.3% | 63.6% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 7.7% | 7.7% | 42.9% | 75.0% | 75.0% | 42.9% | 61.5% | 0.231 | 85.7% | 54.5% | 66.7% |
| Wednesday | 7 | 1 | 3 | 63.6% | 9.1% | 27.3% | 20.0% | 30.0% | 55.6% | 100.0% | 66.7% | 60.0% | 40.0% | -0.200 | 70.0% | 63.6% | 66.7% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 18.2% | 18.2% | 44.4% | 66.7% | 50.0% | 50.0% | 54.5% | 0.091 | 75.0% | 50.0% | 60.0% |
| Friday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 41.7% | 33.3% | 25.0% | 50.0% | 33.3% | 33.3% | 25.0% | -0.500 | 44.4% | 33.3% | 38.1% |
| Saturday | 4 | 0 | 10 | 28.6% | 0.0% | 71.4% | 30.0% | 20.0% | 20.0% | 50.0% | 25.0% | 33.3% | 30.0% | -0.400 | 57.1% | 28.6% | 38.1% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 9.1% | 9.1% | 60.0% | 50.0% | 75.0% | 40.0% | 54.5% | 0.091 | 83.3% | 55.6% | 66.7% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 13 |
| Monday | calendar | 1 |
| Monday | clock | 12 |
| Monday | email | 4 |
| Monday | library_hold | 13 |
| Monday | reservation_waitlist | 1 |
| Monday | shipment_status | 2 |
| Tuesday | appointment_portal | 5 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 13 |
| Tuesday | email | 13 |
| Tuesday | laundry_status | 1 |
| Wednesday | appointment_portal | 3 |
| Wednesday | bank_balance | 9 |
| Wednesday | calendar | 2 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 9 |
| Wednesday | email | 6 |
| Wednesday | laundry_status | 1 |
| Wednesday | library_hold | 10 |
| Thursday | appointment_portal | 9 |
| Thursday | calendar | 11 |
| Thursday | clock | 11 |
| Thursday | shipment_status | 8 |
| Friday | bank_balance | 1 |
| Friday | calendar | 4 |
| Friday | clock | 12 |
| Friday | email | 11 |
| Friday | laundry_status | 3 |
| Friday | library_hold | 12 |
| Saturday | appointment_portal | 6 |
| Saturday | calendar | 4 |
| Saturday | clock | 10 |
| Saturday | email | 10 |
| Saturday | shipment_status | 10 |
| Sunday | appointment_portal | 5 |
| Sunday | bank_balance | 11 |
| Sunday | calendar | 4 |
| Sunday | clock | 11 |
| Sunday | course_portal | 2 |
| Sunday | email | 1 |
| Sunday | laundry_status | 3 |

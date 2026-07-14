# PM-Bench score report

## Summary

Hit: 47 | Late: 3 | Miss: 31 | False alarms: 49 | Commission: 11 | Wrong-content: 29 | Dependency violations: 0 | Overkill steps: 36 | state query calls: 300 | check_time calls: 79 | Actions: 110
Exact-set: matches 23 | mismatches 57 | reward -34
Set micro: TP 47 | FP 63 | FN 34
Cross-day: hit 3 | late 0 | miss 4 | total 7
Updates: hit 3 | late 1 | miss 5 | canceled 2 | total 11 | violations 10
Rates: hit 58.0% | late 3.7% | miss 38.3% | false alarm/step 61.3% | commission 13.6% | wrong-content 35.8% | dependency/step 0.0% | overkill/step 45.0% | cross-day miss 57.1% | update miss 55.6% | precision_hit 42.7% | precision_any 45.5% | exact-set match rate 28.7% | exact-set avg reward -0.425 | set_precision 42.7% | set_recall 58.0% | set_f1 49.2%
Hit rates (by modality): event 50.9% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T05:03:17.801Z |
| Finished (UTC) | 2026-03-28T05:03:17.801Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 47 |
| Late | 3 |
| Miss | 31 |
| False alarms | 49 |
| Commission | 11 |
| Wrong-content | 29 |
| Dependency violations | 0 |
| Overkill steps | 36 |
| State query calls | 300 |
| Check_time calls | 79 |
| Actions | 110 |
| Exact-set matches | 23 |
| Exact-set mismatches | 57 |
| Exact-set reward | -34 |
| Set TP | 47 |
| Set FP | 63 |
| Set FN | 34 |

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
| Hit rate | 58.0% |
| Late rate | 3.7% |
| Miss rate | 38.3% |
| False alarm/step | 61.3% |
| Commission rate | 13.6% |
| Wrong-content rate | 35.8% |
| Dependency/step | 0.0% |
| Overkill/step | 45.0% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 55.6% |
| Precision hit | 42.7% |
| Precision any | 45.5% |
| Exact-set match rate | 28.7% |
| Exact-set avg reward | -0.425 |
| Set precision | 42.7% |
| Set recall | 58.0% |
| Set F1 | 49.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 29 | 57 | 50.9% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 29 | 0 | 13 | 42 | 69.0% | 69.0% |
| proactive_monitoring_required | 18 | 3 | 18 | 39 | 46.2% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 18 | 1 | 5 | 24 | 75.0% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 46.2% | 30.8% | 44.4% | 66.7% | 66.7% | 33.3% | 46.2% | -0.077 | 50.0% | 50.0% | 50.0% |
| Tuesday | 6 | 3 | 2 | 54.5% | 27.3% | 18.2% | 38.5% | 53.8% | 42.9% | 75.0% | 75.0% | 42.9% | 15.4% | -0.692 | 27.3% | 54.5% | 36.4% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 80.0% | 50.0% | 44.4% | 100.0% | 66.7% | 40.0% | 20.0% | -0.600 | 42.9% | 54.5% | 48.0% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 54.5% | 54.5% | 66.7% | 100.0% | 75.0% | 75.0% | 27.3% | -0.455 | 50.0% | 75.0% | 60.0% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 91.7% | 50.0% | 25.0% | 75.0% | 33.3% | 50.0% | 16.7% | -0.667 | 31.2% | 41.7% | 35.7% |
| Saturday | 10 | 0 | 4 | 71.4% | 0.0% | 28.6% | 110.0% | 60.0% | 70.0% | 75.0% | 87.5% | 50.0% | 30.0% | -0.400 | 47.6% | 71.4% | 57.1% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 18.2% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 71.4% | 55.6% | 62.5% |

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

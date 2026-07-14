# PM-Bench score report

## Summary

Hit: 52 | Late: 6 | Miss: 23 | False alarms: 50 | Commission: 6 | Wrong-content: 29 | Dependency violations: 0 | Overkill steps: 40 | state query calls: 312 | check_time calls: 80 | Actions: 114
Exact-set: matches 23 | mismatches 57 | reward -34
Set micro: TP 52 | FP 62 | FN 29
Cross-day: hit 2 | late 3 | miss 2 | total 7
Updates: hit 4 | late 1 | miss 4 | canceled 2 | total 11 | violations 8
Rates: hit 64.2% | late 7.4% | miss 28.4% | false alarm/step 62.5% | commission 7.4% | wrong-content 35.8% | dependency/step 0.0% | overkill/step 50.0% | cross-day miss 28.6% | update miss 44.4% | precision_hit 45.6% | precision_any 50.9% | exact-set match rate 28.7% | exact-set avg reward -0.425 | set_precision 45.6% | set_recall 64.2% | set_f1 53.3%
Hit rates (by modality): event 57.9% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T05:03:17.801Z |
| Finished (UTC) | 2026-03-28T05:03:17.801Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 6 |
| Miss | 23 |
| False alarms | 50 |
| Commission | 6 |
| Wrong-content | 29 |
| Dependency violations | 0 |
| Overkill steps | 40 |
| State query calls | 312 |
| Check_time calls | 80 |
| Actions | 114 |
| Exact-set matches | 23 |
| Exact-set mismatches | 57 |
| Exact-set reward | -34 |
| Set TP | 52 |
| Set FP | 62 |
| Set FN | 29 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 30 |
| bank_balance | 8 |
| calendar | 74 |
| clock | 80 |
| course_portal | 13 |
| email | 41 |
| laundry_status | 22 |
| library_hold | 25 |
| reservation_waitlist | 1 |
| shipment_status | 18 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 64.2% |
| Late rate | 7.4% |
| Miss rate | 28.4% |
| False alarm/step | 62.5% |
| Commission rate | 7.4% |
| Wrong-content rate | 35.8% |
| Dependency/step | 0.0% |
| Overkill/step | 50.0% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 44.4% |
| Precision hit | 45.6% |
| Precision any | 50.9% |
| Exact-set match rate | 28.7% |
| Exact-set avg reward | -0.425 |
| Set precision | 45.6% |
| Set recall | 64.2% |
| Set F1 | 53.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 33 | 57 | 57.9% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 3 | 8 | 42 | 73.8% | 81.0% |
| proactive_monitoring_required | 21 | 3 | 15 | 39 | 53.8% | 61.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 19 | 1 | 4 | 24 | 79.2% | 83.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 38.5% | 23.1% | 44.4% | 100.0% | 66.7% | 50.0% | 46.2% | -0.077 | 58.3% | 58.3% | 58.3% |
| Tuesday | 8 | 2 | 1 | 72.7% | 18.2% | 9.1% | 100.0% | 76.9% | 71.4% | 75.0% | 100.0% | 57.1% | 7.7% | -0.846 | 33.3% | 72.7% | 45.7% |
| Wednesday | 6 | 2 | 3 | 54.5% | 18.2% | 27.3% | 30.0% | 40.0% | 55.6% | 50.0% | 66.7% | 40.0% | 20.0% | -0.600 | 54.5% | 54.5% | 54.5% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 63.6% | 45.5% | 66.7% | 66.7% | 75.0% | 50.0% | 36.4% | -0.273 | 53.3% | 66.7% | 59.3% |
| Friday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 66.7% | 50.0% | 25.0% | 75.0% | 33.3% | 50.0% | 16.7% | -0.667 | 35.7% | 41.7% | 38.5% |
| Saturday | 11 | 1 | 2 | 78.6% | 7.1% | 14.3% | 80.0% | 50.0% | 70.0% | 100.0% | 87.5% | 66.7% | 50.0% | 0.000 | 52.4% | 78.6% | 62.9% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 54.5% | 63.6% | 80.0% | 75.0% | 100.0% | 60.0% | 27.3% | -0.455 | 41.2% | 77.8% | 53.8% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 7 |
| Monday | calendar | 11 |
| Monday | clock | 13 |
| Monday | email | 5 |
| Monday | laundry_status | 5 |
| Monday | library_hold | 7 |
| Monday | shipment_status | 3 |
| Tuesday | appointment_portal | 2 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 13 |
| Tuesday | email | 13 |
| Tuesday | laundry_status | 2 |
| Wednesday | appointment_portal | 3 |
| Wednesday | bank_balance | 5 |
| Wednesday | calendar | 10 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 8 |
| Wednesday | email | 7 |
| Wednesday | laundry_status | 1 |
| Wednesday | library_hold | 6 |
| Thursday | appointment_portal | 7 |
| Thursday | calendar | 11 |
| Thursday | clock | 11 |
| Thursday | laundry_status | 1 |
| Thursday | shipment_status | 8 |
| Friday | bank_balance | 2 |
| Friday | calendar | 11 |
| Friday | clock | 12 |
| Friday | email | 4 |
| Friday | laundry_status | 11 |
| Friday | library_hold | 9 |
| Friday | reservation_waitlist | 1 |
| Friday | shipment_status | 2 |
| Saturday | appointment_portal | 1 |
| Saturday | calendar | 8 |
| Saturday | clock | 10 |
| Saturday | email | 7 |
| Saturday | library_hold | 3 |
| Saturday | shipment_status | 5 |
| Sunday | appointment_portal | 10 |
| Sunday | bank_balance | 1 |
| Sunday | calendar | 10 |
| Sunday | clock | 11 |
| Sunday | course_portal | 5 |
| Sunday | email | 5 |
| Sunday | laundry_status | 2 |

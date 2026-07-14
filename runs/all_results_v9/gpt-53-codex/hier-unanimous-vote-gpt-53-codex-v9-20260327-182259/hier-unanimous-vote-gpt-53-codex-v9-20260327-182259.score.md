# PM-Bench score report

## Summary

Hit: 47 | Late: 3 | Miss: 31 | False alarms: 60 | Commission: 8 | Wrong-content: 32 | Dependency violations: 0 | Overkill steps: 36 | state query calls: 281 | check_time calls: 72 | Actions: 118
Exact-set: matches 24 | mismatches 56 | reward -32
Set micro: TP 47 | FP 71 | FN 34
Cross-day: hit 3 | late 0 | miss 4 | total 7
Updates: hit 1 | late 1 | miss 7 | canceled 2 | total 11 | violations 12
Rates: hit 58.0% | late 3.7% | miss 38.3% | false alarm/step 75.0% | commission 9.9% | wrong-content 39.5% | dependency/step 0.0% | overkill/step 45.0% | cross-day miss 57.1% | update miss 77.8% | precision_hit 39.8% | precision_any 42.4% | exact-set match rate 30.0% | exact-set avg reward -0.400 | set_precision 39.8% | set_recall 58.0% | set_f1 47.2%
Hit rates (by modality): event 56.1% | time 62.5%

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
| False alarms | 60 |
| Commission | 8 |
| Wrong-content | 32 |
| Dependency violations | 0 |
| Overkill steps | 36 |
| State query calls | 281 |
| Check_time calls | 72 |
| Actions | 118 |
| Exact-set matches | 24 |
| Exact-set mismatches | 56 |
| Exact-set reward | -32 |
| Set TP | 47 |
| Set FP | 71 |
| Set FN | 34 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 21 |
| bank_balance | 10 |
| calendar | 63 |
| clock | 72 |
| course_portal | 7 |
| email | 60 |
| laundry_status | 5 |
| library_hold | 20 |
| reservation_waitlist | 2 |
| shipment_status | 21 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 58.0% |
| Late rate | 3.7% |
| Miss rate | 38.3% |
| False alarm/step | 75.0% |
| Commission rate | 9.9% |
| Wrong-content rate | 39.5% |
| Dependency/step | 0.0% |
| Overkill/step | 45.0% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 77.8% |
| Precision hit | 39.8% |
| Precision any | 42.4% |
| Exact-set match rate | 30.0% |
| Exact-set avg reward | -0.400 |
| Set precision | 39.8% |
| Set recall | 58.0% |
| Set F1 | 47.2% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 32 | 57 | 56.1% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 30 | 0 | 12 | 42 | 71.4% | 71.4% |
| proactive_monitoring_required | 17 | 3 | 19 | 39 | 43.6% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 2 | 1 | 3 | 0.0% | 66.7% |
| clock | 15 | 1 | 8 | 24 | 62.5% | 66.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 69.2% | 46.2% | 66.7% | 66.7% | 66.7% | 66.7% | 30.8% | -0.385 | 47.1% | 66.7% | 55.2% |
| Tuesday | 6 | 3 | 2 | 54.5% | 27.3% | 18.2% | 53.8% | 53.8% | 42.9% | 75.0% | 75.0% | 42.9% | 30.8% | -0.385 | 33.3% | 54.5% | 41.4% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 50.0% | 30.0% | 44.4% | 100.0% | 66.7% | 40.0% | 40.0% | -0.200 | 54.5% | 54.5% | 54.5% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 90.9% | 54.5% | 77.8% | 66.7% | 87.5% | 50.0% | 36.4% | -0.273 | 37.5% | 75.0% | 50.0% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 108.3% | 41.7% | 37.5% | 50.0% | 50.0% | 33.3% | 16.7% | -0.667 | 27.8% | 41.7% | 33.3% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 90.0% | 30.0% | 60.0% | 50.0% | 75.0% | 33.3% | 40.0% | -0.200 | 47.1% | 57.1% | 51.6% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 63.6% | 54.5% | 60.0% | 50.0% | 75.0% | 40.0% | 18.2% | -0.636 | 38.5% | 55.6% | 45.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 10 |
| Monday | calendar | 8 |
| Monday | clock | 10 |
| Monday | email | 6 |
| Monday | library_hold | 6 |
| Monday | shipment_status | 5 |
| Tuesday | appointment_portal | 2 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 13 |
| Tuesday | email | 12 |
| Wednesday | bank_balance | 6 |
| Wednesday | calendar | 9 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 3 |
| Wednesday | email | 9 |
| Wednesday | library_hold | 5 |
| Thursday | appointment_portal | 4 |
| Thursday | calendar | 8 |
| Thursday | clock | 10 |
| Thursday | email | 10 |
| Thursday | shipment_status | 8 |
| Friday | bank_balance | 1 |
| Friday | calendar | 9 |
| Friday | clock | 9 |
| Friday | email | 6 |
| Friday | laundry_status | 2 |
| Friday | library_hold | 9 |
| Friday | reservation_waitlist | 2 |
| Friday | shipment_status | 2 |
| Saturday | appointment_portal | 3 |
| Saturday | calendar | 7 |
| Saturday | clock | 9 |
| Saturday | email | 9 |
| Saturday | shipment_status | 6 |
| Sunday | appointment_portal | 2 |
| Sunday | bank_balance | 3 |
| Sunday | calendar | 9 |
| Sunday | clock | 11 |
| Sunday | course_portal | 4 |
| Sunday | email | 8 |
| Sunday | laundry_status | 3 |

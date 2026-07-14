# PM-Bench score report

## Summary

Hit: 40 | Late: 1 | Miss: 40 | False alarms: 21 | Commission: 0 | Wrong-content: 7 | Dependency violations: 0 | Overkill steps: 19 | state query calls: 281 | check_time calls: 72 | Actions: 62
Exact-set: matches 33 | mismatches 47 | reward -14
Set micro: TP 40 | FP 22 | FN 41
Cross-day: hit 0 | late 1 | miss 6 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 4
Rates: hit 49.4% | late 1.2% | miss 49.4% | false alarm/step 26.2% | commission 0.0% | wrong-content 8.6% | dependency/step 0.0% | overkill/step 23.8% | cross-day miss 85.7% | update miss 88.9% | precision_hit 64.5% | precision_any 66.1% | exact-set match rate 41.2% | exact-set avg reward -0.175 | set_precision 64.5% | set_recall 49.4% | set_f1 55.9%
Hit rates (by modality): event 43.9% | time 62.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T01:22:59.997Z |
| Finished (UTC) | 2026-03-28T03:32:27.937Z |
| Duration | 2h 9m 27.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 40 |
| Late | 1 |
| Miss | 40 |
| False alarms | 21 |
| Commission | 0 |
| Wrong-content | 7 |
| Dependency violations | 0 |
| Overkill steps | 19 |
| State query calls | 281 |
| Check_time calls | 72 |
| Actions | 62 |
| Exact-set matches | 33 |
| Exact-set mismatches | 47 |
| Exact-set reward | -14 |
| Set TP | 40 |
| Set FP | 22 |
| Set FN | 41 |

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
| Hit rate | 49.4% |
| Late rate | 1.2% |
| Miss rate | 49.4% |
| False alarm/step | 26.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.6% |
| Dependency/step | 0.0% |
| Overkill/step | 23.8% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 88.9% |
| Precision hit | 64.5% |
| Precision any | 66.1% |
| Exact-set match rate | 41.2% |
| Exact-set avg reward | -0.175 |
| Set precision | 64.5% |
| Set recall | 49.4% |
| Set F1 | 55.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 25 | 57 | 43.9% |
| Time (time + time_check) | 15 | 24 | 62.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 1 | 18 | 42 | 54.8% | 57.1% |
| proactive_monitoring_required | 17 | 0 | 22 | 39 | 43.6% | 43.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 15 | 0 | 9 | 24 | 62.5% | 62.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 23.1% | 15.4% | 66.7% | 66.7% | 66.7% | 66.7% | 61.5% | 0.231 | 72.7% | 66.7% | 69.6% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 15.4% | 15.4% | 42.9% | 75.0% | 75.0% | 42.9% | 53.8% | 0.077 | 75.0% | 54.5% | 63.2% |
| Wednesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 30.0% | 40.0% | 33.3% | 100.0% | 50.0% | 40.0% | 30.0% | -0.400 | 55.6% | 45.5% | 50.0% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 27.3% | 27.3% | 55.6% | 66.7% | 62.5% | 50.0% | 45.5% | -0.091 | 70.0% | 58.3% | 63.6% |
| Friday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 33.3% | 25.0% | 25.0% | 50.0% | 33.3% | 33.3% | 33.3% | -0.333 | 50.0% | 33.3% | 40.0% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 20.0% | 20.0% | 40.0% | 50.0% | 50.0% | 33.3% | 30.0% | -0.400 | 75.0% | 42.9% | 54.5% |
| Sunday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 36.4% | 27.3% | 40.0% | 50.0% | 50.0% | 40.0% | 27.3% | -0.455 | 50.0% | 44.4% | 47.1% |

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

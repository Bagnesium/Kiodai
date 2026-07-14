# PM-Bench score report

## Summary

Hit: 52 | Late: 7 | Miss: 22 | False alarms: 39 | Commission: 0 | Wrong-content: 18 | Dependency violations: 0 | Overkill steps: 29 | state query calls: 312 | check_time calls: 80 | Actions: 98
Exact-set: matches 33 | mismatches 47 | reward -14
Set micro: TP 52 | FP 46 | FN 29
Cross-day: hit 2 | late 3 | miss 2 | total 7
Updates: hit 3 | late 2 | miss 4 | canceled 2 | total 11 | violations 8
Rates: hit 64.2% | late 8.6% | miss 27.2% | false alarm/step 48.8% | commission 0.0% | wrong-content 22.2% | dependency/step 0.0% | overkill/step 36.2% | cross-day miss 28.6% | update miss 44.4% | precision_hit 53.1% | precision_any 60.2% | exact-set match rate 41.2% | exact-set avg reward -0.175 | set_precision 53.1% | set_recall 64.2% | set_f1 58.1%
Hit rates (by modality): event 57.9% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T23:32:46.920Z |
| Finished (UTC) | 2026-03-27T23:59:47.214Z |
| Duration | 27m 0.3s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 52 |
| Late | 7 |
| Miss | 22 |
| False alarms | 39 |
| Commission | 0 |
| Wrong-content | 18 |
| Dependency violations | 0 |
| Overkill steps | 29 |
| State query calls | 312 |
| Check_time calls | 80 |
| Actions | 98 |
| Exact-set matches | 33 |
| Exact-set mismatches | 47 |
| Exact-set reward | -14 |
| Set TP | 52 |
| Set FP | 46 |
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
| Late rate | 8.6% |
| Miss rate | 27.2% |
| False alarm/step | 48.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 22.2% |
| Dependency/step | 0.0% |
| Overkill/step | 36.2% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 44.4% |
| Precision hit | 53.1% |
| Precision any | 60.2% |
| Exact-set match rate | 41.2% |
| Exact-set avg reward | -0.175 |
| Set precision | 53.1% |
| Set recall | 64.2% |
| Set F1 | 58.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 33 | 57 | 57.9% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 3 | 8 | 42 | 73.8% | 81.0% |
| proactive_monitoring_required | 21 | 4 | 14 | 39 | 53.8% | 64.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 19 | 2 | 3 | 24 | 79.2% | 87.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 53.8% | 23.1% | 55.6% | 100.0% | 66.7% | 66.7% | 53.8% | 0.077 | 53.3% | 66.7% | 59.3% |
| Tuesday | 7 | 3 | 1 | 63.6% | 27.3% | 9.1% | 38.5% | 38.5% | 57.1% | 75.0% | 100.0% | 42.9% | 38.5% | -0.231 | 46.7% | 63.6% | 53.8% |
| Wednesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 40.0% | 40.0% | 55.6% | 100.0% | 66.7% | 60.0% | 30.0% | -0.400 | 53.8% | 63.6% | 58.3% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 36.4% | 27.3% | 66.7% | 100.0% | 75.0% | 75.0% | 54.5% | 0.091 | 69.2% | 75.0% | 72.0% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 41.7% | 33.3% | 25.0% | 75.0% | 33.3% | 50.0% | 33.3% | -0.333 | 50.0% | 41.7% | 45.5% |
| Saturday | 10 | 2 | 2 | 71.4% | 14.3% | 14.3% | 70.0% | 50.0% | 70.0% | 75.0% | 87.5% | 50.0% | 40.0% | -0.200 | 52.6% | 71.4% | 60.6% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 63.6% | 45.5% | 80.0% | 50.0% | 100.0% | 40.0% | 36.4% | -0.273 | 46.2% | 66.7% | 54.5% |

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

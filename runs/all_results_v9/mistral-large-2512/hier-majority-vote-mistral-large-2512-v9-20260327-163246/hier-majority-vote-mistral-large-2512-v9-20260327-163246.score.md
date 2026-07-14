# PM-Bench score report

## Summary

Hit: 61 | Late: 5 | Miss: 15 | False alarms: 115 | Commission: 20 | Wrong-content: 76 | Dependency violations: 0 | Overkill steps: 69 | state query calls: 312 | check_time calls: 80 | Actions: 201
Exact-set: matches 3 | mismatches 77 | reward -74
Set micro: TP 61 | FP 140 | FN 20
Cross-day: hit 2 | late 4 | miss 1 | total 7
Updates: hit 7 | late 0 | miss 2 | canceled 2 | total 11 | violations 20
Rates: hit 75.3% | late 6.2% | miss 18.5% | false alarm/step 143.8% | commission 24.7% | wrong-content 93.8% | dependency/step 0.0% | overkill/step 86.2% | cross-day miss 14.3% | update miss 22.2% | precision_hit 30.3% | precision_any 32.8% | exact-set match rate 3.8% | exact-set avg reward -0.925 | set_precision 30.3% | set_recall 75.3% | set_f1 43.3%
Hit rates (by modality): event 68.4% | time 91.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T04:56:10.126Z |
| Finished (UTC) | 2026-03-28T04:56:10.126Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 61 |
| Late | 5 |
| Miss | 15 |
| False alarms | 115 |
| Commission | 20 |
| Wrong-content | 76 |
| Dependency violations | 0 |
| Overkill steps | 69 |
| State query calls | 312 |
| Check_time calls | 80 |
| Actions | 201 |
| Exact-set matches | 3 |
| Exact-set mismatches | 77 |
| Exact-set reward | -74 |
| Set TP | 61 |
| Set FP | 140 |
| Set FN | 20 |

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
| Hit rate | 75.3% |
| Late rate | 6.2% |
| Miss rate | 18.5% |
| False alarm/step | 143.8% |
| Commission rate | 24.7% |
| Wrong-content rate | 93.8% |
| Dependency/step | 0.0% |
| Overkill/step | 86.2% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 22.2% |
| Precision hit | 30.3% |
| Precision any | 32.8% |
| Exact-set match rate | 3.8% |
| Exact-set avg reward | -0.925 |
| Set precision | 30.3% |
| Set recall | 75.3% |
| Set F1 | 43.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 22 | 24 | 91.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 33 | 4 | 5 | 42 | 78.6% | 88.1% |
| proactive_monitoring_required | 28 | 1 | 10 | 39 | 71.8% | 74.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| clock | 22 | 0 | 2 | 24 | 91.7% | 91.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 3 | 0 | 0 | 3 | 100.0% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 123.1% | 92.3% | 77.8% | 100.0% | 83.3% | 83.3% | 0.0% | -1.000 | 37.0% | 83.3% | 51.3% |
| Tuesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 184.6% | 84.6% | 71.4% | 100.0% | 100.0% | 71.4% | 0.0% | -1.000 | 25.0% | 81.8% | 38.3% |
| Wednesday | 7 | 2 | 2 | 63.6% | 18.2% | 18.2% | 180.0% | 80.0% | 66.7% | 50.0% | 66.7% | 60.0% | 0.0% | -1.000 | 25.0% | 63.6% | 35.9% |
| Thursday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 100.0% | 72.7% | 66.7% | 100.0% | 75.0% | 75.0% | 9.1% | -0.818 | 39.1% | 75.0% | 51.4% |
| Friday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 166.7% | 100.0% | 50.0% | 100.0% | 50.0% | 83.3% | 0.0% | -1.000 | 22.2% | 66.7% | 33.3% |
| Saturday | 11 | 1 | 2 | 78.6% | 7.1% | 14.3% | 140.0% | 80.0% | 70.0% | 100.0% | 87.5% | 66.7% | 20.0% | -0.600 | 40.7% | 78.6% | 53.7% |
| Sunday | 7 | 0 | 2 | 77.8% | 0.0% | 22.2% | 109.1% | 90.9% | 80.0% | 75.0% | 100.0% | 60.0% | 0.0% | -1.000 | 29.2% | 77.8% | 42.4% |

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

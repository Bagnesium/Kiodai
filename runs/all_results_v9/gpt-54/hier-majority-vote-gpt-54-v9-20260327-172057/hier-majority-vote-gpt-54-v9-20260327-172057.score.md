# PM-Bench score report

## Summary

Hit: 58 | Late: 6 | Miss: 17 | False alarms: 118 | Commission: 35 | Wrong-content: 87 | Dependency violations: 0 | Overkill steps: 64 | state query calls: 300 | check_time calls: 79 | Actions: 217
Exact-set: matches 5 | mismatches 75 | reward -70
Set micro: TP 58 | FP 159 | FN 23
Cross-day: hit 3 | late 2 | miss 2 | total 7
Updates: hit 4 | late 1 | miss 4 | canceled 2 | total 11 | violations 16
Rates: hit 71.6% | late 7.4% | miss 21.0% | false alarm/step 147.5% | commission 43.2% | wrong-content 107.4% | dependency/step 0.0% | overkill/step 80.0% | cross-day miss 28.6% | update miss 44.4% | precision_hit 26.7% | precision_any 29.5% | exact-set match rate 6.2% | exact-set avg reward -0.875 | set_precision 26.7% | set_recall 71.6% | set_f1 38.9%
Hit rates (by modality): event 68.4% | time 79.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T04:56:10.126Z |
| Finished (UTC) | 2026-03-28T04:56:10.126Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 58 |
| Late | 6 |
| Miss | 17 |
| False alarms | 118 |
| Commission | 35 |
| Wrong-content | 87 |
| Dependency violations | 0 |
| Overkill steps | 64 |
| State query calls | 300 |
| Check_time calls | 79 |
| Actions | 217 |
| Exact-set matches | 5 |
| Exact-set mismatches | 75 |
| Exact-set reward | -70 |
| Set TP | 58 |
| Set FP | 159 |
| Set FN | 23 |

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
| Hit rate | 71.6% |
| Late rate | 7.4% |
| Miss rate | 21.0% |
| False alarm/step | 147.5% |
| Commission rate | 43.2% |
| Wrong-content rate | 107.4% |
| Dependency/step | 0.0% |
| Overkill/step | 80.0% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 44.4% |
| Precision hit | 26.7% |
| Precision any | 29.5% |
| Exact-set match rate | 6.2% |
| Exact-set avg reward | -0.875 |
| Set precision | 26.7% |
| Set recall | 71.6% |
| Set F1 | 38.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 39 | 57 | 68.4% |
| Time (time + time_check) | 19 | 24 | 79.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 32 | 2 | 8 | 42 | 76.2% | 81.0% |
| proactive_monitoring_required | 26 | 4 | 9 | 39 | 66.7% | 76.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 1 | 1 | 1 | 3 | 33.3% | 66.7% |
| clock | 19 | 2 | 3 | 24 | 79.2% | 87.5% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 9 | 1 | 2 | 75.0% | 8.3% | 16.7% | 138.5% | 76.9% | 77.8% | 66.7% | 66.7% | 83.3% | 15.4% | -0.692 | 31.0% | 75.0% | 43.9% |
| Tuesday | 7 | 3 | 1 | 63.6% | 27.3% | 9.1% | 138.5% | 92.3% | 57.1% | 75.0% | 75.0% | 57.1% | 0.0% | -1.000 | 15.6% | 63.6% | 25.0% |
| Wednesday | 8 | 1 | 2 | 72.7% | 9.1% | 18.2% | 160.0% | 80.0% | 66.7% | 100.0% | 66.7% | 80.0% | 0.0% | -1.000 | 30.8% | 72.7% | 43.2% |
| Thursday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 127.3% | 81.8% | 77.8% | 100.0% | 87.5% | 75.0% | 9.1% | -0.818 | 28.6% | 83.3% | 42.6% |
| Friday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 183.3% | 75.0% | 62.5% | 75.0% | 66.7% | 66.7% | 8.3% | -0.833 | 25.8% | 66.7% | 37.2% |
| Saturday | 11 | 1 | 2 | 78.6% | 7.1% | 14.3% | 150.0% | 90.0% | 70.0% | 100.0% | 87.5% | 66.7% | 0.0% | -1.000 | 35.5% | 78.6% | 48.9% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 136.4% | 63.6% | 60.0% | 50.0% | 75.0% | 40.0% | 9.1% | -0.818 | 25.0% | 55.6% | 34.5% |

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

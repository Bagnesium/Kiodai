# PM-Bench score report

## Summary

Hit: 54 | Late: 6 | Miss: 21 | False alarms: 107 | Commission: 26 | Wrong-content: 70 | Dependency violations: 0 | Overkill steps: 61 | state query calls: 281 | check_time calls: 72 | Actions: 193
Exact-set: matches 7 | mismatches 73 | reward -66
Set micro: TP 54 | FP 139 | FN 27
Cross-day: hit 4 | late 1 | miss 2 | total 7
Updates: hit 2 | late 1 | miss 6 | canceled 2 | total 11 | violations 17
Rates: hit 66.7% | late 7.4% | miss 25.9% | false alarm/step 133.8% | commission 32.1% | wrong-content 86.4% | dependency/step 0.0% | overkill/step 76.2% | cross-day miss 28.6% | update miss 66.7% | precision_hit 28.0% | precision_any 31.1% | exact-set match rate 8.8% | exact-set avg reward -0.825 | set_precision 28.0% | set_recall 66.7% | set_f1 39.4%
Hit rates (by modality): event 63.2% | time 75.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T04:56:10.126Z |
| Finished (UTC) | 2026-03-28T04:56:10.126Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 54 |
| Late | 6 |
| Miss | 21 |
| False alarms | 107 |
| Commission | 26 |
| Wrong-content | 70 |
| Dependency violations | 0 |
| Overkill steps | 61 |
| State query calls | 281 |
| Check_time calls | 72 |
| Actions | 193 |
| Exact-set matches | 7 |
| Exact-set mismatches | 73 |
| Exact-set reward | -66 |
| Set TP | 54 |
| Set FP | 139 |
| Set FN | 27 |

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
| Hit rate | 66.7% |
| Late rate | 7.4% |
| Miss rate | 25.9% |
| False alarm/step | 133.8% |
| Commission rate | 32.1% |
| Wrong-content rate | 86.4% |
| Dependency/step | 0.0% |
| Overkill/step | 76.2% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 66.7% |
| Precision hit | 28.0% |
| Precision any | 31.1% |
| Exact-set match rate | 8.8% |
| Exact-set avg reward | -0.825 |
| Set precision | 28.0% |
| Set recall | 66.7% |
| Set F1 | 39.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 36 | 57 | 63.2% |
| Time (time + time_check) | 18 | 24 | 75.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 1 | 10 | 42 | 73.8% | 76.2% |
| proactive_monitoring_required | 23 | 5 | 11 | 39 | 59.0% | 71.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 0 | 2 | 1 | 3 | 0.0% | 66.7% |
| clock | 18 | 1 | 5 | 24 | 75.0% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 2 | 1 | 0 | 3 | 66.7% | 100.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 10 | 0 | 2 | 83.3% | 0.0% | 16.7% | 138.5% | 69.2% | 77.8% | 100.0% | 66.7% | 100.0% | 15.4% | -0.692 | 34.5% | 83.3% | 48.8% |
| Tuesday | 6 | 4 | 1 | 54.5% | 36.4% | 9.1% | 92.3% | 76.9% | 42.9% | 75.0% | 75.0% | 42.9% | 7.7% | -0.846 | 17.1% | 54.5% | 26.1% |
| Wednesday | 9 | 1 | 1 | 81.8% | 9.1% | 9.1% | 130.0% | 80.0% | 77.8% | 100.0% | 83.3% | 80.0% | 10.0% | -0.800 | 33.3% | 81.8% | 47.4% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 127.3% | 72.7% | 77.8% | 66.7% | 87.5% | 50.0% | 18.2% | -0.636 | 31.0% | 75.0% | 43.9% |
| Friday | 6 | 1 | 5 | 50.0% | 8.3% | 41.7% | 158.3% | 75.0% | 37.5% | 75.0% | 50.0% | 50.0% | 0.0% | -1.000 | 23.1% | 50.0% | 31.6% |
| Saturday | 9 | 0 | 5 | 64.3% | 0.0% | 35.7% | 150.0% | 80.0% | 60.0% | 75.0% | 75.0% | 50.0% | 10.0% | -0.800 | 36.0% | 64.3% | 46.2% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 145.5% | 81.8% | 60.0% | 50.0% | 75.0% | 40.0% | 0.0% | -1.000 | 22.7% | 55.6% | 32.3% |

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

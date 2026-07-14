# PM-Bench score report

## Summary

Hit: 19 | Late: 2 | Miss: 60 | False alarms: 11 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 9 | state query calls: 237 | check_time calls: 80 | Actions: 32
Exact-set: matches 28 | mismatches 52 | reward -24
Set micro: TP 19 | FP 13 | FN 62
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 2 | late 1 | miss 6 | canceled 2 | total 11 | violations 3
Rates: hit 23.5% | late 2.5% | miss 74.1% | false alarm/step 13.8% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 11.2% | cross-day miss 85.7% | update miss 66.7% | precision_hit 59.4% | precision_any 65.6% | exact-set match rate 35.0% | exact-set avg reward -0.300 | set_precision 59.4% | set_recall 23.5% | set_f1 33.6%
Hit rates (by modality): event 21.1% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T23:59:47.430Z |
| Finished (UTC) | 2026-03-28T00:20:57.313Z |
| Duration | 21m 9.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 19 |
| Late | 2 |
| Miss | 60 |
| False alarms | 11 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 9 |
| State query calls | 237 |
| Check_time calls | 80 |
| Actions | 32 |
| Exact-set matches | 28 |
| Exact-set mismatches | 52 |
| Exact-set reward | -24 |
| Set TP | 19 |
| Set FP | 13 |
| Set FN | 62 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 50 |
| bank_balance | 5 |
| calendar | 36 |
| clock | 80 |
| email | 20 |
| laundry_status | 1 |
| library_hold | 40 |
| shipment_status | 5 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 23.5% |
| Late rate | 2.5% |
| Miss rate | 74.1% |
| False alarm/step | 13.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 11.2% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 59.4% |
| Precision any | 65.6% |
| Exact-set match rate | 35.0% |
| Exact-set avg reward | -0.300 |
| Set precision | 59.4% |
| Set recall | 23.5% |
| Set F1 | 33.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 12 | 57 | 21.1% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 12 | 1 | 29 | 42 | 28.6% | 31.0% |
| proactive_monitoring_required | 7 | 1 | 31 | 39 | 17.9% | 20.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 7 | 1 | 16 | 24 | 29.2% | 33.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 15.4% | 7.7% | 11.1% | 0.0% | 16.7% | 0.0% | 30.8% | -0.385 | 33.3% | 8.3% | 13.3% |
| Tuesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 15.4% | 15.4% | 28.6% | 75.0% | 50.0% | 42.9% | 46.2% | -0.077 | 62.5% | 45.5% | 52.6% |
| Wednesday | 2 | 1 | 8 | 18.2% | 9.1% | 72.7% | 30.0% | 30.0% | 22.2% | 0.0% | 33.3% | 0.0% | 20.0% | -0.600 | 33.3% | 18.2% | 23.5% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 9.1% | 9.1% | 55.6% | 33.3% | 62.5% | 25.0% | 54.5% | 0.091 | 85.7% | 50.0% | 63.2% |
| Friday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 16.7% | 8.3% | 12.5% | 25.0% | 16.7% | 16.7% | 41.7% | -0.167 | 50.0% | 16.7% | 25.0% |
| Saturday | 2 | 0 | 12 | 14.3% | 0.0% | 85.7% | 10.0% | 10.0% | 10.0% | 25.0% | 12.5% | 16.7% | 10.0% | -0.800 | 66.7% | 14.3% | 23.5% |
| Sunday | 1 | 0 | 8 | 11.1% | 0.0% | 88.9% | 0.0% | 0.0% | 0.0% | 25.0% | 0.0% | 20.0% | 36.4% | -0.273 | 100.0% | 11.1% | 20.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 7 |
| Monday | clock | 13 |
| Monday | email | 6 |
| Monday | library_hold | 6 |
| Tuesday | calendar | 11 |
| Tuesday | clock | 13 |
| Tuesday | email | 2 |
| Tuesday | library_hold | 6 |
| Wednesday | bank_balance | 3 |
| Wednesday | calendar | 7 |
| Wednesday | clock | 10 |
| Thursday | appointment_portal | 10 |
| Thursday | bank_balance | 2 |
| Thursday | clock | 11 |
| Thursday | shipment_status | 5 |
| Friday | appointment_portal | 12 |
| Friday | clock | 12 |
| Friday | email | 11 |
| Friday | laundry_status | 1 |
| Friday | library_hold | 7 |
| Saturday | appointment_portal | 10 |
| Saturday | calendar | 7 |
| Saturday | clock | 10 |
| Saturday | email | 1 |
| Saturday | library_hold | 10 |
| Sunday | appointment_portal | 11 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |
| Sunday | library_hold | 11 |

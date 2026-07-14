# PM-Bench score report

## Summary

Hit: 20 | Late: 1 | Miss: 60 | False alarms: 31 | Commission: 12 | Wrong-content: 22 | Dependency violations: 0 | Overkill steps: 24 | state query calls: 237 | check_time calls: 80 | Actions: 64
Exact-set: matches 17 | mismatches 63 | reward -46
Set micro: TP 20 | FP 44 | FN 61
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 3 | late 1 | miss 5 | canceled 2 | total 11 | violations 10
Rates: hit 24.7% | late 1.2% | miss 74.1% | false alarm/step 38.8% | commission 14.8% | wrong-content 27.2% | dependency/step 0.0% | overkill/step 30.0% | cross-day miss 100.0% | update miss 55.6% | precision_hit 31.2% | precision_any 32.8% | exact-set match rate 21.2% | exact-set avg reward -0.575 | set_precision 31.2% | set_recall 24.7% | set_f1 27.6%
Hit rates (by modality): event 22.8% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T04:56:10.126Z |
| Finished (UTC) | 2026-03-28T04:56:10.126Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 20 |
| Late | 1 |
| Miss | 60 |
| False alarms | 31 |
| Commission | 12 |
| Wrong-content | 22 |
| Dependency violations | 0 |
| Overkill steps | 24 |
| State query calls | 237 |
| Check_time calls | 80 |
| Actions | 64 |
| Exact-set matches | 17 |
| Exact-set mismatches | 63 |
| Exact-set reward | -46 |
| Set TP | 20 |
| Set FP | 44 |
| Set FN | 61 |

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
| Hit rate | 24.7% |
| Late rate | 1.2% |
| Miss rate | 74.1% |
| False alarm/step | 38.8% |
| Commission rate | 14.8% |
| Wrong-content rate | 27.2% |
| Dependency/step | 0.0% |
| Overkill/step | 30.0% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 55.6% |
| Precision hit | 31.2% |
| Precision any | 32.8% |
| Exact-set match rate | 21.2% |
| Exact-set avg reward | -0.575 |
| Set precision | 31.2% |
| Set recall | 24.7% |
| Set F1 | 27.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 13 | 57 | 22.8% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 12 | 0 | 30 | 42 | 28.6% | 28.6% |
| proactive_monitoring_required | 8 | 1 | 30 | 39 | 20.5% | 23.1% |

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
| library_hold | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 38.5% | 23.1% | 11.1% | 0.0% | 16.7% | 0.0% | 15.4% | -0.692 | 16.7% | 8.3% | 11.1% |
| Tuesday | 3 | 1 | 7 | 27.3% | 9.1% | 63.6% | 7.7% | 38.5% | 14.3% | 50.0% | 25.0% | 28.6% | 23.1% | -0.538 | 27.3% | 27.3% | 27.3% |
| Wednesday | 3 | 0 | 8 | 27.3% | 0.0% | 72.7% | 30.0% | 20.0% | 33.3% | 0.0% | 50.0% | 0.0% | 30.0% | -0.400 | 42.9% | 27.3% | 33.3% |
| Thursday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 109.1% | 72.7% | 33.3% | 66.7% | 37.5% | 50.0% | 9.1% | -0.818 | 26.3% | 41.7% | 32.3% |
| Friday | 3 | 0 | 9 | 25.0% | 0.0% | 75.0% | 50.0% | 25.0% | 25.0% | 25.0% | 16.7% | 33.3% | 25.0% | -0.500 | 30.0% | 25.0% | 27.3% |
| Saturday | 4 | 0 | 10 | 28.6% | 0.0% | 71.4% | 40.0% | 30.0% | 30.0% | 25.0% | 37.5% | 16.7% | 10.0% | -0.800 | 40.0% | 28.6% | 33.3% |
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

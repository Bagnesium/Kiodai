# PM-Bench score report

## Summary

Hit: 41 | Late: 3 | Miss: 37 | False alarms: 41 | Commission: 0 | Wrong-content: 17 | Dependency violations: 0 | Overkill steps: 29 | state query calls: 140 | check_time calls: 76 | Actions: 85
Exact-set: matches 24 | mismatches 56 | reward -32
Set micro: TP 41 | FP 44 | FN 40
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 1 | late 2 | miss 6 | canceled 2 | total 11 | violations 13
Rates: hit 50.6% | late 3.7% | miss 45.7% | false alarm/step 51.2% | commission 0.0% | wrong-content 21.0% | dependency/step 0.0% | overkill/step 36.2% | cross-day miss 85.7% | update miss 66.7% | precision_hit 48.2% | precision_any 51.8% | exact-set match rate 30.0% | exact-set avg reward -0.400 | set_precision 48.2% | set_recall 50.6% | set_f1 49.4%
Hit rates (by modality): event 42.1% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T04:56:10.126Z |
| Finished (UTC) | 2026-03-28T04:56:10.126Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 41 |
| Late | 3 |
| Miss | 37 |
| False alarms | 41 |
| Commission | 0 |
| Wrong-content | 17 |
| Dependency violations | 0 |
| Overkill steps | 29 |
| State query calls | 140 |
| Check_time calls | 76 |
| Actions | 85 |
| Exact-set matches | 24 |
| Exact-set mismatches | 56 |
| Exact-set reward | -32 |
| Set TP | 41 |
| Set FP | 44 |
| Set FN | 40 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 5 |
| bank_balance | 3 |
| calendar | 29 |
| clock | 76 |
| course_portal | 1 |
| email | 7 |
| laundry_status | 5 |
| library_hold | 5 |
| shipment_status | 9 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 50.6% |
| Late rate | 3.7% |
| Miss rate | 45.7% |
| False alarm/step | 51.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 21.0% |
| Dependency/step | 0.0% |
| Overkill/step | 36.2% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 48.2% |
| Precision any | 51.8% |
| Exact-set match rate | 30.0% |
| Exact-set avg reward | -0.400 |
| Set precision | 48.2% |
| Set recall | 50.6% |
| Set F1 | 49.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 24 | 57 | 42.1% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 1 | 18 | 42 | 54.8% | 57.1% |
| proactive_monitoring_required | 18 | 2 | 19 | 39 | 46.2% | 51.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 2 | 5 | 24 | 70.8% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 69.2% | 46.2% | 55.6% | 100.0% | 66.7% | 66.7% | 30.8% | -0.385 | 47.1% | 66.7% | 55.2% |
| Tuesday | 5 | 2 | 4 | 45.5% | 18.2% | 36.4% | 38.5% | 38.5% | 28.6% | 75.0% | 50.0% | 42.9% | 30.8% | -0.385 | 41.7% | 45.5% | 43.5% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 40.0% | 40.0% | 44.4% | 100.0% | 66.7% | 40.0% | 30.0% | -0.400 | 60.0% | 54.5% | 57.1% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 54.5% | 36.4% | 44.4% | 66.7% | 50.0% | 50.0% | 27.3% | -0.455 | 50.0% | 50.0% | 50.0% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 66.7% | 41.7% | 37.5% | 75.0% | 50.0% | 50.0% | 25.0% | -0.500 | 42.9% | 50.0% | 46.2% |
| Saturday | 5 | 1 | 8 | 35.7% | 7.1% | 57.1% | 40.0% | 20.0% | 30.0% | 50.0% | 37.5% | 33.3% | 30.0% | -0.400 | 50.0% | 35.7% | 41.7% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 45.5% | 27.3% | 60.0% | 50.0% | 75.0% | 40.0% | 36.4% | -0.273 | 50.0% | 55.6% | 52.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 4 |
| Monday | calendar | 4 |
| Monday | clock | 11 |
| Monday | email | 2 |
| Monday | library_hold | 3 |
| Monday | shipment_status | 1 |
| Tuesday | calendar | 9 |
| Tuesday | clock | 13 |
| Tuesday | email | 1 |
| Wednesday | bank_balance | 1 |
| Wednesday | calendar | 2 |
| Wednesday | clock | 9 |
| Thursday | appointment_portal | 1 |
| Thursday | calendar | 6 |
| Thursday | clock | 11 |
| Thursday | shipment_status | 2 |
| Friday | bank_balance | 1 |
| Friday | clock | 12 |
| Friday | email | 4 |
| Friday | laundry_status | 4 |
| Friday | library_hold | 2 |
| Friday | shipment_status | 2 |
| Saturday | calendar | 1 |
| Saturday | clock | 9 |
| Saturday | shipment_status | 4 |
| Sunday | bank_balance | 1 |
| Sunday | calendar | 7 |
| Sunday | clock | 11 |
| Sunday | course_portal | 1 |
| Sunday | laundry_status | 1 |

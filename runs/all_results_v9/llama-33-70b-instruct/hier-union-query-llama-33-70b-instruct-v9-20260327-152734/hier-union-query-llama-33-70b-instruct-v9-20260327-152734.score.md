# PM-Bench score report

## Summary

Hit: 42 | Late: 4 | Miss: 35 | False alarms: 38 | Commission: 0 | Wrong-content: 16 | Dependency violations: 0 | Overkill steps: 24 | state query calls: 140 | check_time calls: 76 | Actions: 84
Exact-set: matches 31 | mismatches 49 | reward -18
Set micro: TP 42 | FP 42 | FN 39
Cross-day: hit 2 | late 1 | miss 4 | total 7
Updates: hit 1 | late 2 | miss 6 | canceled 2 | total 11 | violations 11
Rates: hit 51.9% | late 4.9% | miss 43.2% | false alarm/step 47.5% | commission 0.0% | wrong-content 19.8% | dependency/step 0.0% | overkill/step 30.0% | cross-day miss 57.1% | update miss 66.7% | precision_hit 50.0% | precision_any 54.8% | exact-set match rate 38.8% | exact-set avg reward -0.225 | set_precision 50.0% | set_recall 51.9% | set_f1 50.9%
Hit rates (by modality): event 43.9% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T22:27:34.579Z |
| Finished (UTC) | 2026-03-27T23:32:46.704Z |
| Duration | 1h 5m 12.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 42 |
| Late | 4 |
| Miss | 35 |
| False alarms | 38 |
| Commission | 0 |
| Wrong-content | 16 |
| Dependency violations | 0 |
| Overkill steps | 24 |
| State query calls | 140 |
| Check_time calls | 76 |
| Actions | 84 |
| Exact-set matches | 31 |
| Exact-set mismatches | 49 |
| Exact-set reward | -18 |
| Set TP | 42 |
| Set FP | 42 |
| Set FN | 39 |

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
| Hit rate | 51.9% |
| Late rate | 4.9% |
| Miss rate | 43.2% |
| False alarm/step | 47.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 19.8% |
| Dependency/step | 0.0% |
| Overkill/step | 30.0% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 66.7% |
| Precision hit | 50.0% |
| Precision any | 54.8% |
| Exact-set match rate | 38.8% |
| Exact-set avg reward | -0.225 |
| Set precision | 50.0% |
| Set recall | 51.9% |
| Set F1 | 50.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 25 | 57 | 43.9% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 25 | 2 | 15 | 42 | 59.5% | 64.3% |
| proactive_monitoring_required | 17 | 2 | 20 | 39 | 43.6% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
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
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 53.8% | 30.8% | 44.4% | 100.0% | 66.7% | 50.0% | 46.2% | -0.077 | 50.0% | 58.3% | 53.8% |
| Tuesday | 5 | 2 | 4 | 45.5% | 18.2% | 36.4% | 23.1% | 23.1% | 28.6% | 75.0% | 50.0% | 42.9% | 46.2% | -0.077 | 50.0% | 45.5% | 47.6% |
| Wednesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 40.0% | 40.0% | 44.4% | 100.0% | 66.7% | 40.0% | 30.0% | -0.400 | 54.5% | 54.5% | 54.5% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 45.5% | 36.4% | 66.7% | 66.7% | 75.0% | 50.0% | 36.4% | -0.273 | 61.5% | 66.7% | 64.0% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 83.3% | 41.7% | 37.5% | 75.0% | 50.0% | 50.0% | 33.3% | -0.333 | 37.5% | 50.0% | 42.9% |
| Saturday | 5 | 1 | 8 | 35.7% | 7.1% | 57.1% | 40.0% | 10.0% | 30.0% | 50.0% | 37.5% | 33.3% | 40.0% | -0.200 | 50.0% | 35.7% | 41.7% |
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

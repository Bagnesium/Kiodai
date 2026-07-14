# PM-Bench score report

## Summary

Hit: 39 | Late: 3 | Miss: 39 | False alarms: 25 | Commission: 0 | Wrong-content: 10 | Dependency violations: 0 | Overkill steps: 19 | state query calls: 140 | check_time calls: 76 | Actions: 67
Exact-set: matches 33 | mismatches 47 | reward -14
Set micro: TP 39 | FP 28 | FN 42
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 1 | late 2 | miss 6 | canceled 2 | total 11 | violations 11
Rates: hit 48.1% | late 3.7% | miss 48.1% | false alarm/step 31.2% | commission 0.0% | wrong-content 12.3% | dependency/step 0.0% | overkill/step 23.8% | cross-day miss 85.7% | update miss 66.7% | precision_hit 58.2% | precision_any 62.7% | exact-set match rate 41.2% | exact-set avg reward -0.175 | set_precision 58.2% | set_recall 48.1% | set_f1 52.7%
Hit rates (by modality): event 40.4% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T05:03:17.801Z |
| Finished (UTC) | 2026-03-28T05:03:17.801Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 39 |
| Late | 3 |
| Miss | 39 |
| False alarms | 25 |
| Commission | 0 |
| Wrong-content | 10 |
| Dependency violations | 0 |
| Overkill steps | 19 |
| State query calls | 140 |
| Check_time calls | 76 |
| Actions | 67 |
| Exact-set matches | 33 |
| Exact-set mismatches | 47 |
| Exact-set reward | -14 |
| Set TP | 39 |
| Set FP | 28 |
| Set FN | 42 |

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
| Hit rate | 48.1% |
| Late rate | 3.7% |
| Miss rate | 48.1% |
| False alarm/step | 31.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 12.3% |
| Dependency/step | 0.0% |
| Overkill/step | 23.8% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 58.2% |
| Precision any | 62.7% |
| Exact-set match rate | 41.2% |
| Exact-set avg reward | -0.175 |
| Set precision | 58.2% |
| Set recall | 48.1% |
| Set F1 | 52.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 23 | 57 | 40.4% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 1 | 18 | 42 | 54.8% | 57.1% |
| proactive_monitoring_required | 16 | 2 | 21 | 39 | 41.0% | 46.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 16 | 2 | 6 | 24 | 66.7% | 75.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 30.8% | 23.1% | 44.4% | 66.7% | 66.7% | 33.3% | 46.2% | -0.077 | 60.0% | 50.0% | 54.5% |
| Tuesday | 5 | 2 | 4 | 45.5% | 18.2% | 36.4% | 23.1% | 23.1% | 28.6% | 75.0% | 50.0% | 42.9% | 46.2% | -0.077 | 50.0% | 45.5% | 47.6% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 30.0% | 30.0% | 44.4% | 100.0% | 66.7% | 40.0% | 40.0% | -0.200 | 66.7% | 54.5% | 60.0% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 18.2% | 18.2% | 44.4% | 66.7% | 50.0% | 50.0% | 45.5% | -0.091 | 75.0% | 50.0% | 60.0% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 66.7% | 41.7% | 37.5% | 75.0% | 50.0% | 50.0% | 25.0% | -0.500 | 42.9% | 50.0% | 46.2% |
| Saturday | 5 | 1 | 8 | 35.7% | 7.1% | 57.1% | 20.0% | 10.0% | 30.0% | 50.0% | 37.5% | 33.3% | 40.0% | -0.200 | 62.5% | 35.7% | 45.5% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 27.3% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 62.5% | 55.6% | 58.8% |

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

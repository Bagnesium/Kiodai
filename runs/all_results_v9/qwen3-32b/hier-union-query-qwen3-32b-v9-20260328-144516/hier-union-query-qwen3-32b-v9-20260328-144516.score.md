# PM-Bench score report

## Summary

Hit: 27 | Late: 5 | Miss: 49 | False alarms: 31 | Commission: 0 | Wrong-content: 18 | Dependency violations: 0 | Overkill steps: 15 | state query calls: 169 | check_time calls: 80 | Actions: 63
Exact-set: matches 29 | mismatches 51 | reward -22
Set micro: TP 27 | FP 36 | FN 54
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 3 | late 2 | miss 4 | canceled 2 | total 11 | violations 15
Rates: hit 33.3% | late 6.2% | miss 60.5% | false alarm/step 38.8% | commission 0.0% | wrong-content 22.2% | dependency/step 0.0% | overkill/step 18.8% | cross-day miss 100.0% | update miss 44.4% | precision_hit 42.9% | precision_any 50.8% | exact-set match rate 36.2% | exact-set avg reward -0.275 | set_precision 42.9% | set_recall 33.3% | set_f1 37.5%
Hit rates (by modality): event 17.5% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T21:45:16.440Z |
| Finished (UTC) | 2026-03-28T21:49:07.045Z |
| Duration | 3m 50.6s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 27 |
| Late | 5 |
| Miss | 49 |
| False alarms | 31 |
| Commission | 0 |
| Wrong-content | 18 |
| Dependency violations | 0 |
| Overkill steps | 15 |
| State query calls | 169 |
| Check_time calls | 80 |
| Actions | 63 |
| Exact-set matches | 29 |
| Exact-set mismatches | 51 |
| Exact-set reward | -22 |
| Set TP | 27 |
| Set FP | 36 |
| Set FN | 54 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 47 |
| calendar | 18 |
| clock | 80 |
| email | 1 |
| laundry_status | 9 |
| library_hold | 14 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 33.3% |
| Late rate | 6.2% |
| Miss rate | 60.5% |
| False alarm/step | 38.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 22.2% |
| Dependency/step | 0.0% |
| Overkill/step | 18.8% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 44.4% |
| Precision hit | 42.9% |
| Precision any | 50.8% |
| Exact-set match rate | 36.2% |
| Exact-set avg reward | -0.275 |
| Set precision | 42.9% |
| Set recall | 33.3% |
| Set F1 | 37.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 10 | 57 | 17.5% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 10 | 3 | 29 | 42 | 23.8% | 31.0% |
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
| Monday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 15.4% | 0.0% | 33.3% | 66.7% | 50.0% | 33.3% | 53.8% | 0.077 | 62.5% | 41.7% | 50.0% |
| Tuesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 46.2% | 23.1% | 14.3% | 75.0% | 25.0% | 42.9% | 38.5% | -0.231 | 36.4% | 36.4% | 36.4% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 20.0% | 20.0% | 22.2% | 100.0% | 33.3% | 40.0% | 40.0% | -0.200 | 66.7% | 36.4% | 47.1% |
| Thursday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 9.1% | 0.0% | 22.2% | 66.7% | 25.0% | 50.0% | 54.5% | 0.091 | 80.0% | 33.3% | 47.1% |
| Friday | 3 | 1 | 8 | 25.0% | 8.3% | 66.7% | 133.3% | 58.3% | 0.0% | 75.0% | 0.0% | 50.0% | 8.3% | -0.833 | 15.0% | 25.0% | 18.8% |
| Saturday | 3 | 1 | 10 | 21.4% | 7.1% | 71.4% | 0.0% | 0.0% | 10.0% | 50.0% | 12.5% | 33.3% | 30.0% | -0.400 | 75.0% | 21.4% | 33.3% |
| Sunday | 4 | 1 | 4 | 44.4% | 11.1% | 44.4% | 36.4% | 27.3% | 20.0% | 75.0% | 25.0% | 60.0% | 27.3% | -0.455 | 44.4% | 44.4% | 44.4% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 12 |
| Monday | clock | 13 |
| Monday | library_hold | 6 |
| Tuesday | appointment_portal | 13 |
| Tuesday | clock | 13 |
| Wednesday | appointment_portal | 10 |
| Wednesday | clock | 10 |
| Thursday | appointment_portal | 11 |
| Thursday | clock | 11 |
| Friday | appointment_portal | 1 |
| Friday | clock | 12 |
| Friday | email | 1 |
| Friday | laundry_status | 8 |
| Friday | library_hold | 7 |
| Saturday | calendar | 7 |
| Saturday | clock | 10 |
| Saturday | laundry_status | 1 |
| Saturday | library_hold | 1 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |

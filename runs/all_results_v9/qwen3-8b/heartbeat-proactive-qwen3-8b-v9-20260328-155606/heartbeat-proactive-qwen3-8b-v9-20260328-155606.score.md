# PM-Bench score report

## Summary

Hit: 64 | Late: 0 | Miss: 17 | False alarms: 33 | Commission: 0 | Wrong-content: 9 | Dependency violations: 0 | Overkill steps: 16 | state query calls: 0 | check_time calls: 0 | Actions: 97
Exact-set: matches 50 | mismatches 30 | reward 20
Set micro: TP 64 | FP 33 | FN 17
Cross-day: hit 5 | late 0 | miss 2 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 6
Rates: hit 79.0% | late 0.0% | miss 21.0% | false alarm/step 41.2% | commission 0.0% | wrong-content 11.1% | dependency/step 0.0% | overkill/step 20.0% | cross-day miss 28.6% | update miss 44.4% | precision_hit 66.0% | precision_any 66.0% | exact-set match rate 62.5% | exact-set avg reward 0.250 | set_precision 66.0% | set_recall 79.0% | set_f1 71.9%
Hit rates (by modality): event 84.2% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:56:06.326Z |
| Finished (UTC) | 2026-03-28T23:03:18.053Z |
| Duration | 7m 11.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 64 |
| Late | 0 |
| Miss | 17 |
| False alarms | 33 |
| Commission | 0 |
| Wrong-content | 9 |
| Dependency violations | 0 |
| Overkill steps | 16 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 97 |
| Exact-set matches | 50 |
| Exact-set mismatches | 30 |
| Exact-set reward | 20 |
| Set TP | 64 |
| Set FP | 33 |
| Set FN | 17 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 79.0% |
| Late rate | 0.0% |
| Miss rate | 21.0% |
| False alarm/step | 41.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 11.1% |
| Dependency/step | 0.0% |
| Overkill/step | 20.0% |
| Cross-day miss rate | 28.6% |
| Update miss rate | 44.4% |
| Precision hit | 66.0% |
| Precision any | 66.0% |
| Exact-set match rate | 62.5% |
| Exact-set avg reward | 0.250 |
| Set precision | 66.0% |
| Set recall | 79.0% |
| Set F1 | 71.9% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 48 | 57 | 84.2% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
| proactive_monitoring_required | 26 | 0 | 13 | 39 | 66.7% | 66.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| bank_balance | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| calendar | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| clock | 16 | 0 | 8 | 24 | 66.7% | 66.7% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 1 | 0 | 1 | 2 | 50.0% | 50.0% |
| library_hold | 2 | 0 | 1 | 3 | 66.7% | 66.7% |
| shipment_status | 1 | 0 | 0 | 1 | 100.0% | 100.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 12 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Tuesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Wednesday | 11 | 0 | 0 | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 1.000 | 100.0% | 100.0% | 100.0% |
| Thursday | 11 | 0 | 1 | 91.7% | 0.0% | 8.3% | 90.9% | 36.4% | 100.0% | 66.7% | 100.0% | 75.0% | 54.5% | 0.091 | 52.4% | 91.7% | 66.7% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 75.0% | 41.7% | 62.5% | 25.0% | 83.3% | 16.7% | 16.7% | -0.667 | 40.0% | 50.0% | 44.4% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 60.0% | 30.0% | 50.0% | 75.0% | 62.5% | 50.0% | 30.0% | -0.400 | 57.1% | 57.1% | 57.1% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 72.7% | 36.4% | 80.0% | 25.0% | 100.0% | 20.0% | 27.3% | -0.455 | 38.5% | 55.6% | 45.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | (none) | 0 |
| Tuesday | (none) | 0 |
| Wednesday | (none) | 0 |
| Thursday | (none) | 0 |
| Friday | (none) | 0 |
| Saturday | (none) | 0 |
| Sunday | (none) | 0 |

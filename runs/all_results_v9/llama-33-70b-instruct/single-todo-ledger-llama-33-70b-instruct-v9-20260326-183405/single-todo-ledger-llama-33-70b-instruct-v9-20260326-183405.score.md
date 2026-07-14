# PM-Bench score report

## Summary

Hit: 50 | Late: 0 | Miss: 31 | False alarms: 7 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 5 | state query calls: 0 | check_time calls: 0 | Actions: 57
Exact-set: matches 50 | mismatches 30 | reward 20
Set micro: TP 50 | FP 7 | FN 31
Cross-day: hit 6 | late 0 | miss 1 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 4
Rates: hit 61.7% | late 0.0% | miss 38.3% | false alarm/step 8.8% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 6.2% | cross-day miss 14.3% | update miss 44.4% | precision_hit 87.7% | precision_any 87.7% | exact-set match rate 62.5% | exact-set avg reward 0.250 | set_precision 87.7% | set_recall 61.7% | set_f1 72.5%
Hit rates (by modality): event 70.2% | time 41.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-26T22:34:05.307Z |
| Finished (UTC) | 2026-03-26T22:49:03.843Z |
| Duration | 14m 58.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 50 |
| Late | 0 |
| Miss | 31 |
| False alarms | 7 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 5 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 57 |
| Exact-set matches | 50 |
| Exact-set mismatches | 30 |
| Exact-set reward | 20 |
| Set TP | 50 |
| Set FP | 7 |
| Set FN | 31 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 61.7% |
| Late rate | 0.0% |
| Miss rate | 38.3% |
| False alarm/step | 8.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 6.2% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 44.4% |
| Precision hit | 87.7% |
| Precision any | 87.7% |
| Exact-set match rate | 62.5% |
| Exact-set avg reward | 0.250 |
| Set precision | 87.7% |
| Set recall | 61.7% |
| Set F1 | 72.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 40 | 57 | 70.2% |
| Time (time + time_check) | 10 | 24 | 41.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 40 | 0 | 2 | 42 | 95.2% | 95.2% |
| proactive_monitoring_required | 10 | 0 | 29 | 39 | 25.6% | 25.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 10 | 0 | 14 | 24 | 41.7% | 41.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 15.4% | 7.7% | 66.7% | 33.3% | 100.0% | 16.7% | 61.5% | 0.231 | 77.8% | 58.3% | 66.7% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 66.7% | 50.0% | 100.0% | 20.0% | 70.0% | 0.400 | 100.0% | 63.6% | 77.8% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 9.1% | 9.1% | 88.9% | 33.3% | 100.0% | 25.0% | 72.7% | 0.455 | 90.0% | 75.0% | 81.8% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 33.3% | 25.0% | 62.5% | 25.0% | 83.3% | 16.7% | 33.3% | -0.333 | 60.0% | 50.0% | 54.5% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 0.0% | 0.0% | 70.0% | 25.0% | 87.5% | 16.7% | 60.0% | 0.200 | 100.0% | 57.1% | 72.7% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 80.0% | 50.0% | 100.0% | 40.0% | 72.7% | 0.455 | 100.0% | 66.7% | 80.0% |

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

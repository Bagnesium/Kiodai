# PM-Bench score report

## Summary

Hit: 34 | Late: 4 | Miss: 43 | False alarms: 43 | Commission: 0 | Wrong-content: 18 | Dependency violations: 0 | Overkill steps: 30 | state query calls: 0 | check_time calls: 0 | Actions: 81
Exact-set: matches 15 | mismatches 65 | reward -50
Set micro: TP 34 | FP 47 | FN 47
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 1 | late 1 | miss 7 | canceled 2 | total 11 | violations 13
Rates: hit 42.0% | late 4.9% | miss 53.1% | false alarm/step 53.8% | commission 0.0% | wrong-content 22.2% | dependency/step 0.0% | overkill/step 37.5% | cross-day miss 100.0% | update miss 77.8% | precision_hit 42.0% | precision_any 46.9% | exact-set match rate 18.8% | exact-set avg reward -0.625 | set_precision 42.0% | set_recall 42.0% | set_f1 42.0%
Hit rates (by modality): event 43.9% | time 37.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:53:32.456Z |
| Finished (UTC) | 2026-03-28T22:53:56.093Z |
| Duration | 23.637s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 34 |
| Late | 4 |
| Miss | 43 |
| False alarms | 43 |
| Commission | 0 |
| Wrong-content | 18 |
| Dependency violations | 0 |
| Overkill steps | 30 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 81 |
| Exact-set matches | 15 |
| Exact-set mismatches | 65 |
| Exact-set reward | -50 |
| Set TP | 34 |
| Set FP | 47 |
| Set FN | 47 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 42.0% |
| Late rate | 4.9% |
| Miss rate | 53.1% |
| False alarm/step | 53.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 22.2% |
| Dependency/step | 0.0% |
| Overkill/step | 37.5% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 77.8% |
| Precision hit | 42.0% |
| Precision any | 46.9% |
| Exact-set match rate | 18.8% |
| Exact-set avg reward | -0.625 |
| Set precision | 42.0% |
| Set recall | 42.0% |
| Set F1 | 42.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 25 | 57 | 43.9% |
| Time (time + time_check) | 9 | 24 | 37.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 2 | 17 | 42 | 54.8% | 59.5% |
| proactive_monitoring_required | 11 | 2 | 26 | 39 | 28.2% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 9 | 2 | 13 | 24 | 37.5% | 45.8% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 61.5% | 38.5% | 55.6% | 33.3% | 66.7% | 33.3% | 23.1% | -0.538 | 42.9% | 50.0% | 46.2% |
| Tuesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 61.5% | 46.2% | 42.9% | 50.0% | 75.0% | 28.6% | 15.4% | -0.692 | 38.5% | 45.5% | 41.7% |
| Wednesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 50.0% | 40.0% | 33.3% | 100.0% | 33.3% | 60.0% | 30.0% | -0.400 | 50.0% | 45.5% | 47.6% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 45.5% | 36.4% | 55.6% | 33.3% | 62.5% | 25.0% | 27.3% | -0.455 | 54.5% | 50.0% | 52.2% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 58.3% | 41.7% | 37.5% | 50.0% | 50.0% | 33.3% | 8.3% | -0.833 | 41.7% | 41.7% | 41.7% |
| Saturday | 4 | 3 | 7 | 28.6% | 21.4% | 50.0% | 30.0% | 20.0% | 30.0% | 25.0% | 37.5% | 16.7% | 10.0% | -0.800 | 40.0% | 28.6% | 33.3% |
| Sunday | 3 | 1 | 5 | 33.3% | 11.1% | 55.6% | 63.6% | 36.4% | 60.0% | 0.0% | 75.0% | 0.0% | 18.2% | -0.636 | 27.3% | 33.3% | 30.0% |

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

# PM-Bench score report

## Summary

Hit: 40 | Late: 3 | Miss: 38 | False alarms: 41 | Commission: 0 | Wrong-content: 13 | Dependency violations: 0 | Overkill steps: 30 | state query calls: 0 | check_time calls: 0 | Actions: 84
Exact-set: matches 20 | mismatches 60 | reward -40
Set micro: TP 40 | FP 44 | FN 41
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 15
Rates: hit 49.4% | late 3.7% | miss 46.9% | false alarm/step 51.2% | commission 0.0% | wrong-content 16.0% | dependency/step 0.0% | overkill/step 37.5% | cross-day miss 100.0% | update miss 88.9% | precision_hit 47.6% | precision_any 51.2% | exact-set match rate 25.0% | exact-set avg reward -0.500 | set_precision 47.6% | set_recall 49.4% | set_f1 48.5%
Hit rates (by modality): event 56.1% | time 33.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T21:13:03.504Z |
| Finished (UTC) | 2026-03-28T21:14:00.674Z |
| Duration | 57.170s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 40 |
| Late | 3 |
| Miss | 38 |
| False alarms | 41 |
| Commission | 0 |
| Wrong-content | 13 |
| Dependency violations | 0 |
| Overkill steps | 30 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 84 |
| Exact-set matches | 20 |
| Exact-set mismatches | 60 |
| Exact-set reward | -40 |
| Set TP | 40 |
| Set FP | 44 |
| Set FN | 41 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 49.4% |
| Late rate | 3.7% |
| Miss rate | 46.9% |
| False alarm/step | 51.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 16.0% |
| Dependency/step | 0.0% |
| Overkill/step | 37.5% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 88.9% |
| Precision hit | 47.6% |
| Precision any | 51.2% |
| Exact-set match rate | 25.0% |
| Exact-set avg reward | -0.500 |
| Set precision | 47.6% |
| Set recall | 49.4% |
| Set F1 | 48.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 32 | 57 | 56.1% |
| Time (time + time_check) | 8 | 24 | 33.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 32 | 0 | 10 | 42 | 76.2% | 76.2% |
| proactive_monitoring_required | 8 | 3 | 28 | 39 | 20.5% | 28.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 8 | 2 | 14 | 24 | 33.3% | 41.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 53.8% | 30.8% | 44.4% | 33.3% | 66.7% | 16.7% | 30.8% | -0.385 | 38.5% | 41.7% | 40.0% |
| Tuesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 61.5% | 46.2% | 57.1% | 50.0% | 100.0% | 28.6% | 23.1% | -0.538 | 40.0% | 54.5% | 46.2% |
| Wednesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 50.0% | 40.0% | 44.4% | 50.0% | 66.7% | 20.0% | 20.0% | -0.600 | 50.0% | 45.5% | 47.6% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 36.4% | 36.4% | 66.7% | 33.3% | 75.0% | 25.0% | 36.4% | -0.273 | 63.6% | 58.3% | 60.9% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 58.3% | 41.7% | 50.0% | 50.0% | 66.7% | 33.3% | 16.7% | -0.667 | 46.2% | 50.0% | 48.0% |
| Saturday | 6 | 1 | 7 | 42.9% | 7.1% | 50.0% | 40.0% | 30.0% | 60.0% | 0.0% | 75.0% | 0.0% | 20.0% | -0.600 | 54.5% | 42.9% | 48.0% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 54.5% | 36.4% | 80.0% | 25.0% | 100.0% | 20.0% | 27.3% | -0.455 | 45.5% | 55.6% | 50.0% |

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

# PM-Bench score report

## Summary

Hit: 38 | Late: 2 | Miss: 41 | False alarms: 58 | Commission: 0 | Wrong-content: 27 | Dependency violations: 0 | Overkill steps: 38 | state query calls: 0 | check_time calls: 0 | Actions: 98
Exact-set: matches 12 | mismatches 68 | reward -56
Set micro: TP 38 | FP 60 | FN 43
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 1 | late 1 | miss 7 | canceled 2 | total 11 | violations 14
Rates: hit 46.9% | late 2.5% | miss 50.6% | false alarm/step 72.5% | commission 0.0% | wrong-content 33.3% | dependency/step 0.0% | overkill/step 47.5% | cross-day miss 71.4% | update miss 77.8% | precision_hit 38.8% | precision_any 40.8% | exact-set match rate 15.0% | exact-set avg reward -0.700 | set_precision 38.8% | set_recall 46.9% | set_f1 42.5%
Hit rates (by modality): event 50.9% | time 37.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T23:07:00.231Z |
| Finished (UTC) | 2026-03-28T23:07:24.895Z |
| Duration | 24.665s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 38 |
| Late | 2 |
| Miss | 41 |
| False alarms | 58 |
| Commission | 0 |
| Wrong-content | 27 |
| Dependency violations | 0 |
| Overkill steps | 38 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 98 |
| Exact-set matches | 12 |
| Exact-set mismatches | 68 |
| Exact-set reward | -56 |
| Set TP | 38 |
| Set FP | 60 |
| Set FN | 43 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 46.9% |
| Late rate | 2.5% |
| Miss rate | 50.6% |
| False alarm/step | 72.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 33.3% |
| Dependency/step | 0.0% |
| Overkill/step | 47.5% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 77.8% |
| Precision hit | 38.8% |
| Precision any | 40.8% |
| Exact-set match rate | 15.0% |
| Exact-set avg reward | -0.700 |
| Set precision | 38.8% |
| Set recall | 46.9% |
| Set F1 | 42.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 29 | 57 | 50.9% |
| Time (time + time_check) | 9 | 24 | 37.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 27 | 1 | 14 | 42 | 64.3% | 66.7% |
| proactive_monitoring_required | 11 | 1 | 27 | 39 | 28.2% | 30.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 9 | 1 | 14 | 24 | 37.5% | 41.7% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 69.2% | 46.2% | 55.6% | 33.3% | 66.7% | 33.3% | 15.4% | -0.692 | 40.0% | 50.0% | 44.4% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 69.2% | 61.5% | 57.1% | 50.0% | 100.0% | 28.6% | 7.7% | -0.846 | 40.0% | 54.5% | 46.2% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 80.0% | 50.0% | 33.3% | 50.0% | 33.3% | 40.0% | 10.0% | -0.800 | 33.3% | 36.4% | 34.8% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 63.6% | 45.5% | 66.7% | 33.3% | 75.0% | 25.0% | 27.3% | -0.455 | 50.0% | 58.3% | 53.8% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 83.3% | 41.7% | 50.0% | 25.0% | 66.7% | 16.7% | 16.7% | -0.667 | 33.3% | 41.7% | 37.0% |
| Saturday | 5 | 2 | 7 | 35.7% | 14.3% | 50.0% | 50.0% | 30.0% | 30.0% | 50.0% | 37.5% | 33.3% | 10.0% | -0.800 | 41.7% | 35.7% | 38.5% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 90.9% | 54.5% | 80.0% | 25.0% | 100.0% | 20.0% | 18.2% | -0.636 | 33.3% | 55.6% | 41.7% |

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

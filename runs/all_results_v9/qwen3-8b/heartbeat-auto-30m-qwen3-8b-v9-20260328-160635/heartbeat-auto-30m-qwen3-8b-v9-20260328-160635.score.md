# PM-Bench score report

## Summary

Hit: 33 | Late: 4 | Miss: 44 | False alarms: 48 | Commission: 0 | Wrong-content: 23 | Dependency violations: 0 | Overkill steps: 32 | state query calls: 0 | check_time calls: 0 | Actions: 85
Exact-set: matches 12 | mismatches 68 | reward -56
Set micro: TP 33 | FP 52 | FN 48
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 2 | late 0 | miss 7 | canceled 2 | total 11 | violations 14
Rates: hit 40.7% | late 4.9% | miss 54.3% | false alarm/step 60.0% | commission 0.0% | wrong-content 28.4% | dependency/step 0.0% | overkill/step 40.0% | cross-day miss 85.7% | update miss 77.8% | precision_hit 38.8% | precision_any 43.5% | exact-set match rate 15.0% | exact-set avg reward -0.700 | set_precision 38.8% | set_recall 40.7% | set_f1 39.8%
Hit rates (by modality): event 43.9% | time 33.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T23:06:35.973Z |
| Finished (UTC) | 2026-03-28T23:07:00.017Z |
| Duration | 24.044s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 33 |
| Late | 4 |
| Miss | 44 |
| False alarms | 48 |
| Commission | 0 |
| Wrong-content | 23 |
| Dependency violations | 0 |
| Overkill steps | 32 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 85 |
| Exact-set matches | 12 |
| Exact-set mismatches | 68 |
| Exact-set reward | -56 |
| Set TP | 33 |
| Set FP | 52 |
| Set FN | 48 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 40.7% |
| Late rate | 4.9% |
| Miss rate | 54.3% |
| False alarm/step | 60.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 28.4% |
| Dependency/step | 0.0% |
| Overkill/step | 40.0% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 77.8% |
| Precision hit | 38.8% |
| Precision any | 43.5% |
| Exact-set match rate | 15.0% |
| Exact-set avg reward | -0.700 |
| Set precision | 38.8% |
| Set recall | 40.7% |
| Set F1 | 39.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 25 | 57 | 43.9% |
| Time (time + time_check) | 8 | 24 | 33.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 2 | 17 | 42 | 54.8% | 59.5% |
| proactive_monitoring_required | 10 | 2 | 27 | 39 | 25.6% | 30.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 8 | 2 | 14 | 24 | 33.3% | 41.7% |
| course_portal | 1 | 0 | 0 | 1 | 100.0% | 100.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 69.2% | 38.5% | 55.6% | 0.0% | 66.7% | 16.7% | 15.4% | -0.692 | 35.7% | 41.7% | 38.5% |
| Tuesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 69.2% | 53.8% | 42.9% | 50.0% | 75.0% | 28.6% | 7.7% | -0.846 | 35.7% | 45.5% | 40.0% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 60.0% | 40.0% | 33.3% | 50.0% | 33.3% | 40.0% | 20.0% | -0.600 | 40.0% | 36.4% | 38.1% |
| Thursday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 54.5% | 45.5% | 44.4% | 33.3% | 50.0% | 25.0% | 18.2% | -0.636 | 41.7% | 41.7% | 41.7% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 66.7% | 41.7% | 37.5% | 50.0% | 50.0% | 33.3% | 8.3% | -0.833 | 38.5% | 41.7% | 40.0% |
| Saturday | 4 | 3 | 7 | 28.6% | 21.4% | 50.0% | 30.0% | 20.0% | 30.0% | 25.0% | 37.5% | 16.7% | 10.0% | -0.800 | 40.0% | 28.6% | 33.3% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 63.6% | 36.4% | 80.0% | 25.0% | 100.0% | 20.0% | 27.3% | -0.455 | 41.7% | 55.6% | 47.6% |

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

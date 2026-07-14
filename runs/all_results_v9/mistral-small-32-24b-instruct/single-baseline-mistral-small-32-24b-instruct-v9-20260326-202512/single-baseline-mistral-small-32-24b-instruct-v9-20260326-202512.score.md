# PM-Bench score report

## Summary

Hit: 36 | Late: 3 | Miss: 42 | False alarms: 17 | Commission: 0 | Wrong-content: 5 | Dependency violations: 0 | Overkill steps: 13 | state query calls: 0 | check_time calls: 0 | Actions: 56
Exact-set: matches 35 | mismatches 45 | reward -10
Set micro: TP 36 | FP 20 | FN 45
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 1 | late 1 | miss 7 | canceled 2 | total 11 | violations 6
Rates: hit 44.4% | late 3.7% | miss 51.9% | false alarm/step 21.2% | commission 0.0% | wrong-content 6.2% | dependency/step 0.0% | overkill/step 16.2% | cross-day miss 85.7% | update miss 77.8% | precision_hit 64.3% | precision_any 69.6% | exact-set match rate 43.8% | exact-set avg reward -0.125 | set_precision 64.3% | set_recall 44.4% | set_f1 52.6%
Hit rates (by modality): event 49.1% | time 33.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:25:12.771Z |
| Finished (UTC) | 2026-03-27T03:26:55.240Z |
| Duration | 1m 42.5s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 36 |
| Late | 3 |
| Miss | 42 |
| False alarms | 17 |
| Commission | 0 |
| Wrong-content | 5 |
| Dependency violations | 0 |
| Overkill steps | 13 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 56 |
| Exact-set matches | 35 |
| Exact-set mismatches | 45 |
| Exact-set reward | -10 |
| Set TP | 36 |
| Set FP | 20 |
| Set FN | 45 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 44.4% |
| Late rate | 3.7% |
| Miss rate | 51.9% |
| False alarm/step | 21.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 6.2% |
| Dependency/step | 0.0% |
| Overkill/step | 16.2% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 77.8% |
| Precision hit | 64.3% |
| Precision any | 69.6% |
| Exact-set match rate | 43.8% |
| Exact-set avg reward | -0.125 |
| Set precision | 64.3% |
| Set recall | 44.4% |
| Set F1 | 52.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 28 | 57 | 49.1% |
| Time (time + time_check) | 8 | 24 | 33.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 27 | 2 | 13 | 42 | 64.3% | 69.0% |
| proactive_monitoring_required | 9 | 1 | 29 | 39 | 23.1% | 25.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 8 | 1 | 15 | 24 | 33.3% | 37.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 38.5% | 15.4% | 55.6% | 66.7% | 66.7% | 50.0% | 46.2% | -0.077 | 58.3% | 58.3% | 58.3% |
| Tuesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 15.4% | 15.4% | 57.1% | 50.0% | 100.0% | 28.6% | 53.8% | 0.077 | 66.7% | 54.5% | 60.0% |
| Wednesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 10.0% | 20.0% | 33.3% | 50.0% | 50.0% | 20.0% | 40.0% | -0.200 | 66.7% | 36.4% | 47.1% |
| Thursday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 27.3% | 27.3% | 33.3% | 33.3% | 37.5% | 25.0% | 36.4% | -0.273 | 57.1% | 33.3% | 42.1% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 25.0% | 16.7% | 62.5% | 25.0% | 83.3% | 16.7% | 41.7% | -0.167 | 66.7% | 50.0% | 57.1% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 10.0% | 10.0% | 50.0% | 25.0% | 62.5% | 16.7% | 40.0% | -0.200 | 85.7% | 42.9% | 57.1% |
| Sunday | 3 | 1 | 5 | 33.3% | 11.1% | 55.6% | 18.2% | 9.1% | 60.0% | 0.0% | 75.0% | 0.0% | 45.5% | -0.091 | 50.0% | 33.3% | 40.0% |

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

# PM-Bench score report

## Summary

Hit: 44 | Late: 0 | Miss: 37 | False alarms: 20 | Commission: 0 | Wrong-content: 3 | Dependency violations: 0 | Overkill steps: 17 | state query calls: 16 | check_time calls: 16 | Actions: 64
Exact-set: matches 35 | mismatches 45 | reward -10
Set micro: TP 44 | FP 20 | FN 37
Cross-day: hit 2 | late 0 | miss 5 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 8
Rates: hit 54.3% | late 0.0% | miss 45.7% | false alarm/step 25.0% | commission 0.0% | wrong-content 3.7% | dependency/step 0.0% | overkill/step 21.2% | cross-day miss 71.4% | update miss 66.7% | precision_hit 68.8% | precision_any 68.8% | exact-set match rate 43.8% | exact-set avg reward -0.125 | set_precision 68.8% | set_recall 54.3% | set_f1 60.7%
Hit rates (by modality): event 54.4% | time 54.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T02:00:40.816Z |
| Finished (UTC) | 2026-03-27T02:04:21.997Z |
| Duration | 3m 41.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 44 |
| Late | 0 |
| Miss | 37 |
| False alarms | 20 |
| Commission | 0 |
| Wrong-content | 3 |
| Dependency violations | 0 |
| Overkill steps | 17 |
| State query calls | 16 |
| Check_time calls | 16 |
| Actions | 64 |
| Exact-set matches | 35 |
| Exact-set mismatches | 45 |
| Exact-set reward | -10 |
| Set TP | 44 |
| Set FP | 20 |
| Set FN | 37 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 16 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 54.3% |
| Late rate | 0.0% |
| Miss rate | 45.7% |
| False alarm/step | 25.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 3.7% |
| Dependency/step | 0.0% |
| Overkill/step | 21.2% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 66.7% |
| Precision hit | 68.8% |
| Precision any | 68.8% |
| Exact-set match rate | 43.8% |
| Exact-set avg reward | -0.125 |
| Set precision | 68.8% |
| Set recall | 54.3% |
| Set F1 | 60.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 31 | 57 | 54.4% |
| Time (time + time_check) | 13 | 24 | 54.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 31 | 0 | 11 | 42 | 73.8% | 73.8% |
| proactive_monitoring_required | 13 | 0 | 26 | 39 | 33.3% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 13 | 0 | 11 | 24 | 54.2% | 54.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 23.1% | 15.4% | 44.4% | 66.7% | 66.7% | 33.3% | 46.2% | -0.077 | 66.7% | 50.0% | 57.1% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 23.1% | 23.1% | 42.9% | 75.0% | 75.0% | 42.9% | 38.5% | -0.231 | 66.7% | 54.5% | 60.0% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 30.0% | 20.0% | 33.3% | 50.0% | 50.0% | 20.0% | 40.0% | -0.200 | 57.1% | 36.4% | 44.4% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 18.2% | 18.2% | 77.8% | 33.3% | 87.5% | 25.0% | 63.6% | 0.273 | 80.0% | 66.7% | 72.7% |
| Friday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 33.3% | 33.3% | 50.0% | 75.0% | 66.7% | 50.0% | 33.3% | -0.333 | 63.6% | 58.3% | 60.9% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 30.0% | 20.0% | 70.0% | 25.0% | 87.5% | 16.7% | 40.0% | -0.200 | 72.7% | 57.1% | 64.0% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 18.2% | 18.2% | 60.0% | 50.0% | 75.0% | 40.0% | 45.5% | -0.091 | 71.4% | 55.6% | 62.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 4 |
| Tuesday | clock | 4 |
| Wednesday | clock | 2 |
| Thursday | clock | 2 |
| Friday | clock | 2 |
| Saturday | (none) | 0 |
| Sunday | clock | 2 |

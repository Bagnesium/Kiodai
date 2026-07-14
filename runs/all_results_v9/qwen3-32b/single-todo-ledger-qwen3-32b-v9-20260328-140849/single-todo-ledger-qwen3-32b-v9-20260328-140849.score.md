# PM-Bench score report

## Summary

Hit: 37 | Late: 6 | Miss: 38 | False alarms: 19 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 19 | state query calls: 8 | check_time calls: 8 | Actions: 62
Exact-set: matches 29 | mismatches 51 | reward -22
Set micro: TP 37 | FP 25 | FN 44
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 12
Rates: hit 45.7% | late 7.4% | miss 46.9% | false alarm/step 23.8% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 23.8% | cross-day miss 100.0% | update miss 66.7% | precision_hit 59.7% | precision_any 69.4% | exact-set match rate 36.2% | exact-set avg reward -0.275 | set_precision 59.7% | set_recall 45.7% | set_f1 51.7%
Hit rates (by modality): event 52.6% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T21:08:49.374Z |
| Finished (UTC) | 2026-03-28T21:13:03.303Z |
| Duration | 4m 13.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 37 |
| Late | 6 |
| Miss | 38 |
| False alarms | 19 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 19 |
| State query calls | 8 |
| Check_time calls | 8 |
| Actions | 62 |
| Exact-set matches | 29 |
| Exact-set mismatches | 51 |
| Exact-set reward | -22 |
| Set TP | 37 |
| Set FP | 25 |
| Set FN | 44 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 8 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 45.7% |
| Late rate | 7.4% |
| Miss rate | 46.9% |
| False alarm/step | 23.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 23.8% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 66.7% |
| Precision hit | 59.7% |
| Precision any | 69.4% |
| Exact-set match rate | 36.2% |
| Exact-set avg reward | -0.275 |
| Set precision | 59.7% |
| Set recall | 45.7% |
| Set F1 | 51.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 30 | 57 | 52.6% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 30 | 2 | 10 | 42 | 71.4% | 76.2% |
| proactive_monitoring_required | 7 | 4 | 28 | 39 | 17.9% | 28.2% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 7 | 3 | 14 | 24 | 29.2% | 41.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 30.8% | 23.1% | 55.6% | 66.7% | 83.3% | 33.3% | 53.8% | 0.077 | 63.6% | 58.3% | 60.9% |
| Tuesday | 5 | 2 | 4 | 45.5% | 18.2% | 36.4% | 23.1% | 30.8% | 57.1% | 25.0% | 100.0% | 14.3% | 30.8% | -0.385 | 50.0% | 45.5% | 47.6% |
| Wednesday | 4 | 2 | 5 | 36.4% | 18.2% | 45.5% | 10.0% | 20.0% | 33.3% | 50.0% | 50.0% | 20.0% | 40.0% | -0.200 | 57.1% | 36.4% | 44.4% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 9.1% | 9.1% | 66.7% | 0.0% | 75.0% | 0.0% | 54.5% | 0.091 | 85.7% | 50.0% | 63.2% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 41.7% | 33.3% | 50.0% | 50.0% | 66.7% | 33.3% | 25.0% | -0.500 | 54.5% | 50.0% | 52.2% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 30.0% | 20.0% | 50.0% | 25.0% | 62.5% | 16.7% | 20.0% | -0.600 | 66.7% | 42.9% | 52.2% |
| Sunday | 3 | 2 | 4 | 33.3% | 22.2% | 44.4% | 18.2% | 27.3% | 60.0% | 0.0% | 75.0% | 0.0% | 27.3% | -0.455 | 42.9% | 33.3% | 37.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 1 |
| Wednesday | clock | 1 |
| Thursday | clock | 1 |
| Friday | clock | 2 |
| Saturday | clock | 1 |
| Sunday | clock | 1 |

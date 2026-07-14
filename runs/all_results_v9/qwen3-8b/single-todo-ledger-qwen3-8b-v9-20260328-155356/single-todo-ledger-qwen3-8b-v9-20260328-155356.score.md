# PM-Bench score report

## Summary

Hit: 32 | Late: 6 | Miss: 43 | False alarms: 15 | Commission: 0 | Wrong-content: 7 | Dependency violations: 0 | Overkill steps: 14 | state query calls: 8 | check_time calls: 8 | Actions: 53
Exact-set: matches 33 | mismatches 47 | reward -14
Set micro: TP 32 | FP 21 | FN 49
Cross-day: hit 1 | late 1 | miss 5 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 7
Rates: hit 39.5% | late 7.4% | miss 53.1% | false alarm/step 18.8% | commission 0.0% | wrong-content 8.6% | dependency/step 0.0% | overkill/step 17.5% | cross-day miss 71.4% | update miss 88.9% | precision_hit 60.4% | precision_any 71.7% | exact-set match rate 41.2% | exact-set avg reward -0.175 | set_precision 60.4% | set_recall 39.5% | set_f1 47.8%
Hit rates (by modality): event 42.1% | time 33.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:53:56.273Z |
| Finished (UTC) | 2026-03-28T22:56:06.142Z |
| Duration | 2m 9.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 32 |
| Late | 6 |
| Miss | 43 |
| False alarms | 15 |
| Commission | 0 |
| Wrong-content | 7 |
| Dependency violations | 0 |
| Overkill steps | 14 |
| State query calls | 8 |
| Check_time calls | 8 |
| Actions | 53 |
| Exact-set matches | 33 |
| Exact-set mismatches | 47 |
| Exact-set reward | -14 |
| Set TP | 32 |
| Set FP | 21 |
| Set FN | 49 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 8 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 39.5% |
| Late rate | 7.4% |
| Miss rate | 53.1% |
| False alarm/step | 18.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.6% |
| Dependency/step | 0.0% |
| Overkill/step | 17.5% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 88.9% |
| Precision hit | 60.4% |
| Precision any | 71.7% |
| Exact-set match rate | 41.2% |
| Exact-set avg reward | -0.175 |
| Set precision | 60.4% |
| Set recall | 39.5% |
| Set F1 | 47.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 24 | 57 | 42.1% |
| Time (time + time_check) | 8 | 24 | 33.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 2 | 17 | 42 | 54.8% | 59.5% |
| proactive_monitoring_required | 9 | 4 | 26 | 39 | 23.1% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 1 | 0 | 2 | 3 | 33.3% | 33.3% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 8 | 4 | 12 | 24 | 33.3% | 50.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 23.1% | 7.7% | 44.4% | 66.7% | 50.0% | 50.0% | 53.8% | 0.077 | 66.7% | 50.0% | 57.1% |
| Tuesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 23.1% | 23.1% | 42.9% | 25.0% | 75.0% | 14.3% | 38.5% | -0.231 | 50.0% | 36.4% | 42.1% |
| Wednesday | 3 | 2 | 6 | 27.3% | 18.2% | 54.5% | 0.0% | 10.0% | 22.2% | 50.0% | 33.3% | 20.0% | 50.0% | 0.000 | 60.0% | 27.3% | 37.5% |
| Thursday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 18.2% | 18.2% | 44.4% | 33.3% | 50.0% | 25.0% | 45.5% | -0.091 | 71.4% | 41.7% | 52.6% |
| Friday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 41.7% | 33.3% | 37.5% | 50.0% | 50.0% | 33.3% | 25.0% | -0.500 | 50.0% | 41.7% | 45.5% |
| Saturday | 4 | 2 | 8 | 28.6% | 14.3% | 57.1% | 10.0% | 10.0% | 40.0% | 0.0% | 50.0% | 0.0% | 30.0% | -0.400 | 57.1% | 28.6% | 38.1% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 9.1% | 18.2% | 80.0% | 25.0% | 100.0% | 20.0% | 45.5% | -0.091 | 71.4% | 55.6% | 62.5% |

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

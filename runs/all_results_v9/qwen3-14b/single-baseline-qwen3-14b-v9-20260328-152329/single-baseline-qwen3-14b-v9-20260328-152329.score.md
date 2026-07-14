# PM-Bench score report

## Summary

Hit: 39 | Late: 3 | Miss: 39 | False alarms: 58 | Commission: 0 | Wrong-content: 29 | Dependency violations: 0 | Overkill steps: 36 | state query calls: 0 | check_time calls: 0 | Actions: 100
Exact-set: matches 13 | mismatches 67 | reward -54
Set micro: TP 39 | FP 61 | FN 42
Cross-day: hit 1 | late 1 | miss 5 | total 7
Updates: hit 2 | late 0 | miss 7 | canceled 2 | total 11 | violations 18
Rates: hit 48.1% | late 3.7% | miss 48.1% | false alarm/step 72.5% | commission 0.0% | wrong-content 35.8% | dependency/step 0.0% | overkill/step 45.0% | cross-day miss 71.4% | update miss 77.8% | precision_hit 39.0% | precision_any 42.0% | exact-set match rate 16.2% | exact-set avg reward -0.675 | set_precision 39.0% | set_recall 48.1% | set_f1 43.1%
Hit rates (by modality): event 56.1% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:23:29.598Z |
| Finished (UTC) | 2026-03-28T22:24:02.104Z |
| Duration | 32.506s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 39 |
| Late | 3 |
| Miss | 39 |
| False alarms | 58 |
| Commission | 0 |
| Wrong-content | 29 |
| Dependency violations | 0 |
| Overkill steps | 36 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 100 |
| Exact-set matches | 13 |
| Exact-set mismatches | 67 |
| Exact-set reward | -54 |
| Set TP | 39 |
| Set FP | 61 |
| Set FN | 42 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 48.1% |
| Late rate | 3.7% |
| Miss rate | 48.1% |
| False alarm/step | 72.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 35.8% |
| Dependency/step | 0.0% |
| Overkill/step | 45.0% |
| Cross-day miss rate | 71.4% |
| Update miss rate | 77.8% |
| Precision hit | 39.0% |
| Precision any | 42.0% |
| Exact-set match rate | 16.2% |
| Exact-set avg reward | -0.675 |
| Set precision | 39.0% |
| Set recall | 48.1% |
| Set F1 | 43.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 32 | 57 | 56.1% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 32 | 1 | 9 | 42 | 76.2% | 78.6% |
| proactive_monitoring_required | 7 | 2 | 30 | 39 | 17.9% | 23.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 7 | 0 | 17 | 24 | 29.2% | 29.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 2 | 0 | 2 | 0.0% | 100.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 92.3% | 46.2% | 44.4% | 33.3% | 66.7% | 16.7% | 23.1% | -0.538 | 29.4% | 41.7% | 34.5% |
| Tuesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 61.5% | 53.8% | 57.1% | 25.0% | 100.0% | 14.3% | 7.7% | -0.846 | 35.7% | 45.5% | 40.0% |
| Wednesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 70.0% | 50.0% | 44.4% | 50.0% | 66.7% | 20.0% | 10.0% | -0.800 | 38.5% | 45.5% | 41.7% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 54.5% | 45.5% | 66.7% | 33.3% | 75.0% | 25.0% | 27.3% | -0.455 | 53.8% | 58.3% | 56.0% |
| Friday | 6 | 1 | 5 | 50.0% | 8.3% | 41.7% | 75.0% | 41.7% | 62.5% | 25.0% | 83.3% | 16.7% | 16.7% | -0.667 | 37.5% | 50.0% | 42.9% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 70.0% | 30.0% | 50.0% | 25.0% | 62.5% | 16.7% | 10.0% | -0.800 | 46.2% | 42.9% | 44.4% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 81.8% | 45.5% | 80.0% | 25.0% | 100.0% | 20.0% | 18.2% | -0.636 | 35.7% | 55.6% | 43.5% |

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

# PM-Bench score report

## Summary

Hit: 46 | Late: 0 | Miss: 35 | False alarms: 18 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 16 | check_time calls: 16 | Actions: 64
Exact-set: matches 42 | mismatches 38 | reward 4
Set micro: TP 46 | FP 18 | FN 35
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 2 | late 0 | miss 7 | canceled 2 | total 11 | violations 9
Rates: hit 56.8% | late 0.0% | miss 43.2% | false alarm/step 22.5% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 85.7% | update miss 77.8% | precision_hit 71.9% | precision_any 71.9% | exact-set match rate 52.5% | exact-set avg reward 0.050 | set_precision 71.9% | set_recall 56.8% | set_f1 63.4%
Hit rates (by modality): event 56.1% | time 58.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T01:57:36.647Z |
| Finished (UTC) | 2026-03-27T02:00:40.638Z |
| Duration | 3m 4.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 46 |
| Late | 0 |
| Miss | 35 |
| False alarms | 18 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 16 |
| Check_time calls | 16 |
| Actions | 64 |
| Exact-set matches | 42 |
| Exact-set mismatches | 38 |
| Exact-set reward | 4 |
| Set TP | 46 |
| Set FP | 18 |
| Set FN | 35 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 16 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 56.8% |
| Late rate | 0.0% |
| Miss rate | 43.2% |
| False alarm/step | 22.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 77.8% |
| Precision hit | 71.9% |
| Precision any | 71.9% |
| Exact-set match rate | 52.5% |
| Exact-set avg reward | 0.050 |
| Set precision | 71.9% |
| Set recall | 56.8% |
| Set F1 | 63.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 32 | 57 | 56.1% |
| Time (time + time_check) | 14 | 24 | 58.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 32 | 0 | 10 | 42 | 76.2% | 76.2% |
| proactive_monitoring_required | 14 | 0 | 25 | 39 | 35.9% | 35.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 14 | 0 | 10 | 24 | 58.3% | 58.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 23.1% | 7.7% | 44.4% | 100.0% | 66.7% | 50.0% | 61.5% | 0.231 | 70.0% | 58.3% | 63.6% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 23.1% | 7.7% | 57.1% | 50.0% | 100.0% | 28.6% | 61.5% | 0.231 | 66.7% | 54.5% | 60.0% |
| Wednesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 10.0% | 10.0% | 44.4% | 100.0% | 66.7% | 40.0% | 60.0% | 0.200 | 85.7% | 54.5% | 66.7% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 9.1% | 9.1% | 77.8% | 33.3% | 87.5% | 25.0% | 72.7% | 0.455 | 88.9% | 66.7% | 76.2% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 41.7% | 41.7% | 50.0% | 50.0% | 66.7% | 33.3% | 16.7% | -0.667 | 54.5% | 50.0% | 52.2% |
| Saturday | 7 | 0 | 7 | 50.0% | 0.0% | 50.0% | 30.0% | 10.0% | 60.0% | 25.0% | 75.0% | 16.7% | 40.0% | -0.200 | 70.0% | 50.0% | 58.3% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 18.2% | 18.2% | 60.0% | 75.0% | 75.0% | 60.0% | 54.5% | 0.091 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 3 |
| Tuesday | clock | 4 |
| Wednesday | clock | 3 |
| Thursday | clock | 3 |
| Friday | clock | 2 |
| Saturday | clock | 1 |
| Sunday | (none) | 0 |

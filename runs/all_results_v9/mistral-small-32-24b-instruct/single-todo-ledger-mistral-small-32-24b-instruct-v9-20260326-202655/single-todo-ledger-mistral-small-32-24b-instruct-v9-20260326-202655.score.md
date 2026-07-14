# PM-Bench score report

## Summary

Hit: 46 | Late: 2 | Miss: 33 | False alarms: 16 | Commission: 0 | Wrong-content: 11 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 10 | check_time calls: 10 | Actions: 64
Exact-set: matches 40 | mismatches 40 | reward 0
Set micro: TP 46 | FP 18 | FN 35
Cross-day: hit 3 | late 1 | miss 3 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 4
Rates: hit 56.8% | late 2.5% | miss 40.7% | false alarm/step 20.0% | commission 0.0% | wrong-content 13.6% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 42.9% | update miss 55.6% | precision_hit 71.9% | precision_any 75.0% | exact-set match rate 50.0% | exact-set avg reward 0.000 | set_precision 71.9% | set_recall 56.8% | set_f1 63.4%
Hit rates (by modality): event 59.6% | time 50.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:26:55.464Z |
| Finished (UTC) | 2026-03-27T03:31:15.577Z |
| Duration | 4m 20.1s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 46 |
| Late | 2 |
| Miss | 33 |
| False alarms | 16 |
| Commission | 0 |
| Wrong-content | 11 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 10 |
| Check_time calls | 10 |
| Actions | 64 |
| Exact-set matches | 40 |
| Exact-set mismatches | 40 |
| Exact-set reward | 0 |
| Set TP | 46 |
| Set FP | 18 |
| Set FN | 35 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 10 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 56.8% |
| Late rate | 2.5% |
| Miss rate | 40.7% |
| False alarm/step | 20.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 13.6% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 42.9% |
| Update miss rate | 55.6% |
| Precision hit | 71.9% |
| Precision any | 75.0% |
| Exact-set match rate | 50.0% |
| Exact-set avg reward | 0.000 |
| Set precision | 71.9% |
| Set recall | 56.8% |
| Set F1 | 63.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 34 | 57 | 59.6% |
| Time (time + time_check) | 12 | 24 | 50.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 34 | 1 | 7 | 42 | 81.0% | 83.3% |
| proactive_monitoring_required | 12 | 1 | 26 | 39 | 30.8% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 12 | 0 | 12 | 24 | 50.0% | 50.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 23.1% | 7.7% | 55.6% | 66.7% | 83.3% | 33.3% | 61.5% | 0.231 | 70.0% | 58.3% | 63.6% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 15.4% | 15.4% | 57.1% | 75.0% | 100.0% | 42.9% | 53.8% | 0.077 | 77.8% | 63.6% | 70.0% |
| Wednesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 10.0% | 20.0% | 44.4% | 50.0% | 66.7% | 20.0% | 40.0% | -0.200 | 71.4% | 45.5% | 55.6% |
| Thursday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 27.3% | 18.2% | 66.7% | 33.3% | 75.0% | 25.0% | 45.5% | -0.091 | 70.0% | 58.3% | 63.6% |
| Friday | 7 | 1 | 4 | 58.3% | 8.3% | 33.3% | 25.0% | 16.7% | 62.5% | 50.0% | 83.3% | 33.3% | 50.0% | 0.000 | 63.6% | 58.3% | 60.9% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 20.0% | 10.0% | 60.0% | 50.0% | 75.0% | 33.3% | 50.0% | 0.000 | 80.0% | 57.1% | 66.7% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 18.2% | 18.2% | 80.0% | 25.0% | 100.0% | 20.0% | 45.5% | -0.091 | 71.4% | 55.6% | 62.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 2 |
| Wednesday | (none) | 0 |
| Thursday | clock | 2 |
| Friday | clock | 3 |
| Saturday | clock | 1 |
| Sunday | clock | 1 |

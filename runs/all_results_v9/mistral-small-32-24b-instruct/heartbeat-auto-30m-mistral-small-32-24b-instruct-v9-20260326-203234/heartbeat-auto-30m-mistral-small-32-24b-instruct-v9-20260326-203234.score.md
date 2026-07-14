# PM-Bench score report

## Summary

Hit: 32 | Late: 2 | Miss: 47 | False alarms: 9 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 6 | state query calls: 7 | check_time calls: 7 | Actions: 43
Exact-set: matches 43 | mismatches 37 | reward 6
Set micro: TP 32 | FP 11 | FN 49
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 5
Rates: hit 39.5% | late 2.5% | miss 58.0% | false alarm/step 11.2% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 7.5% | cross-day miss 85.7% | update miss 88.9% | precision_hit 74.4% | precision_any 79.1% | exact-set match rate 53.8% | exact-set avg reward 0.075 | set_precision 74.4% | set_recall 39.5% | set_f1 51.6%
Hit rates (by modality): event 40.4% | time 37.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:32:34.889Z |
| Finished (UTC) | 2026-03-27T03:33:58.754Z |
| Duration | 1m 23.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 32 |
| Late | 2 |
| Miss | 47 |
| False alarms | 9 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 6 |
| State query calls | 7 |
| Check_time calls | 7 |
| Actions | 43 |
| Exact-set matches | 43 |
| Exact-set mismatches | 37 |
| Exact-set reward | 6 |
| Set TP | 32 |
| Set FP | 11 |
| Set FN | 49 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 7 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 39.5% |
| Late rate | 2.5% |
| Miss rate | 58.0% |
| False alarm/step | 11.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 7.5% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 88.9% |
| Precision hit | 74.4% |
| Precision any | 79.1% |
| Exact-set match rate | 53.8% |
| Exact-set avg reward | 0.075 |
| Set precision | 74.4% |
| Set recall | 39.5% |
| Set F1 | 51.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 23 | 57 | 40.4% |
| Time (time + time_check) | 9 | 24 | 37.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 23 | 1 | 18 | 42 | 54.8% | 57.1% |
| proactive_monitoring_required | 9 | 1 | 29 | 39 | 23.1% | 25.6% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 9 | 1 | 14 | 24 | 37.5% | 41.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 23.1% | 7.7% | 44.4% | 66.7% | 66.7% | 33.3% | 61.5% | 0.231 | 66.7% | 50.0% | 57.1% |
| Tuesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 7.7% | 15.4% | 42.9% | 25.0% | 75.0% | 14.3% | 53.8% | 0.077 | 66.7% | 36.4% | 47.1% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 10.0% | 0.0% | 33.3% | 50.0% | 50.0% | 20.0% | 60.0% | 0.200 | 80.0% | 36.4% | 50.0% |
| Thursday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 9.1% | 9.1% | 33.3% | 33.3% | 37.5% | 25.0% | 54.5% | 0.091 | 80.0% | 33.3% | 47.1% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 8.3% | 0.0% | 50.0% | 50.0% | 66.7% | 33.3% | 58.3% | 0.167 | 85.7% | 50.0% | 63.2% |
| Saturday | 6 | 0 | 8 | 42.9% | 0.0% | 57.1% | 0.0% | 0.0% | 40.0% | 50.0% | 50.0% | 33.3% | 50.0% | 0.000 | 100.0% | 42.9% | 60.0% |
| Sunday | 2 | 1 | 6 | 22.2% | 11.1% | 66.7% | 18.2% | 18.2% | 40.0% | 0.0% | 50.0% | 0.0% | 36.4% | -0.273 | 40.0% | 22.2% | 28.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 1 |
| Wednesday | clock | 1 |
| Thursday | clock | 1 |
| Friday | clock | 1 |
| Saturday | clock | 1 |
| Sunday | clock | 1 |

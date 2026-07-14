# PM-Bench score report

## Summary

Hit: 34 | Late: 2 | Miss: 45 | False alarms: 12 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 8 | state query calls: 0 | check_time calls: 0 | Actions: 48
Exact-set: matches 39 | mismatches 41 | reward -2
Set micro: TP 34 | FP 14 | FN 47
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 3
Rates: hit 42.0% | late 2.5% | miss 55.6% | false alarm/step 15.0% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 10.0% | cross-day miss 85.7% | update miss 88.9% | precision_hit 70.8% | precision_any 75.0% | exact-set match rate 48.8% | exact-set avg reward -0.025 | set_precision 70.8% | set_recall 42.0% | set_f1 52.7%
Hit rates (by modality): event 47.4% | time 29.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:33:58.976Z |
| Finished (UTC) | 2026-03-27T03:35:22.986Z |
| Duration | 1m 24.0s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 34 |
| Late | 2 |
| Miss | 45 |
| False alarms | 12 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 8 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 48 |
| Exact-set matches | 39 |
| Exact-set mismatches | 41 |
| Exact-set reward | -2 |
| Set TP | 34 |
| Set FP | 14 |
| Set FN | 47 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 42.0% |
| Late rate | 2.5% |
| Miss rate | 55.6% |
| False alarm/step | 15.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 10.0% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 88.9% |
| Precision hit | 70.8% |
| Precision any | 75.0% |
| Exact-set match rate | 48.8% |
| Exact-set avg reward | -0.025 |
| Set precision | 70.8% |
| Set recall | 42.0% |
| Set F1 | 52.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 27 | 57 | 47.4% |
| Time (time + time_check) | 7 | 24 | 29.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 27 | 0 | 15 | 42 | 64.3% | 64.3% |
| proactive_monitoring_required | 7 | 2 | 30 | 39 | 17.9% | 23.1% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 7 | 2 | 15 | 24 | 29.2% | 37.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 30.8% | 15.4% | 44.4% | 33.3% | 66.7% | 16.7% | 46.2% | -0.077 | 50.0% | 41.7% | 45.5% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 7.7% | 7.7% | 57.1% | 50.0% | 100.0% | 28.6% | 61.5% | 0.231 | 85.7% | 54.5% | 66.7% |
| Wednesday | 3 | 0 | 8 | 27.3% | 0.0% | 72.7% | 20.0% | 10.0% | 33.3% | 0.0% | 50.0% | 0.0% | 40.0% | -0.200 | 60.0% | 27.3% | 37.5% |
| Thursday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 18.2% | 18.2% | 44.4% | 33.3% | 50.0% | 25.0% | 45.5% | -0.091 | 71.4% | 41.7% | 52.6% |
| Friday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 8.3% | 8.3% | 50.0% | 25.0% | 66.7% | 16.7% | 41.7% | -0.167 | 71.4% | 41.7% | 52.6% |
| Saturday | 5 | 0 | 9 | 35.7% | 0.0% | 64.3% | 10.0% | 0.0% | 40.0% | 25.0% | 50.0% | 16.7% | 50.0% | 0.000 | 83.3% | 35.7% | 50.0% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 9.1% | 9.1% | 80.0% | 25.0% | 100.0% | 20.0% | 54.5% | 0.091 | 83.3% | 55.6% | 66.7% |

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

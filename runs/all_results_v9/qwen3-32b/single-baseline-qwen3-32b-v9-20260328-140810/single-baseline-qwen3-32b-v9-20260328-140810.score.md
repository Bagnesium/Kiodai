# PM-Bench score report

## Summary

Hit: 36 | Late: 2 | Miss: 43 | False alarms: 21 | Commission: 0 | Wrong-content: 7 | Dependency violations: 0 | Overkill steps: 16 | state query calls: 0 | check_time calls: 0 | Actions: 59
Exact-set: matches 29 | mismatches 51 | reward -22
Set micro: TP 36 | FP 23 | FN 45
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 1 | late 0 | miss 8 | canceled 2 | total 11 | violations 9
Rates: hit 44.4% | late 2.5% | miss 53.1% | false alarm/step 26.2% | commission 0.0% | wrong-content 8.6% | dependency/step 0.0% | overkill/step 20.0% | cross-day miss 100.0% | update miss 88.9% | precision_hit 61.0% | precision_any 64.4% | exact-set match rate 36.2% | exact-set avg reward -0.275 | set_precision 61.0% | set_recall 44.4% | set_f1 51.4%
Hit rates (by modality): event 56.1% | time 16.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T21:08:10.458Z |
| Finished (UTC) | 2026-03-28T21:08:49.173Z |
| Duration | 38.715s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 36 |
| Late | 2 |
| Miss | 43 |
| False alarms | 21 |
| Commission | 0 |
| Wrong-content | 7 |
| Dependency violations | 0 |
| Overkill steps | 16 |
| State query calls | 0 |
| Check_time calls | 0 |
| Actions | 59 |
| Exact-set matches | 29 |
| Exact-set mismatches | 51 |
| Exact-set reward | -22 |
| Set TP | 36 |
| Set FP | 23 |
| Set FN | 45 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| (none) | 0 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 44.4% |
| Late rate | 2.5% |
| Miss rate | 53.1% |
| False alarm/step | 26.2% |
| Commission rate | 0.0% |
| Wrong-content rate | 8.6% |
| Dependency/step | 0.0% |
| Overkill/step | 20.0% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 88.9% |
| Precision hit | 61.0% |
| Precision any | 64.4% |
| Exact-set match rate | 36.2% |
| Exact-set avg reward | -0.275 |
| Set precision | 61.0% |
| Set recall | 44.4% |
| Set F1 | 51.4% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 32 | 57 | 56.1% |
| Time (time + time_check) | 4 | 24 | 16.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 32 | 0 | 10 | 42 | 76.2% | 76.2% |
| proactive_monitoring_required | 4 | 2 | 33 | 39 | 10.3% | 15.4% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 4 | 1 | 19 | 24 | 16.7% | 20.8% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 30.8% | 7.7% | 44.4% | 0.0% | 66.7% | 0.0% | 46.2% | -0.077 | 50.0% | 33.3% | 40.0% |
| Tuesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 15.4% | 23.1% | 57.1% | 25.0% | 100.0% | 14.3% | 38.5% | -0.231 | 62.5% | 45.5% | 52.6% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 20.0% | 20.0% | 44.4% | 0.0% | 66.7% | 0.0% | 30.0% | -0.400 | 66.7% | 36.4% | 47.1% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 18.2% | 18.2% | 66.7% | 0.0% | 75.0% | 0.0% | 45.5% | -0.091 | 75.0% | 50.0% | 60.0% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 25.0% | 16.7% | 50.0% | 50.0% | 66.7% | 33.3% | 41.7% | -0.167 | 66.7% | 50.0% | 57.1% |
| Saturday | 6 | 1 | 7 | 42.9% | 7.1% | 50.0% | 40.0% | 30.0% | 60.0% | 0.0% | 75.0% | 0.0% | 10.0% | -0.800 | 54.5% | 42.9% | 48.0% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 36.4% | 27.3% | 80.0% | 25.0% | 100.0% | 20.0% | 36.4% | -0.273 | 55.6% | 55.6% | 55.6% |

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

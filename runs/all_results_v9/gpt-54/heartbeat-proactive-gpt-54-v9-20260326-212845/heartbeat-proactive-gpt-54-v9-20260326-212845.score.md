# PM-Bench score report

## Summary

Hit: 55 | Late: 1 | Miss: 25 | False alarms: 2 | Commission: 0 | Wrong-content: 1 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 11 | check_time calls: 8 | Actions: 58
Exact-set: matches 56 | mismatches 24 | reward 32
Set micro: TP 55 | FP 3 | FN 26
Cross-day: hit 7 | late 0 | miss 0 | total 7
Updates: hit 6 | late 0 | miss 3 | canceled 2 | total 11 | violations 1
Rates: hit 67.9% | late 1.2% | miss 30.9% | false alarm/step 2.5% | commission 0.0% | wrong-content 1.2% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 0.0% | update miss 33.3% | precision_hit 94.8% | precision_any 96.6% | exact-set match rate 70.0% | exact-set avg reward 0.400 | set_precision 94.8% | set_recall 67.9% | set_f1 79.1%
Hit rates (by modality): event 71.9% | time 58.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T04:28:45.442Z |
| Finished (UTC) | 2026-03-27T04:32:40.612Z |
| Duration | 3m 55.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 55 |
| Late | 1 |
| Miss | 25 |
| False alarms | 2 |
| Commission | 0 |
| Wrong-content | 1 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 11 |
| Check_time calls | 8 |
| Actions | 58 |
| Exact-set matches | 56 |
| Exact-set mismatches | 24 |
| Exact-set reward | 32 |
| Set TP | 55 |
| Set FP | 3 |
| Set FN | 26 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 8 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 67.9% |
| Late rate | 1.2% |
| Miss rate | 30.9% |
| False alarm/step | 2.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 1.2% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 0.0% |
| Update miss rate | 33.3% |
| Precision hit | 94.8% |
| Precision any | 96.6% |
| Exact-set match rate | 70.0% |
| Exact-set avg reward | 0.400 |
| Set precision | 94.8% |
| Set recall | 67.9% |
| Set F1 | 79.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 41 | 57 | 71.9% |
| Time (time + time_check) | 14 | 24 | 58.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 41 | 0 | 1 | 42 | 97.6% | 97.6% |
| proactive_monitoring_required | 14 | 1 | 24 | 39 | 35.9% | 38.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 14 | 0 | 10 | 24 | 58.3% | 58.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 7.7% | 7.7% | 55.6% | 66.7% | 83.3% | 33.3% | 69.2% | 0.385 | 87.5% | 58.3% | 70.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 66.7% | 50.0% | 100.0% | 20.0% | 70.0% | 0.400 | 100.0% | 63.6% | 77.8% |
| Thursday | 9 | 0 | 3 | 75.0% | 0.0% | 25.0% | 0.0% | 0.0% | 88.9% | 33.3% | 100.0% | 25.0% | 81.8% | 0.636 | 100.0% | 75.0% | 85.7% |
| Friday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 8.3% | 8.3% | 75.0% | 50.0% | 100.0% | 33.3% | 58.3% | 0.167 | 80.0% | 66.7% | 72.7% |
| Saturday | 11 | 0 | 3 | 78.6% | 0.0% | 21.4% | 0.0% | 0.0% | 80.0% | 75.0% | 100.0% | 50.0% | 70.0% | 0.400 | 100.0% | 78.6% | 88.0% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 80.0% | 50.0% | 100.0% | 40.0% | 72.7% | 0.455 | 100.0% | 66.7% | 80.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 2 |
| Wednesday | bank_balance | 1 |
| Thursday | clock | 1 |
| Thursday | shipment_status | 1 |
| Friday | clock | 2 |
| Saturday | clock | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 1 |

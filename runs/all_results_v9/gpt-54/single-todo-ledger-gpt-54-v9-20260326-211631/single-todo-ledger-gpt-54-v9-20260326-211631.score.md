# PM-Bench score report

## Summary

Hit: 50 | Late: 2 | Miss: 29 | False alarms: 3 | Commission: 0 | Wrong-content: 4 | Dependency violations: 0 | Overkill steps: 2 | state query calls: 15 | check_time calls: 11 | Actions: 55
Exact-set: matches 54 | mismatches 26 | reward 28
Set micro: TP 50 | FP 5 | FN 31
Cross-day: hit 3 | late 0 | miss 4 | total 7
Updates: hit 6 | late 1 | miss 2 | canceled 2 | total 11 | violations 1
Rates: hit 61.7% | late 2.5% | miss 35.8% | false alarm/step 3.8% | commission 0.0% | wrong-content 4.9% | dependency/step 0.0% | overkill/step 2.5% | cross-day miss 57.1% | update miss 22.2% | precision_hit 90.9% | precision_any 94.5% | exact-set match rate 67.5% | exact-set avg reward 0.350 | set_precision 90.9% | set_recall 61.7% | set_f1 73.5%
Hit rates (by modality): event 66.7% | time 50.0%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T04:16:31.172Z |
| Finished (UTC) | 2026-03-27T04:22:58.855Z |
| Duration | 6m 27.7s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 50 |
| Late | 2 |
| Miss | 29 |
| False alarms | 3 |
| Commission | 0 |
| Wrong-content | 4 |
| Dependency violations | 0 |
| Overkill steps | 2 |
| State query calls | 15 |
| Check_time calls | 11 |
| Actions | 55 |
| Exact-set matches | 54 |
| Exact-set mismatches | 26 |
| Exact-set reward | 28 |
| Set TP | 50 |
| Set FP | 5 |
| Set FN | 31 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 11 |
| library_hold | 1 |
| shipment_status | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 61.7% |
| Late rate | 2.5% |
| Miss rate | 35.8% |
| False alarm/step | 3.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 4.9% |
| Dependency/step | 0.0% |
| Overkill/step | 2.5% |
| Cross-day miss rate | 57.1% |
| Update miss rate | 22.2% |
| Precision hit | 90.9% |
| Precision any | 94.5% |
| Exact-set match rate | 67.5% |
| Exact-set avg reward | 0.350 |
| Set precision | 90.9% |
| Set recall | 61.7% |
| Set F1 | 73.5% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 57 | 66.7% |
| Time (time + time_check) | 12 | 24 | 50.0% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 0 | 4 | 42 | 90.5% | 90.5% |
| proactive_monitoring_required | 12 | 2 | 25 | 39 | 30.8% | 35.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 12 | 1 | 11 | 24 | 50.0% | 54.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 0.0% | 0.0% | 66.7% | 66.7% | 100.0% | 33.3% | 76.9% | 0.538 | 100.0% | 66.7% | 80.0% |
| Tuesday | 7 | 0 | 4 | 63.6% | 0.0% | 36.4% | 0.0% | 0.0% | 57.1% | 75.0% | 100.0% | 42.9% | 69.2% | 0.385 | 100.0% | 63.6% | 77.8% |
| Wednesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 0.0% | 0.0% | 44.4% | 50.0% | 66.7% | 20.0% | 60.0% | 0.200 | 100.0% | 45.5% | 62.5% |
| Thursday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 0.0% | 9.1% | 77.8% | 33.3% | 87.5% | 25.0% | 72.7% | 0.455 | 88.9% | 66.7% | 76.2% |
| Friday | 8 | 1 | 3 | 66.7% | 8.3% | 25.0% | 8.3% | 8.3% | 75.0% | 50.0% | 100.0% | 33.3% | 58.3% | 0.167 | 80.0% | 66.7% | 72.7% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 0.0% | 0.0% | 70.0% | 25.0% | 87.5% | 16.7% | 60.0% | 0.200 | 100.0% | 57.1% | 72.7% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 18.2% | 0.0% | 80.0% | 50.0% | 100.0% | 40.0% | 72.7% | 0.455 | 75.0% | 66.7% | 70.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 2 |
| Wednesday | bank_balance | 1 |
| Thursday | clock | 2 |
| Thursday | shipment_status | 1 |
| Friday | clock | 3 |
| Friday | library_hold | 1 |
| Saturday | clock | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 2 |

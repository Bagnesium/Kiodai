# PM-Bench score report

## Summary

Hit: 48 | Late: 4 | Miss: 29 | False alarms: 11 | Commission: 0 | Wrong-content: 6 | Dependency violations: 0 | Overkill steps: 12 | state query calls: 24 | check_time calls: 21 | Actions: 63
Exact-set: matches 43 | mismatches 37 | reward 6
Set micro: TP 48 | FP 15 | FN 33
Cross-day: hit 5 | late 1 | miss 1 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 3
Rates: hit 59.3% | late 4.9% | miss 35.8% | false alarm/step 13.8% | commission 0.0% | wrong-content 7.4% | dependency/step 0.0% | overkill/step 15.0% | cross-day miss 14.3% | update miss 66.7% | precision_hit 76.2% | precision_any 82.5% | exact-set match rate 53.8% | exact-set avg reward 0.075 | set_precision 76.2% | set_recall 59.3% | set_f1 66.7%
Hit rates (by modality): event 66.7% | time 41.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-27T03:06:32.476Z |
| Finished (UTC) | 2026-03-27T03:13:26.311Z |
| Duration | 6m 53.8s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 48 |
| Late | 4 |
| Miss | 29 |
| False alarms | 11 |
| Commission | 0 |
| Wrong-content | 6 |
| Dependency violations | 0 |
| Overkill steps | 12 |
| State query calls | 24 |
| Check_time calls | 21 |
| Actions | 63 |
| Exact-set matches | 43 |
| Exact-set mismatches | 37 |
| Exact-set reward | 6 |
| Set TP | 48 |
| Set FP | 15 |
| Set FN | 33 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| bank_balance | 2 |
| clock | 21 |
| email | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 59.3% |
| Late rate | 4.9% |
| Miss rate | 35.8% |
| False alarm/step | 13.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 7.4% |
| Dependency/step | 0.0% |
| Overkill/step | 15.0% |
| Cross-day miss rate | 14.3% |
| Update miss rate | 66.7% |
| Precision hit | 76.2% |
| Precision any | 82.5% |
| Exact-set match rate | 53.8% |
| Exact-set avg reward | 0.075 |
| Set precision | 76.2% |
| Set recall | 59.3% |
| Set F1 | 66.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 38 | 57 | 66.7% |
| Time (time + time_check) | 10 | 24 | 41.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 38 | 1 | 3 | 42 | 90.5% | 92.9% |
| proactive_monitoring_required | 10 | 3 | 26 | 39 | 25.6% | 33.3% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 10 | 2 | 12 | 24 | 41.7% | 50.0% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 1 | 1 | 2 | 0.0% | 50.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 30.8% | 30.8% | 55.6% | 66.7% | 83.3% | 33.3% | 46.2% | -0.077 | 63.6% | 58.3% | 60.9% |
| Tuesday | 6 | 0 | 5 | 54.5% | 0.0% | 45.5% | 23.1% | 15.4% | 57.1% | 50.0% | 100.0% | 28.6% | 53.8% | 0.077 | 66.7% | 54.5% | 60.0% |
| Wednesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 0.0% | 10.0% | 55.6% | 50.0% | 83.3% | 20.0% | 60.0% | 0.200 | 85.7% | 54.5% | 66.7% |
| Thursday | 8 | 0 | 4 | 66.7% | 0.0% | 33.3% | 18.2% | 18.2% | 77.8% | 33.3% | 87.5% | 25.0% | 63.6% | 0.273 | 80.0% | 66.7% | 72.7% |
| Friday | 8 | 2 | 2 | 66.7% | 16.7% | 16.7% | 8.3% | 16.7% | 62.5% | 75.0% | 83.3% | 50.0% | 50.0% | 0.000 | 72.7% | 66.7% | 69.6% |
| Saturday | 8 | 0 | 6 | 57.1% | 0.0% | 42.9% | 0.0% | 0.0% | 80.0% | 0.0% | 100.0% | 0.0% | 50.0% | 0.000 | 100.0% | 57.1% | 72.7% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 9.1% | 9.1% | 80.0% | 25.0% | 100.0% | 20.0% | 54.5% | 0.091 | 71.4% | 55.6% | 62.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 2 |
| Tuesday | clock | 4 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 1 |
| Thursday | clock | 4 |
| Friday | clock | 5 |
| Friday | email | 1 |
| Saturday | clock | 1 |
| Sunday | bank_balance | 1 |
| Sunday | clock | 4 |

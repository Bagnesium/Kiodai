# PM-Bench score report

## Summary

Hit: 36 | Late: 1 | Miss: 44 | False alarms: 48 | Commission: 9 | Wrong-content: 29 | Dependency violations: 0 | Overkill steps: 31 | state query calls: 87 | check_time calls: 76 | Actions: 94
Exact-set: matches 21 | mismatches 59 | reward -38
Set micro: TP 36 | FP 58 | FN 45
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 5 | late 0 | miss 4 | canceled 2 | total 11 | violations 20
Rates: hit 44.4% | late 1.2% | miss 54.3% | false alarm/step 60.0% | commission 11.1% | wrong-content 35.8% | dependency/step 0.0% | overkill/step 38.8% | cross-day miss 100.0% | update miss 44.4% | precision_hit 38.3% | precision_any 39.4% | exact-set match rate 26.2% | exact-set avg reward -0.475 | set_precision 38.3% | set_recall 44.4% | set_f1 41.1%
Hit rates (by modality): event 28.1% | time 83.3%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:50:31.259Z |
| Finished (UTC) | 2026-03-28T22:50:31.259Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 36 |
| Late | 1 |
| Miss | 44 |
| False alarms | 48 |
| Commission | 9 |
| Wrong-content | 29 |
| Dependency violations | 0 |
| Overkill steps | 31 |
| State query calls | 87 |
| Check_time calls | 76 |
| Actions | 94 |
| Exact-set matches | 21 |
| Exact-set mismatches | 59 |
| Exact-set reward | -38 |
| Set TP | 36 |
| Set FP | 58 |
| Set FN | 45 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 2 |
| bank_balance | 1 |
| clock | 76 |
| email | 4 |
| library_hold | 3 |
| reservation_waitlist | 1 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 44.4% |
| Late rate | 1.2% |
| Miss rate | 54.3% |
| False alarm/step | 60.0% |
| Commission rate | 11.1% |
| Wrong-content rate | 35.8% |
| Dependency/step | 0.0% |
| Overkill/step | 38.8% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 44.4% |
| Precision hit | 38.3% |
| Precision any | 39.4% |
| Exact-set match rate | 26.2% |
| Exact-set avg reward | -0.475 |
| Set precision | 38.3% |
| Set recall | 44.4% |
| Set F1 | 41.1% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 16 | 57 | 28.1% |
| Time (time + time_check) | 20 | 24 | 83.3% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 16 | 0 | 26 | 42 | 38.1% | 38.1% |
| proactive_monitoring_required | 20 | 1 | 18 | 39 | 51.3% | 53.8% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 20 | 1 | 3 | 24 | 83.3% | 87.5% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 53.8% | 30.8% | 22.2% | 100.0% | 33.3% | 50.0% | 30.8% | -0.385 | 41.7% | 41.7% | 41.7% |
| Tuesday | 5 | 0 | 6 | 45.5% | 0.0% | 54.5% | 61.5% | 38.5% | 14.3% | 100.0% | 25.0% | 57.1% | 23.1% | -0.538 | 35.7% | 45.5% | 40.0% |
| Wednesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 20.0% | 50.0% | 22.2% | 100.0% | 33.3% | 40.0% | 20.0% | -0.600 | 33.3% | 36.4% | 34.8% |
| Thursday | 5 | 0 | 7 | 41.7% | 0.0% | 58.3% | 54.5% | 45.5% | 33.3% | 66.7% | 37.5% | 50.0% | 18.2% | -0.636 | 45.5% | 41.7% | 43.5% |
| Friday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 100.0% | 50.0% | 25.0% | 50.0% | 33.3% | 33.3% | 16.7% | -0.667 | 25.0% | 33.3% | 28.6% |
| Saturday | 7 | 1 | 6 | 50.0% | 7.1% | 42.9% | 60.0% | 20.0% | 40.0% | 75.0% | 50.0% | 50.0% | 30.0% | -0.400 | 50.0% | 50.0% | 50.0% |
| Sunday | 6 | 0 | 3 | 66.7% | 0.0% | 33.3% | 63.6% | 36.4% | 40.0% | 100.0% | 50.0% | 80.0% | 45.5% | -0.091 | 40.0% | 66.7% | 50.0% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 2 |
| Monday | clock | 10 |
| Monday | email | 2 |
| Monday | library_hold | 3 |
| Monday | reservation_waitlist | 1 |
| Tuesday | clock | 13 |
| Wednesday | bank_balance | 1 |
| Wednesday | clock | 10 |
| Thursday | clock | 11 |
| Friday | clock | 11 |
| Friday | email | 2 |
| Saturday | clock | 10 |
| Sunday | clock | 11 |

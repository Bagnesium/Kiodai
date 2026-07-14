# PM-Bench score report

## Summary

Hit: 36 | Late: 4 | Miss: 41 | False alarms: 44 | Commission: 0 | Wrong-content: 21 | Dependency violations: 0 | Overkill steps: 28 | state query calls: 87 | check_time calls: 76 | Actions: 84
Exact-set: matches 23 | mismatches 57 | reward -34
Set micro: TP 36 | FP 48 | FN 45
Cross-day: hit 0 | late 1 | miss 6 | total 7
Updates: hit 4 | late 1 | miss 4 | canceled 2 | total 11 | violations 15
Rates: hit 44.4% | late 4.9% | miss 50.6% | false alarm/step 55.0% | commission 0.0% | wrong-content 25.9% | dependency/step 0.0% | overkill/step 35.0% | cross-day miss 85.7% | update miss 44.4% | precision_hit 42.9% | precision_any 47.6% | exact-set match rate 28.7% | exact-set avg reward -0.425 | set_precision 42.9% | set_recall 44.4% | set_f1 43.6%
Hit rates (by modality): event 33.3% | time 70.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:28:01.125Z |
| Finished (UTC) | 2026-03-28T22:31:09.282Z |
| Duration | 3m 8.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 36 |
| Late | 4 |
| Miss | 41 |
| False alarms | 44 |
| Commission | 0 |
| Wrong-content | 21 |
| Dependency violations | 0 |
| Overkill steps | 28 |
| State query calls | 87 |
| Check_time calls | 76 |
| Actions | 84 |
| Exact-set matches | 23 |
| Exact-set mismatches | 57 |
| Exact-set reward | -34 |
| Set TP | 36 |
| Set FP | 48 |
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
| Late rate | 4.9% |
| Miss rate | 50.6% |
| False alarm/step | 55.0% |
| Commission rate | 0.0% |
| Wrong-content rate | 25.9% |
| Dependency/step | 0.0% |
| Overkill/step | 35.0% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 44.4% |
| Precision hit | 42.9% |
| Precision any | 47.6% |
| Exact-set match rate | 28.7% |
| Exact-set avg reward | -0.425 |
| Set precision | 42.9% |
| Set recall | 44.4% |
| Set F1 | 43.6% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 19 | 57 | 33.3% |
| Time (time + time_check) | 17 | 24 | 70.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 19 | 2 | 21 | 42 | 45.2% | 50.0% |
| proactive_monitoring_required | 17 | 2 | 20 | 39 | 43.6% | 48.7% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 17 | 2 | 5 | 24 | 70.8% | 79.2% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 7 | 0 | 5 | 58.3% | 0.0% | 41.7% | 53.8% | 38.5% | 44.4% | 100.0% | 66.7% | 50.0% | 30.8% | -0.385 | 50.0% | 58.3% | 53.8% |
| Tuesday | 5 | 1 | 5 | 45.5% | 9.1% | 45.5% | 69.2% | 53.8% | 28.6% | 75.0% | 50.0% | 42.9% | 15.4% | -0.692 | 33.3% | 45.5% | 38.5% |
| Wednesday | 4 | 1 | 6 | 36.4% | 9.1% | 54.5% | 40.0% | 30.0% | 33.3% | 50.0% | 50.0% | 20.0% | 30.0% | -0.400 | 44.4% | 36.4% | 40.0% |
| Thursday | 5 | 1 | 6 | 41.7% | 8.3% | 50.0% | 36.4% | 36.4% | 33.3% | 66.7% | 37.5% | 50.0% | 27.3% | -0.455 | 50.0% | 41.7% | 45.5% |
| Friday | 3 | 0 | 9 | 25.0% | 0.0% | 75.0% | 58.3% | 33.3% | 12.5% | 50.0% | 16.7% | 33.3% | 25.0% | -0.500 | 30.0% | 25.0% | 27.3% |
| Saturday | 7 | 1 | 6 | 50.0% | 7.1% | 42.9% | 40.0% | 10.0% | 40.0% | 75.0% | 50.0% | 50.0% | 40.0% | -0.200 | 58.3% | 50.0% | 53.8% |
| Sunday | 5 | 0 | 4 | 55.6% | 0.0% | 44.4% | 81.8% | 36.4% | 40.0% | 75.0% | 50.0% | 60.0% | 36.4% | -0.273 | 35.7% | 55.6% | 43.5% |

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

# PM-Bench score report

## Summary

Hit: 20 | Late: 1 | Miss: 60 | False alarms: 25 | Commission: 2 | Wrong-content: 12 | Dependency violations: 0 | Overkill steps: 15 | state query calls: 87 | check_time calls: 76 | Actions: 48
Exact-set: matches 28 | mismatches 52 | reward -24
Set micro: TP 20 | FP 28 | FN 61
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 11
Rates: hit 24.7% | late 1.2% | miss 74.1% | false alarm/step 31.2% | commission 2.5% | wrong-content 14.8% | dependency/step 0.0% | overkill/step 18.8% | cross-day miss 100.0% | update miss 55.6% | precision_hit 41.7% | precision_any 43.8% | exact-set match rate 35.0% | exact-set avg reward -0.300 | set_precision 41.7% | set_recall 24.7% | set_f1 31.0%
Hit rates (by modality): event 12.3% | time 54.2%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:50:31.260Z |
| Finished (UTC) | 2026-03-28T22:50:31.260Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 20 |
| Late | 1 |
| Miss | 60 |
| False alarms | 25 |
| Commission | 2 |
| Wrong-content | 12 |
| Dependency violations | 0 |
| Overkill steps | 15 |
| State query calls | 87 |
| Check_time calls | 76 |
| Actions | 48 |
| Exact-set matches | 28 |
| Exact-set mismatches | 52 |
| Exact-set reward | -24 |
| Set TP | 20 |
| Set FP | 28 |
| Set FN | 61 |

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
| Hit rate | 24.7% |
| Late rate | 1.2% |
| Miss rate | 74.1% |
| False alarm/step | 31.2% |
| Commission rate | 2.5% |
| Wrong-content rate | 14.8% |
| Dependency/step | 0.0% |
| Overkill/step | 18.8% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 55.6% |
| Precision hit | 41.7% |
| Precision any | 43.8% |
| Exact-set match rate | 35.0% |
| Exact-set avg reward | -0.300 |
| Set precision | 41.7% |
| Set recall | 24.7% |
| Set F1 | 31.0% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 7 | 57 | 12.3% |
| Time (time + time_check) | 13 | 24 | 54.2% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 7 | 0 | 35 | 42 | 16.7% | 16.7% |
| proactive_monitoring_required | 13 | 1 | 25 | 39 | 33.3% | 35.9% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 13 | 1 | 10 | 24 | 54.2% | 58.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 23.1% | 7.7% | 22.2% | 66.7% | 33.3% | 33.3% | 46.2% | -0.077 | 57.1% | 33.3% | 42.1% |
| Tuesday | 3 | 0 | 8 | 27.3% | 0.0% | 72.7% | 46.2% | 30.8% | 14.3% | 50.0% | 25.0% | 28.6% | 23.1% | -0.538 | 30.0% | 27.3% | 28.6% |
| Wednesday | 1 | 0 | 10 | 9.1% | 0.0% | 90.9% | 0.0% | 0.0% | 0.0% | 50.0% | 0.0% | 20.0% | 50.0% | 0.000 | 50.0% | 9.1% | 15.4% |
| Thursday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 36.4% | 27.3% | 11.1% | 33.3% | 12.5% | 25.0% | 27.3% | -0.455 | 33.3% | 16.7% | 22.2% |
| Friday | 3 | 0 | 9 | 25.0% | 0.0% | 75.0% | 25.0% | 16.7% | 12.5% | 50.0% | 16.7% | 33.3% | 41.7% | -0.167 | 50.0% | 25.0% | 33.3% |
| Saturday | 3 | 1 | 10 | 21.4% | 7.1% | 71.4% | 20.0% | 10.0% | 10.0% | 50.0% | 12.5% | 33.3% | 30.0% | -0.400 | 50.0% | 21.4% | 30.0% |
| Sunday | 4 | 0 | 5 | 44.4% | 0.0% | 55.6% | 63.6% | 36.4% | 20.0% | 75.0% | 25.0% | 60.0% | 27.3% | -0.455 | 36.4% | 44.4% | 40.0% |

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

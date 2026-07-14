# PM-Bench score report

## Summary

Hit: 20 | Late: 0 | Miss: 61 | False alarms: 20 | Commission: 1 | Wrong-content: 9 | Dependency violations: 0 | Overkill steps: 15 | state query calls: 169 | check_time calls: 80 | Actions: 41
Exact-set: matches 26 | mismatches 54 | reward -28
Set micro: TP 20 | FP 21 | FN 61
Cross-day: hit 0 | late 0 | miss 7 | total 7
Updates: hit 4 | late 0 | miss 5 | canceled 2 | total 11 | violations 10
Rates: hit 24.7% | late 0.0% | miss 75.3% | false alarm/step 25.0% | commission 1.2% | wrong-content 11.1% | dependency/step 0.0% | overkill/step 18.8% | cross-day miss 100.0% | update miss 55.6% | precision_hit 48.8% | precision_any 48.8% | exact-set match rate 32.5% | exact-set avg reward -0.350 | set_precision 48.8% | set_recall 24.7% | set_f1 32.8%
Hit rates (by modality): event 7.0% | time 66.7%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:06:37.753Z |
| Finished (UTC) | 2026-03-28T22:06:37.753Z |
| Duration | 0.000s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 20 |
| Late | 0 |
| Miss | 61 |
| False alarms | 20 |
| Commission | 1 |
| Wrong-content | 9 |
| Dependency violations | 0 |
| Overkill steps | 15 |
| State query calls | 169 |
| Check_time calls | 80 |
| Actions | 41 |
| Exact-set matches | 26 |
| Exact-set mismatches | 54 |
| Exact-set reward | -28 |
| Set TP | 20 |
| Set FP | 21 |
| Set FN | 61 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 47 |
| calendar | 18 |
| clock | 80 |
| email | 1 |
| laundry_status | 9 |
| library_hold | 14 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 24.7% |
| Late rate | 0.0% |
| Miss rate | 75.3% |
| False alarm/step | 25.0% |
| Commission rate | 1.2% |
| Wrong-content rate | 11.1% |
| Dependency/step | 0.0% |
| Overkill/step | 18.8% |
| Cross-day miss rate | 100.0% |
| Update miss rate | 55.6% |
| Precision hit | 48.8% |
| Precision any | 48.8% |
| Exact-set match rate | 32.5% |
| Exact-set avg reward | -0.350 |
| Set precision | 48.8% |
| Set recall | 24.7% |
| Set F1 | 32.8% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 4 | 57 | 7.0% |
| Time (time + time_check) | 16 | 24 | 66.7% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 4 | 0 | 38 | 42 | 9.5% | 9.5% |
| proactive_monitoring_required | 16 | 0 | 23 | 39 | 41.0% | 41.0% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| clock | 16 | 0 | 8 | 24 | 66.7% | 66.7% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 38.5% | 30.8% | 22.2% | 66.7% | 33.3% | 33.3% | 23.1% | -0.538 | 44.4% | 33.3% | 38.1% |
| Tuesday | 4 | 0 | 7 | 36.4% | 0.0% | 63.6% | 30.8% | 23.1% | 14.3% | 75.0% | 25.0% | 42.9% | 38.5% | -0.231 | 50.0% | 36.4% | 42.1% |
| Wednesday | 2 | 0 | 9 | 18.2% | 0.0% | 81.8% | 0.0% | 0.0% | 0.0% | 100.0% | 0.0% | 40.0% | 60.0% | 0.200 | 100.0% | 18.2% | 30.8% |
| Thursday | 3 | 0 | 9 | 25.0% | 0.0% | 75.0% | 0.0% | 0.0% | 11.1% | 66.7% | 12.5% | 50.0% | 54.5% | 0.091 | 100.0% | 25.0% | 40.0% |
| Friday | 1 | 0 | 11 | 8.3% | 0.0% | 91.7% | 33.3% | 33.3% | 0.0% | 25.0% | 0.0% | 16.7% | 16.7% | -0.667 | 20.0% | 8.3% | 11.8% |
| Saturday | 3 | 0 | 11 | 21.4% | 0.0% | 78.6% | 30.0% | 10.0% | 0.0% | 75.0% | 0.0% | 50.0% | 20.0% | -0.600 | 42.9% | 21.4% | 28.6% |
| Sunday | 3 | 0 | 6 | 33.3% | 0.0% | 66.7% | 36.4% | 27.3% | 0.0% | 75.0% | 0.0% | 60.0% | 18.2% | -0.636 | 42.9% | 33.3% | 37.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 12 |
| Monday | clock | 13 |
| Monday | library_hold | 6 |
| Tuesday | appointment_portal | 13 |
| Tuesday | clock | 13 |
| Wednesday | appointment_portal | 10 |
| Wednesday | clock | 10 |
| Thursday | appointment_portal | 11 |
| Thursday | clock | 11 |
| Friday | appointment_portal | 1 |
| Friday | clock | 12 |
| Friday | email | 1 |
| Friday | laundry_status | 8 |
| Friday | library_hold | 7 |
| Saturday | calendar | 7 |
| Saturday | clock | 10 |
| Saturday | laundry_status | 1 |
| Saturday | library_hold | 1 |
| Sunday | calendar | 11 |
| Sunday | clock | 11 |

# PM-Bench score report

## Summary

Hit: 19 | Late: 2 | Miss: 60 | False alarms: 46 | Commission: 0 | Wrong-content: 20 | Dependency violations: 0 | Overkill steps: 22 | state query calls: 135 | check_time calls: 69 | Actions: 67
Exact-set: matches 18 | mismatches 62 | reward -44
Set micro: TP 19 | FP 48 | FN 62
Cross-day: hit 1 | late 0 | miss 6 | total 7
Updates: hit 0 | late 0 | miss 9 | canceled 2 | total 11 | violations 10
Rates: hit 23.5% | late 2.5% | miss 74.1% | false alarm/step 57.5% | commission 0.0% | wrong-content 24.7% | dependency/step 0.0% | overkill/step 27.5% | cross-day miss 85.7% | update miss 100.0% | precision_hit 28.4% | precision_any 31.3% | exact-set match rate 22.5% | exact-set avg reward -0.550 | set_precision 28.4% | set_recall 23.5% | set_f1 25.7%
Hit rates (by modality): event 17.5% | time 37.5%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T23:03:18.230Z |
| Finished (UTC) | 2026-03-28T23:05:05.379Z |
| Duration | 1m 47.2s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 19 |
| Late | 2 |
| Miss | 60 |
| False alarms | 46 |
| Commission | 0 |
| Wrong-content | 20 |
| Dependency violations | 0 |
| Overkill steps | 22 |
| State query calls | 135 |
| Check_time calls | 69 |
| Actions | 67 |
| Exact-set matches | 18 |
| Exact-set mismatches | 62 |
| Exact-set reward | -44 |
| Set TP | 19 |
| Set FP | 48 |
| Set FN | 62 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| appointment_portal | 8 |
| calendar | 22 |
| clock | 69 |
| course_portal | 1 |
| email | 8 |
| laundry_status | 4 |
| library_hold | 7 |
| reservation_waitlist | 4 |
| shipment_status | 12 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 23.5% |
| Late rate | 2.5% |
| Miss rate | 74.1% |
| False alarm/step | 57.5% |
| Commission rate | 0.0% |
| Wrong-content rate | 24.7% |
| Dependency/step | 0.0% |
| Overkill/step | 27.5% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 100.0% |
| Precision hit | 28.4% |
| Precision any | 31.3% |
| Exact-set match rate | 22.5% |
| Exact-set avg reward | -0.550 |
| Set precision | 28.4% |
| Set recall | 23.5% |
| Set F1 | 25.7% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 10 | 57 | 17.5% |
| Time (time + time_check) | 9 | 24 | 37.5% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 10 | 1 | 31 | 42 | 23.8% | 26.2% |
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
| Monday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 61.5% | 23.1% | 22.2% | 66.7% | 33.3% | 33.3% | 23.1% | -0.538 | 33.3% | 33.3% | 33.3% |
| Tuesday | 2 | 0 | 9 | 18.2% | 0.0% | 81.8% | 84.6% | 46.2% | 28.6% | 0.0% | 50.0% | 0.0% | 7.7% | -0.846 | 15.4% | 18.2% | 16.7% |
| Wednesday | 3 | 1 | 7 | 27.3% | 9.1% | 63.6% | 80.0% | 50.0% | 22.2% | 50.0% | 33.3% | 20.0% | 20.0% | -0.600 | 25.0% | 27.3% | 26.1% |
| Thursday | 2 | 0 | 10 | 16.7% | 0.0% | 83.3% | 54.5% | 27.3% | 0.0% | 66.7% | 0.0% | 50.0% | 18.2% | -0.636 | 25.0% | 16.7% | 20.0% |
| Friday | 4 | 0 | 8 | 33.3% | 0.0% | 66.7% | 50.0% | 16.7% | 25.0% | 50.0% | 33.3% | 33.3% | 41.7% | -0.167 | 40.0% | 33.3% | 36.4% |
| Saturday | 1 | 1 | 12 | 7.1% | 7.1% | 85.7% | 30.0% | 0.0% | 10.0% | 0.0% | 12.5% | 0.0% | 20.0% | -0.600 | 20.0% | 7.1% | 10.5% |
| Sunday | 3 | 0 | 6 | 33.3% | 0.0% | 66.7% | 36.4% | 27.3% | 20.0% | 50.0% | 25.0% | 40.0% | 27.3% | -0.455 | 42.9% | 33.3% | 37.5% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | appointment_portal | 6 |
| Monday | calendar | 4 |
| Monday | clock | 8 |
| Monday | library_hold | 4 |
| Tuesday | calendar | 13 |
| Tuesday | clock | 10 |
| Tuesday | email | 2 |
| Tuesday | reservation_waitlist | 1 |
| Wednesday | calendar | 3 |
| Wednesday | clock | 10 |
| Wednesday | course_portal | 1 |
| Wednesday | email | 2 |
| Thursday | appointment_portal | 2 |
| Thursday | clock | 11 |
| Friday | clock | 9 |
| Friday | email | 3 |
| Friday | laundry_status | 4 |
| Friday | library_hold | 3 |
| Friday | shipment_status | 5 |
| Saturday | calendar | 1 |
| Saturday | clock | 10 |
| Saturday | email | 1 |
| Saturday | shipment_status | 7 |
| Sunday | calendar | 1 |
| Sunday | clock | 11 |
| Sunday | reservation_waitlist | 3 |

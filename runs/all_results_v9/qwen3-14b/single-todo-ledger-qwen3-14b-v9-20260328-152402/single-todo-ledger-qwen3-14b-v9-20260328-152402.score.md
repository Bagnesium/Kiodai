# PM-Bench score report

## Summary

Hit: 40 | Late: 5 | Miss: 36 | False alarms: 27 | Commission: 0 | Wrong-content: 12 | Dependency violations: 0 | Overkill steps: 21 | state query calls: 11 | check_time calls: 11 | Actions: 72
Exact-set: matches 29 | mismatches 51 | reward -22
Set micro: TP 40 | FP 32 | FN 41
Cross-day: hit 0 | late 1 | miss 6 | total 7
Updates: hit 3 | late 0 | miss 6 | canceled 2 | total 11 | violations 11
Rates: hit 49.4% | late 6.2% | miss 44.4% | false alarm/step 33.8% | commission 0.0% | wrong-content 14.8% | dependency/step 0.0% | overkill/step 26.2% | cross-day miss 85.7% | update miss 66.7% | precision_hit 55.6% | precision_any 62.5% | exact-set match rate 36.2% | exact-set avg reward -0.275 | set_precision 55.6% | set_recall 49.4% | set_f1 52.3%
Hit rates (by modality): event 50.9% | time 45.8%

## Run Timing

| Field | Value |
| --- | --- |
| Started (UTC) | 2026-03-28T22:24:02.329Z |
| Finished (UTC) | 2026-03-28T22:26:53.182Z |
| Duration | 2m 50.9s |

## Overall Counts

| Metric | Value |
| --- | --- |
| Hit | 40 |
| Late | 5 |
| Miss | 36 |
| False alarms | 27 |
| Commission | 0 |
| Wrong-content | 12 |
| Dependency violations | 0 |
| Overkill steps | 21 |
| State query calls | 11 |
| Check_time calls | 11 |
| Actions | 72 |
| Exact-set matches | 29 |
| Exact-set mismatches | 51 |
| Exact-set reward | -22 |
| Set TP | 40 |
| Set FP | 32 |
| Set FN | 41 |

## State Query Calls by Channel (Overall)

| Channel | Calls |
| --- | --- |
| clock | 11 |

## Overall Rates

| Metric | Value |
| --- | --- |
| Hit rate | 49.4% |
| Late rate | 6.2% |
| Miss rate | 44.4% |
| False alarm/step | 33.8% |
| Commission rate | 0.0% |
| Wrong-content rate | 14.8% |
| Dependency/step | 0.0% |
| Overkill/step | 26.2% |
| Cross-day miss rate | 85.7% |
| Update miss rate | 66.7% |
| Precision hit | 55.6% |
| Precision any | 62.5% |
| Exact-set match rate | 36.2% |
| Exact-set avg reward | -0.275 |
| Set precision | 55.6% |
| Set recall | 49.4% |
| Set F1 | 52.3% |

## Modality Hit Rates

| Modality | Hit | Total | Hit rate |
| --- | --- | --- | --- |
| Event | 29 | 57 | 50.9% |
| Time (time + time_check) | 11 | 24 | 45.8% |

## Monitoring Categories

| Category | Hit | Late | Miss | Total | Hit rate | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| no_proactive_monitoring | 29 | 1 | 12 | 42 | 69.0% | 71.4% |
| proactive_monitoring_required | 11 | 4 | 24 | 39 | 28.2% | 38.5% |

Note: `proactive_monitoring_required` hit rate is no-late-credit by design.

## Proactive Required by Channel

| Channel | Hit | Late | Miss | Total | Hit rate (no late credit) | Any rate (hit+late) |
| --- | --- | --- | --- | --- | --- | --- |
| appointment_portal | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| bank_balance | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| calendar | 0 | 1 | 2 | 3 | 0.0% | 33.3% |
| clock | 11 | 3 | 10 | 24 | 45.8% | 58.3% |
| course_portal | 0 | 0 | 1 | 1 | 0.0% | 0.0% |
| email | 0 | 0 | 2 | 2 | 0.0% | 0.0% |
| library_hold | 0 | 0 | 3 | 3 | 0.0% | 0.0% |
| shipment_status | 0 | 0 | 1 | 1 | 0.0% | 0.0% |

## Per-Day Summary

| Day | Hit | Late | Miss | Hit rate | Late rate | Miss rate | False alarm/step | Overkill/step | Event hit rate | Time hit rate | No-proactive hit rate | Proactive hit rate (no late credit) | Exact-set match rate | Exact-set avg reward | Set precision | Set recall | Set F1 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Monday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 61.5% | 38.5% | 44.4% | 66.7% | 66.7% | 33.3% | 30.8% | -0.385 | 42.9% | 50.0% | 46.2% |
| Tuesday | 6 | 1 | 4 | 54.5% | 9.1% | 36.4% | 38.5% | 38.5% | 57.1% | 50.0% | 100.0% | 28.6% | 30.8% | -0.385 | 50.0% | 54.5% | 52.2% |
| Wednesday | 3 | 2 | 6 | 27.3% | 18.2% | 54.5% | 30.0% | 20.0% | 33.3% | 0.0% | 50.0% | 0.0% | 30.0% | -0.400 | 37.5% | 27.3% | 31.6% |
| Thursday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 36.4% | 27.3% | 55.6% | 33.3% | 62.5% | 25.0% | 45.5% | -0.091 | 60.0% | 50.0% | 54.5% |
| Friday | 6 | 0 | 6 | 50.0% | 0.0% | 50.0% | 25.0% | 25.0% | 50.0% | 50.0% | 66.7% | 33.3% | 33.3% | -0.333 | 66.7% | 50.0% | 57.1% |
| Saturday | 8 | 1 | 5 | 57.1% | 7.1% | 35.7% | 10.0% | 10.0% | 50.0% | 75.0% | 62.5% | 50.0% | 40.0% | -0.200 | 80.0% | 57.1% | 66.7% |
| Sunday | 5 | 1 | 3 | 55.6% | 11.1% | 33.3% | 27.3% | 18.2% | 80.0% | 25.0% | 100.0% | 20.0% | 45.5% | -0.091 | 55.6% | 55.6% | 55.6% |

## State Query Calls by Channel (Per Day)

| Day | Channel | Calls |
| --- | --- | --- |
| Monday | clock | 1 |
| Tuesday | clock | 1 |
| Wednesday | clock | 2 |
| Thursday | clock | 2 |
| Friday | clock | 2 |
| Saturday | clock | 1 |
| Sunday | clock | 2 |

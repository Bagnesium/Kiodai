# v2.1-comparison-v1

Exploratory comparison on exposed synthetic development cases; four template families.

Primary: A2 minus B_ledger. Secondary: A2 minus A0. Arithmetic mean of the 12 per-trajectory A2 minus B_ledger Set-F1 differences; require all declared pairs and completed study, otherwise null. A2 minus A0 separately.

| Trajectory | Family | Method | Status | TP | FP | FN | Precision | Recall | Set-F1 | Calls | Queries |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| v2_hidden_91320 | hidden | A2 | completed | 0 | 0 | 2 | None | 0.0 | 0.0 | 17 | 6 |
| v2_hidden_91320 | hidden | B_ledger | completed | 1 | 0 | 1 | 1.0 | 0.5 | 0.6666666666666666 | 19 | 1 |
| v2_hidden_91320 | hidden | A0 | completed | 3 | 0 | 0 | 1.0 | 1.0 | 1.0 | 13 | 5 |
| v2_hidden_91321 | hidden | B_ledger | completed | 3 | 0 | 0 | 1.0 | 1.0 | 1.0 | 32 | 5 |
| v2_hidden_91321 | hidden | A0 | completed | 3 | 0 | 0 | 1.0 | 1.0 | 1.0 | 13 | 5 |
| v2_hidden_91321 | hidden | A2 | completed | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 17 | 5 |
| v2_hidden_91322 | hidden | A0 | completed | 3 | 0 | 0 | 1.0 | 1.0 | 1.0 | 13 | 5 |
| v2_hidden_91322 | hidden | A2 | completed | 3 | 0 | 0 | 1.0 | 1.0 | 1.0 | 18 | 7 |
| v2_hidden_91322 | hidden | B_ledger | completed | 1 | 0 | 1 | 1.0 | 0.5 | 0.6666666666666666 | 22 | 2 |
| v2_visible_events_91310 | visible_events | A2 | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 20 | 0 |
| v2_visible_events_91310 | visible_events | B_ledger | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 18 | 0 |
| v2_visible_events_91310 | visible_events | A0 | completed | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 8 | 0 |
| v2_visible_events_91311 | visible_events | B_ledger | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 20 | 0 |
| v2_visible_events_91311 | visible_events | A0 | completed | 1 | 1 | 1 | 0.5 | 0.5 | 0.5 | 8 | 0 |
| v2_visible_events_91311 | visible_events | A2 | completed | 2 | 0 | 0 | 1.0 | 1.0 | 1.0 | 21 | 0 |
| v2_visible_events_91312 | visible_events | A0 | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 8 | 0 |
| v2_visible_events_91312 | visible_events | A2 | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 20 | 0 |
| v2_visible_events_91312 | visible_events | B_ledger | completed | 2 | 1 | 0 | 0.6666666666666666 | 1.0 | 0.8 | 19 | 0 |
| v2_cross_day_91331 | cross_day | A2 | completed | 0 | 1 | 1 | 0.0 | 0.0 | 0.0 | 23 | 0 |
| v2_cross_day_91331 | cross_day | B_ledger | completed | 0 | 1 | 1 | 0.0 | 0.0 | 0.0 | 22 | 0 |
| v2_cross_day_91331 | cross_day | A0 | completed | 2 | 3 | 0 | 0.4 | 1.0 | 0.5714285714285714 | 8 | 0 |
| v2_cross_day_91332 | cross_day | B_ledger | completed | 2 | 0 | 0 | 1.0 | 1.0 | 1.0 | 19 | 0 |
| v2_cross_day_91332 | cross_day | A0 | completed | 2 | 0 | 0 | 1.0 | 1.0 | 1.0 | 9 | 0 |
| v2_cross_day_91332 | cross_day | A2 | completed | 0 | 0 | 1 | None | 0.0 | 0.0 | 23 | 0 |
| v2_cross_day_91330 | cross_day | A0 | completed | 2 | 0 | 0 | 1.0 | 1.0 | 1.0 | 9 | 0 |
| v2_cross_day_91330 | cross_day | A2 | completed | 0 | 0 | 1 | None | 0.0 | 0.0 | 22 | 0 |
| v2_cross_day_91330 | cross_day | B_ledger | completed | 2 | 0 | 0 | 1.0 | 1.0 | 1.0 | 21 | 1 |
| v2_revision_91301 | revision | A2 | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 18 | 0 |
| v2_revision_91301 | revision | B_ledger | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 20 | 0 |
| v2_revision_91301 | revision | A0 | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 9 | 1 |
| v2_revision_91302 | revision | B_ledger | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 18 | 0 |
| v2_revision_91302 | revision | A0 | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 10 | 2 |
| v2_revision_91302 | revision | A2 | completed | 0 | 0 | 1 | None | 0.0 | 0.0 | 19 | 0 |
| v2_revision_91300 | revision | A0 | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 9 | 1 |
| v2_revision_91300 | revision | A2 | completed | 1 | 1 | 0 | 0.5 | 1.0 | 0.6666666666666666 | 16 | 0 |
| v2_revision_91300 | revision | B_ledger | completed | 1 | 0 | 0 | 1.0 | 1.0 | 1.0 | 21 | 2 |

## Declared paired comparisons

| Group | Contrast | Usable/planned pairs | Declared mean |
|---|---|---:|---:|
| all | A2 minus B_ledger | 12/12 | -0.33055555555555555 |
| all | A2 minus A0 | 12/12 | -0.3837301587301587 |
| family:hidden | A2 minus B_ledger | 3/3 | -0.27777777777777773 |
| family:hidden | A2 minus A0 | 3/3 | -0.5 |
| family:visible_events | A2 minus B_ledger | 3/3 | 0.06666666666666665 |
| family:visible_events | A2 minus A0 | 3/3 | 0.26666666666666666 |
| family:cross_day | A2 minus B_ledger | 3/3 | -0.6666666666666666 |
| family:cross_day | A2 minus A0 | 3/3 | -0.8571428571428571 |
| family:revision | A2 minus B_ledger | 3/3 | -0.4444444444444445 |
| family:revision | A2 minus A0 | 3/3 | -0.4444444444444445 |
| prior-network-smoke:True | A2 minus B_ledger | 1/1 | -0.6666666666666666 |
| prior-network-smoke:True | A2 minus A0 | 1/1 | -1.0 |
| prior-network-smoke:False | A2 minus B_ledger | 11/11 | -0.3 |
| prior-network-smoke:False | A2 minus A0 | 11/11 | -0.3277056277056277 |

Null means undefined or unavailable, never zero. Descriptive micro totals, obligation/dependency diagnostics, hidden evidence categories, costs and manual-review status are in the JSON report.
Semantic correctness is unmeasured until manual review; A0 extraction is not applicable. Queries without an immediate hit are not automatically unnecessary.
No independent replication, significance or equivalence claim. MOCK tokens/API cost remain unavailable.

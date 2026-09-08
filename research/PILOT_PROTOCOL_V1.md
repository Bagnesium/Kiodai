# First development day pilot v1

Frozen on 2026-09-08 before any genuine Kiodai inference. This is a new, smaller development diagnostic. The original `EXPERIMENT_PREREGISTRATION_A0_A1.md` and `a0_a1_freeze_manifest.json` remain unchanged.

Selection rule: take the first chronological day, without editing its tasks, observations, updates, lures or scoring rules, from `data/development/prospective_memory_dev_v1.json`. The whole development scenario's new padded maximum-growth estimate exceeds $0.30; the first day fits. This is a cost-driven choice, not selection by observed model performance. Exact source, scenario and configuration hashes are frozen in `pilot_freeze_v1.json`. Demo cases remain separate.

A0/A1 use the recovered frozen prompts and unchanged generation/tool settings. Run one repeat, seed 20260904 where supported. Order A0 then A1 at each supplied interaction step; no state is shared. Runtime `pair.json` records actual order, hashes, route metadata and output directories before inference. Two eight-step trajectories require 16 minimum calls and at most 64 billable attempts with one query per step and one retry per interaction. Cost ceiling: $0.30 shared across the pair. Conservative maximum-growth reservation: approximately $0.137 at the frozen prices, not an actual bill.

Stop on insufficient budget, route/model mismatch, unavailable credentials, failed route preflight, repeated transport failure, or user interruption. Invalid model output gets one schema-only corrective retry then no task action, without exclusion. No live-to-mock fallback. Keep partial runs and incomplete pairs visible. No billable preflight or additional monitoring calls.

Primary analysis: report each full trajectory's TP/FP/FN, precision, recall, Set-F1 and A1 minus A0 Set-F1. Report all lifecycle failures, parsing failures, retries, queries, latency, tokens and cost alongside scores. Undefined metrics remain unavailable. With future repeats, first average repeated differences within this same scenario. Do not count its steps as independent samples. This one-scenario pilot uses descriptive analysis and has no success threshold or significance claim. The original full-suite thresholds are not applicable to this subset.

A negative or mixed result is valid. Do not modify P1 from pilot/final-week failures and keep calling it the same frozen intervention. Any later prompt would need a new version and a fresh evaluation design. The pilot does not evaluate all original cases, cross-day retention, broad generalization or final-week PM-Bench performance.

Command, only after explicit spending authorization and a locally set key:

```bash
python3 scripts/run_paired.py --suite pilot --live --budget-usd 0.30 --repeats 1
```

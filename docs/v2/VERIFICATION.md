# Verification and executed evidence — 9 September 2026

**98 tests passed**: the original 62 plus 36 v2 tests. **164 protected-file hashes passed**. The 404-file historical baseline inventory also passes; the only change to an original file is the explicitly appended v2 claims section. Python compilation, JavaScript syntax, the existing smoke command and frozen v2 preflight passed. Logs: `artifacts/verification/v2-final/`.

The tests cover atomic cited extraction, multiple intentions, ambiguous updates, cancellation/rescheduling, version-safe checks, dependencies, negative/near-match events, hidden false→true state, hidden-clock queries, stale evidence, query limits/grouping/rotation, success/failure/uncertainty, restart/idempotency, full agent/evaluator isolation, independent run state, inference modes, cumulative reservations, malformed retries, interrupted artifacts and report pairing. The interrupted local smoke exposed a partial-scoring finalizer bug; the fix has a regression test and does not impute missing actions.

The exact frozen command `python3 scripts/run_v2.py --mock` completed 36 method-trajectories and 288 steps. The full path ran through observation, extraction, SQLite updates, channel queries, action binding, native simulator execution, receipt updates, the unchanged official scorer and saved-artifact reporting.

| MOCK only | Trajectories | TP | FP | FN | Set-F1 | Fixture model calls | Tool queries |
|---|---:|---:|---:|---:|---:|---:|---:|
| A0 | 12 | 24 | 0 | 0 | 1.00 | 117 | 21 |
| B_ledger | 12 | 24 | 0 | 0 | 1.00 | 213 | 21 |
| A2 | 12 | 24 | 0 | 0 | 1.00 | 192 | 21 |

Both mean paired Set-F1 differences are zero. These are **restricted-language mock fixtures**, not model accuracy results. Six hidden due opportunities per method were query-supported in the complete mock traces. No baseline was scripted to lose. The complete native results, per-trajectory paired differences, raw requests/responses, observations, private evaluator records and SQLite states are under `results/v2/mock-verification-v2/`. `report.json` and `report.md` regenerate from saved raw artifacts with no inference.

All earlier development attempts remain: `results/v2/development/initial-mechanics/` includes shared-fixture false positives on the override instruction; `verified-mechanics/` records the corrected restricted grammar. These were software development fixes, not tuning against a live comparative result. The first cooling-only regression failed to bind its paraphrased action label and missed the action even after querying. It remains under `results/v2/known-cooling-regression/`. The corrected fixture, under `known-cooling-regression-v2/`, runs the intact original 20-step story: the positive reading at checkpoint 13 supports the cooling hit, with TP1/FP0/FN10 overall and five queries. It does not model other task semantics or claim comparative accuracy.

The **real local smoke** used the already installed `llama3.2:latest` through Ollama 0.17.5 on loopback, with backend digest preserved in `results/v2/local-smoke-v2/local_backend.json`. It had four extraction attempts: two invalid source citations, a truncated malformed output at 3,072 output tokens, then a 120-second timeout. Only checkpoint 1/8 completed, with no task action. There is no usable trajectory or primary Set-F1. Three saved responses report 2,618 input and 3,883 output tokens; complete usage is unavailable because the final request timed out. No paid API cost was incurred by this loopback run; API-response cost and verified billing fields remain unavailable, not measured zero. The local daemon was stopped after the attempt. No download, backend substitution in the frozen evaluation, or paid v2 call occurred.

The local run began before the final implementation freeze. `recovery.json` preserves original-file hashes and separately discloses post-hoc artifact finalization; the raw failed responses and interrupted request were not replaced. Source hashes are captured at the start of subsequent runs. This local attempt provides evidence of extraction/formatting and infrastructure failure, not successful model-driven end-to-end operation.

Browser verification opened the existing-style read-only v2 dashboard, changed trajectory/method/checkpoint, inspected the negative reading at checkpoint 1 and positive reading at checkpoint 7, confirmed actual stored completion receipts, and revealed evaluator annotations separately. The final saved run is served at `http://127.0.0.1:8767/`. The viewer cannot make inference calls. Original A0/A1 recorded replay commands remain unchanged.

Preservation: `artifacts/verification/v2-20260909.zip` and `research/v2/artifact_inventory.json` archive **all** executed v2 attempts. `python3 scripts/restore_v2_artifacts.py` verifies/restores missing artifacts without overwriting different evidence. This preserves local reproducibility, not an independently hosted backup.

Remaining model-evidence blocker: the fixed OpenRouter comparison has not been authorized. Its usage-informed projection is $0.67219, conservative allowance $19.95251712 and proposed explicit ceiling $20.00. Do not transfer unused historical authorization. No v2 superiority claim is ready for submission.

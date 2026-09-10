# v2.1-comparison-v1 — frozen exploratory protocol

**Prepared, not authorized or executed with models.** This is one 12-trajectory, three-method comparison on **exposed synthetic development material**, organized into four template families. It is not an independently held-out benchmark. Deadline: 13 September 2026, Asia/Almaty. No paid or network inference was used in preparation.

The sole comparison manifest is [`research/v2_1/comparison_v1.json`](../../research/v2_1/comparison_v1.json). Candidate behavior remains implementation `959db38dac8b68f63ecf79420dcd53bea2278cf2`. Study support is committed at `832d6ff1e3f43f9086da9d6aac33b79f5212ecdc`. The manifest hashes the candidate, support code, exact scenarios/configuration, prompt/schema definitions, exposure/cost sources and complete preparation recording. Original v2 and smoke freezes are unchanged.

## Question and design

Hypothesis: the bounded monitoring policy may improve timely, query-supported execution and trajectory Set-F1 relative to the same ledger architecture when the model controls queries, with possible query/compute overhead. The primary descriptive contrast is **A2 minus B_ledger**. The secondary contrast is **A2 minus A0**; it compares the complete system and cannot isolate monitoring alone. A zero or negative primary difference is retained as no observed improvement on this set. No significance or general superiority claim is licensed by this small exposed design.

| Method | Frozen behavior |
|---|---|
| A0 | Existing baseline prompt and action selector; no explicit intention extraction/ledger input. The implementation produces an empty store artifact, not an extraction score. |
| B_ledger | v2.1 extraction, Store, quarantine, lifecycle and selection; model decides whether/when to query. |
| A2 | The same components and prompts; the existing bounded controller chooses queries at shared checkpoints. |

Each method starts with a new agent, empty store, gateway sequence, environment and history for each trajectory. All receive the same initial instructions, available channels/tools, decision checkpoints, visible-time policy and one-query-per-checkpoint allowance. They retain their own full received history and documented simulator receipts. Their later histories may differ through legitimate queries and actions; discoveries are not shared across runs. Heartbeat remains disabled, with no extra A2 decision opportunities.

Both ledger methods load `prompts/v2_1/extract.txt`, `prompts/v2_1/select.txt` and the shared schema/Agent/Store/Gateway implementation. No semantic rule, quarantine behavior, retry, monitoring, execution, scoring or model setting changed. In particular, the observed prerequisite omission is a behavior to measure, not silently fixed before comparison.

This is **not compute-matched**. A0's unchanged output cap is 256; ledger selection is 1,536 and extraction 3,072. Every checkpoint permits one extraction for ledger methods and a selection, plus an extra model selection after a model-chosen query for A0/B_ledger. Each call allows one validation retry. A2 controller queries do not themselves invoke a model. All internal calls and costs are counted.

## Cases, exposure and execution order

All twelve cases from the existing `data/v2/catalog.json` are retained, with one repeat: **36 method-trajectories, 12 matched triples, 288 checkpoints**. Each trajectory contains eight checkpoints. Cross-day cases span two days; the other families span one. No new benchmark or case selection occurred.

Seed **20260910** determines a shuffled family order, shuffled variants within each family and an initial method permutation. The existing executor rotates that permutation by trajectory index. Each method occupies each execution position once within every family and four times overall. These are three cyclic orders, not all six possible method permutations; position is balanced but all possible carryover orders are not.

| Block | Trajectory | Method order |
|---:|---|---|
| 1 | v2_hidden_91320 | A2 → B_ledger → A0 |
| 2 | v2_hidden_91321 | B_ledger → A0 → A2 |
| 3 | v2_hidden_91322 | A0 → A2 → B_ledger |
| 4 | v2_visible_events_91310 | A2 → B_ledger → A0 |
| 5 | v2_visible_events_91311 | B_ledger → A0 → A2 |
| 6 | v2_visible_events_91312 | A0 → A2 → B_ledger |
| 7 | v2_cross_day_91331 | A2 → B_ledger → A0 |
| 8 | v2_cross_day_91332 | B_ledger → A0 → A2 |
| 9 | v2_cross_day_91330 | A0 → A2 → B_ledger |
| 10 | v2_revision_91301 | A2 → B_ledger → A0 |
| 11 | v2_revision_91302 | B_ledger → A0 → A2 |
| 12 | v2_revision_91300 | A0 → A2 → B_ledger |

All twelve were authored/inspected during development and appear in the original initial-mechanics, verified-mechanics and full MOCK recordings. `v2_hidden_91320` additionally appears, with identical scenario bytes, in the failed v2 network smoke, successful v2.1 network smoke, interrupted local-model smoke and v2.1 repair fixture. The manifest records exact overlap paths and hashes. Predeclared descriptive breakdowns show this one previously network-smoke-tested case separately from the other eleven. Those eleven are still exposed; renamed variants do not create twelve independent task families.

## Configuration and interruption rules

Pinned OpenRouter model `deepseek/deepseek-chat-v3.1`, Novita only, fp8, no fallback, `require_parameters=true`, reasoning disabled/excluded; temperature 0, top_p 1, generation seed 20260904. Timeout 120 seconds, one validation retry, zero transport retries. Full-history policy, unchanged 65,536 runtime context limit and 48,000 serialized request-byte gate; no truncation to force completion.

The manifest records each trajectory's rendered baseline and ledger-selection system-prompt hashes, shared extraction schema, binding template and action-schema template hashes. Runtime schema enums depend only on each method's offered handles/channels and eligible ledger records; exact schemas, messages and responses are logged per attempt.

The launcher reuses `scripts/run_v2.py:execute` and `kiodai_v2.runner.run_case`. Its only executor binding change supplies the new manifest path instead of the historical freeze. Agent code is unchanged. Additional comparison reporting happens after execution, outside the agent boundary.

Validation failures get the existing single corrective retry, then an explicit fail-closed checkpoint with no task action. A transport/runner interruption stops the entire study, retains all partial files and unknown-cost reservations, and withholds unavailable primary values. No supported resume, fresh-output restart, selective rerun or extra repetition exists. An interrupted process may leave status `running`; that is incomplete evidence, not permission to restart. The fixed LIVE directory prevents a second invocation. The final report retains all 36 planned units, including unstarted or invalid artifacts.

Technical completion requires 36 scoreable trajectories, matching frozen hashes, reproducible official scoring and complete call/receipt/accounting records. Unexpected failures remain visible and are not removed to improve results. A complete run with poor performance is still reportable.

## Analysis fixed before inference

The headline is the **arithmetic mean of twelve per-trajectory Set-F1 differences, A2 minus B_ledger**. A2 minus A0 is separate. The declared mean is unavailable until the study and all declared pairs are complete with defined values. Available-pair diagnostics are explicitly labeled; missing or undefined scores are never zero-filled.

The report includes every trajectory, all four family summaries, the smoke-overlap split, and descriptive micro totals: sum unchanged official TP/FP/FN across complete cases, then calculate precision/recall/Set-F1 from those totals. Coverage is shown; micro totals do not replace the headline. Official zero-denominator conventions remain null/undefined. Checkpoints, calls and near-identical variants are not independent replications; no significance/equivalence test or post-hoc metric switching is planned.

Per method-trajectory: official task metrics; executions and successful/failed simulator receipts; false/canceled/updated-task actions; official commission and dependency violations; superseded ledger versions; queries, hidden opportunities and evidence categories; extraction/selection structural/application failures; retries, fail-closed outcomes, calls, input/output tokens, latency, API-reported cost and accounting completeness. Native completed handles disappear, so independent duplicate side effects are **unidentifiable**, not asserted to be zero. Semantic stale instructions and wrong action bindings require manual review.

Dependency diagnostics separately report total instructed obligations, unique obligations ever due, obligations blocked at a trigger opportunity by an unmet prerequisite, completed obligations, unfinished obligations including/excluding canceled ones, and cancellation counts. These use saved actions and unchanged evaluator helpers after the run. They do not replace the official score. Never-due obligations remain distinct from successful completion.

Hidden behavior distinguishes same-checkpoint relevant-query-supported hits, legitimate visible-supported hits, hits without identifiable support, misses and false actions. Evidence matching identifies support, not causal reliance by the model. Report query cost and a manual necessity assessment. A negative check or a query without an immediate hit is not automatically unnecessary; seven checks are not automatically better than one effective check.

**Semantic extraction review is separate for B_ledger and A2; A0 is not applicable.** A generated `semantic_review_template.json` retains all 24 ledger cases with pending status and no implied zero error count. Review every instruction, checkpoint, accepted/rejected draft and action binding for missing intentions/prerequisites/required fields, incorrect triggers/bindings, unsupported intentions and unresolved/quarantined records. Record repairing revisions too. Findings require reviewer, source references, first defect checkpoint and optional repair checkpoint. The report computes repair timing relative to the run's first official due checkpoint; never-due tasks have null timing, and strict earlier-checkpoint repair is distinguished from repair by the due decision. Valid JSON or quotations do not certify semantics. Annotations stay outside agent inputs and do not change scoring.

## Budget and authorization

| Method | Usage-informed estimate | Retry-heavy sensitivity | Conservative allowance |
|---|---:|---:|---:|
| A0 | $0.068613 | $0.394425 | $5.18111232 |
| B_ledger | $0.341188 | $2.428526 | $8.80386048 |
| A2 | $0.302297 | $1.749425 | $5.96754432 |
| Complete study | **$0.712098** | **$4.572376** | **$19.95251712** |

Recommended fresh authorization: **$20.00 cumulative**, one execution of this protocol. This is the authorized ceiling the guard needs; expected spend is not $20. There is no new monetary cap from the user requiring a smaller design.

The estimate uses each method/trajectory's complete MOCK request and response sizes, including its own growing history and query cycles. Kind-specific token/byte ratios come from the successful v2.1 smoke for extraction/selection and the historical A0 follow-up for baseline calls. Assumptions: 1.35 input and 1.20 output growth margins, no cache discount, selection retries at 1/8 initial calls as observed in the successful smoke, zero extraction/baseline retries in the point estimate. Output estimates remain bounded by existing caps. B_ledger has no genuine v2.1 calibration, and fixture language/queries differ from model behavior; this is a planning estimate, not a guaranteed statistical expectation.

Sensitivity allows a query at every A0/B_ledger checkpoint and a retry at every internal call, with full output caps and prior-response/feedback growth. It covers **1,344 attempts**. The conservative guard assumes 48,000+1,024 input tokens and full output allowances for each possible attempt. At 96 checkpoints per method, A0 reserves for four baseline attempts/checkpoint; B_ledger for two extraction plus four selection attempts; A2 for two extraction plus two selection attempts. Recalculation happens to equal the historical allowance because these caps and checkpoint counts are unchanged; the old $1.03943 projection was not reused.

Preflight requires sufficient ceiling for the entire worst-case study. The existing executor also checks that each next complete matched block fits the remaining allowance, then reserves each attempt durably before sending it. Reservations are never refunded. Unknown charges stay reserved; no restart resets the allowance. The planning maximum MOCK request was 21,212 bytes, but longer real responses can still exhaust the byte gate and interrupt the study. Metadata/route/price availability is rechecked only after fresh LIVE authorization; no billable credential or capability probe was run. Endpoint acceptance was observed in the smoke, but enforcement of every schema keyword remains unverified. Independent billing is unavailable unless separately obtained later.

## Verification and commands

**162 tests pass and all 164 protected hashes pass.** Compilation passes. The full unchanged-fixture MOCK execution completed **36/36 method-trajectories, 288 checkpoints, 522 fixture requests/responses and 63 queries**, with no network or model inference. Shared v2.1 loading, balanced order, fresh state, public observation boundary, all internal call accounting, unavailable real token/cost fields and MOCK replay labels were verified. Failure-injection tests retain interrupted/unstarted units and null primary results. The report regenerates exactly. All twelve baselines have extraction marked not applicable; all 24 ledger semantic reviews remain pending. These are software checks, not comparative model results.

Artifacts: [`results/v2_1/comparison-preparation-v1/`](../../results/v2_1/comparison-preparation-v1/), [derived MOCK report](../../results/v2_1/comparison-preparation-v1/comparison_report.md), and [`artifacts/verification/v21-comparison-preparation/`](../../artifacts/verification/v21-comparison-preparation/). The full MOCK execution preceded final manifest creation to supply costing data; its recorded specification and source hashes match the final freeze. Existing successful/failed smokes and historical A0/A1/local/MOCK recordings remain unchanged and usable. No new smoke experiment ran.

Free preflight, with no credentials or network:

```bash
python3 scripts/run_v21_comparison.py --preflight
```

**Proposed LIVE command — NOT AUTHORIZED:**

```bash
python3 scripts/run_v21_comparison.py --live --authorize-study v2.1-comparison-v1 --budget-usd 20.00 --env-file .env
```

The sole future LIVE output is `results/v2_1/comparison-v1/`, currently absent. MOCK cannot use that path. All original requests/responses, actions before/after handle mapping, failures/retries, manifests, databases, receipts, scores and costs are retained. After any future run, saved reporting can be reproduced without inference:

```bash
python3 scripts/report_v21_comparison.py --study results/v2_1/comparison-v1
```

Supply a separately completed copy of the review template using `--annotations PATH` to create additional reviewed reports; original traces and reports remain unchanged. The existing viewer can replay the future LIVE artifact as RECORDED with inference disabled.

Authorization message:

> I authorize exactly v2.1-comparison-v1 once, with a cumulative paid-inference ceiling of $20.00, following its frozen 12-trajectory A0/B_ledger/A2 protocol. Run the existing preflight first. No prompt or configuration changes, selective reruns, or additional experiments afterward. Preserve all outputs and interrupted attempts.

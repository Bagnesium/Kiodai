# Genuine v2.1-comparison-v1 results — 11 September 2026

The frozen comparison completed all 36 method-trajectories, 288 checkpoints and 12 matched blocks. Kiodai A2 did not outperform either comparator: mean paired trajectory Set-F1 difference was -0.330556 versus B_ledger and -0.383730 versus A0. This is negative comparative development evidence, with working integration in some traces; it does not establish general inferiority, equivalence, reliability or held-out performance.

## Execution, authorization and preservation

The exact authorized command ran once from a clean checkout at `cd0ce89e10d036918d1af06e5f5f2140930a0981`:

```bash
python3 scripts/run_v21_comparison.py --live --authorize-study v2.1-comparison-v1 --budget-usd 20.00 --env-file .env
```

Started 2026-09-11T07:57:27.608Z; finished 2026-09-11T09:11:23.296Z. Candidate `959db38dac8b68f63ecf79420dcd53bea2278cf2`, support `832d6ff1e3f43f9086da9d6aac33b79f5212ecdc`, and manifest SHA-256 `bfaf52df48553e35978f39f406fd5eb3d78c918a5ac2713a0a169746f23036d5` remain unchanged. The exact free preflight passed. Read-only funding checks at 07:57:12 UTC found $21.85988004 remaining key allowance and $21.92988004 account credit, both above the frozen $19.95251712 requirement. No account setting was changed. The earlier funding-blocked attempt made zero model calls; this was the first actual execution.

The 59 frozen source/config/scenario files, 442 preparation records and 65 provenance records match. Every recorded request matches the pinned configuration, and every response reports the pinned DeepSeek V3.1 model and Novita provider. No fallback occurred. Provider enforcement of every schema or sampling parameter remains unverified. Maximum serialized request size was 21,460 bytes versus the frozen 48,000-byte gate. Saved requests contain no canonical private scenario/evaluator identifiers or due-set fields. All official scores, case hashes, complete eight-checkpoint traces, frozen method order and accounting entries reproduce. No source, prompt, scenario, retry or scorer was changed; no failure was excluded, no run restarted, no selective repeat or extra inference occurred.

All **445 original runner files** were archived and hash-verified before adding post-hoc annotations. Original reports and raw traces remain intact. The frozen specification retains its historical preparation-time authorization/status fields; actual authorization and execution are documented separately. Historical smokes, preparation outputs, A0/A1 studies and the prior funding-block record remain historical evidence, not independent repeats pooled into this study.

## Primary results

| Method | TP | FP | FN | Micro precision | Micro recall | Micro Set-F1 | Mean trajectory Set-F1 |
|---|---|---|---|---|---|---|---|
| A0 | 22 | 6 | 2 | 0.7857 | 0.9167 | 0.8462 | 0.8643 |
| B_ledger | 18 | 4 | 3 | 0.8182 | 0.8571 | 0.8372 | 0.8111 |
| A2 | 12 | 5 | 7 | 0.7059 | 0.6316 | 0.6667 | 0.4806 |

The headline uses the **arithmetic mean of twelve paired trajectory Set-F1 differences**, not a difference of micro scores: **A2 − B_ledger = -0.330556**, secondary **A2 − A0 = -0.383730**. Coverage is 12/12 for both. A2 wins 2, ties 4 and loses 6 pairs against B_ledger; it wins 2, ties 3 and loses 7 against A0. These are descriptive counts, not independent significance tests. The micro metrics sum unchanged official TP/FP/FN first; their different denominators and weighting do not replace the frozen estimand.

| Trajectory | A0 F1 | B_ledger F1 | A2 F1 | A2 − B_ledger | A2 − A0 |
|---|---|---|---|---|---|
| v2_hidden_91320 | 1.0000 | 0.6667 | 0.0000 | -0.6667 | -1.0000 |
| v2_hidden_91321 | 1.0000 | 1.0000 | 0.5000 | -0.5000 | -0.5000 |
| v2_hidden_91322 | 1.0000 | 0.6667 | 1.0000 | 0.3333 | 0.0000 |
| v2_visible_events_91310 | 0.5000 | 0.8000 | 0.8000 | 0.0000 | 0.3000 |
| v2_visible_events_91311 | 0.5000 | 0.8000 | 1.0000 | 0.2000 | 0.5000 |
| v2_visible_events_91312 | 0.8000 | 0.8000 | 0.8000 | 0.0000 | 0.0000 |
| v2_cross_day_91331 | 0.5714 | 0.0000 | 0.0000 | 0.0000 | -0.5714 |
| v2_cross_day_91332 | 1.0000 | 1.0000 | 0.0000 | -1.0000 | -1.0000 |
| v2_cross_day_91330 | 1.0000 | 1.0000 | 0.0000 | -1.0000 | -1.0000 |
| v2_revision_91301 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 |
| v2_revision_91302 | 1.0000 | 1.0000 | 0.0000 | -1.0000 | -1.0000 |
| v2_revision_91300 | 1.0000 | 1.0000 | 0.6667 | -0.3333 | -0.3333 |

Per-trajectory TP/FP/FN, precision, recall, costs, failures and receipts are in `results/v2_1/comparison-v1/comparison_report_reviewed.json` and the original generated comparison table.

## Predeclared family and exposure breakdowns

Each family has three exposed variants. Entries below are mean trajectory F1, not micro F1.

| Family | A0 | B_ledger | A2 | A2 − B_ledger | A2 − A0 |
|---|---|---|---|---|---|
| cross_day | 0.8571 | 0.6667 | 0.0000 | -0.6667 | -0.8571 |
| hidden | 1.0000 | 0.7778 | 0.5000 | -0.2778 | -0.5000 |
| revision | 1.0000 | 1.0000 | 0.5556 | -0.4444 | -0.4444 |
| visible_events | 0.6000 | 0.8000 | 0.8667 | 0.0667 | 0.2667 |

A2's small visible-event advantage occurred with zero tool queries in that family; it is not evidence that polling caused the improvement. Cross-day performance was zero in all three A2 cases, while B_ledger completed two and A0 completed the instructed tasks in all three (with false actions in one). Revision failures include abstention after a citation retry and an accepted stale-deadline execution.

| Exposure group | Trajectories | A0 | B_ledger | A2 | A2 − B_ledger | A2 − A0 |
|---|---|---|---|---|---|---|
| Prior smoke overlap | 1 | 1.0000 | 0.6667 | 0.0000 | -0.6667 | -1.0000 |
| Other exposed cases | 11 | 0.8519 | 0.8242 | 0.5242 | -0.3000 | -0.3277 |

The sole smoke-overlap case is `v2_hidden_91320`. The remaining eleven are still exposed development cases. Negative mean differences persist in that predeclared group; this is not a post-hoc exclusion or a held-out test.

## Obligations and execution

| Method | Instructed | Ever due | Dependency-blocked at trigger | Completed | Unfinished incl. canceled | Unfinished excl. canceled | Canceled |
|---|---|---|---|---|---|---|---|
| A0 | 27 | 24 | 0 | 22 | 5 | 2 | 3 |
| B_ledger | 27 | 21 | 3 | 18 | 9 | 6 | 3 |
| A2 | 27 | 19 | 5 | 12 | 15 | 12 | 3 |

Never-due dependent obligations are not successful completions and do not automatically add official FN. In this run the five blocked A2 obligations comprise two hidden sealing tasks and all three cross-day sealing tasks. Canceled obligations explain three legitimate non-completions per method. Official FN counts remain 2/3/7 for A0/B_ledger/A2; active unfinished counts are 2/6/12. Official commission counters are not generic counts of every early action; the complete FP/receipt and updated-task diagnostics are retained.

| Method | Extract schema / application failures | Selection schema / application failures | Extract / selection retries | Accepted operation responses / empty updates | Fail-closed checkpoints | Executions / successful / failed receipts |
|---|---|---|---|---|---|---|
| A0 | N/A | 2 / 0 | N/A / 2 | N/A | 0 | 28 / 22 / 6 |
| B_ledger | 3 / 37 | 18 / 6 | 32 / 24 | 45 / 43 | 8 | 22 / 18 / 4 |
| A2 | 3 / 34 | 6 / 9 | 33 / 13 | 42 / 50 | 6 | 17 / 12 / 5 |

All 602 requests have responses; transport errors and unknown-cost attempts are zero. Total invalid responses are 2/64/52 and retries 2/56/46 for A0/B_ledger/A2. Counts include both initial and second-attempt failures. Accepted empty updates are decisions to make no ledger change; they do not establish correct extraction. The ledger methods each eventually store 27 instructed intentions. A0 has no extraction layer, so its empty store is not a zero-error extraction result.

## Monitoring evidence and its costs

A0 made 15 hidden-board queries and 4 clock queries; B_ledger made 8 board and 3 clock queries; A2 made 18 board queries and no clock queries. Same-checkpoint query-supported hidden hits were **6, 4 and 3**, respectively. A2 additionally had one due hidden miss and one false hidden action. No scored hidden hit lacked identifiable query support. Hidden due opportunities were 6/4/4 and differ because prerequisite failures suppress later due tasks; comparing hit ratios alone would conceal those failures.

A2 made ten more board queries than B_ledger (+125%) and three more than A0 (+20%), yet recorded fewer supported hidden successes. Across all families A2 made seven more queries than B_ledger and one fewer than A0. Manual review identified **4 A0 and 3 B_ledger clock queries** that repeated the already visible current time and stopwatch; no A2 query was demonstrably informationally redundant. All hidden-board checks addressed unfinished obligations. This does not establish optimal polling or prove that negative checks were necessary; the number without an immediate hit is only a proxy. Evidence support is observable, not proof of internal causal reliance.

The methods are not compute-matched. A2 used 17 fewer model calls and $0.01341268 less API-reported cost than B_ledger, despite more queries; B_ledger's query decisions and retries required additional selections. A2 used twice A0's model calls and $0.15823455 more reported cost, with substantially lower mean F1. There is no observed efficiency/superiority claim from these totals.

## Semantic fidelity, independently of task score

All **24/24 ledger cases** and all **12 A0 behavioral traces** were reviewed using saved instructions, every response draft, checkpoint snapshots, bindings and receipts. No case remains unreviewed. Review is AI-assisted and has no independent human annotator; internal understanding and causal explanations remain uncertain. Source-linked annotations and repair timing are in `semantic_review.json` and `comparison_report_reviewed.json`.

| Post-hoc annotation category | B_ledger | A2 |
|---|---|---|
| missing_intention | 10 | 6 |
| missing_prerequisite | 6 | 6 |
| missing_required_field | 2 | 0 |
| incorrect_trigger | 6 | 7 |
| incorrect_binding | 1 | 2 |
| unsupported_intention | 5 | 5 |
| other | 1 | 0 |

These are annotation findings, **not independent error trials or an error-rate comparison**. Layers distinguish 10/6 absent stored intentions after rejected batches, 15/12 accepted representation findings, 1/2 accepted binding findings, and 5/5 rejected unsupported-intention proposals for B_ledger/A2. A2 also has one explicitly labeled intermediate regression repaired within an atomic transaction before any selector sees it. Composite predicate loss counts once; repeated unsupported proposals count by checkpoint. Invalid draft fields and retries have separate raw-attempt counts above.

- In all six dependency-bearing cases per ledger method, initial structured prerequisite information was incomplete. Some records incorrectly became eligible with empty dependencies; others were safely quarantined as unknown but omitted the required unresolved-prerequisite text from `condition`, even though their source quotations retained it. Initial quarantine itself is not an error. Repairs and delays are explicitly recorded.
- Both methods proposed five unsupported spare-sample obligations from action menus. All ten proposals were rejected; **zero unsupported/distractor intentions were stored**. This does not mean distractor execution was impossible: both ledger methods bound a spare-sample handle to the genuine registration intention in cross-day 91331 and attached its failed receipt to that real record.
- Accepted cue regressions affected two A2 and all three B_ledger visible-event cases, restoring a superseded lantern cue after a triangle update. Premature sealing received failed receipts; subsequent correction sometimes yielded a final high score.
- All three revision variants in both ledger methods had accepted deadline regressions. A2 91300 had a second regression that caused a premature registration before successful repair; all sixteen model responses in that case passed validation. A2 91302 also regressed and immediately repaired within a single later transaction; that intermediate value was not a selector input.
- B_ledger 91322 canceled registration based only on the clock, without a cancellation instruction. A2 91321 accepted a sealing handle bound to the registration intention after rejecting the ineligible sealing ID. Correct citation spans and valid versions did not establish correct action identity.
- Quarantine appeared in 5 B_ledger cases (9 checkpoint snapshots) and 2 A2 cases (2 snapshots); no final record remained quarantined. That is not proof that all obligations were completed or all earlier representations faithful. Repairs for never-due tasks have undefined pre-due timing. In A2 cross-day 91330/91332 and revision 91302, a correct-time selection was rejected for a stale citation and the retry abstained despite correct stored fields.

These observations separate **extraction/storage working in some cases**, **monitoring obtaining relevant observations**, **execution producing genuine simulator receipts**, and **task score**. The integration runs, but its accepted semantics and execution are unreliable on this development set. Receipt-based lifecycle mechanics do not guarantee a correct binding or trigger. Superseded-version rejection is a mechanical invariant; it cannot detect an obsolete instruction stored as a new version. Independent duplicate side effects remain unidentifiable because native completed handles disappear.

## Concrete instruction-to-receipt comparison

In `v2_hidden_91322`, the instruction is to register the cobalt91322 sample at DayOne 10:00, then seal its case when `board_cobalt91322` reports “Cooling is now fully stable,” only after registration succeeds. Archiving the note has the same hidden condition and no registration prerequisite.

A2 stores registration as `i_03f566d207977b50`, sealing as `i_32eed3e206a06cd0`, and archiving as `i_2bb5fdd81f55c08b` at checkpoint 1. Its accepted sealing record incorrectly omits the prerequisite. Checkpoint 2 repairs the dependency while retaining the condition and channel. A stale instruction citation rejects the first registration selection; the allowed retry uses the current time observation and registration receives `simulator_completed`. These are distinct extraction, validation and execution events, despite the final perfect score.

A2 queries the board at checkpoints 1–7. The first six observations say cooling is nearly stable and final stabilization is not complete. At checkpoint 7 (15:00), observation `m28` says “State [board_cobalt91322]: Cooling is now fully stable.” The model binds `task_12` to sealing version 2 and `task_7` to archiving version 1, citing `m28`. Handle mapping produces the two corresponding simulator tasks, both receive `simulator_completed`, and the ledger records completion from those receipts. The saved evidence supports this chain without proving an internal cognitive mechanism.

| Method in this matched block | Queries | Calls | TP | FP | FN | Set-F1 |
|---|---:|---:|---:|---:|---:|---:|
| A0 | 5 | 13 | 3 | 0 | 0 | 1.0000 |
| B_ledger | 2 | 22 | 1 | 0 | 1 | 0.6667 |
| A2 | 7 | 18 | 3 | 0 | 0 | 1.0000 |

A0 registers at checkpoint 2 and obtains the positive board reading at checkpoint 7, also completing all three tasks with fewer queries and calls than A2. B_ledger's rejected early extraction batches delay storage until checkpoint 3, after registration is due. It later cancels its registration record without a cancellation instruction, but obtains the positive board evidence and successfully archives at checkpoint 7. Sealing remains blocked and never adds another official FN. The difference in this block therefore cannot be credited solely to polling frequency: all three methods obtained the positive reading, while extraction and lifecycle behavior differed.

Trace sources: `results/v2_1/comparison-v1/v2_hidden_91322/A2/calls.jsonl` lines 2, 6, 8, 10 and 32; `A2/steps.jsonl` lines 1–7; the matched `A0` and `B_ledger` directories; and the source-linked semantic annotations. Ground-truth task IDs are confined to saved evaluator diagnostics and post-hoc analysis, never used to choose an action.


## Resources and billing status

| Method | Calls | Retries | Input tokens | Output tokens | Recorded call latency (s) | Queries | API-response USD |
|---|---|---|---|---|---|---|---|
| A0 | 117 | 2 | 177,855 | 3,175 | 343.60 | 19 | 0.04047361 |
| B_ledger | 251 | 56 | 910,740 | 44,534 | 2103.46 | 11 | 0.21212084 |
| A2 | 234 | 46 | 843,540 | 42,889 | 1984.12 | 18 | 0.19870816 |

Totals: **602 calls**, **1,932,135 input tokens**, **90,598 output tokens**, **48 tool queries**, and **$0.45130261 API-response-reported cost**. Recorded call latency sums to 4431.18 seconds; wall-clock execution lasted 73 minutes 55.688 seconds. Latency is the sum of recorded calls including failed validation attempts, not a compute-matched efficiency estimate. The durable guard reserved **$9.13802496** under the **$20.00 cumulative ceiling**; reservations are not charges. All response-reported costs reconcile with the ledger; **independently verified billed cost remains unavailable**. Account credit checks before the run are funding evidence, not independent study billing. No remaining credit or unused authorization was spent afterward.

## Relationship to earlier evidence

The failed original v2 DeepSeek smoke had an empty ledger, no queries or receipts and TP0/FP0/FN2 (24 calls, API $0.01525668). The separately frozen v2.1 repair smoke populated three intentions, queried seven times and completed three tasks with Set-F1 1.00 (17 calls, API $0.016737), while still showing prerequisite/predicate defects. Those original files and conclusions remain intact.

On the identical smoke-overlap scenario in this comparison, A2 again scored 0 but with a different trace: three intentions eventually stored, six board queries, and no executed task or receipt because early extraction failures missed registration and later selections failed validation. Thus the repair made integration feasible; the one successful smoke did not establish reproducible task success or robust extraction. This study is not a controlled repair-versus-original causal comparison, and prior smokes are not pooled with its twelve blocks.

## Interpretation and submission scope

The frozen monitoring hypothesis received **no observed improvement** on its declared primary contrast. A2 had lower mean trajectory Set-F1 than both controls, with a small visible-event advantage and negative hidden, cross-day and revision contrasts. Four dependent template families, exposed scenarios, one repeat, full-history access and unequal compute prevent broad generalization, significance, equivalence or intrinsic-memory claims. Checkpoints and model calls are not replications. The contribution is a recorded engineering evaluation with localized failure evidence, not demonstrated A2 superiority or a faithful PIS reproduction.

Manuscript replacement paragraphs and Russian defense: `docs/v2_1/FINDINGS_AND_DEFENSE.md`. The Pages manuscript was not overwritten. Remaining submission work is author review and integration of those paragraphs/tables, consistency of historical/current wording, reference/format checks and final submission export; no additional experiment is proposed or authorized.

## Artifacts, replay and offline reproduction

- Original recording: `results/v2_1/comparison-v1/`; original `comparison_report.json/.md` remain unchanged.
- Reviewed report: `comparison_report_reviewed.json/.md`; source-linked `semantic_review.json`, `baseline_behavior_review.json`; `supplementary_analysis.json` contains reconciled metrics, every validation failure and accounting.
- Original 445-file ZIP: `artifacts/v2_1/comparison_v1_original_run.zip`; SHA-256 inventory: `research/v2_1/live_comparison_v1_inventory.json`. Restore only absent files; refuse to overwrite any differing local bytes.
- Authorization, funding, preflight, offline verification and reproducible analysis helper: `artifacts/verification/v21-comparison-live-20260911/`.
- Prior funding-block documents are retained unchanged in `prior_funding_block_original.zip` and commit `cd0ce89`; its old inventory is commit/archive-bound because current handoff/CLAIMS/V2 status documents necessarily change.

Run from `/Users/bagnesium/Documents/GitHub/Kiodai`:

```bash
python3 scripts/report_v21_comparison.py --study results/v2_1/comparison-v1 --annotations results/v2_1/comparison-v1/semantic_review.json
python3 artifacts/verification/v21-comparison-live-20260911/audit_saved_comparison.py results/v2_1/comparison-v1/semantic_review.json
python3 scripts/run_v21_comparison.py --preflight
python3 scripts/verify_benchmark_integrity.py
python3 -m unittest discover -s tests -v
python3 scripts/serve_v2.py --study results/v2_1/comparison-v1 --port 8772
```

Open `http://127.0.0.1:8772/`. Select any trajectory, method and checkpoint; the existing viewer labels genuine LIVE artifacts **RECORDED**, with inference disabled. Evaluator reveal remains separate. The viewer cannot launch a paid run. Offline verification passed: 162 tests, 164 protected hashes, Python compilation, the free frozen preflight, and 72 recorded-viewer checkpoint checks. Detailed outcomes are recorded under the verification directory; no new smoke was run.

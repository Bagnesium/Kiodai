# Current Kiodai handoff — frozen comparison completed

**11 September 2026:** The authorized `v2.1-comparison-v1` ran exactly once, with no implementation or protocol changes, from commit `cd0ce89e10d036918d1af06e5f5f2140930a0981`. All **36 method-trajectories, 288 checkpoints and 12 matched blocks** completed. Mean trajectory Set-F1: **A0 0.864286, B_ledger 0.811111, A2 0.480556**. Frozen primary A2 − B_ledger = **−0.330556**; secondary A2 − A0 = **−0.383730**. A2 did not outperform either comparator in this study. Exposed development scenarios, four dependent families, one repeat, full history and unequal compute limit generalization.

Read [COMPARISON_RESULTS.md](../v2_1/COMPARISON_RESULTS.md) and [manuscript replacement paragraphs / Russian defense](../v2_1/FINDINGS_AND_DEFENSE.md). All 24 ledger cases and 12 baseline traces were reviewed from saved instructions/drafts/bindings/receipts. Both ledger methods stored all 27 intentions eventually; completion was A0 22, B_ledger 18, A2 12. Schema acceptance did not prevent prerequisite, stale-trigger or binding errors. Five unsupported menu-intention proposals per ledger method were rejected; none was stored. A2 made 18 hidden queries for 3 supported hits; B_ledger 8 for 4 and A0 15 for 6. Never-due dependency-blocked obligations remain separate from official FN.

**602 recorded requests/responses**, 1,932,135 input / 90,598 output tokens; API-response cost **$0.45130261**, all known and reconciled. Durable reservations **$9.13802496** under the cumulative **$20.00** ceiling. Independent billed cost is unavailable. Before the run, read-only funding checks showed key allowance $21.85988004 and account credit $21.92988004, covering $19.95251712. The previous funding-blocked attempt made zero model calls.

Genuine recording: `results/v2_1/comparison-v1/`. Original 445 files preserved in `artifacts/v2_1/comparison_v1_original_run.zip`, inventory `research/v2_1/live_comparison_v1_inventory.json`. Source-linked review and supplementary analysis are additional files, not replacements. Authorization, funding evidence and offline verification are in `artifacts/verification/v21-comparison-live-20260911/`. The older funding-block inventory is bound to its original commit and the preserved `prior_funding_block_original.zip`, because current status documents have now changed.

Replay with the unchanged viewer:

```bash
python3 scripts/serve_v2.py --study results/v2_1/comparison-v1 --port 8772
```

Open `http://127.0.0.1:8772/`; select trajectory/method/checkpoint in **RECORDED** mode. Inference is disabled. The original smoke viewer at 8771 is separate. Saved analysis can be reproduced with `scripts/report_v21_comparison.py --study results/v2_1/comparison-v1 --annotations results/v2_1/comparison-v1/semantic_review.json` and the read-only `artifacts/verification/v21-comparison-live-20260911/audit_saved_comparison.py` helper.

**No further model inference is authorized or scheduled. Do not rerun, resume, repair, selectively repeat or launch another experiment. No push.** The completed comparison is the submission evidence. Pages was not overwritten; remaining author tasks are review/integration of the replacement paragraphs and tables, consistency of historical/current claims, references/formatting and final export. Candidate `959db38` and all frozen sources remain unchanged; the manifest retains its historical preparation-time status fields rather than being rewritten after outcomes.

## Historical handoff preserved below

The following text is retained as the previous state. Its “current,” “absent,” “blocked,” and “not yet authorized” statements are historical and are superseded by the completed execution above.

# Current Kiodai handoff — comparison authorized, blocked before inference

**11 September 2026:** The user authorized exactly frozen `v2.1-comparison-v1` once, with a cumulative $20.00 paid-inference ceiling, and required stopping before inference if external funding could not cover $19.95251712. The existing offline preflight passed at `d7e92d38fc333846670ae196c9ee37f9d616f61a`; all 59 frozen source/config/scenario files, 442 preparation files and 65 provenance files matched. No frozen implementation or configuration was changed.

Authenticated read-only OpenRouter key and credit checks returned HTTP 200 at 07:06:07 UTC: **key limit $5.00, remaining key allowance $4.92988004; account credit $9.92988004** ($10.00 credits minus $0.07011996 usage). Both available amounts are below the required conservative allowance. **Stopped before the LIVE command; zero model calls, zero inference tokens, zero paid inference.** Settings and funds were not changed. No interrupted study or reservations exist. `results/v2_1/comparison-v1/` remains absent; 0/36 method-trajectories and 0/12 matched blocks exist. Comparative metrics and semantic review are unavailable, not zero errors or zero task scores.

Read [COMPARISON_FUNDING_BLOCK.md](../v2_1/COMPARISON_FUNDING_BLOCK.md). Sanitized check evidence, authorization and offline verification are under `artifacts/verification/v21-comparison-funding-block-20260911/`. The API account totals are not independent study billing. There is no genuine comparison replay; the previous smoke remains available with the existing RECORDED viewer. No additional inference, automatic retry, account change or push was performed or scheduled.

Authorization is limited to this one frozen study and its stated funding checks; it does not authorize any other inference. This turn stopped at the funding gate. Any user-directed continuation must respect that gate and the existing one-attempt/no-resume policy. The historical preparation handoff below is retained for context; its statements that authorization has not arrived are superseded by this update. The frozen manifest itself retains its original preparation-time fields unchanged.

## Historical preparation handoff — 10 September 2026

Repository: `/Users/bagnesium/Documents/GitHub/Kiodai`. Author: Bagdat Beimzhan. Deadline: **13 September 2026**, Asia/Almaty. Read `AGENTS.md` before work.

Branch: **`codex/kiodai-v2.1-extraction`**. Candidate behavior: **`959db38dac8b68f63ecf79420dcd53bea2278cf2`**, unchanged. Successful smoke executed at `392c58f80b61252759d0eb60df98be6c16d94e47`, preserved at `b1f4a0007003021b16bb50d238192cc063fd2e55`. Comparison support: **`832d6ff1e3f43f9086da9d6aac33b79f5212ecdc`**. The following preparation-evidence commit adds the manifest, protocol, full MOCK recording and this handoff. Prior smoke handoff remains at `b1f4a00:docs/v2/CODEX_HANDOFF.md`.

**No paid or network model inference is authorized. No new model inference ran during comparison preparation.** The user authorized only offline preparation and local commits. Prior spending permissions are exhausted regardless of unused credit. No push, deployment, fresh smoke or selective rerun is authorized.

Read **[COMPARISON_PROTOCOL.md](../v2_1/COMPARISON_PROTOCOL.md)** first. The sole frozen study is **`research/v2_1/comparison_v1.json`**, identifier **`v2.1-comparison-v1`**: 12 existing trajectories, four template families, A0/B_ledger/A2, one repeat, 36 method-trajectories, 288 checkpoints. Primary contrast: A2 minus B_ledger paired trajectory Set-F1; secondary: A2 minus A0. All cases are exposed development material. Only `v2_hidden_91320` overlaps the genuine/local smokes; the other eleven are not blind. Family and overlap breakdowns are predeclared.

## What is frozen

No candidate extraction/schema/prompt, semantic/quarantine rule, monitor, retry, lifecycle/execution behavior, provider/model or official scorer changed. New code only wraps the existing executor and analyzes saved outputs. Both ledger conditions still load the same repaired v2.1 modules and prompts.

- `scripts/run_v21_comparison.py`: named authorization/ceiling gates, seeded complete catalog, new manifest path, fixed LIVE output. Reuses `scripts/run_v2.py:execute` and `kiodai_v2.runner.run_case`; no new execution engine.
- `scripts/report_v21_comparison.py`: all planned units including missing/invalid runs, primary paired means, descriptive micro/family/overlap tables, dependency/hidden/evidence diagnostics and manual semantic-review queue.
- `scripts/prepare_v21_comparison.py`: offline exposure audit, successful-smoke/historical-baseline cost calibration, full-MOCK verification and one-time freeze creation. The freeze already exists; do not overwrite it.
- `configs/v21_comparison_v1.json`: existing generation/provider/resource settings; new version and predeclared order only. Order seed 20260910; each method occupies each position once per family. Generation seed stays 20260904.
- `tests/test_comparison_preparation.py`: 16 new tests for scope/order, gates, unchanged candidate, partial reports, dependency denominators, review semantics, zero denominators and durable accounting.

The manifest hashes **59 source/config/scenario files**, **442 preparation recording files**, and calibration/exposure/provenance evidence. The full MOCK run preceded final manifest creation to supply costing data; its source hashes and exact specification match the final freeze. Genuine output `results/v2_1/comparison-v1/` is absent. MOCK cannot use that path. A later LIVE invocation requires a clean checkout, the exact study token and $20.00 cap. No supported resume exists; an interrupted directory is not permission to restart. Preserve partial evidence and reserved unknown charges.

## Offline verification and cost

**162 tests pass, 164 protected hashes pass, compilation passes.** Full existing-fixture MOCK: **36/36 method-trajectories, 288 checkpoints, 522 requests/responses, 63 queries**. State reset, shared repaired loading, public payload boundaries, order, accounting, reporting and MOCK labels verified. All 24 ledger semantic reviews remain pending; A0 extraction is not applicable. No correctness claim from valid JSON or mock outcomes.

Evidence: `results/v2_1/comparison-preparation-v1/`, including `comparison_report.json/.md`, `semantic_review_template.json` and raw case files; verification logs under `artifacts/verification/v21-comparison-preparation/`. The read-only preflight passes with zero network requests/model calls. Original 40 candidate hashes, 404 historical baseline files, 1,355 local/MOCK archived files, both genuine smokes (24 original v2 files and 20 original v2.1 files), and original execution source hashes remain verified. No historical freeze or result was rewritten.

Usage-informed estimate **$0.71209837**, retry-heavy sensitivity **$4.57237647**, conservative allowance **$19.95251712**. Recommended complete-study cumulative ceiling **$20.00**. These are not charges. Guard covers 1,344 attempts; it requires full-study feasibility, then checks each matched block and reserves each attempt without refunds. Token/byte calibration, full-history MOCK sizes and assumed retries are uncertain; B_ledger has no genuine v2.1 calibration. Route/pricing metadata will be checked only after fresh authorization; no billable preflight occurred.

## Existing genuine evidence and limitations

Successful v2.1 smoke remains `results/v2_1/deepseek-smoke-v1/`: 8/8 checkpoints; 3 intentions, 7 queries, 3 successful receipts; TP3/FP0/FN0, Set-F1 1.00; 17 calls, 68,964 input / 2,238 output tokens, API-response cost $0.016737. Independent billing unavailable. Sealing initially omitted its prerequisite, then lost known trigger fields during quarantine before repair at checkpoint 4. That defect remains a measurement target, not a silent repair.

The previous failed v2 smoke remains TP0/FP0/FN2, empty ledger, 24 calls and $0.01525668. Dependent sealing never became due there. Both scenarios/scorers are unchanged. Historical A0/A1 studies showed no observed P1 improvement and overlap; do not pool them as independent replications. The existing successful-smoke RECORDED viewer was available at http://127.0.0.1:8771/ and remains separate from MOCK preparation.

## Exact next action

Free/offline:

```bash
python3 scripts/run_v21_comparison.py --preflight
```

**Not yet authorized**:

```bash
python3 scripts/run_v21_comparison.py --live --authorize-study v2.1-comparison-v1 --budget-usd 20.00 --env-file .env
```

The user can authorize by sending:

> I authorize exactly v2.1-comparison-v1 once, with a cumulative paid-inference ceiling of $20.00, following its frozen 12-trajectory A0/B_ledger/A2 protocol. Run the existing preflight first. No prompt or configuration changes, selective reruns, or additional experiments afterward. Preserve all outputs and interrupted attempts.

Stop after preparation. Do not infer approval from the candidate ceiling, key credit, this handoff, or earlier smoke permission. After a future authorized run, use `scripts/report_v21_comparison.py --study results/v2_1/comparison-v1`; manual annotation copies create separate reviewed reports with `--annotations PATH`. Pending reviews are not zero errors; task score is not semantic extraction fidelity.

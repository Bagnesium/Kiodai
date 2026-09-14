# Verification of the completed frozen comparison

The first actual execution of `v2.1-comparison-v1` completed on 11 September 2026. It ran once, from execution commit `cd0ce89e10d036918d1af06e5f5f2140930a0981`, under the user's cumulative $20 authorization. All 36 method-trajectories, 288 checkpoints and 12 matched blocks completed. No inference followed the study. The previous funding-blocked attempt made zero model calls and remains separately preserved.

## Evidence and outcomes

- `authorization.txt`, `preflight.json`, `funding_check.json` and `execution_record.json` preserve the authorization, existing free preflight, read-only funding checks and actual execution. The live command in the execution record is historical evidence, not a replay command.
- `tests.log`: all 162 unit tests passed. `protected_hashes.log`: all 164 protected files passed. `compile.log`: Python compilation exited successfully. `final_preflight.json`: the frozen free preflight passed after reporting.
- `audit_saved_comparison.py` reproduces the supplementary analysis from saved evidence without provider calls. It verifies the original 445-file recording and archive, prior funding-block archive, frozen source/configuration/scenario and provenance hashes, official scoring, method order, pinned requests and reported route, token/cost accounting, and cumulative budget reservations.
- `dashboard_check.json` records 72 first/last checkpoint checks across all 36 cases, plus the successful hidden-condition trace and separate evaluator endpoint. `verification_summary.json` records actual UI inspection in RECORDED mode with inference disabled.
- All 24 ledger cases and 12 baseline behavioral traces were reviewed. Semantic annotations are AI-assisted, with no independent human annotator. No case remains unreviewed; internal understanding and causal explanations remain uncertain.
- The original recording is archived at `artifacts/v2_1/comparison_v1_original_run.zip`, with its separate SHA-256 inventory at `research/v2_1/live_comparison_v1_inventory.json`. Original generated reports and traces have not been replaced by reviewed reports.
- `staged_diff_check.json`: authored documentation and post-hoc artifacts pass the whitespace check. The full check flags one pre-existing trailing space in each of the 36 recorded system prompts; those original hash-verified bytes are deliberately preserved.
- `inventory.json` hashes the intended artifacts and documentation in this completion commit, excluding itself. The containing Git commit identifies the inventory's historical scope; later documentation revisions do not redefine the recorded experiment.

API responses report $0.45130261 across 602 calls. Independently verified billed cost is unavailable. Budget reservations of $9.13802496 are conservative allowances, not charges. No unused authorization was spent afterward.

## Offline reproduction

Run from `/Users/bagnesium/Documents/GitHub/Kiodai`:

```bash
python3 scripts/verify_benchmark_integrity.py
python3 scripts/run_v21_comparison.py --preflight
python3 -m unittest discover -s tests -v
python3 -m compileall -q research_harness kiodai_v2 scripts tests
python3 artifacts/verification/v21-comparison-live-20260911/audit_saved_comparison.py results/v2_1/comparison-v1/semantic_review.json
```

The audit prints reproducible supplementary JSON to stdout. `write_submission_docs.py` regenerates the two new Markdown submission documents from saved reviewed results and the preserved background/trace fragments. It makes no inference calls and does not edit the Pages manuscript.

For recorded replay, use the unchanged viewer:

```bash
python3 scripts/serve_v2.py --study results/v2_1/comparison-v1 --port 8772
```

Open <http://127.0.0.1:8772/> and choose a trajectory, method and checkpoint. `v2_hidden_91322`, A2, checkpoint 7 shows the positive board observation and two successful receipts. Replay is read-only and makes no model calls. The server was left running at completion.

## Reports and submission status

The full report is `docs/v2_1/COMPARISON_RESULTS.md`; source-linked reviewed results are `results/v2_1/comparison-v1/comparison_report_reviewed.json`. Manuscript replacement text and Russian defense are in `docs/v2_1/FINDINGS_AND_DEFENSE.md`. The handoff, `V2.md` and `research/CLAIMS.md` distinguish this result from preserved historical studies. The author still needs to review and integrate the supplied text and tables into Pages, check citations and required formatting, and export the submission. No additional experiment or architecture change is proposed.

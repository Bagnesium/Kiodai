# Current Kiodai handoff — recorded v2.1 smoke

Repository: `/Users/bagnesium/Documents/GitHub/Kiodai`. Author: Bagdat Beimzhan. Deadline: **September 13, 2026**, Asia/Almaty. Read `AGENTS.md` before work.

Branch: **`codex/kiodai-v2.1-extraction`**. Evaluated implementation: **`959db38dac8b68f63ecf79420dcd53bea2278cf2`**. Smoke execution commit: **`392c58f80b61252759d0eb60df98be6c16d94e47`**. The subsequent evidence commit only adds the recording, read-only analysis and documentation. The prior preparation handoff remains at `392c58f:docs/v2/CODEX_HANDOFF.md`.

The user explicitly authorized exactly one `v2.1-deepseek-smoke-v1` with a cumulative $1.00 ceiling. It **ran once and completed** after the existing preflight, without modifying the frozen implementation/configuration/prompts/scenario/retries/evaluator/manifest. **No additional paid inference, selective rerun, full study, push or deployment is authorized.** Existing key credit and unused budget authorize nothing further.

Read **[the live smoke report](../v2_1/DEEPSEEK_SMOKE_RESULTS.md)** first, then [the repair report](../v2_1/EXTRACTION_REPAIR.md) for implementation details. The prepared manifest `research/v2_1/smoke_v1.json` stays unchanged, including its historical preparation-time status. Later authorization and preservation are recorded separately in `research/v2_1/live_smoke_v1_inventory.json`.

## Actual result

`results/v2_1/deepseek-smoke-v1/`: genuine LIVE, displayed as RECORDED. **8/8 checkpoints; 3 intentions stored; 3 creates + 2 revisions; 5 accepted empty updates; 0 extraction validation failures; 0 distractor proposals/stored intentions; 1 selection validation failure, corrected by the single retry; 7 queries; 3 task executions and successful receipts.** All three intentions completed. Official **TP3/FP0/FN0, precision/recall/Set-F1 1.00**. Seventeen calls, 68,964 input / 2,238 output tokens, API-response cost **$0.016737**, reservations **$0.26342016**, no unknown-cost attempts. Independent billing unavailable.

Do not equate the perfect score with perfect extraction. Sealing v1 omitted its dependency at checkpoint 1; at checkpoint 2 the model added registration's ID but dropped known trigger fields and quarantined v2. Checkpoint 3's empty update retained that defect. Checkpoint 4 restored a complete hidden trigger with the dependency at v3. Registration completed at checkpoint 2; sealing and archive at checkpoint 7. The selection retry corrected a stale `m1` citation to current `m6`. All intermediate errors remain in the original files.

This resolves the previous empty-ledger bottleneck and demonstrates narrow integration feasibility. It does not establish reliability, dependency fidelity throughout, provider enforcement of every schema keyword, or A2 superiority over A0/B_ledger. The recommendation is to freeze this implementation for comparison with semantic-field errors measured alongside task score; a new matching comparative freeze and fresh spending authorization are still required. Do not tune/select evaluation cases based on whether A0 loses.

## Implementation and evidence map

- `kiodai_v2/contract.py`, `common.py`, `store.py`, `agent.py`: shared schema/context validation, atomic batches, dependencies/version/receipt constraints, eligible binding IDs. Semantic entailment remains model-dependent.
- `prompts/v2_1/` and `gateway.py`: revised extraction/selection instructions, specific bounded feedback and explicit outcome metadata. Shared B_ledger/A2 repair; monitoring distinction remains narrow.
- `scripts/run_v21_smoke.py`: existing engine, frozen one-smoke scope; its live output already exists and must not be restarted.
- `scripts/analyze_v21_smoke.py`: post-run read-only archive/report/accounting/trace analysis. Outputs JSON to stdout, makes no inference calls, never rewrites original reports.
- `results/v2_1/deepseek-smoke-v1/analysis.json`: reproducible derived analysis; original raw files and reports unchanged.
- `artifacts/verification/v21-deepseek-smoke-v1-20260909.zip`: all 20 original output files captured before analysis, inventory in `research/v2_1/live_smoke_v1_inventory.json`.
- `results/v2_1/deepseek-smoke-v1/verification/`: post-run test and integrity records.

**146 tests pass; 164 protected hashes pass; compilation and original free MOCK smoke pass.** Forty v2.1 frozen files match. Historical preservation checks retain 404 baseline files, 1,355 local/MOCK archive files, 24 original DeepSeek archive files and 59 original source paths at their execution commit. Original freezes and failed artifacts are unchanged; CLAIMS gains an append-only entry.

The previous genuine v2 smoke remains `results/v2/deepseek-smoke-v1/`, execution commit `a754559351ba017bb4fc00aa5e0527ea68d05572`: 8/8 checkpoints, TP0/FP0/FN2, empty ledger, no queries/actions/receipts, 24 calls, 8 retries, $0.01525668 API-response cost. The score denominator differs because only v2.1 completes registration, making dependent sealing due. Historical A0/A1 studies found no observed P1 benefit and overlap; never pool them as independent replications.

## Read-only commands

```bash
python3 scripts/analyze_v21_smoke.py > /tmp/kiodai-v21-recorded-analysis.json
python3 scripts/run_v21_smoke.py --preflight
python3 scripts/verify_saved_smoke.py --historical-sources
python3 scripts/verify_benchmark_integrity.py
python3 scripts/serve_v2.py --study results/v2_1/deepseek-smoke-v1 --port 8771
```

The RECORDED dashboard was started at **http://127.0.0.1:8771/**, with inference disabled. Inspect checkpoints 1, 2, 4 and 7. The prior v2 recording can be served separately on port 8768. Original full-v2 preflight correctly rejects changed v2.1 sources; do not rewrite old hashes. No comparative run has been launched. The next research step is a separately reviewed matching freeze, not more smoke inference.

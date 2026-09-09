# Current Kiodai handoff — v2.1 extraction repair

Repository: `/Users/bagnesium/Documents/GitHub/Kiodai`. Author: Bagdat Beimzhan. Deadline: **September 13, 2026**, Asia/Almaty. Read `AGENTS.md` before work.

Branch: **`codex/kiodai-v2.1-extraction`**. Implementation: **`959db38dac8b68f63ecf79420dcd53bea2278cf2`**. The documentation/manifest commit follows it; resolve its hash with `git log -1 --format=%H`. Initial checkout `6e1c25e` was clean; there were no unrelated user edits. The earlier detailed handoff remains at `6e1c25e:docs/v2/CODEX_HANDOFF.md`.

The requested repair is implemented and verified offline. **No new model inference ran.** Exactly one intact A2 smoke is prepared but not authorized. Existing credit, `.env` credentials and historical approvals authorize no spending. No full study, push or deployment is authorized.

Read **[the repair report](../v2_1/EXTRACTION_REPAIR.md)** first for request IDs, old/new behavior, test evidence, remaining uncertainty and costs. The new manifest is **`research/v2_1/smoke_v1.json`**; its 40 source/config/scenario/test hashes match the implementation commit.

## Implementation map

- `kiodai_v2/contract.py`: shared extraction schema and obligation-provenance routing. Time-only conditions may be null with stated day/time; event/hidden predicates must be nonblank; unknowns are quarantined. Operation shapes are explicit.
- `common.py`, `store.py`, `agent.py`: shared validation, atomic batches, dependency/version/receipt constraints, exact duplicate checks and eligible binding-ID enums. Ambiguity cannot reopen attempted/uncertain executions.
- `prompts/v2_1/`: delegation contrasts and trigger/ID/evidence rules. Original v2 and historical A0/A1 prompts remain unchanged. B_ledger/A2 share the repair; their monitoring-policy distinction remains narrow.
- `Gateway.call`: specific error on the existing bounded retry, request IDs, separate accepted-operation/empty-update/rejection/exhaustion/transport outcomes.
- `scripts/run_v21_smoke.py`: new frozen scope using existing `run_v2_smoke.execute` and `run_case`. Single-method report scope is explicit. Historical verification uses `verify_saved_smoke.py --historical-sources`.

## Evidence

**146 tests pass**, including 35 new regressions; Python compilation and the original mock smoke pass. Independent JSON Schema validation agrees on 144 trigger/condition/time/channel combinations. These checks do not establish live semantics.

`results/v2_1/offline-repair-v1/` is **MOCK**: 8 checkpoints, 16 fixture requests, 7 queries, 3 receipt-completed intentions, zero validation failures. It exercises negative evidence, a later check, positive evidence and receipts. A deliberate regression shows that narrative hypothetical entailment remains model-dependent.

Logs: `artifacts/verification/v21-extraction/`. **164 protected hashes**, **404 historical baseline files**, **1,355 local/MOCK archived files**, **24 genuine smoke archived files** and **59 original source paths at the recorded commit** verify. Old freezes, inventories and historical/failed artifacts were not rewritten. The claims register gains only an append-only entry.

Latest genuine evidence remains `results/v2/deepseek-smoke-v1/`, execution commit `a754559351ba017bb4fc00aa5e0527ea68d05572`: 8/8 checkpoints, TP0/FP0/FN2, empty ledger, no queries/actions/receipts; 24 calls, 8 retries, 57,052 input / 4,380 output tokens, $0.01525668 API-response cost, no truncation. Independent billing is unavailable. Historical A0/A1 studies both showed no observed P1 Set-F1 improvement and overlap; never pool them as independent replications.

## Commands and next action

Free/offline, from the repository root:

```bash
python3 scripts/run_v21_smoke.py --preflight
python3 scripts/verify_saved_smoke.py --historical-sources
python3 scripts/verify_benchmark_integrity.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q kiodai_v2 research_harness scripts tests
```

Optional MOCK replay in a fresh directory:

```bash
python3 scripts/verify_v21_offline.py --output /tmp/kiodai-v21-new-mock
```

Historical read-only viewer:

```bash
python3 scripts/serve_v2.py --study results/v2/deepseek-smoke-v1 --port 8768
```

The old full-v2/original-smoke preflights correctly reject changed v2.1 sources. **Do not rewrite old hashes.** Original code is verified at its recorded commit. A future full study needs its own matching freeze and fresh authorization.

Only after the user freshly authorizes exactly one A2 development smoke:

```bash
python3 scripts/run_v21_smoke.py --live --authorize-new-smoke v2.1-deepseek-smoke-v1 --budget-usd 1.00 --env-file .env
```

Future output: `results/v2_1/deepseek-smoke-v1/`, currently absent; no restart/alternate output allowed. Intact `v2_hidden_91320`, eight checkpoints, unchanged DeepSeek V3.1 / Novita / fp8 settings and output limits. Usage projection **$0.03201778**, all-calls-retry sensitivity **$0.12188694**, conservative reservation **$0.49729536**. It fits a **candidate $1 ceiling**, which has not been authorized. Exact new schema-keyword enforcement on the endpoint remains unverified; local validation is enforced without silent fallback.

Next action: the user decides whether to authorize this one prepared smoke. Even success establishes only narrow integration feasibility on exposed development data, not reliability or superiority. Do not restart literature review, redesign the architecture, change scoring, tune against A0 losses, or launch the full evaluation.

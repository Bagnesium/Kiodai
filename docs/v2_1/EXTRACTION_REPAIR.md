# v2.1 extraction repair and one proposed smoke

Implemented on `codex/kiodai-v2.1-extraction`, source commit **`959db38dac8b68f63ecf79420dcd53bea2278cf2`**. No new local/network model inference, paid credential check, push or deployment occurred. Only public structured-output documentation was browsed. A live smoke requires fresh explicit authorization.

The checkout was clean at `6e1c25e`, with an actual handoff following `c28acac`. Baseline verification found **111 passing tests**, newer than the request's 101-test snapshot. The failed smoke used `a754559351ba017bb4fc00aa5e0527ea68d05572`. Historical A0/A1 results remain separate: pilot TP5/FP0/FN0 for both; follow-up TP11/FP0/FN1 for both. They overlap and cannot be pooled; Set-F1 is not ordinary percentage accuracy. The existing attribution matrix was read; no unavailable literature PDF is claimed to have been read.

## Root causes

Request numbers below are one-based ordinals in `results/v2/deepseek-smoke-v1/v2_hidden_91320/A2/calls.jsonl`. Each request is followed by its response. `research/v2_1/diagnosis.json` records all 24 ordinals, response IDs, line numbers and outcomes. `tests/fixtures/v21_failed_smoke_minimized.json` contains labeled public request/output subsets, never evaluator answers.

Claim: v2 had a schema/application mismatch for intention content.
Status: **Observed**.
Evidence: request **1**, `gen-1788975238-6Gw2hWqx4LlluVoFnIxT`, lines 1–2, receives the three actual instructions in `m1`, the menu in `m2`, an empty ledger, and the old extraction prompt/schema. Its registration draft has `trigger=time`, `when="08:00 on DayOne"`, `condition=""`. The archival schema and `common.parse` accept it; historical `Store.apply` rejects it with `Missing intention content`. Requests **4, 8, 14, 19, 22** receive the same error. Request 1 also represents channel predicates as `event`, omits an archive predicate and does not bind the sealing dependency; application validation did not reach those defects.
Limit: the old output remains rejected. A time-only intention can now intentionally specify `condition=null`; an event/hidden predicate cannot. No historical response was repaired or replaced.

Claim: a matching quotation did not establish an assigned obligation.
Status: **Observed**.
Evidence: requests **14**, `gen-1788975347-wdHZHZ1rmsjvTMwzRy0z` (`m11`), and **19**, `gen-1788975365-sL9bRkcYH6QHwTbHVYGM` (`m15`), promote an actual discard-menu line into an intention. Their quotes exist, but the source does not delegate that task. Both also have empty conditions and were rejected before semantic distinction.
Limit: the repair deterministically rejects menu-only and tool-only obligation support. Whether arbitrary narrative text entails delegation remains model-dependent.

Claim: an empty ledger prevented the proposed pipeline from operating; selection also had distinct contract failures.
Status: **Observed** for the trace; **Inferred** for whether better feedback will improve future behavior.
Evidence: six rejected extraction batches received generic retry feedback omitting the actual error. Each retry returned an accepted empty update; two other extraction calls were also empty. All checkpoints retained an empty ledger. Selection requests **6**, `gen-1788975294-6mYch4B7KPScDPQpV6Z0`, **7**, `gen-1788975300-5kN2mtzUAWWqnXcgtqkg`, and **10**, `gen-1788975333-sLGHESP2tVO7UfdASGni`, supplied an action description as `bindings.intention`. The old schema allowed any string; eligibility rejected the nonexistent ID. Requests 6/7 exhausted retries at checkpoint 2; request 10 recovered to empty selection. All three also cite stale `m1` instruction evidence, a defect validation never reached.
Limit: fixing extraction does not by itself guarantee correct IDs, timing, evidence or action interpretation. Better feedback has not been tested with this real model.

Claim: the live run did not establish successful monitoring or execution.
Status: **Observed**.
Evidence: read-only verification reproduces 8/8 checkpoints, TP0/FP0/FN2, 24 calls, 8 retries, 57,052 input and 4,380 output tokens, and $0.01525668 API-response cost. It has zero queries/actions/receipts, all finish reasons `stop`, and no transport errors. Three obligations remained unfinished; the dependent task never became due. Agent, memory, step and accounting artifacts agree.
Limit: truncation and generic “bad memory” are unsupported explanations. Downstream real-model operation remains untested; independent billing is unavailable.

## Contract and implementation

| Boundary | New behavior | Implementation |
|---|---|---|
| Structural validation | Same JSON Schema validates provider-request shape, local parsing and ledger operations | `kiodai_v2/contract.py:EXTRACTION`; `common.py:validate/parse`; `Store.apply` |
| Time trigger | Nonblank stated day/time in `when`; channel null; condition null unless an additional predicate is stated | `contract.py:record_schema` |
| Event trigger | Nonblank predicate; null channel; optional stated day/time restriction | same |
| Hidden trigger | Nonblank predicate and legitimate offered channel; optional stated day/time restriction | same plus contextual channel check |
| Unknown trigger | Preserve supported details, use null for missing details, quarantine until revision resolves trigger/dependency | `Store.apply` and existing eligibility checks |
| Operations | Create: null target/version and full record. Revise: ID, positive version, full record. Cancel: ID/version, null record. Ambiguous: null target/version/record | shared schema |
| Context/provenance | Exact observed quotes; populated-field support; visible obligation support outside menu spans; available channels, IDs/versions and dependencies | `obligation_sources_valid`, `Store.apply` |
| Selection | Eligible ledger ID enums; empty task/binding arrays when none are eligible; current-checkpoint citations remain required | `Agent.decide`, `prompts/v2_1/select.txt` |
| Retries/accounting | Specific validation error on the existing one retry; request IDs and separate accepted-operation, accepted-empty, rejection, exhaustion and transport outcomes | `Gateway.call` |
| Version/replay | Additive version metadata, historical-source verification and correct single-method report scope | `runner.py`, `verify_saved_smoke.py`, `report.py` |

The entire extraction batch remains atomic: a failed later operation rolls back earlier operations and event writes. The first historical batch was lost as a whole, but the evidence does not establish that its other records were independently valid actionable intentions. Atomicity is retained to avoid partially applied dependent revisions. Empty updates remain legitimate for non-instructions and already-recorded instructions; rejection is not an empty-update success.

New prerequisites lack IDs until the batch finishes. A dependent obligation can use the existing `unknown` trigger, preserving the unresolved dependency in cited text and remaining quarantined; a later extraction can revise it with the assigned prerequisite ID. No ID, deadline, channel or “always” predicate is fabricated. Exact duplicate live records are rejected even with different source refs; paraphrased duplicate detection remains model-dependent. Ambiguity quarantine now preserves attempted/uncertain executions, preventing that path from reopening an unresolved side effect.

`prompts/v2_1/extract.txt` adds hand-authored contrasts created after inspecting the failure class: menu mention versus discard request, quoted menu title versus print request, tool evidence versus an instruction to check a channel, and unspecified timing versus an invented deadline. These are exposed development material, not benchmark answers or held-out tests. No keyword blacklist, scenario-specific rule, classifier, additional model stage or evaluator-informed fallback was added. The actual renderer's menu delimiter is an interface boundary.

B_ledger and A2 share the revision. Their query-policy difference, full history, one-query allowance, disabled heartbeat, monitoring schedule, simulated receipts and official scorer remain unchanged. Original `prompts/v2/` and historical A0/A1 prompts are preserved.

## Verification and preservation

Claim: the repaired boundaries and mocked integration work locally.
Status: **Locally verified**.
Evidence: **146 tests pass**: 111 baseline plus 35 new regressions. `tests/test_v21_extraction.py` covers the historical gap, trigger/condition states, source spans, menu/tool-only support, genuine same-vocabulary requests, unknown dependencies, duplicates, atomic batches, revisions/cancellation/cycles, rollback, bounded feedback/exhaustion and all three selection failures. It also checks shared extraction requests, renamed entities/handles, paraphrased instructions, shifted times and every internal request—including retries—for evaluator/future-state leakage in both ledger methods. `tests/test_v21_smoke.py` covers budgets, live gates, pinned settings, historical verification and integration.
Evidence: installed `jsonschema` 4.26.0 independently validates the schema and agrees with local validation on **144** trigger/condition/time/channel combinations. This is not a provider capability probe.
Evidence: `results/v2_1/offline-repair-v1/` preserves **MOCK** raw artifacts: 8 checkpoints, 16 fixture requests, 7 queries, 3 receipt-completed intentions, 2 accepted-operation responses, 6 accepted-empty updates, zero validation failures. Negative evidence at checkpoint 1 causes no action; a later permitted check receives positive evidence at checkpoint 7; completion follows successful receipts. Official mocked TP3/FP0/FN0 is software-fixture output, not model performance. The restricted-language fixture now quarantines a dependent record until its new prerequisite has an assigned ID.
Limit: one regression deliberately shows that a cited narrative hypothetical can still pass deterministic structure/provenance. The prompt asks the model to reject it; mocks cannot prove compliance. Initial test failures—the old ambiguous-operation fixture supplying a target and a new mocked accounting fixture lacking synthetic provider metadata—are preserved in the logs and were corrected. No new model run failed or succeeded.

Evidence logs: `artifacts/verification/v21-extraction/`. **164 protected hashes**, **404 historical baseline files**, **1,355 local/MOCK archive files**, **24 genuine smoke archive files**, and **59 original source paths at the recorded commit** pass. Both old freezes match their recorded bytes. A broader before/after snapshot of **2,225** pre-existing artifact/prompt/research files is unchanged. Python compilation and the original mock smoke pass; code/docs pass whitespace and secret-pattern scans. The raw saved baseline system prompt retains its original trailing space instead of altering evidence. The claims register is append-only. No historical artifacts, freezes, inventories or failed runs were rewritten.

The old v2 preflight correctly rejects current v2.1 hashes. Do not update old hashes to make it pass. Historical code verification uses the original execution commit; replay remains read-only and does not infer new results.

## Prepared smoke — not executed

Manifest: **`research/v2_1/smoke_v1.json`**. It records source commit, 40 source/config/scenario/test hashes, normalized extraction-schema hash, binding-template hash, versioned prompt hashes, validation/retry policy, output limits, costs and observable criteria. Generated schema snapshot: `research/v2_1/extraction.schema.json`.

Free/offline, from `/Users/bagnesium/Documents/GitHub/Kiodai`:

```bash
python3 scripts/run_v21_smoke.py --preflight
python3 scripts/verify_saved_smoke.py --historical-sources
```

Optional MOCK reproduction in a fresh local directory:

```bash
python3 scripts/verify_v21_offline.py --output /tmp/kiodai-v21-new-mock
```

**Only after fresh explicit authorization**, proposed live command:

```bash
python3 scripts/run_v21_smoke.py --live --authorize-new-smoke v2.1-deepseek-smoke-v1 --budget-usd 1.00 --env-file .env
```

It uses the existing `run_v2_smoke.execute` and native `run_case`, one intact `v2_hidden_91320` trajectory, all eight checkpoints, and unique future output **`results/v2_1/deepseek-smoke-v1/`**, currently absent. It refuses overwrite/restart, changed frozen implementation/configuration, a dirty checkout or missing named authorization/budget flags. No new execution engine was created.

Pinned settings remain: OpenRouter `deepseek/deepseek-chat-v3.1`, Novita only, fp8, no fallbacks, `require_parameters=true`, reasoning disabled/excluded; temperature 0, top_p 1, seed 20260904; timeout 120 s; one validation retry, zero transport retries; 48,000-byte requests; extraction 3,072 and selection 1,536 output tokens. No output limit was raised: the failed DeepSeek run was not truncated. Keys remain local, `.env` interpolation is disabled, and TLS verification remains enabled.

| Planning quantity | Value |
|---|---|
| Normal model calls | 8 extraction + 8 selection; controller queries add evidence to selection without another model cycle |
| Permitted maximum | 32 attempts including all retries; at most 8 queries |
| Usage-informed projection | **$0.03201778**; 88,777 projected input / 8,048 output tokens |
| All-calls-retry sensitivity | **$0.12188694**; prior-response/feedback growth and maximal retry outputs included |
| Conservative reservation | **$0.49729536**, using 48,000+1,024 input-token allowance and full output limits for all 32 attempts |
| Candidate ceiling | **$1.00**, sufficient but **not renewed authorization** |

The usage projection uses complete populated-ledger mock request sizes, the actual failed-smoke tokens/byte ratio, a 1.35 input-growth margin and no cache discount. The maximum mocked request is 21,190 bytes. Verbose later history/retries can still hit the 48,000-byte limit and stop before inference; no truncation or guard relaxation is allowed. Durable reservations are never refunded, including unknown transport outcomes. Actual future cost and independent billing remain unknown.

Saved route metadata advertises structured outputs. [OpenRouter's official documentation](https://github.com/OpenRouterTeam/docs/blob/main/guides/features/structured-outputs.mdx) says enforcement varies by provider; [Novita's documentation](https://docs.novita.ai/guides/llm-structured-outputs) does not certify the added `$defs`, `$ref`, `anyOf`, `pattern`, `minimum`, `minItems` features on this exact route. **Endpoint acceptance/enforcement remains unverified.** Local validation enforces them. No inference or credential probe ran. The future authorized launcher checks route metadata and stops on unsupported requests without changing provider or relaxing the schema.

The next smoke must visibly store supported intentions, avoid unsupported distractors, preserve validation failures, monitor actual eligible records, support selections with available current evidence, and complete only after successful receipts. Scoreability is separate from these integration criteria. A perfect score is unnecessary for a scoreable experiment; even success establishes only narrow feasibility on exposed development material. Do not tune/select a future evaluation to make A0 lose. The old 12-trajectory freeze is not a v2.1 study; a later comparison needs a matching freeze and fresh authorization.

Next action: review this protocol and decide whether to authorize **exactly this one A2 development smoke with a cumulative $1 ceiling**.

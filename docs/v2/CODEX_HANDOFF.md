# 1. CURRENT STATE

Repository: `/Users/bagnesium/Documents/GitHub/Kiodai`. Author: Bagdat Beimzhan. **Deadline: September 13, 2026, Asia/Almaty.** Read repository `AGENTS.md` before editing.

Verified source branch: **`codex/kiodai-v2`**. Source HEAD: **`c28acac07528bdede8aa9174a3e0139a30e2b227`**. The working tree was clean before creating this handoff. This documentation-only commit follows that HEAD; resolve its own hash with `git log -1 --format=%H -- docs/v2/CODEX_HANDOFF.md`. No push is requested.

Current evaluated implementation is **v2.0**, with a separate `v2.0-deepseek-smoke-v1` scope configuration. **No v2.1 repair exists yet.** The typed SQLite ledger, lifecycle controls, bounded polling, isolated runner, durable inference accounting and read-only viewer are implemented and pass software tests. Real-model extraction has not made that pipeline operate successfully end to end.

Fresh handoff checks: **111 tests passed; 164 protected file hashes passed; full and smoke preflights passed; saved smoke verification passed for 24 archived files and 59 frozen source paths.** No inference was performed for this handoff. Existing durable verification logs: `artifacts/verification/evidence-maintenance-20260909/`.

| Workstream | Actual state |
|---|---|
| Historical A0 versus A1/P1 | Two completed exploratory paired studies; neither showed P1 improving Set-F1. |
| V2 MOCK | 36 method-trajectories completed; software-fixture success, not model-performance evidence. |
| V2 local Llama | Interrupted; 1/8 checkpoints, zero usable complete trajectories. |
| V2 genuine DeepSeek/Novita | One A2-only trajectory completed; zero stored intentions and zero task actions. |
| Full v2 comparison | Frozen but **not run**; `results/v2/live-frozen-v2/` does not exist. |

Latest relevant commits:

| Commit | Meaning |
|---|---|
| `c28acac` | 111 passing checks; unchanged frozen evidence. |
| `5ee03c9`, `ee86557`, `6978ef1` | Safer replay guidance; restoration regressions; read-only evidence verifier. |
| `c3460f7`, `f05ece0`, `a7a3644` | Corrected verification, authorization history, manuscript replacements and Russian defense. |
| `621d3b9`, `e905b8c` | Archived and reported the genuine failed DeepSeek smoke. |
| `a754559` | Smoke protocol committed **before** its paid invocation. |
| `1f51213` | Original full v2 freeze. |

# 2. PROJECT PURPOSE

Prospective memory means retaining an instruction and acting later when its time or event condition becomes true. Kiodai studies the gap between having an instruction available and obtaining the evidence needed to execute it at the right opportunity.

- **A0:** baseline language-model action selection from the public history/menu and permitted queries.
- **Historical A1/P1:** the same baseline plus frozen prospective-memory instructions in `prompts/prospective_memory_system.txt`. P1 assumes completion after selection.
- **B_ledger:** v2 extraction, external ledger, selection and receipt logic; the model decides whether to query.
- **A2/Kiodai v2:** the same ledger architecture, with deterministic bounded channel polling replacing the model's query decision. The model still extracts/revises intentions and interprets evidence/action bindings.

A2 is an architectural experiment: persistent state, multiple internal inference calls, deterministic monitoring and receipt-driven lifecycle rules. It is not merely an alternative P1 prompt, and its comparison is not compute-matched. The historical A1 condition must retain its identity and results.

# 3. ARCHITECTURE

Implemented path: **observation → extraction/update → persistent ledger → monitoring → returned evidence → selection → simulated execution → receipt → lifecycle update → evaluation/logging**.

| Component / main interface | Deterministic code | LLM responsibility / invariant |
|---|---|---|
| `kiodai_v2/runner.py:Adapter.select_action` | Converts the native public history into a serialized frame; assigns local checkpoint and `mN` observation references. | No scenario object or evaluator state reaches the agent. |
| `kiodai_v2/agent.py:Agent.receive` | Checks frame shape; calls extraction once per new checkpoint for ledger methods. | Extract/revise from received observations, `new_refs`, current intentions and allowed channels, using `prompts/v2/extract.txt`. |
| `kiodai_v2/common.py:parse`, `validate`, `citations_valid` | Strict types/fields/enums, duplicate-key rejection, exact nonempty source spans; current-checkpoint evidence where required. | Provenance validation does **not** prove semantic fidelity. |
| `kiodai_v2/store.py:Store.apply` | Atomic SQLite batch validation/application; local IDs, versions, dependencies and lifecycle constraints. | Propose correct operations and field interpretations; no deterministic semantic instruction classifier is implemented. |
| `Store.monitor`, `check_valid`; `Agent.decide` | A2 groups eligible intentions by allowed channel, orders least recently checked first (channel-name tie break), queries at most one channel/checkpoint, validates version tickets. Hidden clock can use `clock`. | B_ledger instead delegates query choice to its model. A2 selection still interprets whether evidence supports acting. |
| `research_harness/runner.py:iter_environment`; `Store.query_received` | Native allowed queries return current public observations; store records their reference, checkpoint and version. | Unqueried values and future observations remain private. |
| `Agent.decide`, `prompts/v2/select.txt` | Validates action schema, offered handles, one binding per selected handle, current eligible intention version, current evidence. | Select anonymous menu handles and bind them to agent intention IDs. Exact citations can still be semantically irrelevant. |
| Native iterator; `Adapter.execution` | Executes in PM-Bench; maps anonymous public receipts to stable agent execution IDs. | Selection is not completion. Receipt fields contain no canonical task IDs or due flags. |
| `Store.select`, `attempted`, `receipt` | `pending/failed → selected → attempted`; only `success` receipt produces `completed`; `failed`/`uncertain` remain explicit. | No model-written completion flag is trusted. |
| `kiodai_v2/runner.py:run_case`; `kiodai_v2/report.py` | Saves raw artifacts and scores with unchanged `sim.pm_bench.score_log`; incomplete trajectories have unavailable primary scores. | Evaluation occurs after selection; it never supplies repair answers. |

**Public frame keys:** `checkpoint`, `messages`, `observations`, `current_refs`, `channels`, `handles`, `menu`, `receipts`. Observation values contain only `text`, `kind` (`visible`/`query`) and `checkpoint`.

**Current extraction contract:** `store.py:FIELDS`, `RECORD`, `EXTRACTION` define `{"operations": [...]}`. An operation has `kind` (`create`, `revise`, `cancel`, `ambiguous`), `target`, `expected_version`, `record`, `sources`. A record has `action` string, `trigger` enum (`time`, `event`, `hidden`, `unknown`), `condition` string, nullable `channel`/`when`, dependencies as existing agent-ID strings, and per-field evidence arrays of `{ref, quote}`. All declared fields are required; extra fields are rejected. **The empty-condition mismatch is detailed in section 8.**

Creation requires null target/version; code assigns an `i_…` ID and version 1. Revision replaces the complete record and increments its current version. Cancellation uses an existing ID/current version with `record=null` and increments the version. Ambiguous updates quarantine live records; later explicit revisions can resolve quarantine. Completed/canceled or unresolved attempted/uncertain intentions cannot be revised as ordinary pending records.

Dependencies must reference existing records, cannot refer to self, and cannot form cycles. Eligibility requires completed dependencies. Simultaneously extracted new obligations may need a later revision to attach a newly assigned prerequisite ID; semantic omission of a dependency is not automatically detected.

`Store.select` assigns a stable `exec_…` ID per intention/version. **Separate** `store.py:LocalExecutor` tests SQLite side-effect/receipt atomicity, restart behavior and idempotency; it is not an external email/calendar executor or a separate benchmark. Uncertain execution is not automatically retried.

`kiodai_v2/gateway.py:Gateway.call` logs exact requests before sending, then raw responses, validation/transport failures, usage, provider and latency. The current implementation uses attempts `(1, 2)`: one generic corrective validation retry, no transport retry. `Accounting` reserves each attempt durably before sending; reservations are not refunded. The OpenRouter transport is `research_harness/model_gateway.py:OpenAICompatibleTransport`.

Leakage boundary: private canonical task IDs, due sets, updates/ground truth and future/unqueried state stay on the environment/evaluator side. The protected upstream `run-llm` path contains a due-set fallback; do **not** use that path. The audited iterator fixes the action before evaluator annotations. `steps.jsonl` is evaluator-side; `agent.jsonl` records actual public frames.

# 4. RESEARCH HISTORY

Counts were rechecked from saved scenarios/actions using the official scorer; tokens from `raw_model_calls.jsonl`. Precision/recall/F1 below follow TP/FP/FN. Summary reference: `research/v2/history_check.json`; detailed reports: `RESULTS.md`, `FOLLOWUP_RESULTS.md`.

| Study / condition | TP / FP / FN | Precision / Recall / Set-F1 | Input / output tokens | API-response cost |
|---|---|---|---|---:|
| Pilot A0 | 5 / 0 / 0 | 1 / 1 / 1 | 13,819 / 269 | $0.00336941 |
| Pilot A1 | 5 / 0 / 0 | 1 / 1 / 1 | 19,179 / 269 | $0.00428093 |
| Three-day A0 | 11 / 0 / 1 | 1 / 11⁄12 / 22⁄23 | 59,171 / 699 | $0.01454109 |
| Three-day A1 | 11 / 0 / 1 | 1 / 11⁄12 / 22⁄23 | 68,971 / 665 | $0.01593485 |

Exact run directories, relative to the repository:

```text
results/kiodai/live-pair-42433e00474b/live-A0-20260908T164420-7848b46b/
results/kiodai/live-pair-42433e00474b/live-A1-20260908T164420-2fdeb6e6/
results/followup_v1/live-pair-bdf241965f35/live-A0-20260909T131935-b7f6531a/
results/followup_v1/live-pair-bdf241965f35/live-A1-20260909T131935-5232d513/
```

Pilot: one eight-step pair, 16 calls; neither condition queried or needed validation retries. A1 added 5,360 input tokens; combined cost $0.00765034. **No observed P1 accuracy improvement**, with both at ceiling.

Follow-up: one complete three-day, 20-step paired trajectory, one repeat. A0 made 21 calls and one Tuesday 11:30 `sensor_board` query returning “Cooling is nearly stable; final stabilization is not complete.” A1 made 20 calls and no query. Neither obtained the positive hidden reading at 13:00; both missed the cooling action. Both later cross-day actions succeeded with full history available. A1 added 9,800 input tokens and $0.00139376; combined cost $0.03047594. **No observed P1 accuracy improvement** (A1−A0 Set-F1=0).

The follow-up was planned after observing the pilot and overlaps its Monday segment. Do not pool those observations as independent evidence or treat steps/calls as replications. All costs above are saved API-response costs; independently verified billing is unavailable.

# 5. V2 DEVELOPMENT HISTORY

Read [SOURCES.md](SOURCES.md) and `research/v2/source_inventory.json` for the recorded paper versions, hashes, authors, source licenses and repository commits. The source audit is dated September 9; external repositories may later change.

- **PIS / Making Prospective Memory SLM-Shaped** (`2609.01272v1`): typed external trigger/action/status store, model formation/revision and structural filtering inspired `Store`, extraction, and B_ledger. Official runnable code was not located in the audit. This is a **PIS-inspired reconstruction**, not faithful reproduction.
- **PM-Bench** (`2607.12385v1`, `genglinliu/PMBench`, recorded upstream `e1093c4`): unchanged native environment, anonymous menus, state queries, completion mechanics and official scorer. Kiodai reuses its audited iterator and retains the original protected benchmark.
- **TriggerBench** (`2606.23459v1`, `KristenZHANG/TriggerBench-Official`): motivates prospective-versus-retrospective distinctions, distractions, negative/near-match controls and error-stage separation. At the recorded audit its repository contained a README, not runnable released cases. No TriggerBench scores/dataset/judge were imported.
- **MIRAGE** (`sunblaze-ucb/mirage-bench`): evidence-before-decision auditing principle. **MemBench** (`import-myself/Membench`), **MemoryAgentBench**, **Evo-Memory**, and the **Evolving-LLM-Agent-Memory-Survey** repository supplied background/positioning. No implementation or leaderboard reproduction is claimed for these systems.

Versioned receipts, stable simulated execution IDs, persistence and controller integration are engineering work, not demonstrated research novelty. Four synthetic template families were authored and inspected in the same development process. Do not claim original invention of agent memory, state of the art, faithful PIS reproduction, blind evaluation, equal compute, reliable extraction or A2 superiority.

# 6. V2 VERIFICATION

[VERIFICATION.md](VERIFICATION.md) distinguishes historical 98-test preparation, 101-test smoke checks and the current **111-test** maintenance suite. The **164 protected hashes** pass. Full preflight also checks the **404-file historical baseline**, with the claims register allowed append-only additions.

Saved MOCK: `results/v2/mock-verification-v2/`, 12 trajectories × three methods × one repeat = **36 method-trajectories / 288 steps**. Each method's fixture totals are TP24/FP0/FN0, Set-F1=1; calls A0=117, B_ledger=213, A2=192; queries=21 each. These demonstrate that suitable fixture responses can traverse software interfaces, ledger, queries, actions, receipts and scoring. They do **not** establish real extraction reliability, monitoring benefit or model accuracy differences.

Earlier unsuccessful fixtures and the full-story cooling regression remain preserved. Original phase archive: `artifacts/verification/v2-20260909.zip`, inventory `research/v2/artifact_inventory.json`. It covers local/MOCK development, **not** the subsequent DeepSeek smoke; the latter has a separate archive.

# 7. LOCAL MODEL SMOKE

Artifacts: `results/v2/local-smoke-v2/`, raw case `v2_hidden_91320/A2/`; backend metadata in `local_backend.json`. Installed `llama3.2:latest` ran through `kiodai_v2/local.py` / Ollama loopback. **Zero usable complete trajectories; 1/8 checkpoints completed.**

Four extraction attempts: two invalid citations, then malformed JSON at exactly 3,072 output tokens (`done_reason=length`), then a 120-second timeout. Citation examples include nonexistent `null` spans and wrong observation references; the timeout's server-side cause remains unknown. Three responses report known subtotals of 2,618 input and 3,883 output tokens; complete totals are unavailable. No paid API inference was involved in this local run.

An original partial-scoring finalizer bug interrupted artifact finalization; it was fixed before the full v2 freeze. `recovery.json` preserves original-file hashes and distinguishes post-hoc finalization from original evidence. Never replace that failure with new output. This was one exposed local A2 attempt, not a comparison or the intended DeepSeek backend. Detailed retrospective audit: `research/v2/deepseek_smoke_failure_audit.json`.

# 8. DEEPSEEK SMOKE FAILURE

**Most important evidence:** [DEEPSEEK_SMOKE_RESULTS.md](DEEPSEEK_SMOKE_RESULTS.md), `results/v2/deepseek-smoke-v1/`. Raw case: `results/v2/deepseek-smoke-v1/v2_hidden_91320/A2/`.

| Measurement | Saved result |
|---|---|
| Unit | One complete, scoreable A2-only trajectory; 8/8 checkpoints |
| TP / FP / FN | **0 / 0 / 2** |
| Precision / recall / Set-F1 | Undefined (0/0) / **0** / **0** |
| Calls / retries | **24 / 8** |
| Input / output tokens | **57,052 / 4,380** |
| API-response-reported cost | **$0.01525668**; independent billing unavailable |
| Transport failures / truncations | **0 / 0**; all 24 responses ended with `stop` |
| Stored intentions / queries / executed task actions / receipts | **0 / 0 / 0 / 0** |

Execution commit `a754559351ba017bb4fc00aa5e0527ea68d05572`; completed September 9 at 17:36:47.503 UTC. All responses report DeepSeek V3.1 / Novita. Three obligations remained unfinished; dependent sealing never became due because registration failed, so official FN=2 is not “only two unfinished instructions.”

Failure chain: **received instruction → extraction draft → application rejection / accepted empty update → empty ledger → no channel query → no executed action → missed tasks**. Controller monitoring code ran, but selected no channels from an empty store. No negative or positive hidden reading reached the agent. Zero false positives therefore do not demonstrate negative-evidence restraint.

**A. Contract mismatch.** `kiodai_v2/store.py:FIELDS` makes `condition` a `common.py:STRING` (`{"type":"string"}`); `RECORD` and `EXTRACTION` have no nonempty-string constraint. `common.py:validate`/`parse` accept these structural outputs. In contrast, `Store.apply` rejects `record is None or not record['action'] or not record['condition']` with `Missing intention content`. `Agent.receive` passes `Store.apply` as `Gateway.call`'s validator. The generic correction gives no failing-field explanation. The frozen extraction prompt also says unknown information stays null, while the condition field itself is nonnullable: the next session must reconcile the intended contract rather than simply waive validation.

All **14 extraction responses were schema-valid**. Six nonempty drafts failed application validation; **eight accepted responses were empty operation lists**, with zero accepted create/revise operations. The first attempts at checkpoints 1, 2, 3 and 8 proposed the real three actions but empty registration/archive conditions; atomic validation rejected the whole batch. Six retries returned empty updates; checkpoints 4 and 6 returned empty updates immediately. No extraction exhausted both attempts into an explicit extraction fallback. Separately, three selection outputs referenced nonexistent intention IDs; checkpoint 2 exhausted its two attempts into **one explicit fail-closed action**. Other final task selections were model-produced empties, not successful extraction.

**B. Semantic extraction failure.** At checkpoint 5 (11:00), observation `m11` contained a menu distractor `task_5: Discard the cobalt91320 case.`. The model cited that real span and proposed a deferred intention. It repeated the mistake at checkpoint 7 (13:00), using `m15`. Menu availability is not a user instruction. Accurate citation proves the quoted text was seen; it does not establish its role or correct interpretation. These drafts were rejected too. No deterministic semantic classifier currently protects that boundary.

Exact raw references in the case's `calls.jsonl`: **line 2** = checkpoint 1 extraction draft, **line 4** = its empty retry; **line 28** = checkpoint 5 distractor draft, **line 38** = checkpoint 7 distractor draft (JSONL physical lines). Inspect the matching request immediately above each response. `agent.jsonl` contains received frames and actual decisions; `memory.json` is `{}`; `memory.sqlite` retains empty monitoring events; `steps.jsonl` contains post-selection evaluator annotations. `behavior_audit.json` at the study root collects the post-hoc checks. None of those audits were fed back into the model.

These are observed failure classes, not proof that no other defects exist. No paid repair/rerun followed. Cheap failed operation does not establish a cheap functioning pipeline.

# 9. CURRENT BLOCKER

**The immediate blocker is not the monitoring policy or evaluator. It is making real-model intention extraction/update satisfy the application contract and reject non-instruction distractors.** Without legitimate nonempty intentions entering the ledger, the downstream monitoring benefit cannot be meaningfully assessed. The completed failed trajectory remains valid negative integration evidence; do not discard it as “unusable.” This diagnosis does not certify that monitoring, selection or external execution would work after extraction is repaired.

# 10. WHAT MUST NOT BE CHANGED

Preserve these as historical/frozen evidence:

- Historical `prompts/baseline_system.txt`, `prompts/prospective_memory_system.txt`, A0/A1 results and configurations covered by the existing manifests.
- Pilot and follow-up roots in section 4; `research/pilot1_preservation_v1.json`, `research/followup_preservation_v1.json`; archives `artifacts/verification/pilot1-preserved-20260908.zip` and `artifacts/verification/followup-live-20260909.zip`.
- Every path in `research/protected_hashes.json`, including PM-Bench scenarios, original evaluator/generators/runners, released results and original browser implementation.
- Existing manifests/freezes: `research/a0_a1_freeze_manifest.json`, `research/pilot_freeze_v1.json`, `research/followup_freeze_v1.json`, `research/v2/freeze.json`, `research/v2/deepseek_smoke_v1_freeze.json` and other recorded freezes. Never overwrite a freeze to make a changed implementation pass.
- Failed DeepSeek smoke files, its `research/v2/deepseek_smoke_artifact_inventory.json`, and `artifacts/verification/deepseek-smoke-v1-20260909.zip`. This 24-file archive has SHA-256 `f0b9b400520e0950eeb3d7cd6a3665690613f5e3b13e5432812a8937b432d57b`. The inventory also pins post-hoc analysis/replay sources.

The failed smoke **may inform development** through its legitimate observations, requests and outputs. Any repair is a new development revision, e.g. **v2.1**, with a new commit, versioned configuration/prompts and new freeze. Preserve the v2.0 source commit and reproduce its original checks in that checkout; do not silently reuse its freeze after code changes. Use a separate revision/worktree or versioned files as appropriate, rather than rewriting history. Do not amend historical experiment commits or overwrite failed output directories.

Always retain evaluator isolation: **no `due_now`, expected-action, canonical-ID, future-observation or hidden-state leakage; no evaluator-informed output repairs**. Use no expected-answer fallback. Keep full-history/capability fairness unless a separate frozen protocol explicitly changes it. Retain all invalid attempts and unknown costs; no selective reruns or fresh budget after partial failure. Never weaken TLS or silently change provider/model/settings. `OPENROUTER_API_KEY` belongs only in the untracked local environment/`.env`; do not print it, ask for it in chat, or put it into tracked files.

**No paid inference is currently authorized.** Prior authorizations covered specific completed invocations, not a reusable balance. The next smoke and full study both need fresh authorization. No manuscript is overwritten by this handoff; findings/defense files contain proposed replacement text.

# 11. CURRENT RESEARCH FREEZE

`research/v2/freeze.json` and `configs/v2.json`: **12 complete eight-step trajectories**, four families (revision/cancellation, visible events/near matches, hidden state, cross-day), three seeds per family; **A0 / B_ledger / A2**, **one repeat**. Catalog order rotates method order by trajectory index. Full history, one allowed query/checkpoint, heartbeat off. Whole-trajectory differences are primary; steps/calls are not replications.

Pinned backend: `deepseek/deepseek-chat-v3.1`, OpenRouter → **Novita fp8 only**, fallbacks disabled, required parameters enabled, reasoning disabled/excluded. Temperature 0, top_p 1, seed 20260904. Output caps baseline 256 / extraction 3072 / selection 1536; request-byte cap 48,000, timeout 120 seconds; one validation retry, zero transport retries. Endpoint support/pricing must be rechecked before any newly authorized run; saved availability is not a future guarantee.

Original usage projection: **$0.6721910276** in `research/v2/cost_projection.json`. Later planning sensitivity: **$1.0394264194** in `results/v2/deepseek-smoke-v1/full_study_usage_projection.json`; it applies observed retry rates and token/byte ratios to successful MOCK history sizes, retains output floors, and assumes transfer to B_ledger/other templates. That transfer is uncertain.

Unchanged conservative full allowance: **$19.95251712**, proposed explicit cap $20; at most 1,344 attempts, $1.66270976 complete-triple feasibility allowance. **The full study has NOT run.** Its freeze will require a separate version if extraction changes. Neither cheap smoke cost nor a green software test validates this full experimental configuration.

# 12. IMPORTANT FILE MAP

All paths below are relative to the repository in section 1.

| Purpose | Files |
|---|---|
| Start here / overview | `docs/v2/CODEX_HANDOFF.md`, `V2.md`, `AGENTS.md` |
| Claims, attribution, paper text | `research/CLAIMS.md`, `docs/v2/SOURCES.md`, `research/v2/source_inventory.json`, `docs/v2/FINDINGS_AND_DEFENSE.md` |
| Protocol and checks | `docs/v2/METHOD.md`, `docs/v2/VERIFICATION.md`, `research/v2/freeze.json`, `research/v2/legacy_state.json` |
| Smoke protocol/results | `docs/v2/DEEPSEEK_SMOKE_PROTOCOL.md`, `docs/v2/DEEPSEEK_SMOKE_RESULTS.md`, `research/v2/deepseek_smoke_v1_freeze.json` |
| Runners / preparation | `scripts/run_v2.py`, `scripts/run_v2_smoke.py`, `scripts/local_v2_smoke.py`, `scripts/freeze_v2.py`, `scripts/generate_v2_cases.py` |
| Extraction / schema / validation | `kiodai_v2/agent.py`, `kiodai_v2/store.py`, `kiodai_v2/common.py`, `prompts/v2/extract.txt` |
| Ledger / monitoring / lifecycle | `kiodai_v2/store.py`, `kiodai_v2/agent.py` |
| Selection / gateway / spending | `prompts/v2/select.txt`, `kiodai_v2/agent.py`, `kiodai_v2/gateway.py`, `research_harness/model_gateway.py` |
| Adapter / execution / scoring | `kiodai_v2/runner.py`, `research_harness/runner.py`, protected `sim/pm_bench.py`, `kiodai_v2/report.py` |
| Offline evidence tools | `scripts/verify_saved_smoke.py`, `scripts/analyze_v2_smoke.py`, `scripts/restore_deepseek_smoke.py`, `scripts/restore_v2_artifacts.py` |
| Viewer | `scripts/serve_v2.py`, `kiodai_v2/dashboard.py`, `demo/v2/index.html`, `demo/v2/app.js`; unchanged shared `demo/style.css` |
| Fixtures / local transport / cases | `kiodai_v2/fixture.py`, `kiodai_v2/local.py`, `data/v2/catalog.json`, `data/v2/v2_hidden_91320.json` |
| Tests | `tests/test_v2.py`, `tests/test_development_smoke.py`, `tests/test_saved_smoke_integrity.py`, `tests/test_smoke_restoration.py`; original tests throughout `tests/` |
| Genuine smoke | `results/v2/deepseek-smoke-v1/` (report, audit, budget, freeze, case raw files) |
| Earlier v2 artifacts | `results/v2/local-smoke-v2/`, `results/v2/mock-verification-v2/`, `results/v2/development/`, `results/v2/known-cooling-regression/`, `results/v2/known-cooling-regression-v2/` |
| Historical evidence | `results/kiodai/`, `results/followup_v1/`, `RESULTS.md`, `FOLLOWUP_RESULTS.md`, `METHOD.md` |

# 13. IMPORTANT COMMANDS

Run from the repository root; Python 3.11+ and dependencies in `requirements.txt`. Commands/flags below were checked against source/CLI help. Tests, both preflights, protected verification and the read-only smoke verifier were rerun for this handoff. No new local-model or paid invocation was run.

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
git status --short
python3 -m unittest discover -s tests -v
python3 scripts/verify_benchmark_integrity.py
python3 scripts/run_v2.py --preflight
python3 scripts/run_v2_smoke.py --preflight
python3 scripts/verify_saved_smoke.py
python3 -m compileall -q kiodai_v2 research_harness scripts tests
```

Restore only missing evidence (both commands refuse different existing files), then genuine **RECORDED** replay:

```bash
python3 scripts/restore_deepseek_smoke.py
python3 scripts/verify_saved_smoke.py
python3 scripts/serve_v2.py --study results/v2/deepseek-smoke-v1 --port 8768
```

Open `http://127.0.0.1:8768/`; a prior server may still occupy that port. Verify its dataset before relying on it; no running process is guaranteed to survive a new chat. The viewer has no inference controls. Checkpoints 2 and 7 expose selection failure and the unqueried positive opportunity.

Free/local software validation and separate fixture/local evidence viewing:

```bash
python3 -m unittest discover -s tests -p test_v2.py -v
scripts/run_smoke_test.sh
python3 scripts/restore_v2_artifacts.py
python3 scripts/serve_v2.py --study results/v2/mock-verification-v2 --port 8767
# Alternative viewer invocation, LOCAL MODEL evidence, not new inference:
python3 scripts/serve_v2.py --study results/v2/local-smoke-v2 --port 8769
```

For a new **MOCK-only** software run, use a fresh output path that does not exist:

```bash
KIODAI_CHECK_DIR=$(mktemp -d /tmp/kiodai-check.XXXXXX)
python3 scripts/run_v2.py --mock --output "$KIODAI_CHECK_DIR/run"
```

Full-suite preflight additionally requires historical pilot/follow-up artifacts, not just v2 archives; on a fresh checkout restore those from their preserved archives without overwriting different files. The standalone saved-smoke verifier avoids that unrelated-run dependency. `scripts/local_v2_smoke.py` has a fixed already-used directory and no general subset CLI: do not blindly rerun it or pass `--help` expecting argparse. A new real local test needs separately versioned development scope. Do not run the old paid smoke launcher again; its exclusive directory is a one-invocation gate.

`python3 scripts/analyze_v2_smoke.py` regenerates derived reports and can change embedded absolute paths on another checkout. Prefer the **read-only verifier** above for handoff integrity. Original generic report output is preserved as `report.engine.*`; the authoritative smoke report corrects its scope to A2-only.

Historical recorded dashboard (select `live-pair-bdf241965f35`):

```bash
python3 -m research_harness.dashboard --output-root results/followup_v1 --port 8766
```

**NOT AUTHORIZED — reference syntax only, do not execute:**

```bash
python3 scripts/run_v2.py --live --budget-usd 20.00 --env-file .env
```

That command targets the old frozen full v2.0 study. A repaired v2.1 requires its own valid freeze/protocol and fresh authorization, not this command with silently changed sources.

# 14. KNOWN LIMITATIONS

- Exposed synthetic development material, same-process authorship/inspection, only four template families; no blind/independently held-out claim.
- Real extraction reliability is unestablished; the genuine A2 smoke failed before a populated ledger. Format/citation validity does not imply instruction semantics.
- Monitoring/selection after successful real extraction remain untested by this smoke; receipt-based end-to-end success was not observed.
- PM-Bench removes completed handles; native results cannot independently establish prompt-driven duplicate prevention. Prerequisite failures can suppress downstream due opportunities.
- Local SQLite idempotency is not external exactly-once execution or robust external-world confirmation. Historical P1 assumes completion after selection.
- Heartbeat/background calls disabled; A2's polling happens only at supplied checkpoints, not autonomously between them.
- Historical samples are tiny, with overlapping Monday observations. One A2-only smoke is not a condition comparison. Steps, internal calls and within-template seeds are not independent replications.
- Full history and anonymous action-text menus remain available; no intrinsic model-memory advantage or compressed-context benefit established.
- Full v2 comparative study has not run. Methods use different internal compute/query histories; latency, cache and order confounds remain.
- PIS-inspired reconstruction, not faithful reproduction or demonstrated novelty. Source audits do not confer redistribution rights.
- API response cost is not independently verified billing. Unknown values stay unavailable. The original local timeout's cause/usage remain unresolved.

# 15. NEXT MISSION FOR NEW CODEX CHAT

**Narrow mission: repair the extraction/application interface in a separately versioned development revision, using legitimate public observations, then prepare one new smoke without spending.**

1. Read this handoff, `AGENTS.md`, sources and actual artifacts; run read-only integrity checks before edits.
2. Inspect the DeepSeek raw requests, drafts, failures, accepted empties and menu-as-instruction examples.
3. Diagnose the canonical contract for condition/trigger/null/unknown values across prompt, JSON schema and `Store.apply`; preserve the distinction between structural and semantic rejection.
4. Fix the smallest necessary extraction/schema/application-contract issues in a new development revision. Do not merely accept missing content to obtain a passing score.
5. Improve rejection of non-instruction distractors from legitimate observations only; no evaluator answers or benchmark-specific expected actions.
6. Add regression tests using the failed smoke's public instructions/menu spans and outcomes as development examples, including accepted-empty versus successful-extraction distinctions. Do not treat them as held out.
7. Run free/local verification, isolation tests and protected-file checks. Retain failures.
8. Preserve the failed smoke and original freezes; establish a **v2.1** commit/configuration/new freeze if warranted. Do not overwrite old frozen prompts or claims.
9. Prepare **exactly one** new DeepSeek development smoke: intact scenario, prompt/code/config hashes, bounded failure policy, all internal calls, growing contexts and conservative cumulative budget.
10. **Do NOT run paid inference until fresh authorization is given.** Do not launch the full study afterward by implication.

**Do not redesign the architecture unless the evidence shows the extraction issue cannot be fixed locally.** This handoff authorizes documentation only in the current chat; these are the user's specified next-session priorities, not work already implemented.

# 16. OPEN QUESTIONS

- What must a canonical record require for time, event and hidden-state triggers? Is trigger evidence enough, or must the condition independently encode the predicate?
- Should an empty condition ever be valid, and how should unknown versus not-applicable be represented consistently?
- Which layer is authoritative for the contract, and how will schema, prompt and application rules remain aligned? The current lightweight validator does not implement arbitrary JSON Schema keywords; adding schema constraints alone may not enforce them locally.
- Where should semantic “is this an instruction?” classification be enforced? Is a single constrained extraction call sufficient, or would a separate classification stage be justified by free development evidence and its additional cost?
- How should valid empty updates be distinguished from silent omission of still-unrepresented obligations without consulting evaluator state?
- How should dependencies among newly created intentions be represented before their application-assigned IDs exist?
- Can robustness improve using general instruction semantics, without oracle features or templates tailored to the failed scenario?
- What output allowance is needed? The DeepSeek full three-record drafts used 812 tokens and were not truncated; the Llama 3,072-token truncation is different evidence. Neither establishes worst-case repaired extraction/revision length.
- What one intact smoke would establish basic extraction → negative/positive query → action → successful receipt operation? How should success/failure criteria prevent selective reruns? Exact repaired protocol and cost remain undecided.
- What further failures might appear once intentions reach the ledger? The current failure does not settle downstream reliability.

# 17. FINAL HANDOFF STATUS

- **Branch:** `codex/kiodai-v2`.
- **Verified source HEAD:** `c28acac07528bdede8aa9174a3e0139a30e2b227`. This file is committed immediately after it. **Handoff commit:** resolve `git log -1 --format=%H -- docs/v2/CODEX_HANDOFF.md`; the commit cannot embed its own hash without changing that hash.
- **Working tree:** clean at source verification; only this handoff is intended for the new commit. Confirm post-commit with `git status --short` rather than relying on a stale chat snapshot.
- **Tests:** 111 passed in a fresh handoff check; existing evidence-maintenance logs agree.
- **Protected/frozen status:** 164 protected hashes pass; full and smoke preflights pass; saved smoke archive/sources/accounting verified without writes.
- **Last genuine model run:** `results/v2/deepseek-smoke-v1/`, September 9, 2026; 8/8 complete, TP0/FP0/FN2, no stored intentions or actions; cost $0.01525668 reported by API responses.
- **Current blocker:** extraction/application-contract agreement and semantic rejection of non-instruction distractors; downstream monitoring benefit not established.
- **Paid inference:** no fresh authorization for any new smoke, repeat, model or full study. No remaining-budget inference is implied.
- **Exact first file for the new chat:** `/Users/bagnesium/Documents/GitHub/Kiodai/docs/v2/CODEX_HANDOFF.md`.

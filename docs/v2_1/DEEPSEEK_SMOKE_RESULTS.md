# v2.1 DeepSeek development smoke — 9 September 2026

**The previous empty-ledger integration failure did not recur.** The authorized A2 trajectory completed 8/8 checkpoints, stored three intentions, made seven queries, and executed three tasks with three successful simulator receipts. Official TP=3, FP=0, FN=0; precision, recall and Set-F1 are 1.00. **Extraction was not semantically flawless:** sealing initially omitted its prerequisite and was fully represented only at checkpoint 4.

This establishes development-level integration feasibility on one previously exposed story. It establishes neither extraction reliability nor an A2 advantage over A0 or B_ledger. No comparative evaluation, selective rerun or additional paid inference followed.

## Authorization and identity

The user authorized exactly `v2.1-deepseek-smoke-v1`, once, with a cumulative $1.00 ceiling. The existing free preflight passed before this exact command ran:

```bash
python3 scripts/run_v21_smoke.py --live --authorize-new-smoke v2.1-deepseek-smoke-v1 --budget-usd 1.00 --env-file .env
```

Execution commit: `392c58f80b61252759d0eb60df98be6c16d94e47`; evaluated implementation: `959db38dac8b68f63ecf79420dcd53bea2278cf2`, branch `codex/kiodai-v2.1-extraction`. Started `2026-09-09T18:36:08.781Z`, finished `18:37:46.505Z`, exit 0. Run: [`results/v2_1/deepseek-smoke-v1/`](../../results/v2_1/deepseek-smoke-v1/).

All 40 frozen source/configuration/scenario hashes still match [the prepared manifest](../../research/v2_1/smoke_v1.json). No implementation, prompt, scenario, provider/model, retry, evaluator or smoke-manifest change occurred before or during execution. The manifest's preparation-time “not executed/authorized” fields remain historical; the later authorization and completed run are separately recorded in [the preservation inventory](../../research/v2_1/live_smoke_v1_inventory.json) and original `study.json`.

DeepSeek `deepseek/deepseek-chat-v3.1` ran through OpenRouter, Novita only, requested fp8, no route fallback, `require_parameters=true`, reasoning disabled/excluded, temperature 0, top_p 1, seed 20260904. Limits stayed 3,072 extraction / 1,536 selection output tokens, 48,000 request bytes, one validation retry and zero transport retries. Every response reports the requested model and Novita route. The endpoint accepted the submitted schemas; this does not independently prove enforcement of every schema keyword. Local validation remained active.

## Recorded measurements

All values below reproduce from the raw artifacts with [`scripts/analyze_v21_smoke.py`](../../scripts/analyze_v21_smoke.py); its machine-readable output is [`analysis.json`](../../results/v2_1/deepseek-smoke-v1/analysis.json). The prior run and original reports are unchanged.

| Measurement | Previous v2 smoke | Authorized v2.1 smoke |
|---|---:|---:|
| Completed checkpoints | 8/8 | 8/8 |
| Scoreable trajectories | 1 | 1 |
| Unique intentions stored | 0 | 3 |
| Accepted operations | 0 | 5: 3 creates, 2 revisions |
| Extraction responses | 14 | 8 |
| Extraction structural validation failures | 0 | 0 |
| Extraction application validation failures | 6 | 0 |
| Accepted empty updates | 8 | 5 |
| Distractor intentions proposed / accepted | 2 / 0 | 0 / 0 |
| Selection application validation failures | 3 | 1 |
| Selection structural validation failures | 0 | 0 |
| Retries: extraction / selection / total | 6 / 2 / 8 | 0 / 1 / 1 |
| Final fail-closed checkpoints | 1 | 0 |
| Tool queries | 0 | 7 |
| Task executions / successful receipts | 0 / 0 | 3 / 3 |
| Final receipt-completed intentions | 0 | 3 |
| TP / FP / FN | 0 / 0 / 2 | 3 / 0 / 0 |
| Precision / recall / Set-F1 | undefined / 0 / 0 | 1 / 1 / 1 |
| Model calls | 24 | 17 |
| Input / output tokens | 57,052 / 4,380 | 68,964 / 2,238 |
| Total tokens | 61,432 | 71,202 |
| Summed model latency | 170.031 s | 96.060 s |
| API-response-reported cost | $0.01525668 | **$0.016737** |
| Cumulative conservative reservations | $0.37604352 | $0.26342016 |
| Transport errors / interrupted requests / truncations | 0 / 0 / 0 | 0 / 0 / 0 |

All 17 current responses ended with `stop`. Eight were extraction calls; nine were selection calls including the retry. Every request has a matching response and accounting reservation, and there are no unknown-cost attempts. The saved API cost reconciles with `accounting.sqlite`, at 1.6737% of the $1 ceiling. Reservations are budget guards, not charges. Independently verified billing remains unavailable.

Calls and retries decreased, but input grew by 11,912 tokens and total tokens by 9,770; response-reported cost rose by $0.00148032 (9.70%). This before/after bundle does not isolate which repair caused which change. The projected $0.03201778 was a planning estimate, not a billed amount or future-study estimate.

The old FN denominator was two because registration failed and dependent sealing never became due. Registration succeeds in v2.1, making sealing a third due task. Scenario bytes and official scoring are identical; no expected answer or dependency scoring was changed.

## Four separate judgments

**1. Extraction: integration works; semantic fidelity is partial.** `call_0001` creates registration, sealing and archiving, all from the legitimate `m1` task header. Registration has a valid time trigger with a null free-text condition; both hidden tasks have a nonblank predicate/channel. No menu distractor is proposed or stored anywhere in the current run. This resolves the observed empty-ledger bottleneck, but cannot establish general distractor rejection: the new model never challenged the filter with an unsupported draft.

Sealing is the counterexample to a claim of perfect extraction. At checkpoint 1, `i_d1449d3ad46683d8` v1 is pending with `dependencies=[]`, despite its own source quotation including the registration prerequisite. The semantic contract's initial quarantine requirement was not followed. At checkpoint 2, `call_0003` adds the actual registration ID but revises the trigger to `unknown`, drops the already known predicate/channel and quarantines v2. Checkpoint 3 accepts an empty update and leaves it unresolved even though registration now has a receipt. At checkpoint 4, `call_0008` restores the hidden trigger, predicate and channel with the dependency intact, producing v3. No dependency violation occurs in this trajectory, but the early omission means it did not demonstrate faithful prerequisite representation throughout. Validation success checks admissibility, not complete semantic entailment.

The five accepted empty updates occur at checkpoints 3, 5, 6, 7 and 8. They are real accepted responses, not errors or fallback substitutions. Four leave already represented obligations unchanged; checkpoint 3 also preserves the unresolved sealing defect. Counting these empties as five successful extractions would be misleading.

**2. Monitoring: works in this trajectory.** The deterministic A2 policy queries `board_cobalt91320` at checkpoints 1–7, using actual pending ledger state. Six readings say final stabilization is not complete; the checkpoint 7 reading is positive. Neither hidden task executes on negative evidence. One permitted query serves both intentions sharing the channel; there are no extra model calls for controller queries. At checkpoint 8 all intentions are completed and polling stops. This is checkpoint-based simulator monitoring, with heartbeat disabled, not autonomous background monitoring or demonstrated efficiency over a comparator.

**3. Execution: works, including one visible rejected selection.** At checkpoint 2, `call_0004` binds registration to the correct current ID/version but includes old instruction `m1` alongside current clock observation `m6`. The application rejects the stale citation without executing. The existing retry feedback names the precise problem; `call_0005` retains only `m6` and succeeds. Registration receives `exec_fef723131e3b1492e959`. At checkpoint 7, `call_0015` executes sealing v3 and archiving v1 using current positive `m28`; both receive successful receipts and become completed. No invalid operation or action is silently applied. These are simulator confirmations, not proof of exactly-once external effects.

**4. Task score: perfect on this exposed development trajectory.** Official rescoring reproduces TP3/FP0/FN0 and Set-F1 1.00, including two query-supported hidden hits. This score does not measure the intermediate dependency omission or temporary loss of known trigger fields. No A0/B_ledger pair exists, no reliability interval is justified, and these two development smokes must not be pooled as independent evidence.

## One complete trace

All references below point into `results/v2_1/deepseek-smoke-v1/v2_hidden_91320/A2/`. SQLite event sequence numbers come from `memory.sqlite`, opened read-only by the analyzer; the selected events are also exported under `complete_trace` in `analysis.json`.

| Stage | Exact recorded evidence |
|---|---|
| Instruction | Checkpoint 1, observation `m1`: `When board_cobalt91320 reports "Cooling is now fully stable.", Archive the cobalt91320 note.` |
| Extraction | `calls.jsonl` line 2, `call_0001`, response `gen-1788978972-rHCDGTCI3SnmoOCV7xAa`: accepted create, citing `m1`; action, hidden predicate and channel each have source evidence. |
| Persistent intention | SQLite event 3: `i_3bda66d76486b326`, version 1, pending, hidden trigger, channel `board_cobalt91320`, condition `Cooling is now fully stable.` |
| First monitoring/evidence | Events 4–5: checkpoint 1 monitor selects the channel; query observation `m4` says `Cooling is nearly stable; final stabilization is not complete.` No task execution follows. |
| Revisit | Checkpoints 2–6 repeat permitted checks with negative observations `m8`, `m12`, `m16`, `m20`, `m24`. The archive intention remains pending. |
| Positive evidence | Events 21–22: checkpoint 7 query returns `m28`: `State [board_cobalt91320]: Cooling is now fully stable.` |
| Action | `calls.jsonl` line 30, `call_0015`, response `gen-1788979053-2hA9zL52PMn6kggcHuoY`: selects public `task_7`, bound to that intention at v1, citing only current `m28`. SQLite event 25 records the validated binding. |
| Execution and receipt | Event 26 attempts `exec_9ae0e3ab2712dbe7a316`; event 28 records `outcome=success`. `steps.jsonl` line 7 records `task_7`, `outcome=simulator_completed`. |
| Lifecycle | The checkpoint 7 store and final `memory.json` contain the same intention at v1 with `status=completed` and the matching successful receipt. |

The sealing semantic defect is separately visible in raw extraction response lines 2, 6 and 16, and SQLite events 2, 6 and 14. The rejected/retried registration selections are lines 8 and 10; line 9 preserves the exact specific retry feedback. Nothing was repaired retroactively in the run.

## Preservation, checks and replay

The [ZIP archive](../../artifacts/verification/v21-deepseek-smoke-v1-20260909.zip) captures all **20 original output files before post-hoc analysis**, SHA-256 `566625f24819696191b2d5b69d84a2286c9f841b9d2bf01c9b60b55494b6027b`. It includes both databases, raw requests/responses, before/after action mappings, all accepted/rejected attempts, receipts, original report, configuration, manifest and route preflight. The empty `failures.jsonl` indicates no terminal failure; the one recovered validation error is retained in `calls.jsonl`. `analysis.json` and this report are separate post-run additions. The archive is a local Git artifact, not an off-device backup.

Post-run checks: **146 tests pass**, **164 protected files pass**, Python compilation passes and the original free MOCK smoke passes in a fresh temporary directory. The v2.1 preflight and separate archive checks confirm 40 frozen files and historical preservation, including 404 baseline files, 1,355 local/MOCK archive files, 24 original DeepSeek archive files and 59 original frozen source paths at their execution commit. The analyzer independently reproduces both official reports, reconciles costs and execution receipts, verifies the new 20-file archive and checks all eight dashboard frames. UI inspection confirms RECORDED mode, negative/positive evidence, current bindings, receipts and hidden evaluator annotations. No dashboard implementation change was needed.

Read-only verification and replay:

```bash
python3 scripts/analyze_v21_smoke.py > /tmp/kiodai-v21-recorded-analysis.json
python3 scripts/serve_v2.py --study results/v2_1/deepseek-smoke-v1 --port 8771
```

The viewer is available at [localhost:8771](http://127.0.0.1:8771/). Select checkpoints 1, 2, 4 and 7 to inspect formation, quarantine/retry, restoration and positive execution. Source mode stays genuine `LIVE`; the dashboard labels replay **RECORDED**, with inference disabled. The original v2 failure remains replayable separately on port 8768. Do not rerun the live command; its output directory also prevents restart.

**Recommendation: v2.1 is technically ready to freeze for an A0/B_ledger/A2 comparison, with intermediate semantic-field errors explicitly measured alongside task score.** The system now produces auditable extraction, monitoring and execution outcomes, including its errors. Perfect extraction is not a prerequisite for evaluating it. A future comparison needs its own matching freeze and fresh authorization; this smoke provides neither that freeze nor spending permission.

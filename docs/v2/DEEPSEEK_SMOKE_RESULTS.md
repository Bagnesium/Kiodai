# Genuine DeepSeek A2 development smoke — 9 September 2026

**One complete, scoreable real trajectory; unsuccessful end-to-end A2 operation.** All eight checkpoints ran once under the $1.00 authorization. No model/provider substitution, prompt change, paid repair cycle, selective rerun or mock fallback occurred. The full 36-method-trajectory study was not launched. This result is separate from the original pilot, historical follow-up and local Llama attempt.

Execution used freeze `research/v2/deepseek_smoke_v1_freeze.json` and commit `a754559351ba017bb4fc00aa5e0527ea68d05572`. The invocation started at 17:33:54.761 UTC and ended at 17:36:47.503 UTC. All 24 responses identify DeepSeek V3.1 through Novita, terminate with `stop`, and report tokens/cost. The prior complete full-study freeze still verifies unchanged.

## Actual measurements

| Method / independent unit | Checkpoints | TP | FP | FN | Precision | Recall | Set-F1 |
|---|---:|---:|---:|---:|---|---:|---:|
| A2 / one complete hidden-state trajectory | 8/8 | 0 | 0 | 2 | Undefined (0/0) | 0.00 | 0.00 |

The native scorer counts two due misses: registration at 08:00 and archiving at 13:00. There were **three instructed obligations and zero completions**. Sealing never became due because its registration prerequisite was never completed; the official FN=2 must not be described as only two unfulfilled instructions. No comparator ran, so no A2−A0 or A2−B_ledger difference exists. Sequential checkpoints and calls are not replications.

| Internal phase | Calls including retries | Retries | Validator rejections | Input tokens | Output tokens | Sum latency (s) | API-response cost (USD) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Extraction/revision | 14 | 6 | 6 | 30,412 | 3,692 | 129.241 | 0.00882740 |
| Selection | 10 | 2 | 3 | 26,640 | 688 | 40.790 | 0.00642928 |
| Total | 24 | 8 | 9 | 57,052 | 4,380 | 170.031 | 0.01525668 |

There were zero tool queries, transport failures, output truncations, committed intentions, task executions or receipts. All 14 extraction outputs passed the emitted JSON schema. Six then failed application validation. The other **eight were accepted empty operation lists**, not successful intention extraction. No extraction exhausted both attempts into an explicit extraction fallback. Selection exhausted both attempts at checkpoint 2, producing **one explicit fail-closed empty action**; the other seven checkpoints ended with model-produced empty task selections. The raw `calls.jsonl` supplies internal retry counts; the older adapter's per-interaction attempt field is not an internal-call counter.

## What failed, and what the evidence does not establish

The first attempts at checkpoints 1, 2, 3 and 8 proposed the three real tasks, with correct action descriptions and the registration time. The registration and archive records had `condition: ""`. The sealing condition retained its prerequisite, while the cooling requirement appeared in trigger evidence rather than in the structured condition. The application rejects empty condition text and atomically rejected each entire batch. Each permitted retry returned `{"operations": []}`. Checkpoints 5 and 7 proposed a different, semantically wrong record; their retries were also empty. Checkpoints 4 and 6 returned empty updates immediately, despite the ledger still having no retained obligations. Absence of a new instruction at those two checkpoints makes a no-op format-valid; it does not repair the earlier omissions.

This exposes an **integration contract gap**: the emitted schema allows an empty condition string, while `Store.apply` requires nonempty condition content, and the extraction prompt does not clearly state that additional constraint. The generic retry message did not explain the failing field. Schema-conforming output therefore was not sufficient to operate the application. This is not an endpoint/TLS failure or proof that DeepSeek cannot extract intentions under a different contract. The active frozen run was allowed to finish unchanged; no post-result repair or paid rerun was performed.

There is also a separate **semantic failure**, independent of JSON and citation validity. At 11:00 (checkpoint 5), the model cited the legitimate menu line `task_5: Discard the cobalt91320 case.` in observation `m11` and tried to create a deferred intention from it. That line was an available distractor action, not a user instruction. The frozen prompt explicitly says that menu entries are not new instructions. At 13:00 it made the analogous proposal from `m15`. The citations are genuine spans, yet the interpretations are wrong. Application validation rejected these drafts too. Post-hoc checking found zero nonexistent citation spans in the extraction drafts; **valid citations did not imply faithful extraction**.

At 08:00, both selection attempts chose the correct registration handle but used the action sentence as an intention ID, although the supplied intention map was empty. The application rejected the nonexistent reference, then failed closed. At 09:00, one analogous attempt was rejected, followed by an empty valid retry. These are selection/reference failures, not executed false positives. The model's correct association of registration with the visible 08:00 clock did not complete the pipeline.

## Instruction → intention → query → action → receipt trace

| Stage | Saved evidence for the archive obligation |
|---|---|
| Instruction received | Observation `m1`: when `board_cobalt91320` reports “Cooling is now fully stable.”, archive the cobalt91320 note. |
| Draft extraction, checkpoint 1 | Correct action and channel, cited positive-trigger phrase; `condition` empty. |
| Intention commit | Entire extraction batch rejected; retry empty; no archive record assigned an ID. |
| Negative checkpoints 1–6 | Controller logs `selected: []` because the store is empty. No query; no returned negative reading. |
| Positive checkpoint 7, 13:00 | Visible scene says the review window opens while cooling continues out of sight. It does not establish stabilization. Controller again issues no query. |
| Hidden evidence | The evaluator-side scenario contains the positive reading at checkpoint 7, but no such reading reached the agent. It must not be counted as a received observation. |
| Action | No archive handle selected; official missed archive due opportunity. Sealing remains prerequisite-blocked. |
| Receipt / completion | No execution receipt, no completion. |

Thus the smoke **does not demonstrate that a negative reading prevents premature action, rechecking obtains positive evidence, or completion follows a successful receipt**. Those pipeline stages were never reached. Zero false positives here reflect no executed task actions, not demonstrated monitoring quality. Software mechanics established by separate local tests remain separate evidence.

## Cost, authorization and projection

| Quantity | USD | Source / certainty |
|---|---:|---|
| Pre-run usage estimate, no retries | 0.02715084 | Pilot token/byte calibration plus this scenario's full-history MOCK request sizes; estimate only |
| Pre-run all-calls-retried sensitivity | 0.05723518 | Padded projection, not the guard |
| Complete smoke conservative allowance | 0.49729536 | 32 maximum attempts at fixed input/output caps |
| Actual cumulative reservations | 0.37604352 | SQLite reservations for 24 attempts; never refunded |
| Actual API-response-reported cost | 0.01525668 | Sum of 24 saved response usage.cost values; none missing |
| Independently verified billing | Unavailable | No independent billing reconciliation performed |

The API reports 33,536 cached input tokens. At frozen uncached prices, the same reported input/output token totals would cost $0.01978404; the observed response cost is lower. Cache discounts were not used in the conservative guard. The authenticated preflight key limit remaining was $1.96187372; this is a key spending allowance, not verification of account credit or billing. Public endpoint and key metadata reads generated no model calls. The original pilot's $0.00765034 and historical follow-up's $0.03047594 remain separate.

`full_study_usage_projection.json` gives a revised **planning projection of $1.03943**, compared with the original $0.67219. It uses observed extraction/selection token-to-request-byte ratios and retry rates (6/8 and 2/8), retains successful full-study MOCK history sizes, 35% input padding, and output floors of 750/256 tokens. It retains the prior A0 forecast and explicitly assumes transfer of phase calibration to B_ledger. This is an uncertain planning scenario: empty-ledger behavior and one hidden-state template do not represent a functioning pipeline or every template family. The **full conservative allowance stays $19.95251712**. Cheap failure is not a reason to reduce that guard. The full evaluation remains unlaunched.

## Preservation, replay and verification

Artifacts: `results/v2/deepseek-smoke-v1/`. Raw trajectory: `v2_hidden_91320/A2/`, including `calls.jsonl`, `agent.jsonl`, `steps.jsonl`, `actions.jsonl`, `failures.jsonl`, `memory.sqlite`, `memory.json`, `score.json`, scenario/config copies and hashed manifest. Root files include the spending ledger, sanitized preflight, execution commit, saved freeze, reports, detailed `behavior_audit.json` and revised projection. Preservation archive: `artifacts/verification/deepseek-smoke-v1-20260909.zip`; inventory: `research/v2/deepseek_smoke_artifact_inventory.json`. This is local Git preservation, not an off-device backup claim.

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 scripts/restore_v2_artifacts.py
python3 scripts/restore_deepseek_smoke.py
python3 scripts/analyze_v2_smoke.py
python3 scripts/serve_v2.py --study results/v2/deepseek-smoke-v1 --port 8768
```

Open `http://127.0.0.1:8768/`. RECORDED is explicitly labeled genuine LIVE output, with inference disabled. Checkpoint 2 shows the failed selection; checkpoint 7 shows no query at the positive opportunity. The full raw attempts are expandable. Only one inaccurate display string was corrected after execution: an empty A2 ledger is now labeled as having no stored records, rather than saying the method has no external ledger. No interface feature or evaluated code changed.

The generic frozen report renderer's four-family/paired-study description is also corrected **only in the offline smoke report**, with the original generic outputs retained as `report.engine.json` and `.md`. Case measurements and raw artifacts are unchanged. Reproduction uses `scripts/analyze_v2_smoke.py`, which invokes the original scorer, verifies artifacts, then applies the smoke's actual scope label.

Validation: 101 tests passed before inference and again after reporting; all 164 protected hashes, full and smoke freezes passed unchanged. Compilation, the existing smoke check, byte-identical saved-analysis reproduction, archive integrity and all eight RECORDED checkpoints passed. The 24-file archive has SHA-256 `f0b9b400520e0950eeb3d7cd6a3665690613f5e3b13e5432812a8937b432d57b`. Verification made no further paid calls.

**Remaining blocker:** this frozen A2 configuration did not demonstrate functioning extraction, monitoring or receipt-based execution. It is valid negative development evidence, not a successful integration or a basis for comparative superiority. Preserve this result and stop; do not launch the full study from it.

Для одного полного проверочного сценария A2 обработал восемь шагов, но не сохранил ни одного намерения и не выполнил ни одной задачи. Все ответы извлечения соответствовали JSON-схеме, однако часть нарушала дополнительные требования программы, а остальные содержали пустой список изменений. Запросов к скрытому каналу не было. Результат выявляет проблему интеграции и ошибки понимания инструкций, а не подтверждает работоспособность памяти или преимущество над другими методами. Стоимость по ответам API составила 0,01525668 доллара.

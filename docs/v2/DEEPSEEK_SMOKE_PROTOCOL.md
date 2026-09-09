# One authorized A2 development smoke — frozen before inference

The user authorized one cumulative $1.00 development integration run on the complete existing `v2_hidden_91320` scenario. This is one A2 trajectory, eight checkpoints, one repeat, with no A0/B_ledger comparison. It was chosen explicitly by the user after local failures; it is exposed synthetic development material, not a blind test. No additional experiments or full-study execution are authorized here.

## Failure audit before spending

`research/v2/deepseek_smoke_failure_audit.json` records the raw local Llama source hash and independently reproduced validation failures. At checkpoint 1 both responses parse under the schema, but their citations fail: the first cites absent text `null` and uses a channel name as an observation reference; the retry cites `08:00` against the 07:00 menu observation, as well as other nonexistent spans. Both also nominate `m1` as a create target and supply invalid dependencies, which would fail later checks. No intention was partially committed. These are model output/reference and interpretation errors, not evidence of a faulty citation validator. Quotes are checked against the decoded supplied observations, not against escaped JSON text.

Checkpoint 2's first response has `done_reason=length`, exactly 3,072 output tokens, and an unterminated JSON string. This is confirmed output-cap truncation. The next request times out after 120.002 seconds without a response. The preceding long generation makes slow generation plausible, but the saved timeout does not establish the server-side cause. Tokens for that timed-out request remain unknown. Local Llama behavior does not predict DeepSeek behavior.

There was also an artifact-finalization bug in the original local run: the official scorer rejected an incomplete trajectory before all final artifacts were written. The already committed v2 engine fixes that separately, preserves the original failed artifacts with a recovery manifest, and reports incomplete primary metrics as unavailable. This smoke changes no engine, prompt, schema, citation check, or failure policy. It adds only a restricted launcher that calls the same `run_case`/Gateway/Accounting implementation; the original full-study freeze remains unchanged and must still pass.

For output sizing only, the existing software fixture's complete three-record extraction is 2,721 UTF-8 bytes and passes schema validation. This makes a compact answer within 3,072 tokens plausible; it is not an exact DeepSeek token count, a promise of complete extraction, or genuine model evidence. No fixture response or gold answer enters LIVE requests.

## Exact protocol and accounting

`configs/v2_deepseek_smoke_v1.json` differs from `configs/v2.json` only in scope/version/order/cap metadata. DeepSeek `deepseek/deepseek-chat-v3.1`, Novita fp8 only, fallbacks disabled, required parameters enabled, reasoning disabled/excluded, temperature 0, top_p 1, seed 20260904. Full history, one allowed deterministic A2 query per checkpoint, no heartbeat, original anonymous menus and receipt semantics. Each checkpoint has one extraction/revision call and, if extraction validates, one selection call after any query. Each internal call permits exactly one fixed corrective retry. Transport retries are zero. Invalid extraction/selection fails closed; no gold repair, mock replacement, selective rerun, or fresh allowance.

The endpoint metadata saved in `artifacts/verification/deepseek-smoke-preflight/endpoint-and-key.json` advertises `response_format` and `structured_outputs` as well as every other requested sampling parameter, at the frozen prices $0.27/M input and $1/M output. Metadata is checked again immediately before inference. Advertised strict-schema support does not establish semantic correctness or eliminate the need for client validation. [OpenRouter structured-output documentation](https://openrouter.ai/docs/guides/features/structured-outputs).

The authenticated `/key` GET reports a $2 key limit and $1.96187372 remaining before this smoke, with the credential present in untracked `.env`. Only sanitized allowance fields are saved; neither the key nor its label is recorded. This is the key's limit, not independently verified account credit/billing. Metadata GETs generate no model tokens; no paid preflight generation is planned. [Key endpoint](https://openrouter.ai/docs/api/api-reference/api-keys/get-current-api-key).

The input reservation for **every attempt**, including growing full history and retry corrections, is `(48,000 serialized request bytes + 1,024 framing tokens) × $0.27/M = $0.01323648`. Requests above the byte limit stop before inference rather than truncate context. Extraction has 3,072 output tokens: $0.01630848 per attempt. Selection has 1,536: $0.01477248. Therefore the complete bound is `8 × (2 × 0.01630848 + 2 × 0.01477248) = $0.49729536`, at most 32 model attempts plus 8 nonbillable simulator queries. Revision operations share extraction's allowance. The complete bound is checked before starting, and SQLite reserves each attempt durably before sending; reservations, including unknown outcomes, are never refunded. The ceiling remains $1.00. The full-study guard remains **$19.95251712**.

The separate `research/v2/deepseek_smoke_estimate.json` projects usage from this scenario's actual full-history MOCK request sizes and the original genuine pilot's observed token/byte ratio, with 35% input padding and expected 750 extraction/256 selection output tokens per call. It gives both a no-retry projection and an all-calls-retried sensitivity estimate. Neither replaces the conservative guard. Synthetic request sizes inform cost only, not model performance.

## Freeze, success criteria, artifacts

`research/v2/deepseek_smoke_v1_freeze.json` hashes the original frozen code/prompts/scenarios/configuration plus this launcher, smoke configuration, audit, estimate, protocol and scope tests. It is committed before inference. The run records the commit and exact hashes again. All eight checkpoints must be processed for a usable complete trajectory; a perfect score is not required. The official protected scorer computes trajectory TP/FP/FN, precision, recall and Set-F1; checkpoint diagnostics are descriptive only. Primary results are unavailable if interrupted, without imputation or exclusion of unfavorable attempts.

Post-hoc semantic review will compare extracted fields with legitimate received instructions, inspect negative and positive query evidence before action, verify handle/action alignment and receipt-based completion, and separate empty valid updates from failed extraction. These assessments are never fed back into evaluated decisions. Native completed-handle removal still prevents an independent claim of prompt-driven duplicate prevention. Simulator receipts establish completion in this environment, not robust external-world execution. One exposed trajectory cannot establish extractor reliability, general superiority, cross-day performance, or autonomous background monitoring.

The sole LIVE output is `results/v2/deepseek-smoke-v1`. Its exclusive creation prevents any restart or output-directory budget reset. Raw requests/responses, invalid attempts, action mappings, agent observations, SQLite history, receipts, evaluator outputs, costs and manifests are retained, including partial failure. The genuine saved data will be served through the existing RECORDED viewer; no interface redesign.

```bash
python3 scripts/run_v2_smoke.py --preflight
python3 scripts/run_v2_smoke.py --live --budget-usd 1.00 --env-file .env
```

The live command is for this single already-authorized smoke. It must refuse execution once an attempt exists. Stop after reporting; do not launch the full study.

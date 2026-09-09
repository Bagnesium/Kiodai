# Kiodai v2 — method and frozen evaluation

Author: Bagdat Beimzhan. Deadline: **13 September 2026**, Asia/Almaty. Branch: `codex/kiodai-v2`. This architecture change is explicitly separate from historical A1/P1. Research question: **Does a bounded monitoring policy improve end-to-end deferred-action reliability over an otherwise shared structured ledger, and at what total model/tool cost?** A0 provides the prompt-only reference. This is a system comparison, not a test of improved intrinsic model memory.

The existing A0/A1 prompts, runners, original reports, both live studies and 164 protected upstream files remain unchanged. `research/v2/legacy_state.json` preserves the 404-file starting state at `3145bd1`; the claims register may only receive an appended v2 section. Historical raw metrics were rechecked in `history_check.json`: first pilot A0=A1 TP5/FP0/FN0; follow-up A0=A1 TP11/FP0/FN1, Set-F1 22/23. A1 added 9,800 input tokens in the follow-up, with $0.03047594 combined API-response cost. Billing remains unverified. The overlapping Monday segment is not independent evidence.

## What changed

`kiodai_v2/runner.py` adapts the existing native simulator through JSON frames. Only received messages, anonymous handles/menu text, allowed channel names, local checkpoint numbers and documented execution receipts cross into `agent.py`. Canonical IDs, due sets, future steps and unqueried channel values stay in the environment/evaluator. Post-selection evaluator artifacts live separately from `agent.jsonl`. The dashboard reveals evaluator information separately after selection.

For B_ledger and A2, one extraction call per checkpoint proposes a batch of creations/revisions/cancellations with quoted source spans. `store.py` validates the complete batch atomically in SQLite. IDs are assigned locally; versions increase on revision/cancellation. Multiple intentions are supported. Ambiguous updates quarantine active records rather than picking a target; explicit clarification can revise them. Source-span validity does not establish semantic validity. Unknown channels/times cannot be invented. Dependencies use existing intention IDs; dependencies between simultaneously newly extracted records may require a later revision, and missing semantic dependencies remain a real extraction risk.

Code enforces current versions, pending/failed status and completed dependencies. The LLM interprets triggers and binds actions to anonymous handles. Current-checkpoint evidence is required for structured selections; merely citing a current menu can still be a semantic model error and must be scored accordingly. Hidden evidence is classified afterward as a timely query-supported hit, visible-supported hit, unsupported hit, miss, or false action. The classifier matches explicit native event text; semantic paraphrase cases may require manual review of the retained frame.

Both ledger methods share extraction, storage, action selection, lifecycle and one external query per checkpoint. **B_ledger's model chooses whether to query; A2's controller does so.** A2 groups eligible intentions by channel and queries the least recently checked channel, breaking ties by channel name. Query tickets contain intention versions and are revalidated. A new checkpoint expires evidence for action-support purposes: a prior negative does not suppress later checks, and a prior positive alone cannot justify a later action. If the clock is hidden, pending time intentions cause a permitted clock query rather than access to simulator time. A2 polls at ordinary decision points; it adds no heartbeat/background opportunities. This is simple bounded polling, with no claimed efficiency gain over periodic polling. Budget exhaustion and unresolved evidence are logged.

Selection and attempted execution are distinct from success, failure and uncertainty. Only a documented successful native simulator receipt completes a record. Native failure receipts do not pretend a task succeeded. Separate `LocalExecutor` tests commit a simulated side effect and stable-ID receipt atomically, including restart/retry checks. An uncertain outcome blocks automatic re-execution. This does not establish exactly-once external email/calendar behavior. Frozen P1 still assumes completion after selection; PM-Bench still removes completed handles.

## Fixed comparison

| Item | Declaration |
|---|---|
| Primary methods | A0, B_ledger, A2. Historical A1 remains callable through the adapter and existing commands, but is outside this paid matrix. |
| Cases | 12 complete synthetic development trajectories; four families × three predeclared seeds; 8 steps each. 96 steps per method, 288 total; 24 reachable due actions per method under successful play. |
| Families | Repeated rescheduling/cancellation; visible cues/overrides/near matches; hidden negative→positive state and simultaneous intentions; cross-day delay/dependencies. |
| Origins | `scripts/generate_v2_cases.py`, `data/v2/catalog.json`. Existing independent development material informed design; no released final-week modifications. All cases and mock outputs were inspected before freeze. |
| Model | `deepseek/deepseek-chat-v3.1`, OpenRouter → Novita, fp8 only, fallback disabled, required parameters; reasoning disabled/excluded. |
| Generation | Temperature 0, top_p 1, seed 20260904. Maximum outputs: baseline 256, extraction 3072, structured selection 1536. Shared request byte cap 48,000; no truncation. |
| Context/opportunities | Matched full history; same initial observations, menus, native execution semantics, receipts and channel permissions. One external query per checkpoint; no heartbeat. |
| Order/repeats | Catalog order; rotate A0/B_ledger/A2 order by trajectory index. One repeat. Separate ledger state per method and trajectory. |
| Invalid responses | One schema/reference/lifecycle-validation retry. If still invalid, no task action that checkpoint. Retain both raw outputs. Extraction failure is an end-to-end failure, not an exclusion. |
| Infrastructure failure | Any transport failure stops the entire study. Retain the request reservation and unknown cost. No fresh-root restart, automatic resume, substitute output or selective rerun. |
| Primary scoring | Unchanged `PM.score_log`: whole-trajectory TP/FP/FN, precision, recall, Set-F1. Undefined denominators stay null. Incomplete trajectories have no primary score; observed-step diagnostics are separate. |
| Aggregation | Per-trajectory differences and their unweighted mean, A2−B_ledger primary contrast and A2−A0 reference contrast. A complete-study mean requires all 12 matched trajectories; a positive value is descriptive evidence on this suite only. Descriptive pooled micro totals also shown. No independent-replication claim for steps, calls, seeds within a family, or overlapping historical observations. No significance/equivalence claim. |
| Diagnostics | All hidden due opportunities, including extraction failures; invalid/retry/transport counts; official commission/update/dependency diagnostics; query evidence; receipts; total internal calls, tokens, latency and API-response cost. Native duplicate effects are unavailable. |

The freeze is `research/v2/freeze.json`; it records implementation, prompts, scenarios, tests and configuration hashes. Model outputs from the upcoming evaluation must not be used to revise this frozen method. New method changes require a new development version and separate evaluation.

## Cost and authorization

`research/v2/cost_projection.json` projects **$0.67219** uncached, assuming no validation retries. It uses the genuine pilot's input-token/request-byte ratio (32,998/140,262), actual v2 mock request sizes, a 35% input growth margin, 750 output tokens per extraction, 256 per structured selection and the pilot's 33.625 per baseline call. It includes all three methods and conservative extra query cycles: 528 projected calls. Extraction output can be longer or invalid; the local smoke demonstrated that risk. This projection is not the spending guard.

The guard reserves **$19.95251712** for the complete evaluation, against an explicit **$20.00** proposed ceiling. It allows one token per UTF-8 request byte plus 1,024 framing tokens, full output caps, all possible query interactions, and a corrective retry at every internal call: up to 1,344 attempts. Each matched triple needs $1.66270976 available before starting. Durable per-attempt reservations occur before send and are never refunded, including timeouts. Route metadata GET is nonbillable and no model preflight is used. The pinned endpoint/prices are rechecked before LIVE. Charges above an allowance cause an immediate stop; independent provider billing cannot be guaranteed by an application estimate.

**No new paid inference has been authorized or executed.** The prior $0.70 applies only to the completed follow-up. A future authorized run is exactly:

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 scripts/run_v2.py --preflight
python3 scripts/run_v2.py --live --budget-usd 20.00 --env-file .env
```

Only the user should execute the LIVE command after granting that fresh authorization. The `.env` key is parsed locally without interpolation and never printed. LIVE has one fixed artifact directory: `results/v2/live-frozen-v2`. Repeated invocation after any attempt is refused. An incomplete run is reported, not silently shortened or restarted.

# Claims Register

| Claim | Supporting experiment | Supporting metric | Confidence | Limitation | Safe wording |
|---|---|---|---|---|---|
| The original released artifacts can be rescored locally | Released-log replay audit | Deterministic aggregate reconstruction | Preliminary | Does not validate live model execution | “Released trajectories are locally scoreable.” |
| The original live runner is leakage-free | None | None | Rejected | Oracle due-set fallback exists | “The released runner contains a potential oracle fallback.” |
| One static skill improves prospective memory | Frozen first-day pilot, `live-pair-42433e00474b`, one matched pair | A0=A1: TP=5, FP=0, FN=0, Set-F1=1.00; paired difference 0 | No improvement observed in this pilot | One development scenario; baseline ceiling; no general equivalence or superiority established | “The exploratory pilot found no accuracy benefit from P1; both conditions reached the score ceiling.” |
| PIS is reproduced | Not run | None | None | Official code not located | No reproduction claim permitted. |

## Final follow-up evidence — 9 September 2026

| Claim | Actual evidence | Safe wording and limit |
|---|---|---|
| P1 improves accuracy on the follow-up | One three-day pair, both TP=11, FP=0, FN=1, Set-F1=22/23; A1−A0=0 | No observed accuracy improvement; not general equivalence. Planned after pilot 1 and overlaps Monday. |
| Hidden-state monitoring succeeded | A0 queried once at Tuesday 11:30 and received a negative observation; A1 never queried. Both missed the positive event at 13:00 | No query-supported hidden hit in either condition; one negative query does not demonstrate successful monitoring. |
| Cross-day intentions succeeded | Both selected the badge at Wednesday 12:00 and archive card at 15:00, withholding near matches | Two successful cases with full original history and action-text menus available; no independent memory-store claim. |
| A1 imposed overhead | 9,800 extra input tokens (+16.56%); API-response cost +$0.00139376 (+9.58%), despite one fewer model call | Observed overhead in this pair; caching/order/query-history confounds prevent general attribution. Verified billing unavailable. |
| Independent duplicate prevention / execution confirmation / background monitoring established | No supporting experiment | P1 assumes completion after selection; environment removes completed handles; heartbeat disabled. |

Sources: `FOLLOWUP_RESULTS.md`, `artifacts/verification/followup-live-20260909/analysis.json`, `results/followup_v1/live-pair-bdf241965f35/`. Original pilot evidence and zero-difference conclusion remain unchanged. No further experimental development is planned for this submission.

## Explicit scope change: separately versioned v2 — 9 September 2026

The user subsequently authorized a separate v2 implementation and free local verification, with a revised deadline of 13 September. This does not alter or relabel any historical A0/A1 result, and does not authorize new paid inference. The preceding historical scope statement is preserved as written.

| V2 claim | Evidence | Permitted wording |
|---|---|---|
| Typed ledger, version checks, bounded queries and receipt lifecycle work in the simulator | `tests/test_v2.py`; complete MOCK traces in `results/v2/mock-verification-v2/` | Software mechanics verified; model interpretation reliability remains unproven. |
| A2 improves accuracy over A0 or B_ledger | No completed paid v2 evaluation | No improvement claim. Identical mock scores are not model-performance evidence. |
| A2 can revisit a negative hidden state and obtain a later positive state | Cooling-only MOCK regression `results/v2/known-cooling-regression-v2/`; full original 20-step story, other misses retained | A development software regression, not a live comparative success. |
| Local Llama reliably extracts cited intentions | One interrupted local smoke: two invalid citations, one truncated malformed output, then timeout; 1/8 checkpoints completed | This local attempt did not establish reliable extraction or a usable trajectory. Preserve `results/v2/local-smoke-v2/`. |
| The design is novel or PIS was faithfully reproduced | No such evidence; see `docs/v2/SOURCES.md` | PIS-inspired reconstruction plus engineering integration and an untested monitoring ablation. |
| Exactly-once external actions or autonomous monitoring established | None | SQLite simulator idempotency tested separately; native PM-Bench removes completed handles; heartbeat remains disabled. |

Complete v2 protocol, costs, limitations and proposed manuscript text: `docs/v2/METHOD.md`, `docs/v2/FINDINGS_AND_DEFENSE.md`. All v2 cases are exposed synthetic development material, not blind or independently held out.

## Genuine A2 development smoke — 9 September 2026

The user subsequently authorized exactly one intact A2 hidden-state smoke with a cumulative $1.00 cap, expressly withholding the full study. `results/v2/deepseek-smoke-v1/` preserves the complete invocation at code commit `a754559351ba017bb4fc00aa5e0527ea68d05572`; no prompt/model/engine change or paid rerun occurred.

| Claim | Actual evidence | Safe wording |
|---|---|---|
| One real A2 trajectory is available | 8/8 checkpoints, 24 model calls, no transport errors; official TP0/FP0/FN2, precision undefined, recall/F1 0 | Complete negative development evidence; not a successful integration. Three instructed tasks remained incomplete; dependent sealing never became due. |
| DeepSeek operated extraction successfully | 14 schema-valid extraction responses; 6 additional-validation failures; 8 accepted empty updates; 0 accepted operations | A schema/application contract gap and semantic errors prevented a populated ledger. Empty updates are not successful extraction. |
| Correct citations establish correct intentions | Two rejected drafts promoted the visible discard-menu distractor into an instruction, with real source spans | Citation provenance alone does not establish semantic fidelity. |
| Monitoring, selection and receipt completion worked end to end | 0 queries, 0 executed task actions, 0 receipts; 3 invalid selection responses and one final fail-closed checkpoint | No such success demonstrated. Negative/positive hidden readings never reached the model. |
| A2 outperforms a comparator | No comparator in this smoke | No comparative claim permitted; one exposed trajectory is not reliability evidence. |
| Cost and future allowance are established | Saved API costs $0.01525668; independent billing unavailable; full conservative guard unchanged at $19.95251712 | The revised $1.03943 planning projection is uncertain and does not authorize or validate the full study. |

Detailed results, semantic trace, cost sources, preserved failure analysis and replay: `docs/v2/DEEPSEEK_SMOKE_RESULTS.md`. Historical pilot/follow-up results and the original full-study freeze are unchanged. The evaluated engine remains frozen; only post-hoc report scope text and one unfrozen empty-ledger display label were corrected. No further inference follows this smoke.

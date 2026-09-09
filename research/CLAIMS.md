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

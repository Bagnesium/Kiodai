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

## v2.1 extraction repair — offline development only

The user subsequently authorized a narrow integration repair, offline tests and local commits, explicitly forbidding new model inference. Implementation `959db38dac8b68f63ecf79420dcd53bea2278cf2` aligns extraction contracts, adds obligation-provenance and unresolved-state constraints, strengthens binding IDs and supplies specific bounded retry feedback. This is a new development revision; original freezes and failed runs remain unchanged.

**146 passing tests**, including 35 new regressions, and `results/v2_1/offline-repair-v1/` verify structural boundaries and MOCK integration: 8 checkpoints, 16 fixture calls, 7 queries, 3 receipt-completed intentions. They do not prove semantic extraction reliability, provider schema enforcement, real-model monitoring/execution success or superiority. A regression deliberately demonstrates that narrative hypothetical entailment remains model-dependent.

One new A2 development smoke is specified in `research/v2_1/smoke_v1.json` and **has not run or been authorized**. Its candidate $1 ceiling covers a $0.49729536 conservative reservation; usage projection $0.03201778 remains uncertain. The old full-study freeze is not a matching v2.1 evaluation. Evidence, limits and commands: `docs/v2_1/EXTRACTION_REPAIR.md`.


## Authorized v2.1 development smoke — 9 September 2026

The user subsequently authorized exactly one `v2.1-deepseek-smoke-v1` with a cumulative $1.00 cap. It executed at `392c58f80b61252759d0eb60df98be6c16d94e47` using frozen implementation `959db38dac8b68f63ecf79420dcd53bea2278cf2`. The prepared manifest, implementation and earlier negative results remain unchanged. No further paid inference or comparative evaluation followed.

| Claim | Recorded evidence | Safe wording and limit |
|---|---|---|
| The previous empty-ledger bottleneck was resolved | 8/8 checkpoints; 3 creates and 2 revisions; 0 extraction validation failures; 5 accepted empty updates | Supported actions entered the ledger in this one exposed development trajectory. Empty updates are not extra successful extractions. |
| Extraction is fully faithful | Sealing initially omitted its prerequisite; checkpoint 2 added the dependency but dropped known hidden-trigger fields, leaving the record quarantined through checkpoint 3; checkpoint 4 restored it | Rejected: semantic-field errors remain despite no extraction validation rejection and a perfect task score. |
| Menu distractor interpretation is reliable | 0 unsupported action proposals and 0 stored distractor intentions in this run | No distractor error observed here; no general reliability or live rejection-mechanism claim. |
| Monitoring and receipt-based execution can operate end to end | 7 queries, six negative readings followed by a positive reading; 3 task executions and 3 successful simulator receipts; one stale selection citation corrected by the single retry | Narrow development integration feasibility. No autonomous background or external exactly-once execution claim. |
| A2 has high comparative performance | Official TP3/FP0/FN0, precision/recall/Set-F1 1.00; no comparator | One development task score, not A2 superiority over A0/B_ledger. No reliability interval or independent replication claim. |
| Cost is recorded and within authorization | 17 calls; 68,964 input / 2,238 output tokens; API-response cost $0.016737; cumulative reservations $0.26342016; 0 unknown-cost attempts | Recorded response costs reconcile with the ledger; independent billing is unavailable. Unused cap grants no further authorization. |

Sources: `docs/v2_1/DEEPSEEK_SMOKE_RESULTS.md`, `results/v2_1/deepseek-smoke-v1/analysis.json`, all 20 original output files and their ZIP/hash inventory in `research/v2_1/live_smoke_v1_inventory.json`. The recommendation is to freeze the current implementation for an A0/B_ledger/A2 comparison with semantic-field errors measured separately; that requires its own matching protocol freeze and fresh authorization.


## Frozen v2.1 comparison preparation — 10 September 2026

The user authorized only evaluation preparation, offline verification and local commits. Candidate `959db38` is unchanged, including the known prerequisite-formation defect. New support `832d6ff` reuses the existing executor and adds explicit study scope and post-run reporting. `research/v2_1/comparison_v1.json` freezes 12 existing trajectories, four dependent template families, A0/B_ledger/A2 and one repeat, with seed-balanced method positions. Primary contrast is paired trajectory Set-F1, A2 minus B_ledger; A2 minus A0 is secondary.

**No comparative model result exists and no new model inference ran.** The full unchanged-fixture MOCK run (`results/v2_1/comparison-preparation-v1/`) completed 36 method-trajectories, 288 checkpoints, 522 fixture requests and 63 queries. This verifies software mechanics and reporting only. All 24 ledger semantic reviews remain pending, not zero; A0 extraction is not applicable. 162 tests and 164 protected hashes pass. Earlier freezes, prompts, successes and failures are preserved.

All twelve cases were exposed during development/MOCK verification; `v2_hidden_91320` also overlaps the failed and successful network smokes and interrupted local-model smoke. The other eleven are not independently held out. Family and smoke-overlap breakdowns are predeclared; checkpoints/calls/renamed variants are not independent replications. The protocol distinguishes task scores, semantic errors, query evidence/cost and dependency-blocked obligations.

The current planning estimate is $0.71209837, retry-heavy sensitivity $4.57237647, conservative allowance $19.95251712, recommended cumulative authorization $20.00. These are assumptions/guards, not observed comparative costs. A matching named authorization is still required. See `docs/v2_1/COMPARISON_PROTOCOL.md`; no new effectiveness, superiority, reliability or equivalence claim is permitted.

## Authorized comparison blocked before inference — 11 September 2026

The user authorized exactly `v2.1-comparison-v1` once with a $20.00 ceiling, conditional on external funding for its $19.95251712 conservative allowance. The frozen preflight passed at `d7e92d38fc333846670ae196c9ee37f9d616f61a`. Authenticated read-only key/credit checks returned HTTP 200: $4.92988004 key allowance remaining and $9.92988004 account credit. Both failed the funding requirement, so the LIVE command was not invoked. No settings changed and no model inference ran.

This supplies **no comparative result**: 0/36 completed method-trajectories, 0/12 matched blocks, unavailable task scores and paired differences. No comparative semantic correctness, monitoring improvement, superiority, equivalence or generalization claim is permitted. Zero model calls and $0 paid inference do not constitute a model-response cost observation or independently verified billing. The prior smoke's limited feasibility claim and known semantic defects are unchanged. Evidence and manuscript status: `docs/v2_1/COMPARISON_FUNDING_BLOCK.md`; sanitized check artifacts: `artifacts/verification/v21-comparison-funding-block-20260911/`.

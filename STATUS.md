# Current Kiodai status — 8 September 2026

The frozen $0.30 pilot is complete. Exactly one predeclared matched pair ran, with one scenario and two eight-step trajectories. No extra repeat, model, scenario, prompt tuning, or dashboard redesign was added.

| Condition | TP | FP | FN | Precision | Recall | Set-F1 | API-reported USD |
|---|---:|---:|---:|---:|---:|---:|---:|
| A0 | 5 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00336941 |
| A1 | 5 | 0 | 0 | 1.00 | 1.00 | 1.00 | 0.00428093 |

No accuracy improvement was observed. Both conditions reached the score ceiling in this exploratory development pilot. All task selections matched; A1 used 5,360 more input tokens. This single pair cannot establish general equivalence or superiority.

- Pair: `results/kiodai/live-pair-42433e00474b/`; 16 actual calls, no retries, invalid responses, transport errors or tool queries.
- Cost reported in saved responses: **$0.00765034 total**. Prospective stress estimate: $0.13677592. Usage at uncached list prices: $0.00944746. Verified billed cost is unavailable. The remaining authorization was not spent.
- Two earlier TLS startup failures remain unchanged and count as incomplete attempts, not model-performance failures. No model call occurred in either.
- The user-authorized local `.env` supplied only OPENROUTER_API_KEY to the launcher. The key was not printed, copied into artifacts, or tracked. The installed CA bundle enabled verified TLS. The credential blocker is resolved.
- The genuine pair is available in the existing **RECORDED** selector. Its replay and export were verified without model transport. MOCK remains separate.
- All **57 tests** and **164 protected-file hashes** passed after inference; frozen development verification and Python compilation passed. See `artifacts/verification/post-live-tests-20260908.txt`, `post-live-integrity-20260908.txt`, `post-live-development-20260908.txt` and `genuine-pilot-replay-check.json`.
- RESULTS, METHOD, MANUSCRIPT_UPDATES and DEFENSE_RU now describe the actual findings. The supplied manuscript remains unchanged; replacement paragraphs are ready for review.

Known limits remain: frozen P1 assumes completion after selection; PM-Bench removes completed handles; heartbeat is disabled. This pilot covers only the first development day and demonstrates neither hidden-state querying nor cross-day memory.

Rebuild evidence: `python3 artifacts/verification/analyze_live_pilot_20260908.py`.
Replay: `python3 -m research_harness.dashboard`, then RECORDED → first-development-day-pilot-v1 · live-pair-42433e00474b.

Detailed evidence: `artifacts/verification/live-pilot-analysis-20260908.json`. Earlier audit: `artifacts/verification/pilot-retry-audit-20260908T163833Z.json`. No further paid inference is needed for this frozen task.

## Separate follow-up preparation

The completed first pilot above is unchanged and archived. One broader evaluation is now frozen but **not authorized or run**: the whole existing three-day, 20-step development scenario, one matched pair, one repeat. It retains Monday and adds Tuesday/Wednesday rather than slicing away encoding instructions. No new evaluated scenarios or UI features were added.

Usage-informed projection: $0.03935938 (44 calls, two queries per condition, no retries, no cache discount). Unchanged stress allowance: $0.63708409 (up to 160 attempts). Proposed explicit new ceiling: $0.70. Existing pilot/dashboard callers still have their $0.30 default cap. `scripts/run_followup.py` validates the separate freeze and requires new `--live --budget-usd 0.70` authorization; default/preflight performs no inference or credential reads.

Local verification now passes **62 tests**, all 164 protected-file hashes, development integrity and compilation. Offline fixtures validate visible-input solvability and hidden-state isolation; their MOCK outcomes are not new model evidence. No `results/followup_v1/` directory exists. See `COVERAGE.md`, `FOLLOWUP_EVALUATION.md`, `research/followup_freeze_v1.json` and `artifacts/verification/followup-v1-tests.txt`.

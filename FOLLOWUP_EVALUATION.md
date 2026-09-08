# Full-development follow-up v1 — frozen preparation, not run

This evaluation was planned **after observing pilot 1's zero accuracy difference**. Pilot 1 stays in `RESULTS.md` and its preservation archive: both conditions achieved Set-F1=1.00, with 5,360 additional input tokens for A1. No inference is authorized by this preparation, and no follow-up inference has occurred.

## Fixed scope and additions

Use the complete existing `data/development/prospective_memory_dev_v1.json`: **one scenario, three days, 20 steps per condition, one repeat, one matched A0/A1 pair**. There are 14 intentions, including two cancellations; 12 task actions are reachable under a correct trajectory. This adds 12 scheduled steps beyond the pilot's eight, including a prerequisite, a hidden positive event, and two cross-day intentions. Minimum 40 model calls, usage projection 44, maximum 160 billable attempts.

The set was selected by taking the one available independent development scenario whole, rather than selecting cases by model performance. It was authored before the pilot and independently of released PM-Bench task text, but is **development/exploratory, not blind or independently held out**. Monday overlaps the observed pilot, so this is not an independent replication. No new evaluated synthetic cases, slicing, prompt edits, model substitutions or infrastructure redesign were needed. Earlier instructions, dependencies and all day boundaries remain intact.

| Added opportunity | Legitimate information available to both conditions |
|---|---|
| Dependency | Tuesday's initial instruction requires locking before signing; `dev_t_s3` supplies the safety chime, `dev_t_s5` the review window. |
| Hidden-channel check | Tuesday's initial instruction names the sensor board. At `dev_t_s3` it reports nearly stable; at `dev_t_s5` a permitted `sensor_board` query reports fully stable. The latter fact is absent from the visible vignette. |
| Further override/cancellation | Tuesday `dev_t_s2` replaces amber approval with violet; obsolete amber occurs at `dev_t_s3`, violet at `dev_t_s6`. Placard cancellation at `dev_t_s6` precedes its cue at `dev_t_s7`. |
| Two-day delayed intention | Monday `dev_m_s1` instructs filing the archive card on Wednesday's cabinet click; Wednesday gives a scrape lure at `dev_w_s2` and the real click at `dev_w_s4`. |
| Next-day intention | Tuesday `dev_t_s7` instructs hanging the visitor badge on Wednesday's gate opening; `dev_w_s2` keeps it closed, `dev_w_s3` opens it. |
| Distractions / negative steps | Keep all original unrelated notices and negative steps on all three days. Menus still contain action text and some vignettes explicitly identify obsolete cues; this is limited stress, not a hard or cue-free memory benchmark. |

Offline visible-input witnesses traversed every step and legally selected all 12 reachable actions, with zero FP/FN. These are **software reachability checks, not model results**. The witness without queries missed the hidden task (11 TP, 1 FN). In a validation-only counterfactual, changing only the hidden state left all no-query requests identical; the permitted query exposed the change. This confirms that the positive hidden fact requires a query to observe. The unchanged official scorer can nevertheless reward a lucky guess: separately report whether a hidden-task hit followed a query exposing the positive fact. Do not equate an unqueried hit with demonstrated monitoring. The counterfactual is not part of the evaluation. All task-level instruction/trigger/dependency evidence is in `research/followup_solvability_v1.json`; software traces are under `artifacts/verification/followup-v1/`.

## Frozen controls and analysis

- Original A0/A1 development config files and exact baseline/P1 files are unchanged; hashes are in `research/followup_freeze_v1.json`. A0 effective prompt: `a92e6af5cfc6bd7839a0b3ffc00022eb6b332a85ac0e292c61629f5c8a663c38`; A1: `3d8cc7b0a81f5d6ddfa56d526d3299d6582365fdf6e5a5515ca62c53ad9a02b4`.
- OpenRouter `deepseek/deepseek-chat-v3.1`, Novita FP8 only, no fallback; required parameters enforced. Reasoning disabled/excluded; temperature 0, top-p 1, seed 20260904, output limit 256, context cap 32,768 estimated tokens, timeout 120 seconds.
- A0 then A1 at every scheduled step, one repeat (repeat index 0). Histories remain separate and carry forward across all three days, without truncation, external memory, answer sharing or a task legend. Same allowed channels (`clock`, `sensor_board`), at most one executed query per step. Heartbeat disabled in both. Provider determinism and caching are not guaranteed; order is not counterbalanced in this single pair.
- Primary comparison: whole-trajectory official TP/FP/FN, precision, recall and Set-F1; difference A1 minus A0. One scenario and one repeat mean no further averaging. Days/steps are descriptive only, never independent samples. No p-value, confidence interval, equivalence claim, or newly chosen success threshold. Original historical full-study go/no-go thresholds are not adopted by this separately versioned descriptive follow-up.
- Report all failed/partial attempts, invalid output, retries, queries, latency, tokens and separately estimated/response-reported/verified billed cost. Retain unavailable values as null. Record hidden query-supported execution as an auxiliary observation, without changing official scoring. Report full primary trajectory plus clearly descriptive per-day and case breakdowns; do not remove Monday from the primary score or pool it with pilot 1.
- Malformed output and transport errors share at most two attempts per interaction. Malformed output gets a schema-only correction if an attempt remains; exhaustion yields an empty task action and remains scored. Transport failure on the final allowed attempt interrupts the pair. SDK automatic retries stay disabled. Excess query/context-limit failures follow the existing fail-closed rules and remain recorded. No mock substitution or selective rerun.

Frozen P1 assumes completion after selection. PM-Bench removes completed handles. These cases do not independently establish prompt-driven duplicate prevention or robust execution confirmation. Heartbeat is off; querying during supplied steps is not autonomous background monitoring. Only one hidden positive event is included, and successful dependency execution in this simulator does not demonstrate real tool-failure recovery.

## Cost and execution gate

| Cost basis | A0 | A1 | Total USD |
|---|---:|---:|---:|
| Usage-informed projection | 0.01800110 | 0.02135828 | **0.03935938** |
| Unchanged conservative stress allowance | — | — | **0.63708409** |
| Proposed explicit new ceiling | — | — | **0.70** |

The usage projection calibrates each condition's serialized-request-byte/token ratio against its eight genuine pilot calls, then applies it to full 20-step visible-input witness histories with two relevant queries per condition (44 calls total). Projected inputs: A0 63,930, A1 76,364; outputs: 740 each from the pilot mean of 33.625 per call. It assumes no retries, similar JSON formatting, similar token/byte ratios, correct-task histories and no cache discounts. This is an estimate of a plausible path, not a measured follow-up or a budget guarantee. Longer histories are explicitly included; the short pilot's cost was not simply reused or multiplied by 20/8.

The budget guard uses the existing padded stress estimator: request UTF-8 bytes/4 × 1.6 input tokens, 256 output tokens on **every** attempt, one query at every step and one retry for every interaction, yielding 160 attempts across both conditions. Frozen list prices are $0.27/M input and $1.00/M output. Both conditions and all permitted retries/tools are included. Route/price/parameter preflight is a free public GET; no billable preflight or monitoring is planned. Future price/route mismatch stops before inference. The allowance is heuristic, not a guaranteed provider bill. Source numbers and traces: `artifacts/verification/followup-v1/audit.json`.

The original CLI/dashboard still default to a maximum $0.30 budget. The follow-up launcher alone supplies the separately frozen $0.70 protocol ceiling, and requires both `--live` and exactly `--budget-usd 0.70`. Neither the estimator nor request reservations were reduced. It checks full-pair headroom before starting and reserves each call, including retries, before dispatch. Reported overruns and uncertain calls retain their cost/reservation. An exclusive output directory prevents a second invocation from silently resetting the budget; any failure ends this planned invocation and must be audited before another is considered. The first pilot's authorization does not carry over.

Local validation only (safe to run now):

```bash
python3 scripts/run_followup.py --preflight
```

**Proposed command; DO NOT execute until the user chooses to authorize this new study:**

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 scripts/run_followup.py --live --budget-usd 0.70 --env-file .env
```

The command uses the existing `Pair`/`RunSession` execution and scorer, parses only the named local key into the process environment, keeps TLS verification enabled with the installed CA bundle, and writes uniquely named raw runs under **`results/followup_v1/`** with a protocol snapshot and cumulative study ledger. No follow-up LIVE directory is created during preparation. After a future run, analyze separately:

```bash
python3 scripts/analyze_results.py --root results/followup_v1 --mode LIVE --output FOLLOWUP_RESULTS.md
```

Do not use `RESULTS.md` as that output: it preserves pilot 1. The initial pilot and its two TLS failures have a fixed local archive and SHA-256 inventory in `research/pilot1_preservation_v1.json`; the follow-up gate verifies them before execution. No manuscript rewrite or UI change is part of this preparation.

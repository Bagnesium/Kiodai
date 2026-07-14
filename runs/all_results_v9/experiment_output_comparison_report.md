# Experiment Output Comparison Report

## Scope

Compared scored PM-Bench runs under `runs/March_ALL_results_v9` using scenario `data/synthetic_week_v9.json`.
- Runs covered: 64 total (8 models x 8 setups).
- Models covered: GPT-5.3-Codex, GPT-5.4, Llama 3.3 70B Instruct, Mistral Large 2512, Mistral Small 3.2 24B Instruct, Qwen3-14B, Qwen3-32B, Qwen3-8B.
- Setups covered: single-baseline, single-todo-ledger, heartbeat-proactive, heartbeat-auto-60m, heartbeat-auto-30m, hier-union-query, hier-majority-vote, hier-unanimous-vote.
- Primary emphasis: `Set F1`, TP/FP/FN tradeoffs, proactive monitoring performance, cross-day/update handling, and state-query behavior.
- Important interpretation detail: `hier-majority-vote` and `hier-unanimous-vote` are included as separate setups, but they are replay-derived decision-rule variants of `hier-union-query`, not fresh inference runs.

## Setup Definitions

| Setup | Run Type | Meaning |
| --- | --- | --- |
| single-baseline | live | Single-agent baseline with no heartbeat scaffold. |
| single-todo-ledger | live | Single-agent run with the notebook-style in-context TODO ledger memory aid. |
| heartbeat-proactive | live | Single-agent run with optional heartbeat; the model decides whether to use proactive reminders. |
| heartbeat-auto-60m | live | Single-agent run with automatic proactive heartbeat reminders every 60 virtual minutes. |
| heartbeat-auto-30m | live | Single-agent run with automatic proactive heartbeat reminders every 30 virtual minutes. |
| hier-union-query | live | Hierarchical 3-subagent run with union-query evidence gathering and coordinator-only final task selection. |
| hier-majority-vote | replay | Replay-derived variant of the union-query run that keeps the same queried evidence but replaces task selection with strict majority vote over subagent task handles. |
| hier-unanimous-vote | replay | Replay-derived variant of the union-query run that keeps the same queried evidence but replaces task selection with unanimous agreement over subagent task handles. |

## Setup-Level Summary (Across 8 Models)

| Setup | Run Type | Macro Set-F1 | Micro Set-F1 | Micro TP | Micro FP | Micro FN | Macro Hit Rate | Macro Precision(hit) | Macro Proactive Hit | Macro Clock Hit | Macro Non-Clock Hit | Total State Queries | Total Actions | Best Model | Worst Model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| single-baseline | live | 60.0% | 59.4% | 358 | 199 | 290 | 55.2% | 66.7% | 29.8% | 46.4% | 3.3% | 106 | 557 | GPT-5.3-Codex (78.9%) | Qwen3-8B (42.0%) |
| single-todo-ledger | live | 62.8% | 62.8% | 358 | 134 | 290 | 55.2% | 73.2% | 28.5% | 45.3% | 1.7% | 118 | 492 | GPT-5.3-Codex (74.8%) | Qwen3-8B (47.8%) |
| heartbeat-proactive | live | 65.1% | 65.0% | 398 | 178 | 250 | 61.4% | 70.6% | 37.5% | 54.7% | 10.0% | 130 | 576 | GPT-5.4 (79.1%) | Qwen3-32B (48.5%) |
| heartbeat-auto-60m | live | 56.6% | 52.2% | 378 | 422 | 270 | 58.3% | 62.0% | 38.1% | 55.2% | 10.8% | 172 | 800 | GPT-5.3-Codex (74.8%) | Qwen3-14B (34.0%) |
| heartbeat-auto-30m | live | 57.8% | 51.5% | 394 | 489 | 254 | 60.8% | 63.2% | 43.3% | 60.4% | 15.8% | 203 | 883 | Mistral Large 2512 (74.7%) | Qwen3-14B (30.3%) |
| hier-union-query | live | 45.2% | 45.9% | 274 | 273 | 374 | 42.3% | 51.2% | 39.1% | 60.4% | 5.0% | 1661 | 547 | Mistral Large 2512 (58.1%) | Qwen3-8B (25.7%) |
| hier-majority-vote | replay | 37.2% | 38.3% | 309 | 655 | 339 | 47.7% | 34.9% | 48.1% | 67.7% | 16.7% | 1661 | 964 | Llama 3.3 70B Instruct (49.4%) | Qwen3-8B (25.3%) |
| hier-unanimous-vote | replay | 35.3% | 39.6% | 229 | 279 | 419 | 35.3% | 47.3% | 31.7% | 49.5% | 3.3% | 1661 | 508 | Mistral Large 2512 (53.3%) | Qwen3-8B (15.5%) |

## Best Setup Per Model

| Model | Best Set-F1 Setup | Best Proactive Setup | Best Non-Clock Proactive Setup | Best Set-F1 TP/FP/FN |
| --- | --- | --- | --- | --- |
| GPT-5.4 | heartbeat-proactive (79.1%) | hier-majority-vote (66.7%) | hier-majority-vote (46.7%) | heartbeat-proactive: 55/3/26 |
| GPT-5.3-Codex | single-baseline (78.9%) | hier-majority-vote (59.0%) | hier-majority-vote (33.3%) | single-baseline: 60/11/21 |
| Llama 3.3 70B Instruct | single-todo-ledger (72.5%) | hier-majority-vote (46.2%) | hier-majority-vote (6.7%) | single-todo-ledger: 50/7/31 |
| Mistral Large 2512 | single-baseline (75.3%) | hier-majority-vote (71.8%) | hier-majority-vote (40.0%) | single-baseline: 55/10/26 |
| Mistral Small 3.2 24B Instruct | single-todo-ledger (63.4%) | single-todo-ledger (30.8%) | single-baseline (6.7%) | single-todo-ledger: 46/18/35 |
| Qwen3-32B | heartbeat-auto-30m (57.5%) | hier-union-query (43.6%) | heartbeat-auto-30m (0.0%) | heartbeat-auto-30m: 44/28/37 |
| Qwen3-14B | single-todo-ledger (52.3%) | heartbeat-auto-30m (92.3%) | heartbeat-auto-30m (80.0%) | single-todo-ledger: 40/32/41 |
| Qwen3-8B | heartbeat-proactive (71.9%) | heartbeat-proactive (66.7%) | heartbeat-proactive (66.7%) | heartbeat-proactive: 64/33/17 |

## Per-Run Core Metrics

| Model | Setup | Run Type | TP | FP | FN | Set Precision | Set Recall | Set F1 | Hit Rate | Exact-Set Match | State Queries | Check_time | Actions | Duration |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.4 | single-baseline | live | 50 | 7 | 31 | 87.7% | 61.7% | 72.5% | 61.7% | 65.0% | 9 | 6 | 57 | 3m 22.9s |
| GPT-5.4 | single-todo-ledger | live | 50 | 5 | 31 | 90.9% | 61.7% | 73.5% | 61.7% | 67.5% | 15 | 11 | 55 | 6m 27.7s |
| GPT-5.4 | heartbeat-proactive | live | 55 | 3 | 26 | 94.8% | 67.9% | 79.1% | 67.9% | 70.0% | 11 | 8 | 58 | 3m 55.2s |
| GPT-5.4 | heartbeat-auto-60m | live | 45 | 15 | 36 | 75.0% | 55.6% | 63.8% | 55.6% | 53.8% | 23 | 15 | 60 | 3m 31.0s |
| GPT-5.4 | heartbeat-auto-30m | live | 53 | 9 | 28 | 85.5% | 65.4% | 74.1% | 65.4% | 66.2% | 36 | 19 | 62 | 5m 39.5s |
| GPT-5.4 | hier-union-query | live | 39 | 18 | 42 | 68.4% | 48.1% | 56.5% | 48.1% | 46.2% | 300 | 79 | 57 | 21m 33.6s |
| GPT-5.4 | hier-majority-vote | replay | 58 | 159 | 23 | 26.7% | 71.6% | 38.9% | 71.6% | 6.2% | 300 | 79 | 217 | 0.0s |
| GPT-5.4 | hier-unanimous-vote | replay | 47 | 63 | 34 | 42.7% | 58.0% | 49.2% | 58.0% | 28.7% | 300 | 79 | 110 | 0.0s |
| GPT-5.3-Codex | single-baseline | live | 60 | 11 | 21 | 84.5% | 74.1% | 78.9% | 74.1% | 67.5% | 55 | 34 | 71 | 8m 41.5s |
| GPT-5.3-Codex | single-todo-ledger | live | 55 | 11 | 26 | 83.3% | 67.9% | 74.8% | 67.9% | 67.5% | 42 | 33 | 66 | 12m 21.8s |
| GPT-5.3-Codex | heartbeat-proactive | live | 59 | 14 | 22 | 80.8% | 72.8% | 76.6% | 72.8% | 65.0% | 46 | 23 | 73 | 10m 16.7s |
| GPT-5.3-Codex | heartbeat-auto-60m | live | 55 | 11 | 26 | 83.3% | 67.9% | 74.8% | 67.9% | 65.0% | 47 | 31 | 66 | 9m 56.5s |
| GPT-5.3-Codex | heartbeat-auto-30m | live | 55 | 19 | 26 | 74.3% | 67.9% | 71.0% | 67.9% | 58.8% | 43 | 24 | 74 | 9m 31.9s |
| GPT-5.3-Codex | hier-union-query | live | 40 | 22 | 41 | 64.5% | 49.4% | 55.9% | 49.4% | 41.2% | 281 | 72 | 62 | 2h 9m 27.9s |
| GPT-5.3-Codex | hier-majority-vote | replay | 54 | 139 | 27 | 28.0% | 66.7% | 39.4% | 66.7% | 8.8% | 281 | 72 | 193 | 0.0s |
| GPT-5.3-Codex | hier-unanimous-vote | replay | 47 | 71 | 34 | 39.8% | 58.0% | 47.2% | 58.0% | 30.0% | 281 | 72 | 118 | 0.0s |
| Llama 3.3 70B Instruct | single-baseline | live | 48 | 20 | 33 | 70.6% | 59.3% | 64.4% | 59.3% | 52.5% | 0 | 0 | 68 | 1m 52.8s |
| Llama 3.3 70B Instruct | single-todo-ledger | live | 50 | 7 | 31 | 87.7% | 61.7% | 72.5% | 61.7% | 62.5% | 0 | 0 | 57 | 14m 58.5s |
| Llama 3.3 70B Instruct | heartbeat-proactive | live | 49 | 14 | 32 | 77.8% | 60.5% | 68.1% | 60.5% | 55.0% | 13 | 11 | 63 | 2m 24.1s |
| Llama 3.3 70B Instruct | heartbeat-auto-60m | live | 44 | 20 | 37 | 68.8% | 54.3% | 60.7% | 54.3% | 43.8% | 16 | 16 | 64 | 3m 41.2s |
| Llama 3.3 70B Instruct | heartbeat-auto-30m | live | 46 | 18 | 35 | 71.9% | 56.8% | 63.4% | 56.8% | 52.5% | 16 | 16 | 64 | 3m 4.0s |
| Llama 3.3 70B Instruct | hier-union-query | live | 42 | 42 | 39 | 50.0% | 51.9% | 50.9% | 51.9% | 38.8% | 140 | 76 | 84 | 1h 5m 12.1s |
| Llama 3.3 70B Instruct | hier-majority-vote | replay | 41 | 44 | 40 | 48.2% | 50.6% | 49.4% | 50.6% | 30.0% | 140 | 76 | 85 | 0.0s |
| Llama 3.3 70B Instruct | hier-unanimous-vote | replay | 39 | 28 | 42 | 58.2% | 48.1% | 52.7% | 48.1% | 41.2% | 140 | 76 | 67 | 0.0s |
| Mistral Large 2512 | single-baseline | live | 55 | 10 | 26 | 84.6% | 67.9% | 75.3% | 67.9% | 63.7% | 42 | 28 | 65 | 3m 24.9s |
| Mistral Large 2512 | single-todo-ledger | live | 48 | 15 | 33 | 76.2% | 59.3% | 66.7% | 59.3% | 53.8% | 24 | 21 | 63 | 6m 53.8s |
| Mistral Large 2512 | heartbeat-proactive | live | 56 | 15 | 25 | 78.9% | 69.1% | 73.7% | 69.1% | 62.5% | 51 | 30 | 71 | 3m 41.5s |
| Mistral Large 2512 | heartbeat-auto-60m | live | 52 | 17 | 29 | 75.4% | 64.2% | 69.3% | 64.2% | 58.8% | 53 | 29 | 69 | 3m 51.0s |
| Mistral Large 2512 | heartbeat-auto-30m | live | 56 | 13 | 25 | 81.2% | 69.1% | 74.7% | 69.1% | 62.5% | 75 | 40 | 69 | 4m 13.1s |
| Mistral Large 2512 | hier-union-query | live | 52 | 46 | 29 | 53.1% | 64.2% | 58.1% | 64.2% | 41.2% | 312 | 80 | 98 | 27m 0.3s |
| Mistral Large 2512 | hier-majority-vote | replay | 61 | 140 | 20 | 30.3% | 75.3% | 43.3% | 75.3% | 3.8% | 312 | 80 | 201 | 0.0s |
| Mistral Large 2512 | hier-unanimous-vote | replay | 52 | 62 | 29 | 45.6% | 64.2% | 53.3% | 64.2% | 28.7% | 312 | 80 | 114 | 0.0s |
| Mistral Small 3.2 24B Instruct | single-baseline | live | 36 | 20 | 45 | 64.3% | 44.4% | 52.6% | 44.4% | 43.8% | 0 | 0 | 56 | 1m 42.5s |
| Mistral Small 3.2 24B Instruct | single-todo-ledger | live | 46 | 18 | 35 | 71.9% | 56.8% | 63.4% | 56.8% | 50.0% | 10 | 10 | 64 | 4m 20.1s |
| Mistral Small 3.2 24B Instruct | heartbeat-proactive | live | 35 | 16 | 46 | 68.6% | 43.2% | 53.0% | 43.2% | 42.5% | 0 | 0 | 51 | 1m 18.9s |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-60m | live | 34 | 14 | 47 | 70.8% | 42.0% | 52.7% | 42.0% | 48.8% | 0 | 0 | 48 | 1m 24.0s |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-30m | live | 32 | 11 | 49 | 74.4% | 39.5% | 51.6% | 39.5% | 53.8% | 7 | 7 | 43 | 1m 23.9s |
| Mistral Small 3.2 24B Instruct | hier-union-query | live | 19 | 13 | 62 | 59.4% | 23.5% | 33.6% | 23.5% | 35.0% | 237 | 80 | 32 | 21m 9.9s |
| Mistral Small 3.2 24B Instruct | hier-majority-vote | replay | 20 | 44 | 61 | 31.2% | 24.7% | 27.6% | 24.7% | 21.2% | 237 | 80 | 64 | 0.0s |
| Mistral Small 3.2 24B Instruct | hier-unanimous-vote | replay | 8 | 4 | 73 | 66.7% | 9.9% | 17.2% | 9.9% | 41.2% | 237 | 80 | 12 | 0.0s |
| Qwen3-32B | single-baseline | live | 36 | 23 | 45 | 61.0% | 44.4% | 51.4% | 44.4% | 36.2% | 0 | 0 | 59 | 38.7s |
| Qwen3-32B | single-todo-ledger | live | 37 | 25 | 44 | 59.7% | 45.7% | 51.7% | 45.7% | 36.2% | 8 | 8 | 62 | 4m 13.9s |
| Qwen3-32B | heartbeat-proactive | live | 40 | 44 | 41 | 47.6% | 49.4% | 48.5% | 49.4% | 25.0% | 0 | 0 | 84 | 57.2s |
| Qwen3-32B | heartbeat-auto-60m | live | 40 | 24 | 41 | 62.5% | 49.4% | 55.2% | 49.4% | 38.8% | 33 | 17 | 64 | 57.6s |
| Qwen3-32B | heartbeat-auto-30m | live | 44 | 28 | 37 | 61.1% | 54.3% | 57.5% | 54.3% | 41.2% | 26 | 13 | 72 | 56.9s |
| Qwen3-32B | hier-union-query | live | 27 | 36 | 54 | 42.9% | 33.3% | 37.5% | 33.3% | 36.2% | 169 | 80 | 63 | 3m 50.6s |
| Qwen3-32B | hier-majority-vote | replay | 20 | 21 | 61 | 48.8% | 24.7% | 32.8% | 24.7% | 32.5% | 169 | 80 | 41 | 0.0s |
| Qwen3-32B | hier-unanimous-vote | replay | 8 | 9 | 73 | 47.1% | 9.9% | 16.3% | 9.9% | 32.5% | 169 | 80 | 17 | 0.0s |
| Qwen3-14B | single-baseline | live | 39 | 61 | 42 | 39.0% | 48.1% | 43.1% | 48.1% | 16.2% | 0 | 0 | 100 | 32.5s |
| Qwen3-14B | single-todo-ledger | live | 40 | 32 | 41 | 55.6% | 49.4% | 52.3% | 49.4% | 36.2% | 11 | 11 | 72 | 2m 50.9s |
| Qwen3-14B | heartbeat-proactive | live | 40 | 39 | 41 | 50.6% | 49.4% | 50.0% | 49.4% | 27.5% | 9 | 9 | 79 | 1m 7.5s |
| Qwen3-14B | heartbeat-auto-60m | live | 70 | 261 | 11 | 21.1% | 86.4% | 34.0% | 86.4% | 2.5% | 0 | 0 | 331 | 49.5s |
| Qwen3-14B | heartbeat-auto-30m | live | 75 | 339 | 6 | 18.1% | 92.6% | 30.3% | 92.6% | 0.0% | 0 | 0 | 414 | 55.0s |
| Qwen3-14B | hier-union-query | live | 36 | 48 | 45 | 42.9% | 44.4% | 43.6% | 44.4% | 28.7% | 87 | 76 | 84 | 3m 8.2s |
| Qwen3-14B | hier-majority-vote | replay | 36 | 58 | 45 | 38.3% | 44.4% | 41.1% | 44.4% | 26.2% | 87 | 76 | 94 | 0.0s |
| Qwen3-14B | hier-unanimous-vote | replay | 20 | 28 | 61 | 41.7% | 24.7% | 31.0% | 24.7% | 35.0% | 87 | 76 | 48 | 0.0s |
| Qwen3-8B | single-baseline | live | 34 | 47 | 47 | 42.0% | 42.0% | 42.0% | 42.0% | 18.8% | 0 | 0 | 81 | 23.6s |
| Qwen3-8B | single-todo-ledger | live | 32 | 21 | 49 | 60.4% | 39.5% | 47.8% | 39.5% | 41.2% | 8 | 8 | 53 | 2m 9.9s |
| Qwen3-8B | heartbeat-proactive | live | 64 | 33 | 17 | 66.0% | 79.0% | 71.9% | 79.0% | 62.5% | 0 | 0 | 97 | 7m 11.7s |
| Qwen3-8B | heartbeat-auto-60m | live | 38 | 60 | 43 | 38.8% | 46.9% | 42.5% | 46.9% | 15.0% | 0 | 0 | 98 | 24.7s |
| Qwen3-8B | heartbeat-auto-30m | live | 33 | 52 | 48 | 38.8% | 40.7% | 39.8% | 40.7% | 15.0% | 0 | 0 | 85 | 24.0s |
| Qwen3-8B | hier-union-query | live | 19 | 48 | 62 | 28.4% | 23.5% | 25.7% | 23.5% | 22.5% | 135 | 69 | 67 | 1m 47.2s |
| Qwen3-8B | hier-majority-vote | replay | 19 | 50 | 62 | 27.5% | 23.5% | 25.3% | 23.5% | 16.2% | 135 | 69 | 69 | 0.0s |
| Qwen3-8B | hier-unanimous-vote | replay | 8 | 14 | 73 | 36.4% | 9.9% | 15.5% | 9.9% | 30.0% | 135 | 69 | 22 | 0.0s |

## Per-Run Error / Control Metrics

| Model | Setup | Run Type | False Alarms | Commission | Wrong-Content | Dependency Violations | Overkill Steps | Late Rate | Miss Rate | False Alarm/Step | Overkill/Step |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.4 | single-baseline | live | 5 | 0 | 3 | 0 | 4 | 2.5% | 35.8% | 6.2% | 5.0% |
| GPT-5.4 | single-todo-ledger | live | 3 | 0 | 4 | 0 | 2 | 2.5% | 35.8% | 3.8% | 2.5% |
| GPT-5.4 | heartbeat-proactive | live | 2 | 0 | 1 | 0 | 2 | 1.2% | 30.9% | 2.5% | 2.5% |
| GPT-5.4 | heartbeat-auto-60m | live | 10 | 0 | 7 | 0 | 11 | 6.2% | 38.3% | 12.5% | 13.8% |
| GPT-5.4 | heartbeat-auto-30m | live | 5 | 0 | 3 | 0 | 5 | 4.9% | 29.6% | 6.2% | 6.2% |
| GPT-5.4 | hier-union-query | live | 16 | 0 | 5 | 0 | 15 | 2.5% | 49.4% | 20.0% | 18.8% |
| GPT-5.4 | hier-majority-vote | replay | 118 | 35 | 87 | 0 | 64 | 7.4% | 21.0% | 147.5% | 80.0% |
| GPT-5.4 | hier-unanimous-vote | replay | 49 | 11 | 29 | 0 | 36 | 3.7% | 38.3% | 61.3% | 45.0% |
| GPT-5.3-Codex | single-baseline | live | 8 | 0 | 3 | 0 | 7 | 3.7% | 22.2% | 10.0% | 8.8% |
| GPT-5.3-Codex | single-todo-ledger | live | 7 | 0 | 6 | 0 | 7 | 4.9% | 27.2% | 8.8% | 8.8% |
| GPT-5.3-Codex | heartbeat-proactive | live | 9 | 0 | 3 | 0 | 8 | 6.2% | 21.0% | 11.2% | 10.0% |
| GPT-5.3-Codex | heartbeat-auto-60m | live | 8 | 0 | 4 | 0 | 8 | 3.7% | 28.4% | 10.0% | 10.0% |
| GPT-5.3-Codex | heartbeat-auto-30m | live | 11 | 0 | 8 | 0 | 14 | 9.9% | 22.2% | 13.8% | 17.5% |
| GPT-5.3-Codex | hier-union-query | live | 21 | 0 | 7 | 0 | 19 | 1.2% | 49.4% | 26.2% | 23.8% |
| GPT-5.3-Codex | hier-majority-vote | replay | 107 | 26 | 70 | 0 | 61 | 7.4% | 25.9% | 133.8% | 76.2% |
| GPT-5.3-Codex | hier-unanimous-vote | replay | 60 | 8 | 32 | 0 | 36 | 3.7% | 38.3% | 75.0% | 45.0% |
| Llama 3.3 70B Instruct | single-baseline | live | 19 | 0 | 7 | 0 | 12 | 1.2% | 39.5% | 23.8% | 15.0% |
| Llama 3.3 70B Instruct | single-todo-ledger | live | 7 | 0 | 1 | 0 | 5 | 0.0% | 38.3% | 8.8% | 6.2% |
| Llama 3.3 70B Instruct | heartbeat-proactive | live | 12 | 0 | 5 | 0 | 10 | 2.5% | 37.0% | 15.0% | 12.5% |
| Llama 3.3 70B Instruct | heartbeat-auto-60m | live | 20 | 0 | 3 | 0 | 17 | 0.0% | 45.7% | 25.0% | 21.2% |
| Llama 3.3 70B Instruct | heartbeat-auto-30m | live | 18 | 0 | 4 | 0 | 12 | 0.0% | 43.2% | 22.5% | 15.0% |
| Llama 3.3 70B Instruct | hier-union-query | live | 38 | 0 | 16 | 0 | 24 | 4.9% | 43.2% | 47.5% | 30.0% |
| Llama 3.3 70B Instruct | hier-majority-vote | replay | 41 | 0 | 17 | 0 | 29 | 3.7% | 45.7% | 51.2% | 36.2% |
| Llama 3.3 70B Instruct | hier-unanimous-vote | replay | 25 | 0 | 10 | 0 | 19 | 3.7% | 48.1% | 31.2% | 23.8% |
| Mistral Large 2512 | single-baseline | live | 6 | 0 | 3 | 0 | 8 | 4.9% | 27.2% | 7.5% | 10.0% |
| Mistral Large 2512 | single-todo-ledger | live | 11 | 0 | 6 | 0 | 12 | 4.9% | 35.8% | 13.8% | 15.0% |
| Mistral Large 2512 | heartbeat-proactive | live | 10 | 0 | 4 | 0 | 10 | 6.2% | 24.7% | 12.5% | 12.5% |
| Mistral Large 2512 | heartbeat-auto-60m | live | 10 | 0 | 8 | 0 | 12 | 8.6% | 27.2% | 12.5% | 15.0% |
| Mistral Large 2512 | heartbeat-auto-30m | live | 9 | 0 | 4 | 0 | 10 | 4.9% | 25.9% | 11.2% | 12.5% |
| Mistral Large 2512 | hier-union-query | live | 39 | 0 | 18 | 0 | 29 | 8.6% | 27.2% | 48.8% | 36.2% |
| Mistral Large 2512 | hier-majority-vote | replay | 115 | 20 | 76 | 0 | 69 | 6.2% | 18.5% | 143.8% | 86.2% |
| Mistral Large 2512 | hier-unanimous-vote | replay | 50 | 6 | 29 | 0 | 40 | 7.4% | 28.4% | 62.5% | 50.0% |
| Mistral Small 3.2 24B Instruct | single-baseline | live | 17 | 0 | 5 | 0 | 13 | 3.7% | 51.9% | 21.2% | 16.2% |
| Mistral Small 3.2 24B Instruct | single-todo-ledger | live | 16 | 0 | 11 | 0 | 12 | 2.5% | 40.7% | 20.0% | 15.0% |
| Mistral Small 3.2 24B Instruct | heartbeat-proactive | live | 14 | 0 | 3 | 0 | 13 | 2.5% | 54.3% | 17.5% | 16.2% |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-60m | live | 12 | 0 | 6 | 0 | 8 | 2.5% | 55.6% | 15.0% | 10.0% |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-30m | live | 9 | 0 | 6 | 0 | 6 | 2.5% | 58.0% | 11.2% | 7.5% |
| Mistral Small 3.2 24B Instruct | hier-union-query | live | 11 | 0 | 5 | 0 | 9 | 2.5% | 74.1% | 13.8% | 11.2% |
| Mistral Small 3.2 24B Instruct | hier-majority-vote | replay | 31 | 12 | 22 | 0 | 24 | 1.2% | 74.1% | 38.8% | 30.0% |
| Mistral Small 3.2 24B Instruct | hier-unanimous-vote | replay | 3 | 1 | 2 | 0 | 2 | 0.0% | 90.1% | 3.8% | 2.5% |
| Qwen3-32B | single-baseline | live | 21 | 0 | 7 | 0 | 16 | 2.5% | 53.1% | 26.2% | 20.0% |
| Qwen3-32B | single-todo-ledger | live | 19 | 0 | 6 | 0 | 19 | 7.4% | 46.9% | 23.8% | 23.8% |
| Qwen3-32B | heartbeat-proactive | live | 41 | 0 | 13 | 0 | 30 | 3.7% | 46.9% | 51.2% | 37.5% |
| Qwen3-32B | heartbeat-auto-60m | live | 21 | 0 | 6 | 0 | 18 | 3.7% | 46.9% | 26.2% | 22.5% |
| Qwen3-32B | heartbeat-auto-30m | live | 27 | 0 | 7 | 0 | 20 | 1.2% | 44.4% | 33.8% | 25.0% |
| Qwen3-32B | hier-union-query | live | 31 | 0 | 18 | 0 | 15 | 6.2% | 60.5% | 38.8% | 18.8% |
| Qwen3-32B | hier-majority-vote | replay | 20 | 1 | 9 | 0 | 15 | 0.0% | 75.3% | 25.0% | 18.8% |
| Qwen3-32B | hier-unanimous-vote | replay | 8 | 1 | 3 | 0 | 6 | 0.0% | 90.1% | 10.0% | 7.5% |
| Qwen3-14B | single-baseline | live | 58 | 0 | 29 | 0 | 36 | 3.7% | 48.1% | 72.5% | 45.0% |
| Qwen3-14B | single-todo-ledger | live | 27 | 0 | 12 | 0 | 21 | 6.2% | 44.4% | 33.8% | 26.2% |
| Qwen3-14B | heartbeat-proactive | live | 35 | 0 | 11 | 0 | 28 | 4.9% | 45.7% | 43.8% | 35.0% |
| Qwen3-14B | heartbeat-auto-60m | live | 259 | 0 | 140 | 0 | 76 | 2.5% | 11.1% | 323.8% | 95.0% |
| Qwen3-14B | heartbeat-auto-30m | live | 336 | 0 | 187 | 0 | 80 | 3.7% | 3.7% | 420.0% | 100.0% |
| Qwen3-14B | hier-union-query | live | 44 | 0 | 21 | 0 | 28 | 4.9% | 50.6% | 55.0% | 35.0% |
| Qwen3-14B | hier-majority-vote | replay | 48 | 9 | 29 | 0 | 31 | 1.2% | 54.3% | 60.0% | 38.8% |
| Qwen3-14B | hier-unanimous-vote | replay | 25 | 2 | 12 | 0 | 15 | 1.2% | 74.1% | 31.2% | 18.8% |
| Qwen3-8B | single-baseline | live | 43 | 0 | 18 | 0 | 30 | 4.9% | 53.1% | 53.8% | 37.5% |
| Qwen3-8B | single-todo-ledger | live | 15 | 0 | 7 | 0 | 14 | 7.4% | 53.1% | 18.8% | 17.5% |
| Qwen3-8B | heartbeat-proactive | live | 33 | 0 | 9 | 0 | 16 | 0.0% | 21.0% | 41.2% | 20.0% |
| Qwen3-8B | heartbeat-auto-60m | live | 58 | 0 | 27 | 0 | 38 | 2.5% | 50.6% | 72.5% | 47.5% |
| Qwen3-8B | heartbeat-auto-30m | live | 48 | 0 | 23 | 0 | 32 | 4.9% | 54.3% | 60.0% | 40.0% |
| Qwen3-8B | hier-union-query | live | 46 | 0 | 20 | 0 | 22 | 2.5% | 74.1% | 57.5% | 27.5% |
| Qwen3-8B | hier-majority-vote | replay | 43 | 6 | 25 | 0 | 24 | 1.2% | 75.3% | 53.8% | 30.0% |
| Qwen3-8B | hier-unanimous-vote | replay | 14 | 0 | 6 | 0 | 8 | 0.0% | 90.1% | 17.5% | 10.0% |

## Per-Run Proactive Monitoring

| Model | Setup | Run Type | Proactive Hit | Proactive Any | No-Proactive Hit | Clock Hit | Clock Any | Non-Clock Hit | Non-Clock Any | State Queries | Clock Queries | Non-Clock Queries |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.4 | single-baseline | live | 30.8% | 35.9% | 90.5% | 50.0% | 54.2% | 0.0% | 6.7% | 9 | 6 | 3 |
| GPT-5.4 | single-todo-ledger | live | 30.8% | 35.9% | 90.5% | 50.0% | 54.2% | 0.0% | 6.7% | 15 | 11 | 4 |
| GPT-5.4 | heartbeat-proactive | live | 35.9% | 38.5% | 97.6% | 58.3% | 58.3% | 0.0% | 6.7% | 11 | 8 | 3 |
| GPT-5.4 | heartbeat-auto-60m | live | 25.6% | 38.5% | 83.3% | 41.7% | 58.3% | 0.0% | 6.7% | 23 | 15 | 8 |
| GPT-5.4 | heartbeat-auto-30m | live | 46.2% | 56.4% | 83.3% | 70.8% | 70.8% | 6.7% | 33.3% | 36 | 19 | 17 |
| GPT-5.4 | hier-union-query | live | 43.6% | 46.2% | 52.4% | 62.5% | 66.7% | 13.3% | 13.3% | 300 | 79 | 221 |
| GPT-5.4 | hier-majority-vote | replay | 66.7% | 76.9% | 76.2% | 79.2% | 87.5% | 46.7% | 60.0% | 300 | 79 | 221 |
| GPT-5.4 | hier-unanimous-vote | replay | 46.2% | 53.8% | 69.0% | 75.0% | 79.2% | 0.0% | 13.3% | 300 | 79 | 221 |
| GPT-5.3-Codex | single-baseline | live | 53.8% | 61.5% | 92.9% | 83.3% | 83.3% | 6.7% | 26.7% | 55 | 34 | 21 |
| GPT-5.3-Codex | single-todo-ledger | live | 46.2% | 56.4% | 88.1% | 70.8% | 83.3% | 6.7% | 13.3% | 42 | 33 | 9 |
| GPT-5.3-Codex | heartbeat-proactive | live | 51.3% | 64.1% | 92.9% | 79.2% | 83.3% | 6.7% | 33.3% | 46 | 23 | 23 |
| GPT-5.3-Codex | heartbeat-auto-60m | live | 48.7% | 56.4% | 85.7% | 79.2% | 79.2% | 0.0% | 20.0% | 47 | 31 | 16 |
| GPT-5.3-Codex | heartbeat-auto-30m | live | 43.6% | 64.1% | 90.5% | 66.7% | 79.2% | 6.7% | 40.0% | 43 | 24 | 19 |
| GPT-5.3-Codex | hier-union-query | live | 43.6% | 43.6% | 54.8% | 62.5% | 62.5% | 13.3% | 13.3% | 281 | 72 | 209 |
| GPT-5.3-Codex | hier-majority-vote | replay | 59.0% | 71.8% | 73.8% | 75.0% | 79.2% | 33.3% | 60.0% | 281 | 72 | 209 |
| GPT-5.3-Codex | hier-unanimous-vote | replay | 43.6% | 51.3% | 71.4% | 62.5% | 66.7% | 13.3% | 26.7% | 281 | 72 | 209 |
| Llama 3.3 70B Instruct | single-baseline | live | 30.8% | 33.3% | 85.7% | 50.0% | 54.2% | 0.0% | 0.0% | 0 | 0 | 0 |
| Llama 3.3 70B Instruct | single-todo-ledger | live | 25.6% | 25.6% | 95.2% | 41.7% | 41.7% | 0.0% | 0.0% | 0 | 0 | 0 |
| Llama 3.3 70B Instruct | heartbeat-proactive | live | 35.9% | 41.0% | 83.3% | 58.3% | 66.7% | 0.0% | 0.0% | 13 | 11 | 2 |
| Llama 3.3 70B Instruct | heartbeat-auto-60m | live | 33.3% | 33.3% | 73.8% | 54.2% | 54.2% | 0.0% | 0.0% | 16 | 16 | 0 |
| Llama 3.3 70B Instruct | heartbeat-auto-30m | live | 35.9% | 35.9% | 76.2% | 58.3% | 58.3% | 0.0% | 0.0% | 16 | 16 | 0 |
| Llama 3.3 70B Instruct | hier-union-query | live | 43.6% | 48.7% | 59.5% | 70.8% | 79.2% | 0.0% | 0.0% | 140 | 76 | 64 |
| Llama 3.3 70B Instruct | hier-majority-vote | replay | 46.2% | 51.3% | 54.8% | 70.8% | 79.2% | 6.7% | 6.7% | 140 | 76 | 64 |
| Llama 3.3 70B Instruct | hier-unanimous-vote | replay | 41.0% | 46.2% | 54.8% | 66.7% | 75.0% | 0.0% | 0.0% | 140 | 76 | 64 |
| Mistral Large 2512 | single-baseline | live | 43.6% | 51.3% | 90.5% | 70.8% | 75.0% | 0.0% | 13.3% | 42 | 28 | 14 |
| Mistral Large 2512 | single-todo-ledger | live | 25.6% | 33.3% | 90.5% | 41.7% | 50.0% | 0.0% | 6.7% | 24 | 21 | 3 |
| Mistral Large 2512 | heartbeat-proactive | live | 46.2% | 59.0% | 90.5% | 70.8% | 75.0% | 6.7% | 33.3% | 51 | 30 | 21 |
| Mistral Large 2512 | heartbeat-auto-60m | live | 46.2% | 59.0% | 81.0% | 75.0% | 79.2% | 0.0% | 26.7% | 53 | 29 | 24 |
| Mistral Large 2512 | heartbeat-auto-30m | live | 48.7% | 59.0% | 88.1% | 66.7% | 66.7% | 20.0% | 46.7% | 75 | 40 | 35 |
| Mistral Large 2512 | hier-union-query | live | 53.8% | 64.1% | 73.8% | 79.2% | 87.5% | 13.3% | 26.7% | 312 | 80 | 232 |
| Mistral Large 2512 | hier-majority-vote | replay | 71.8% | 74.4% | 78.6% | 91.7% | 91.7% | 40.0% | 46.7% | 312 | 80 | 232 |
| Mistral Large 2512 | hier-unanimous-vote | replay | 53.8% | 61.5% | 73.8% | 79.2% | 83.3% | 13.3% | 26.7% | 312 | 80 | 232 |
| Mistral Small 3.2 24B Instruct | single-baseline | live | 23.1% | 25.6% | 64.3% | 33.3% | 37.5% | 6.7% | 6.7% | 0 | 0 | 0 |
| Mistral Small 3.2 24B Instruct | single-todo-ledger | live | 30.8% | 33.3% | 81.0% | 50.0% | 50.0% | 0.0% | 6.7% | 10 | 10 | 0 |
| Mistral Small 3.2 24B Instruct | heartbeat-proactive | live | 20.5% | 20.5% | 64.3% | 33.3% | 33.3% | 0.0% | 0.0% | 0 | 0 | 0 |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-60m | live | 17.9% | 23.1% | 64.3% | 29.2% | 37.5% | 0.0% | 0.0% | 0 | 0 | 0 |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-30m | live | 23.1% | 25.6% | 54.8% | 37.5% | 41.7% | 0.0% | 0.0% | 7 | 7 | 0 |
| Mistral Small 3.2 24B Instruct | hier-union-query | live | 17.9% | 20.5% | 28.6% | 29.2% | 33.3% | 0.0% | 0.0% | 237 | 80 | 157 |
| Mistral Small 3.2 24B Instruct | hier-majority-vote | replay | 20.5% | 23.1% | 28.6% | 29.2% | 33.3% | 6.7% | 6.7% | 237 | 80 | 157 |
| Mistral Small 3.2 24B Instruct | hier-unanimous-vote | replay | 5.1% | 5.1% | 14.3% | 8.3% | 8.3% | 0.0% | 0.0% | 237 | 80 | 157 |
| Qwen3-32B | single-baseline | live | 10.3% | 15.4% | 76.2% | 16.7% | 20.8% | 0.0% | 6.7% | 0 | 0 | 0 |
| Qwen3-32B | single-todo-ledger | live | 17.9% | 28.2% | 71.4% | 29.2% | 41.7% | 0.0% | 6.7% | 8 | 8 | 0 |
| Qwen3-32B | heartbeat-proactive | live | 20.5% | 28.2% | 76.2% | 33.3% | 41.7% | 0.0% | 6.7% | 0 | 0 | 0 |
| Qwen3-32B | heartbeat-auto-60m | live | 23.1% | 28.2% | 73.8% | 37.5% | 37.5% | 0.0% | 13.3% | 33 | 17 | 16 |
| Qwen3-32B | heartbeat-auto-30m | live | 30.8% | 33.3% | 76.2% | 50.0% | 54.2% | 0.0% | 0.0% | 26 | 13 | 13 |
| Qwen3-32B | hier-union-query | live | 43.6% | 48.7% | 23.8% | 70.8% | 79.2% | 0.0% | 0.0% | 169 | 80 | 89 |
| Qwen3-32B | hier-majority-vote | replay | 41.0% | 41.0% | 9.5% | 66.7% | 66.7% | 0.0% | 0.0% | 169 | 80 | 89 |
| Qwen3-32B | hier-unanimous-vote | replay | 17.9% | 17.9% | 2.4% | 29.2% | 29.2% | 0.0% | 0.0% | 169 | 80 | 89 |
| Qwen3-14B | single-baseline | live | 17.9% | 23.1% | 76.2% | 29.2% | 29.2% | 0.0% | 13.3% | 0 | 0 | 0 |
| Qwen3-14B | single-todo-ledger | live | 28.2% | 38.5% | 69.0% | 45.8% | 58.3% | 0.0% | 6.7% | 11 | 11 | 0 |
| Qwen3-14B | heartbeat-proactive | live | 23.1% | 30.8% | 73.8% | 37.5% | 45.8% | 0.0% | 6.7% | 9 | 9 | 0 |
| Qwen3-14B | heartbeat-auto-60m | live | 82.1% | 84.6% | 90.5% | 87.5% | 87.5% | 73.3% | 80.0% | 0 | 0 | 0 |
| Qwen3-14B | heartbeat-auto-30m | live | 92.3% | 97.4% | 92.9% | 100.0% | 100.0% | 80.0% | 93.3% | 0 | 0 | 0 |
| Qwen3-14B | hier-union-query | live | 43.6% | 48.7% | 45.2% | 70.8% | 79.2% | 0.0% | 0.0% | 87 | 76 | 11 |
| Qwen3-14B | hier-majority-vote | replay | 51.3% | 53.8% | 38.1% | 83.3% | 87.5% | 0.0% | 0.0% | 87 | 76 | 11 |
| Qwen3-14B | hier-unanimous-vote | replay | 33.3% | 35.9% | 16.7% | 54.2% | 58.3% | 0.0% | 0.0% | 87 | 76 | 11 |
| Qwen3-8B | single-baseline | live | 28.2% | 33.3% | 54.8% | 37.5% | 45.8% | 13.3% | 13.3% | 0 | 0 | 0 |
| Qwen3-8B | single-todo-ledger | live | 23.1% | 33.3% | 54.8% | 33.3% | 50.0% | 6.7% | 6.7% | 8 | 8 | 0 |
| Qwen3-8B | heartbeat-proactive | live | 66.7% | 66.7% | 90.5% | 66.7% | 66.7% | 66.7% | 66.7% | 0 | 0 | 0 |
| Qwen3-8B | heartbeat-auto-60m | live | 28.2% | 30.8% | 64.3% | 37.5% | 41.7% | 13.3% | 13.3% | 0 | 0 | 0 |
| Qwen3-8B | heartbeat-auto-30m | live | 25.6% | 30.8% | 54.8% | 33.3% | 41.7% | 13.3% | 13.3% | 0 | 0 | 0 |
| Qwen3-8B | hier-union-query | live | 23.1% | 25.6% | 23.8% | 37.5% | 41.7% | 0.0% | 0.0% | 135 | 69 | 66 |
| Qwen3-8B | hier-majority-vote | replay | 28.2% | 30.8% | 19.0% | 45.8% | 50.0% | 0.0% | 0.0% | 135 | 69 | 66 |
| Qwen3-8B | hier-unanimous-vote | replay | 12.8% | 12.8% | 7.1% | 20.8% | 20.8% | 0.0% | 0.0% | 135 | 69 | 66 |

## Per-Run Proactive Required by Channel

| Model | Setup | Run Type | appointment_portal | bank_balance | calendar | clock | course_portal | email | library_hold | shipment_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.4 | single-baseline | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 12/1/11/24 (50.0%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 12/1/11/24 (50.0%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | heartbeat-proactive | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 14/0/10/24 (58.3%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 10/4/10/24 (41.7%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | heartbeat-auto-30m | live | 0/1/2/3 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 17/0/7/24 (70.8%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | hier-union-query | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 15/1/8/24 (62.5%) | 1/0/0/1 (100.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | hier-majority-vote | replay | 2/0/1/3 (66.7%) | 1/0/1/2 (50.0%) | 1/1/1/3 (33.3%) | 19/2/3/24 (79.2%) | 1/0/0/1 (100.0%) | 0/1/1/2 (0.0%) | 2/0/1/3 (66.7%) | 0/0/1/1 (0.0%) |
| GPT-5.4 | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/1/2/3 (0.0%) | 18/1/5/24 (75.0%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | single-baseline | live | 0/1/2/3 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 20/0/4/24 (83.3%) | 0/0/1/1 (0.0%) | 0/2/0/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 17/3/4/24 (70.8%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | heartbeat-proactive | live | 0/1/2/3 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 19/1/4/24 (79.2%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 19/0/5/24 (79.2%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | heartbeat-auto-30m | live | 0/1/2/3 (0.0%) | 0/0/2/2 (0.0%) | 0/1/2/3 (0.0%) | 16/3/5/24 (66.7%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | hier-union-query | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 15/0/9/24 (62.5%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | hier-majority-vote | replay | 2/0/1/3 (66.7%) | 1/0/1/2 (50.0%) | 0/2/1/3 (0.0%) | 18/1/5/24 (75.0%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 2/1/0/3 (66.7%) | 0/0/1/1 (0.0%) |
| GPT-5.3-Codex | hier-unanimous-vote | replay | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/2/1/3 (0.0%) | 15/1/8/24 (62.5%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | single-baseline | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 12/1/11/24 (50.0%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 10/0/14/24 (41.7%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | heartbeat-proactive | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 14/2/8/24 (58.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 13/0/11/24 (54.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | heartbeat-auto-30m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 14/0/10/24 (58.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | hier-union-query | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/2/5/24 (70.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | hier-majority-vote | replay | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/2/5/24 (70.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Llama 3.3 70B Instruct | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 16/2/6/24 (66.7%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | single-baseline | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/1/6/24 (70.8%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/1/2/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 10/2/12/24 (41.7%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | heartbeat-proactive | live | 0/1/2/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/1/6/24 (70.8%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/1/2/3 (0.0%) | 18/1/5/24 (75.0%) | 0/0/1/1 (0.0%) | 0/2/0/2 (0.0%) | 0/1/2/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | heartbeat-auto-30m | live | 1/1/1/3 (33.3%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 16/0/8/24 (66.7%) | 0/1/0/1 (0.0%) | 0/2/0/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | hier-union-query | live | 1/0/2/3 (33.3%) | 1/0/1/2 (50.0%) | 0/1/2/3 (0.0%) | 19/2/3/24 (79.2%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | hier-majority-vote | replay | 1/0/2/3 (33.3%) | 1/0/1/2 (50.0%) | 1/0/2/3 (33.3%) | 22/0/2/24 (91.7%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 3/0/0/3 (100.0%) | 0/0/1/1 (0.0%) |
| Mistral Large 2512 | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 1/0/1/2 (50.0%) | 1/0/2/3 (33.3%) | 19/1/4/24 (79.2%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/1/2/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | single-baseline | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 8/1/15/24 (33.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 12/0/12/24 (50.0%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | heartbeat-proactive | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 8/0/16/24 (33.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/2/15/24 (29.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-30m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/1/14/24 (37.5%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | hier-union-query | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/1/16/24 (29.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | hier-majority-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/1/16/24 (29.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 1/0/2/3 (33.3%) | 0/0/1/1 (0.0%) |
| Mistral Small 3.2 24B Instruct | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 2/0/22/24 (8.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | single-baseline | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 4/1/19/24 (16.7%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/3/14/24 (29.2%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | heartbeat-proactive | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 8/2/14/24 (33.3%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | heartbeat-auto-60m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/0/15/24 (37.5%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/1/2/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | heartbeat-auto-30m | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 12/1/11/24 (50.0%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | hier-union-query | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/2/5/24 (70.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | hier-majority-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 16/0/8/24 (66.7%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-32B | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/0/17/24 (29.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | single-baseline | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 7/0/17/24 (29.2%) | 0/0/1/1 (0.0%) | 0/2/0/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | single-todo-ledger | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/1/2/3 (0.0%) | 11/3/10/24 (45.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | heartbeat-proactive | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/2/13/24 (37.5%) | 0/0/1/1 (0.0%) | 0/1/1/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | heartbeat-auto-60m | live | 2/0/1/3 (66.7%) | 2/0/0/2 (100.0%) | 3/0/0/3 (100.0%) | 21/0/3/24 (87.5%) | 1/0/0/1 (100.0%) | 1/0/1/2 (50.0%) | 2/0/1/3 (66.7%) | 0/1/0/1 (0.0%) |
| Qwen3-14B | heartbeat-auto-30m | live | 2/1/0/3 (66.7%) | 2/0/0/2 (100.0%) | 3/0/0/3 (100.0%) | 24/0/0/24 (100.0%) | 0/0/1/1 (0.0%) | 1/1/0/2 (50.0%) | 3/0/0/3 (100.0%) | 1/0/0/1 (100.0%) |
| Qwen3-14B | hier-union-query | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 17/2/5/24 (70.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | hier-majority-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 20/1/3/24 (83.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-14B | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 13/1/10/24 (54.2%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | single-baseline | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/2/13/24 (37.5%) | 1/0/0/1 (100.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | single-todo-ledger | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 8/4/12/24 (33.3%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | heartbeat-proactive | live | 2/0/1/3 (66.7%) | 1/0/1/2 (50.0%) | 2/0/1/3 (66.7%) | 16/0/8/24 (66.7%) | 1/0/0/1 (100.0%) | 1/0/1/2 (50.0%) | 2/0/1/3 (66.7%) | 1/0/0/1 (100.0%) |
| Qwen3-8B | heartbeat-auto-60m | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/1/14/24 (37.5%) | 1/0/0/1 (100.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | heartbeat-auto-30m | live | 1/0/2/3 (33.3%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 8/2/14/24 (33.3%) | 1/0/0/1 (100.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | hier-union-query | live | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 9/1/14/24 (37.5%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | hier-majority-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 11/1/12/24 (45.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |
| Qwen3-8B | hier-unanimous-vote | replay | 0/0/3/3 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 5/0/19/24 (20.8%) | 0/0/1/1 (0.0%) | 0/0/2/2 (0.0%) | 0/0/3/3 (0.0%) | 0/0/1/1 (0.0%) |

## Cross-Day and Update Metrics

| Model | Setup | Run Type | Cross-day Hit/Late/Miss/Total | Update Hit/Late/Miss/Canceled/Total | Update Violations | Cross-day Hit | Cross-day Any | Update Hit | Update Any |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| GPT-5.4 | single-baseline | live | 6/0/1/7 | 5/1/3/2/11 | 2 | 85.7% | 85.7% | 55.6% | 66.7% |
| GPT-5.4 | single-todo-ledger | live | 3/0/4/7 | 6/1/2/2/11 | 1 | 42.9% | 42.9% | 66.7% | 77.8% |
| GPT-5.4 | heartbeat-proactive | live | 7/0/0/7 | 6/0/3/2/11 | 1 | 100.0% | 100.0% | 66.7% | 66.7% |
| GPT-5.4 | heartbeat-auto-60m | live | 3/0/4/7 | 4/1/4/2/11 | 2 | 42.9% | 42.9% | 44.4% | 55.6% |
| GPT-5.4 | heartbeat-auto-30m | live | 2/0/5/7 | 8/0/1/2/11 | 1 | 28.6% | 28.6% | 88.9% | 88.9% |
| GPT-5.4 | hier-union-query | live | 0/1/6/7 | 1/0/8/2/11 | 3 | 0.0% | 14.3% | 11.1% | 11.1% |
| GPT-5.4 | hier-majority-vote | replay | 3/2/2/7 | 4/1/4/2/11 | 16 | 42.9% | 71.4% | 44.4% | 55.6% |
| GPT-5.4 | hier-unanimous-vote | replay | 3/0/4/7 | 3/1/5/2/11 | 10 | 42.9% | 42.9% | 33.3% | 44.4% |
| GPT-5.3-Codex | single-baseline | live | 6/0/1/7 | 7/0/2/2/11 | 0 | 85.7% | 85.7% | 77.8% | 77.8% |
| GPT-5.3-Codex | single-todo-ledger | live | 3/0/4/7 | 5/1/3/2/11 | 4 | 42.9% | 42.9% | 55.6% | 66.7% |
| GPT-5.3-Codex | heartbeat-proactive | live | 5/0/2/7 | 7/0/2/2/11 | 1 | 71.4% | 71.4% | 77.8% | 77.8% |
| GPT-5.3-Codex | heartbeat-auto-60m | live | 2/0/5/7 | 6/0/3/2/11 | 2 | 28.6% | 28.6% | 66.7% | 66.7% |
| GPT-5.3-Codex | heartbeat-auto-30m | live | 5/0/2/7 | 6/1/2/2/11 | 5 | 71.4% | 71.4% | 66.7% | 77.8% |
| GPT-5.3-Codex | hier-union-query | live | 0/1/6/7 | 1/0/8/2/11 | 4 | 0.0% | 14.3% | 11.1% | 11.1% |
| GPT-5.3-Codex | hier-majority-vote | replay | 4/1/2/7 | 2/1/6/2/11 | 17 | 57.1% | 71.4% | 22.2% | 33.3% |
| GPT-5.3-Codex | hier-unanimous-vote | replay | 3/0/4/7 | 1/1/7/2/11 | 12 | 42.9% | 42.9% | 11.1% | 22.2% |
| Llama 3.3 70B Instruct | single-baseline | live | 4/0/3/7 | 4/0/5/2/11 | 7 | 57.1% | 57.1% | 44.4% | 44.4% |
| Llama 3.3 70B Instruct | single-todo-ledger | live | 6/0/1/7 | 5/0/4/2/11 | 4 | 85.7% | 85.7% | 55.6% | 55.6% |
| Llama 3.3 70B Instruct | heartbeat-proactive | live | 3/0/4/7 | 3/0/6/2/11 | 8 | 42.9% | 42.9% | 33.3% | 33.3% |
| Llama 3.3 70B Instruct | heartbeat-auto-60m | live | 2/0/5/7 | 3/0/6/2/11 | 8 | 28.6% | 28.6% | 33.3% | 33.3% |
| Llama 3.3 70B Instruct | heartbeat-auto-30m | live | 1/0/6/7 | 2/0/7/2/11 | 9 | 14.3% | 14.3% | 22.2% | 22.2% |
| Llama 3.3 70B Instruct | hier-union-query | live | 2/1/4/7 | 1/2/6/2/11 | 11 | 28.6% | 42.9% | 11.1% | 33.3% |
| Llama 3.3 70B Instruct | hier-majority-vote | replay | 1/0/6/7 | 1/2/6/2/11 | 13 | 14.3% | 14.3% | 11.1% | 33.3% |
| Llama 3.3 70B Instruct | hier-unanimous-vote | replay | 1/0/6/7 | 1/2/6/2/11 | 11 | 14.3% | 14.3% | 11.1% | 33.3% |
| Mistral Large 2512 | single-baseline | live | 7/0/0/7 | 6/0/3/2/11 | 1 | 100.0% | 100.0% | 66.7% | 66.7% |
| Mistral Large 2512 | single-todo-ledger | live | 5/1/1/7 | 3/0/6/2/11 | 3 | 71.4% | 85.7% | 33.3% | 33.3% |
| Mistral Large 2512 | heartbeat-proactive | live | 6/0/1/7 | 6/0/3/2/11 | 1 | 85.7% | 85.7% | 66.7% | 66.7% |
| Mistral Large 2512 | heartbeat-auto-60m | live | 4/1/2/7 | 6/0/3/2/11 | 2 | 57.1% | 71.4% | 66.7% | 66.7% |
| Mistral Large 2512 | heartbeat-auto-30m | live | 5/0/2/7 | 4/0/5/2/11 | 3 | 71.4% | 71.4% | 44.4% | 44.4% |
| Mistral Large 2512 | hier-union-query | live | 2/3/2/7 | 3/2/4/2/11 | 8 | 28.6% | 71.4% | 33.3% | 55.6% |
| Mistral Large 2512 | hier-majority-vote | replay | 2/4/1/7 | 7/0/2/2/11 | 20 | 28.6% | 85.7% | 77.8% | 77.8% |
| Mistral Large 2512 | hier-unanimous-vote | replay | 2/3/2/7 | 4/1/4/2/11 | 8 | 28.6% | 71.4% | 44.4% | 55.6% |
| Mistral Small 3.2 24B Instruct | single-baseline | live | 1/0/6/7 | 1/1/7/2/11 | 6 | 14.3% | 14.3% | 11.1% | 22.2% |
| Mistral Small 3.2 24B Instruct | single-todo-ledger | live | 3/1/3/7 | 4/0/5/2/11 | 4 | 42.9% | 57.1% | 44.4% | 44.4% |
| Mistral Small 3.2 24B Instruct | heartbeat-proactive | live | 2/0/5/7 | 1/0/8/2/11 | 5 | 28.6% | 28.6% | 11.1% | 11.1% |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-60m | live | 1/0/6/7 | 1/0/8/2/11 | 3 | 14.3% | 14.3% | 11.1% | 11.1% |
| Mistral Small 3.2 24B Instruct | heartbeat-auto-30m | live | 1/0/6/7 | 1/0/8/2/11 | 5 | 14.3% | 14.3% | 11.1% | 11.1% |
| Mistral Small 3.2 24B Instruct | hier-union-query | live | 1/0/6/7 | 2/1/6/2/11 | 3 | 14.3% | 14.3% | 22.2% | 33.3% |
| Mistral Small 3.2 24B Instruct | hier-majority-vote | replay | 0/0/7/7 | 3/1/5/2/11 | 10 | 0.0% | 0.0% | 33.3% | 44.4% |
| Mistral Small 3.2 24B Instruct | hier-unanimous-vote | replay | 0/0/7/7 | 0/0/9/2/11 | 1 | 0.0% | 0.0% | 0.0% | 0.0% |
| Qwen3-32B | single-baseline | live | 0/0/7/7 | 1/0/8/2/11 | 9 | 0.0% | 0.0% | 11.1% | 11.1% |
| Qwen3-32B | single-todo-ledger | live | 0/0/7/7 | 3/0/6/2/11 | 12 | 0.0% | 0.0% | 33.3% | 33.3% |
| Qwen3-32B | heartbeat-proactive | live | 0/0/7/7 | 1/0/8/2/11 | 15 | 0.0% | 0.0% | 11.1% | 11.1% |
| Qwen3-32B | heartbeat-auto-60m | live | 0/0/7/7 | 2/0/7/2/11 | 9 | 0.0% | 0.0% | 22.2% | 22.2% |
| Qwen3-32B | heartbeat-auto-30m | live | 1/0/6/7 | 2/0/7/2/11 | 10 | 14.3% | 14.3% | 22.2% | 22.2% |
| Qwen3-32B | hier-union-query | live | 0/0/7/7 | 3/2/4/2/11 | 15 | 0.0% | 0.0% | 33.3% | 55.6% |
| Qwen3-32B | hier-majority-vote | replay | 0/0/7/7 | 4/0/5/2/11 | 10 | 0.0% | 0.0% | 44.4% | 44.4% |
| Qwen3-32B | hier-unanimous-vote | replay | 0/0/7/7 | 3/0/6/2/11 | 5 | 0.0% | 0.0% | 33.3% | 33.3% |
| Qwen3-14B | single-baseline | live | 1/1/5/7 | 2/0/7/2/11 | 18 | 14.3% | 28.6% | 22.2% | 22.2% |
| Qwen3-14B | single-todo-ledger | live | 0/1/6/7 | 3/0/6/2/11 | 11 | 0.0% | 14.3% | 33.3% | 33.3% |
| Qwen3-14B | heartbeat-proactive | live | 0/1/6/7 | 3/0/6/2/11 | 16 | 0.0% | 14.3% | 33.3% | 33.3% |
| Qwen3-14B | heartbeat-auto-60m | live | 4/1/2/7 | 9/0/0/2/11 | 19 | 57.1% | 71.4% | 100.0% | 100.0% |
| Qwen3-14B | heartbeat-auto-30m | live | 4/1/2/7 | 9/0/0/2/11 | 26 | 57.1% | 71.4% | 100.0% | 100.0% |
| Qwen3-14B | hier-union-query | live | 0/1/6/7 | 4/1/4/2/11 | 15 | 0.0% | 14.3% | 44.4% | 55.6% |
| Qwen3-14B | hier-majority-vote | replay | 0/0/7/7 | 5/0/4/2/11 | 20 | 0.0% | 0.0% | 55.6% | 55.6% |
| Qwen3-14B | hier-unanimous-vote | replay | 0/0/7/7 | 4/0/5/2/11 | 11 | 0.0% | 0.0% | 44.4% | 44.4% |
| Qwen3-8B | single-baseline | live | 0/0/7/7 | 1/1/7/2/11 | 13 | 0.0% | 0.0% | 11.1% | 22.2% |
| Qwen3-8B | single-todo-ledger | live | 1/1/5/7 | 1/0/8/2/11 | 7 | 14.3% | 28.6% | 11.1% | 11.1% |
| Qwen3-8B | heartbeat-proactive | live | 5/0/2/7 | 5/0/4/2/11 | 6 | 71.4% | 71.4% | 55.6% | 55.6% |
| Qwen3-8B | heartbeat-auto-60m | live | 2/0/5/7 | 1/1/7/2/11 | 14 | 28.6% | 28.6% | 11.1% | 22.2% |
| Qwen3-8B | heartbeat-auto-30m | live | 1/0/6/7 | 2/0/7/2/11 | 14 | 14.3% | 14.3% | 22.2% | 22.2% |
| Qwen3-8B | hier-union-query | live | 1/0/6/7 | 0/0/9/2/11 | 10 | 14.3% | 14.3% | 0.0% | 0.0% |
| Qwen3-8B | hier-majority-vote | replay | 0/0/7/7 | 2/1/6/2/11 | 14 | 0.0% | 0.0% | 22.2% | 33.3% |
| Qwen3-8B | hier-unanimous-vote | replay | 0/0/7/7 | 1/0/8/2/11 | 7 | 0.0% | 0.0% | 11.1% | 11.1% |

## Setup-Level Proactive Required by Channel (Aggregated Across 8 Models)

| Setup | appointment_portal | bank_balance | calendar | clock | course_portal | email | library_hold | shipment_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| single-baseline | 2/1/21/24 (8.3%) | 0/0/16/16 (0.0%) | 1/0/23/24 (4.2%) | 89/7/96/192 (46.4%) | 1/0/7/8 (12.5%) | 0/7/9/16 (0.0%) | 0/1/23/24 (0.0%) | 0/0/8/8 (0.0%) |
| single-todo-ledger | 1/0/23/24 (4.2%) | 0/0/16/16 (0.0%) | 1/1/22/24 (4.2%) | 87/16/89/192 (45.3%) | 0/0/8/8 (0.0%) | 0/5/11/16 (0.0%) | 0/0/24/24 (0.0%) | 0/0/8/8 (0.0%) |
| heartbeat-proactive | 2/2/20/24 (8.3%) | 1/0/15/16 (6.2%) | 3/0/21/24 (12.5%) | 105/8/79/192 (54.7%) | 1/2/5/8 (12.5%) | 1/7/8/16 (6.2%) | 3/0/21/24 (12.5%) | 1/0/7/8 (12.5%) |
| heartbeat-auto-60m | 3/0/21/24 (12.5%) | 2/0/14/16 (12.5%) | 3/1/20/24 (12.5%) | 106/8/78/192 (55.2%) | 2/1/5/8 (25.0%) | 1/6/9/16 (6.2%) | 2/2/20/24 (8.3%) | 0/1/7/8 (0.0%) |
| heartbeat-auto-30m | 4/4/16/24 (16.7%) | 2/0/14/16 (12.5%) | 5/1/18/24 (20.8%) | 116/7/69/192 (60.4%) | 1/3/4/8 (12.5%) | 1/7/8/16 (6.2%) | 5/0/19/24 (20.8%) | 1/0/7/8 (12.5%) |
| hier-union-query | 3/0/21/24 (12.5%) | 1/0/15/16 (6.2%) | 0/1/23/24 (0.0%) | 116/11/65/192 (60.4%) | 1/0/7/8 (12.5%) | 0/1/15/16 (0.0%) | 1/0/23/24 (4.2%) | 0/0/8/8 (0.0%) |
| hier-majority-vote | 6/0/18/24 (25.0%) | 3/0/13/16 (18.8%) | 2/3/19/24 (8.3%) | 130/8/54/192 (67.7%) | 1/0/7/8 (12.5%) | 0/3/13/16 (0.0%) | 8/1/15/24 (33.3%) | 0/0/8/8 (0.0%) |
| hier-unanimous-vote | 1/0/23/24 (4.2%) | 1/0/15/16 (6.2%) | 1/3/20/24 (4.2%) | 95/6/91/192 (49.5%) | 0/0/8/8 (0.0%) | 0/2/14/16 (0.0%) | 1/1/22/24 (4.2%) | 0/0/8/8 (0.0%) |

## Model-by-Model Notes

- **GPT-5.4**: baseline Set-F1 72.5%; best overall is `heartbeat-proactive` at 79.1% (TP/FP/FN = 55/3/26); best proactive-required hit rate is `hier-majority-vote` at 66.7%.
- **GPT-5.3-Codex**: baseline Set-F1 78.9%; best overall is `single-baseline` at 78.9% (TP/FP/FN = 60/11/21); best proactive-required hit rate is `hier-majority-vote` at 59.0%.
- **Llama 3.3 70B Instruct**: baseline Set-F1 64.4%; best overall is `single-todo-ledger` at 72.5% (TP/FP/FN = 50/7/31); best proactive-required hit rate is `hier-majority-vote` at 46.2%.
- **Mistral Large 2512**: baseline Set-F1 75.3%; best overall is `single-baseline` at 75.3% (TP/FP/FN = 55/10/26); best proactive-required hit rate is `hier-majority-vote` at 71.8%.
- **Mistral Small 3.2 24B Instruct**: baseline Set-F1 52.6%; best overall is `single-todo-ledger` at 63.4% (TP/FP/FN = 46/18/35); best proactive-required hit rate is `single-todo-ledger` at 30.8%.
- **Qwen3-32B**: baseline Set-F1 51.4%; best overall is `heartbeat-auto-30m` at 57.5% (TP/FP/FN = 44/28/37); best proactive-required hit rate is `hier-union-query` at 43.6%.
- **Qwen3-14B**: baseline Set-F1 43.1%; best overall is `single-todo-ledger` at 52.3% (TP/FP/FN = 40/32/41); best proactive-required hit rate is `heartbeat-auto-30m` at 92.3%.
- **Qwen3-8B**: baseline Set-F1 42.0%; best overall is `heartbeat-proactive` at 71.9% (TP/FP/FN = 64/33/17); best proactive-required hit rate is `heartbeat-proactive` at 66.7%.

## Cross-Setup Conclusions

1. Best overall Set-F1 in this V9 batch is `heartbeat-proactive` (macro Set-F1 65.1%).
2. Best proactive-required hit rate is `hier-majority-vote` (macro proactive hit 48.1%); best non-clock proactive hit rate is `hier-majority-vote` (16.7%).
3. `hier-union-query` issues the most state queries (1661 total), while `single-todo-ledger` has the lowest aggregate FP pressure (134 total FP).
4. The strongest proactive-only setup is not the strongest utility setup. `hier-majority-vote` raises macro proactive hit to 48.1%, but it also has the highest aggregate FP count (655 FP for `hier-majority-vote`), which keeps its macro Set-F1 well below the best live single-agent variants.
5. Auto-heartbeat frequency trades recall for noise. `heartbeat-auto-30m` improves macro proactive hit over `heartbeat-auto-60m` (43.3% vs 38.1%), but both trail `heartbeat-proactive` on macro Set-F1, and `auto30` drives the largest action volume among live single-agent setups.
6. Clock monitoring remains far easier than non-clock monitoring. Even the best non-clock macro hit rate is only 16.7%, far below the best clock macro hit rate of 67.7%.
7. The replay-derived hierarchical variants should be interpreted as decision-rule ablations over the same union-query evidence. Macro Set-F1 shifts from union-query 45.2% to majority-vote 37.2% and unanimous-vote 35.3%.

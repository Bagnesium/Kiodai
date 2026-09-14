# Frozen follow-up results — completed 9 September 2026

**One usable matched pair, one repeat, one complete three-day trajectory per condition.** Both conditions achieved TP=11, FP=0, FN=1; Set-F1=22/23=0.956522. A1−A0=0: no observed accuracy improvement. Both missed the hidden cooling event; all task selections matched. The run is genuine LIVE inference, not a mock demonstration.

Execution: 2026-09-09T13:19:33.828Z–2026-09-09T13:21:52.119Z (UTC), 18:19–18:21 on 9 September in Almaty. The exact authorized command completed once. There were no infrastructure failures, invalid responses, retries, interrupted attempts, exclusions, prompt edits, replacements or protocol deviations. Experimental development is finished.

## Primary result: whole three-day trajectory

| Measure | A0 | A1 | A1 minus A0 |
|---|---:|---:|---:|
| TP | 11 | 11 | 0 |
| FP | 0 | 0 | 0 |
| FN | 1 | 1 | 0 |
| Precision | 1.000000 | 1.000000 | 0.000000 |
| Recall | 0.916667 | 0.916667 | 0.000000 |
| Set-F1 | 0.956522 | 0.956522 | 0.000000 |
| Completed steps | 20 | 20 | 0 |
| Model calls | 21 | 20 | -1 |
| Invalid responses | 0 | 0 | 0 |
| Retries | 0 | 0 | 0 |
| Transport errors | 0 | 0 | 0 |
| Executed tool queries | 1 | 0 | -1 |
| Input tokens | 59171 | 68971 | 9800 |
| Output tokens | 699 | 665 | -34 |
| Total tokens | 59870 | 69636 | 9766 |
| Sum of model-call latency, seconds | 68.270222 | 68.147285 | -0.122937 |
| API-response-reported cost, USD | 0.01454109 | 0.01593485 | 0.00139376 |

TP/FP/FN are summed across each complete trajectory before calculating Precision=TP/(TP+FP), Recall=TP/(TP+FN), and Set-F1=2TP/(2TP+FP+FN). The primary difference compares those two trajectory scores. With one scenario and one repeat, no averaging across replications is possible. Model calls, days and steps are not independent experimental replications. No significance, general equivalence or superiority claim is supported.

## Descriptive breakdown — does not replace the primary result

| Portion | Condition | Steps | TP | FP | FN | Precision | Recall | Set-F1 |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Overlapping Monday | A0 | 8 | 5 | 0 | 0 | 1.000000 | 1.000000 | 1.000000 |
| Overlapping Monday | A1 | 8 | 5 | 0 | 0 | 1.000000 | 1.000000 | 1.000000 |
| Additional Tuesday + Wednesday | A0 | 12 | 6 | 0 | 1 | 1.000000 | 0.857143 | 0.923077 |
| Additional Tuesday + Wednesday | A1 | 12 | 6 | 0 | 1 | 1.000000 | 0.857143 | 0.923077 |

A1−A0 is zero for all six accuracy measures in both portions. These descriptive counts use the saved per-step evaluator records from the intact full-context run. Neither portion was rerun or evaluated as a sliced scenario. The additional 12 steps have 7 due actions: Tuesday 4 TP/0 FP/1 FN, Wednesday 2 TP/0 FP/0 FN in each condition. Monday overlaps pilot 1 and must not be pooled with it as independent evidence. Follow-up planning occurred after observing the pilot.

| Portion | Condition | Queries / calls | Input / output tokens | API-reported USD |
|---|---|---:|---:|---:|
| Monday | A0 | 0 / 8 | 13819 / 269 | 0.00339533 |
| Monday | A1 | 0 / 8 | 19179 / 269 | 0.00428957 |
| Additional 12 steps | A0 | 1 / 13 | 45352 / 430 | 0.01114576 |
| Additional 12 steps | A1 | 0 / 12 | 49792 / 396 | 0.01164528 |

## Hidden-condition audit: all seven Tuesday opportunities

Both conditions received the instruction to acknowledge cooling **only when the sensor board reports fully stable cooling**, the same action menu, and permission to query `sensor_board` once per scheduled step. Clock time was already visible. Only the sensor-board condition was hidden. Neither condition ever selected the cooling action.

| Step / simulated time | Relevant visible information | A0 query / information before choice | A1 query / information before choice | Cooling score |
|---|---|---|---|---|
| dev_t_s1 / 07:30 | Initial conditional instruction; routine checks, no positive state | None; no sensor observation | None; no sensor observation | Correctly no action due; no FP |
| dev_t_s2 / 08:00 | Manifest override; no cooling confirmation | None; no sensor observation | None; no sensor observation | Correctly no action due; no FP |
| dev_t_s3 / 09:00 | Vignette explicitly says nearly stable, not fully stable; safety chime | None; visible negative statement available | None; visible negative statement available | Correctly withheld cooling; both locked chamber, TP=1 |
| dev_t_s4 / 11:30 | Unrelated notices; no changed trigger | Queries sensor_board; receives nearly stable / final stabilization not complete, then chooses no task | No query; earlier visible negative statement retained | Correctly no action due; no FP |
| dev_t_s5 / 13:00 | Review window opens; cooling continues out of sight | No new query; previous negative sensor observation remains in history | No query; no positive sensor observation | Both omit due cooling action: FN=1 each; both sign record, TP=1 |
| dev_t_s6 / 15:00 | Violet approval; placard cancellation | No query; no newer sensor evidence | No query; no positive sensor evidence | Cooling no longer in timely due set; no later cooling selection. Both publish, TP=1 |
| dev_t_s7 / 16:00 | Calibration time, canceled placard cue, Wednesday note | No query; no newer sensor evidence | No query; no positive sensor evidence | No later cooling selection. Both call calibration, TP=1; canceled action withheld |

At `dev_t_s4`, A0 raw-call line 12 requests `sensor_board` and finishes at **13:20:53.490 UTC**. The local simulator returns `State [sensor_board]: Cooling is nearly stable; final stabilization is not complete.` That exact observation is in the next request (line 13), which starts at **13:20:53.492 UTC**, before the empty selection. There is no separately timestamped tool-delivery event; ordering and the following saved request establish that delivery preceded selection. The response is the negative state originating at simulated 09:00, returned at 11:30.

At simulated 13:00 the hidden environment event is `Cooling is now fully stable.` **Neither agent retrieved it.** It appears in the saved scenario/evaluator context, not as an observation in either final selection request. A0 raw-call line 14 and A1 line 13 both select only `task_14` (signing the chamber record), supported by the visible review-window cue and earlier lock selection at 09:00. Both miss `dev_t_ack_cooling`; the evaluator reports TP=1, FP=0, FN=1 at steps/evaluator line 13.

**Query-supported hidden hits: A0=0, A1=0. Correct cooling selections without relevant query evidence: A0=0, A1=0.** There is no correct hidden selection to label as a guess. Withholding at 09:00 was supported by a legitimate visible negative observation. The shared miss is task performance in obtaining/acting on the newly available hidden condition, not an infrastructure or format failure. The records do not reveal why either model failed to query at 13:00. One negative query does not establish successful monitoring.

## Cross-day and concrete behavioral evidence

- The Monday 08:00 message instructs filing the blue archive card on Wednesday when the brass cabinet clicks. The Tuesday 16:00 message instructs hanging the visitor badge when the east gate opens on Wednesday. Both original notes are present in the saved final requests at every Wednesday step; Wednesday’s header says only that there are no immediate intentions.
- At Wednesday 10:00 (`dev_w_s2`, steps line 17), the cabinet scrapes without clicking and the gate stays closed. Both select no task.
- At Wednesday 12:00 (`dev_w_s3`, line 18), the gate visibly opens and both select `task_11` (visitor badge), TP=1. The relevant raw-call lines are A0=19 and A1=18.
- At Wednesday 15:00 (`dev_w_s4`, line 19), the cabinet visibly clicks and both select `task_8` (archive card), TP=1. The raw-call lines are A0=20 and A1=19. Neither condition has a cross-day failure in this trajectory.
- The observed between-condition difference is the single negative sensor query by A0 at Tuesday 11:30; A1 directly chooses no task. This changes call count and context but produces no task-score difference. Both preserve the cancellation, rescheduling and prerequisite behavior.

These are successes with complete prior conversation and action-text menus still available, not proof of an independent memory store or an explanation of internal reasoning. The 20 task selections match exactly; there is no observed accuracy advantage.

## Cost and overhead — different sources kept separate

| Quantity / source | USD | Meaning |
|---|---:|---|
| Pre-run usage-informed projection | 0.03935938 | Pilot-calibrated full-history estimate; assumed 44 calls and no retries/cache discount |
| Pre-run conservative allowance | 0.63708409 | Up to 160 attempts including both conditions, queries, retries and output allowances; heuristic |
| Authorized cumulative ceiling | 0.70000000 | Applies only to this follow-up |
| Actual tokens × frozen uncached prices | 0.03596234 | Calculation, not a bill |
| Sum of all saved API response costs | 0.03047594 | Provider-reported inference costs for 41 calls |
| Final cumulative request reservations | 0.06868424 | Budget guard’s retained estimates, not charges |
| Independently verified billing | unavailable | No account ledger or billing statement inspected |

The free public route GET was the only provider preflight; there were **zero billable preflight requests** and zero unreported model attempts. All responses reported the pinned DeepSeek V3.1 / Novita route. API-reported costs were A0 $0.01454109 and A1 $0.01593485: A1 used 9,800 more input tokens (+16.56%), 34 fewer output tokens and one fewer model call, but cost $0.00139376 more (+9.58%). These are observed differences for this ordered pair, not a general cost or speed effect.

The responses report 15,808 cached input tokens for A0 and 24,832 for A1. At the saved route’s $0.135/M cache-read rate, these reconcile the uncached-price estimate with the API-reported costs. No application answer cache was introduced. Provider caching, differing query histories and fixed A0-first order confound attribution of the entire cost/latency difference to prompt length. Summed request latencies are 68.270222 s and 68.147285 s; they are not independent timing trials or the same as total study wall time. Budget snapshots are cumulative and must not be summed. The run was not restarted and unused budget was not spent.

## Original pilot and limitations

Pilot 1 remains unchanged in `RESULTS.md`: one eight-step pair, both 5/0/0 and Set-F1=1.00; A1 used 5,360 extra input tokens; saved API cost $0.00765034. The follow-up was planned after that result and includes the same Monday portion. Report both separately; they are not two independent replications.

This is an exploratory development evaluation, not blind or independently held out. It has one pair, one repeat, one hidden positive event, two cross-day intentions, full histories, action-text menus and some explicit near-match/obsolete-cue wording. Frozen P1 assumes completion after selection; PM-Bench removes completed handles, so independent prompt-driven duplicate prevention and robust execution confirmation are not established. Heartbeat/background calls are disabled; querying during a supplied step is not autonomous monitoring. MOCK and local tests validate software behavior, not model superiority. No additional experimental development or inference follows this evaluation.

## Artifacts and offline replay

- Study ledger: `/Users/bagnesium/Documents/GitHub/Kiodai/results/followup_v1/study.json`.
- Frozen executed snapshot: `/Users/bagnesium/Documents/GitHub/Kiodai/results/followup_v1/protocol_snapshot.json`.
- Pair: `/Users/bagnesium/Documents/GitHub/Kiodai/results/followup_v1/live-pair-bdf241965f35/pair.json`.
- A0: `/Users/bagnesium/Documents/GitHub/Kiodai/results/followup_v1/live-pair-bdf241965f35/live-A0-20260909T131935-b7f6531a`; requests/responses in `raw_model_calls.jsonl`, visible observations/tools in `steps.jsonl`, scores in `score.json`, separate evaluator records in `evaluator.jsonl`, and all input hashes/settings in `manifest.json`.
- A1: `/Users/bagnesium/Documents/GitHub/Kiodai/results/followup_v1/live-pair-bdf241965f35/live-A1-20260909T131935-5232d513`; requests/responses in `raw_model_calls.jsonl`, visible observations/tools in `steps.jsonl`, scores in `score.json`, separate evaluator records in `evaluator.jsonl`, and all input hashes/settings in `manifest.json`.
- Machine-readable audit, including exact JSONL line references: `/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/verification/followup-live-20260909/analysis.json`.
- Preserved raw study archive: `/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/verification/followup-live-20260909.zip`.
- Recorded dashboard export and replay verification: `/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/verification/followup-live-20260909/recorded-export.zip` and `/Users/bagnesium/Documents/GitHub/Kiodai/artifacts/verification/followup-live-20260909/replay-check.json`.

Regenerate the numeric audit without inference:

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 scripts/analyze_followup_saved.py
```

Replay using the unchanged dashboard (LIVE disabled):

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 -m research_harness.dashboard --output-root results/followup_v1 --port 8766
```

Open http://127.0.0.1:8766, choose **RECORDED**, select **frozen-development-v1 · live-pair-bdf241965f35**, then **Start run** and **Advance timeline**. At steps 12 and 13 inspect the query and shared miss; at steps 18 and 19 inspect the cross-day hits. **Reveal this step** displays evaluator information separately. Replay and export make no model calls. The original pilot remains available under its original output root.

# Final Kiodai status — 9 September 2026

The separately authorized frozen follow-up **completed once**. Experimental development is finished. There is one usable matched pair, one repeat, 20 steps per condition, and 41 genuine model calls. No invalid response, retry, transport failure, restart, provider substitution or protocol deviation occurred.

| Full three-day trajectory | A0 | A1 | A1−A0 |
|---|---:|---:|---:|
| TP / FP / FN | 11 / 0 / 1 | 11 / 0 / 1 | 0 / 0 / 0 |
| Precision / Recall / Set-F1 | 1 / 0.916667 / 0.956522 | 1 / 0.916667 / 0.956522 | 0 / 0 / 0 |
| Calls / queries | 21 / 1 | 20 / 0 | −1 / −1 |
| Input / output tokens | 59,171 / 699 | 68,971 / 665 | +9,800 / −34 |
| API-response-reported USD | 0.01454109 | 0.01593485 | +0.00139376 |

No observed accuracy improvement. All task selections matched. A0 queried the sensor board at Tuesday 11:30, received a negative state and did not query again; A1 made no query. Both missed the hidden positive event at 13:00. Both executed the two Wednesday intentions correctly with the original prior-day messages still in context.

Descriptive only: overlapping Monday 5/0/0, F1=1 for both; 12 additional steps 6/0/1, F1≈0.923077 for both. The primary result remains the full trajectory. The follow-up was planned after the original pilot and repeats its Monday portion; they are not independent replications.

Cost: pre-run usage projection $0.03935938; conservative allowance $0.63708409; authorized ceiling $0.70; actual-token uncached-price estimate $0.03596234; saved API costs **$0.03047594**; independently verified billing **unavailable**. Final budget reservations are $0.06868424, not charges. Zero billable preflight requests or unreported model attempts. Unused authorization was not spent.

The original pilot remains unchanged in `RESULTS.md`/`RESULTS.json`: one eight-step pair, both 5/0/0 and F1=1, A1 +5,360 input tokens, API cost $0.00765034. Both earlier TLS startup failures and the pilot preservation archive remain intact. Frozen preparation documents remain historical snapshots; their “not run” wording describes the time of freezing, not current status.

Final deliverables: `FOLLOWUP_RESULTS.md`, `METHOD.md`, `MANUSCRIPT_UPDATES.md`, `DEFENSE_RU.md`. Actual observations, line references and accounting: `artifacts/verification/followup-live-20260909/analysis.json`. Raw study: `results/followup_v1/`. Preserved archive: `artifacts/verification/followup-live-20260909.zip`. Final check outputs and recorded export are in `artifacts/verification/followup-live-20260909/`.

Replay without inference:

```bash
python3 -m research_harness.dashboard --output-root results/followup_v1 --port 8766
```

Open http://127.0.0.1:8766; RECORDED → `frozen-development-v1 · live-pair-bdf241965f35` → Start run. Steps 12–13 show the query/shared miss; 18–19 show cross-day successes. Rebuild the saved audit with `python3 scripts/analyze_followup_saved.py`.

Limits: one paired trajectory, one hidden positive event, overlapping development data, full history and action menus; P1 assumes completion after selection, environment removes completed handles, heartbeat disabled. No general superiority/equivalence, independent duplicate prevention or autonomous monitoring claim is supported.

No inference or implementation blocker remains. The Pages manuscript was intentionally not overwritten. Submission still requires the author to transfer/review the ready-to-paste paragraphs and complete any required formatting/signatures; supervisor approval is not invented.

Final validation passed: 62 tests; smoke and compile checks; all 164 protected files; development/follow-up frozen hashes; official rescoring; API cost reconciliation; original-pilot/archive preservation; deterministic offline analysis; complete RECORDED replay and browser-visible shared miss. Credentials were checked absent from new outputs, including nested archives. See `artifacts/verification/followup-live-20260909/checks.json`, `replay-check.json`, `browser-check.json` and `completion.json`.

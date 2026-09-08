# Kiodai research prototype

Bagdat Beimzhan / Беймжан Багдат, Grade 10 · Daryn, 9 September 2026.

Kiodai tests whether one fixed prospective-memory instruction changes timely action selection by the same language model. **One genuine frozen pilot completed on 8 September 2026: both A0 and A1 scored TP=5, FP=0, FN=0, Set-F1=1.00. No accuracy benefit was observed.** This is one development scenario, not evidence of general equivalence or superiority. The 16 saved model responses report $0.00765034 total cost; verified billed cost is unavailable. MOCK remains software validation only. See `RESULTS.md`.

The first result remains separately archived with hashes in `research/pilot1_preservation_v1.json`. A broader **prepared, not-run** evaluation is frozen in [FOLLOWUP_EVALUATION.md](FOLLOWUP_EVALUATION.md); [COVERAGE.md](COVERAGE.md) distinguishes actual live coverage from mock demonstrations. Its offline check is `python3 scripts/run_followup.py --preflight`. The proposed new ceiling is $0.70, with a $0.63708409 conservative allowance; the original pilot authorization does not cover it. Follow-up results must use `results/followup_v1/` and `FOLLOWUP_RESULTS.md`, never replace or pool with `RESULTS.md`.

## Run the local demo

Python 3.11+ is enough for the offline runner and dashboard. No package installation or API key is needed for MOCK/RECORDED.

```bash
cd /Users/bagnesium/Documents/GitHub/Kiodai
python3 -m research_harness.dashboard
```

Open [the local demo](http://127.0.0.1:8765). Choose a scenario, leave mode **MOCK**, click **Start run**, then **Advance timeline**. Inspect both agents, reveal the evaluator for a completed step, and export the saved pair. Reset preserves an interrupted pair instead of deleting it. Six educational demos cover time, an exact event, cancellation, rescheduling, completion, and a hidden teacher-feed condition.

For the genuine result, choose **RECORDED**, select **first-development-day-pilot-v1 · live-pair-42433e00474b**, and click **Start run**. Advance through the saved steps without making model calls. The pair is stored under `results/kiodai/live-pair-42433e00474b`. The interface is a thin wrapper over the same `RunSession`/`Pair` used by the CLI. The protected upstream human-evaluation UI is preserved separately in `webapp/frontend`; it does not run this paired harness.

## Verify and reproduce offline

```bash
python3 scripts/verify_benchmark_integrity.py
python3 scripts/verify_development_suite.py
python3 -m unittest discover -s tests -v
python3 -m compileall -q research_harness scripts tests
bash scripts/run_smoke_test.sh
python3 scripts/run_paired.py --suite demo --scenario all
python3 scripts/run_paired.py --suite pilot
python3 scripts/analyze_results.py --root results/kiodai --mode MOCK --output MOCK_RESULTS.md
python3 scripts/analyze_results.py --root results/kiodai --mode LIVE --output RESULTS.md
python3 artifacts/verification/analyze_live_pilot_20260908.py
```

For the same checks with output saved to `artifacts/verification/`, run `python3 scripts/verify_local.py`. With the default offline server running, `python3 scripts/exercise_demo.py` also exercises the HTTP API and saves a sample export; it resets the current demo session.

`--suite pilot` in default MOCK mode returns scripted empty actions for both conditions. It checks the experiment machinery; it does not manufacture a prompt benefit. The educational demo suite uses identical visible-input scripts for both conditions. Existing protected scoring semantics are unchanged. Zero-denominator precision/recall/Set-F1 are `unavailable` (`n/a` in the upstream formatter).

## Executed pilot and paid-run controls

The frozen route is OpenRouter → `deepseek/deepseek-chat-v3.1` → `novita`, `fp8`, fallbacks disabled. The key is read only from the local `OPENROUTER_API_KEY` environment variable; never enter it in the browser or commit it. Merely having a key does not authorize spending.

Optional live dependency setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
```

Zero-cost estimates:

```bash
python3 scripts/run_paired.py --suite pilot --preflight
python3 scripts/run_paired.py --suite development --preflight
```

The newly frozen eight-step pilot takes the **first chronological day** of the recovered development suite. It was selected before any live model results because the full suite's conservative stress estimate exceeds the ceiling. Its paired estimate is about **$0.137**, including maximum queries and retries. The original 20-step development suite estimates about **$0.637** under the new conservative stress policy and is blocked at $0.30. These are estimates, not bills. Original prompts, configurations, manifests, and full-study criteria are preserved. The smaller pilot is a separately versioned development diagnostic; its reduced coverage must be disclosed.

The completed pilot used the following existing command (default repeat count 1). It is recorded for reproducibility, not an instruction to spend again:

```bash
python3 scripts/run_paired.py --suite pilot --live --budget-usd 0.30
python3 scripts/analyze_results.py --root results/kiodai --mode LIVE --output RESULTS.md
```

This exact command performs a free route/price/parameter check before inference. It stops if credentials, the pinned route, price support, or budget are missing. It cannot silently change providers or substitute a mock answer. The budget is shared across repeats in one CLI invocation, but resets in a later invocation. That reset does not renew the user's total authorization: inspect prior costs and uncertain attempts first. The one authorized repeat is now complete; unused budget does not authorize extra repetitions. The server shares one budget across its lifetime. Provider-side accounting is not under perfect client control.

The earlier retry audit preserved two TLS failures before model requests. After the user authorized the local `.env` source, a launcher parsed only `OPENROUTER_API_KEY` using `dotenv_values('.env', interpolate=False)` and supplied it to the command's environment. The runner itself does not auto-load `.env`. The ignored file was not copied into artifacts; no key was printed. The child environment set `SSL_CERT_FILE` to `certifi.where()`, keeping TLS verification enabled. No model or generation setting changed. See `artifacts/verification/pilot-env-preflight-20260908T164356Z.json` and `pilot-live-command-20260908T164356Z.txt` for execution provenance; the earlier retry audit remains preserved.

Paid educational demos are outside the completed pilot's authorization. Use the default offline server for MOCK or RECORDED; neither spends model credits.

## Artifacts and research notes

Each pair has `pair.json` with its order, scenario/config provenance, preflight, budget and completion state. Each condition has its own run directory with exact prompts/config/scenario snapshots, requests and raw responses, actions, validation failures, tool observations, separate evaluator annotations, official score, hashes, Git state, and usage/cost metadata. Logs contain no API key. Simulator outcomes are recorded for inspection; evaluator scores and annotations are never returned to the model. Absolute metadata paths describe the local source; exporters include only a fixed list of synthetic run files, never the manuscript.

- `RESULTS.md`: generated LIVE-only result status.
- `METHOD.md`: actual controls and implementation limitations.
- `DEFENSE_RU.md`: a short explanation and demonstration script in Russian.
- `MANUSCRIPT_UPDATES.md`: evidence-backed corrections to the supplied Pages manuscript.
- `IMPLEMENTATION_LOG.md`: what Codex implemented, what the user requested, and what remains unverified.
- `research/PILOT_PROTOCOL_V1.md`: the small pilot and analysis plan.
- `artifacts/verification/`: saved test, integrity, preflight, and verification outputs.

## Attribution and recovery

This initially empty Kiodai repository was populated from the existing local PMBench checkout on `research/prospective-memory-sota`, commit `e1093c470c8981daf522d4ef047a7c3a71e077d7`, including its uncommitted research harness. The source checkout was left unchanged. `research/recovery_snapshot.json` records the recovered files and hashes.

PM-Bench, its scenario, scorer, released results, and original frontend are prior work from [genglinliu/PMBench](https://github.com/genglinliu/PMBench). The original README is preserved in `docs/PMBENCH_UPSTREAM_README.md`; all 164 protected files remain intact. No upstream license file was present in the recovered snapshot; no license or redistribution permission is invented here. Nothing has been pushed or deployed. Historical notes in `research/` and `reports/` describe earlier scope; use the current root documents and pilot protocol for this delivery.

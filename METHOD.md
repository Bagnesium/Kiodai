# Kiodai method and limits

## Research question and intervention

Does the exact frozen P1 instruction improve timely intention execution compared with the same agent without P1, under matched conditions? A0 uses `prompts/baseline_system.txt`; A1 appends two newlines and the stripped contents of `prompts/prospective_memory_system.txt`. No external memory, scheduler, extra agent, retrieval mechanism, monitoring call, or tool is exclusive to A1.

Recovered P1 file SHA-256: `fcbb7048bb57c0046caeb7246c83470a7980129fe27b4c413a09f80b4200651a`.

Frozen development effective prompts: A0 `a92e6af5cfc6bd7839a0b3ffc00022eb6b332a85ac0e292c61629f5c8a663c38`; A1 `3d8cc7b0a81f5d6ddfa56d526d3299d6582365fdf6e5a5515ca62c53ad9a02b4`. Effective hashes vary with legitimate channel names in different scenarios; the P1 file itself never changes.

P1 asks for silent reconstruction of intentions, reconciliation of cancellations/updates, relevant state queries, trigger checks, execution, and retention. **Its VERIFY rule says to treat selection as completion unless later evidence shows failure.** This differs from the manuscript's stronger “only after confirmed success” rule. The prototype tests the frozen text; it does not rewrite it or claim that stronger rule was tested. The strict action schema exposes no persistent textual ledger, so the internal reconstruction instruction cannot be inspected as a memory state.

## Actual execution path

`paired.Pair` creates two fresh `session.RunSession` instances. Both use `runner.iter_environment`; the CLI drives this iterator to completion, while the HTTP dashboard advances it one step per button click. Scheduled observations arrive from the simulator. The agent does not wake itself up: heartbeat is disabled for both conditions.

The runner sends a rendered prompt, accumulated legitimate narrative observations, available channels, permitted query results, and shuffled anonymous action handles. It does not serialize the scenario or task state into a model request. Future observations, canonical task IDs, embedded ground truth, due sets, and evaluator annotations do not enter the selector. The selector has no evaluator import or scenario parameter.

Each raw request and response is logged. Strict JSON validation checks exact fields, choices, channel permissions, handle membership, duplicate handles and duplicate JSON keys. Handle mapping is mechanical and occurs before computing the due set. An incorrect selection stays incorrect. The upstream simulator applies its execution/completion rules after selection. Separate evaluator files store due, missed and false sets and task-state visualizations. These annotations never feed back into the model.

The simulator's completion rules also remove completed handles from later menus. That ordinary environment behavior is shared by both conditions, but materially assists duplicate suppression. A later request to submit a removed handle is a validation error, not evidence that the model independently remembered completion. Scorer tests verify duplicates; the LIVE menu protocol does not provide a strong duplicate-memory test. Late completion is allowed in some upstream windows but remains FP/FN for the timely Set-F1 metric. Selected actions that the simulator rejects remain logged and scored.

No actual messages, calendars, documents, or school systems are modified. “Simulator completed” describes the simulation only. There is no external success receipt in the model-facing interaction; this further limits claims about real tool-failure recovery.

## Controls and context

Both conditions share model, provider, FP8 route, sampling, seed, output limit, context policy, tool permissions, tool-query budget and retry policy. Context is the full accumulated conversation across days until the fixed estimated token cap; no truncation, hidden state, answer cache, or external intention store is added. There is one simulated state query per step. A second query attempt terminates that step with no task action, and the log distinguishes attempted from executed queries. Histories can diverge due to each condition's own actions, query results and execution outcomes; saved requests make that divergence inspectable.

Model: `deepseek/deepseek-chat-v3.1`; route `novita`; quantization `fp8`; fallbacks disabled; require parameters enabled; reasoning disabled; temperature 0; top-p 1; seed 20260904; maximum output 256; context estimate cap 32768. Seeds are requested but provider determinism is not guaranteed. Repeats use the same frozen seed, are not independently seeded draws, and must not be described as independent evidence.

## Failure handling and budget

Malformed responses receive at most one corrective retry containing only schema instructions and the invalid response. If still invalid, the action set is empty and the error stays in evaluation. The old mock config had requested two retries; the runtime now caps retries at one, and the original config remains preserved. Transport errors are logged separately and, if the retry remains, repeat the same request without a corrective message. Malformed output and transport errors share a two-attempt limit per interaction; retries do not stack. A transport error on the final allowed attempt interrupts the run and pair; partial artifacts remain. Budget and route failures are not retried. The OpenAI client has automatic SDK retries disabled, preventing hidden billable retries.

LIVE requires an explicit flag and finite positive budget no greater than $0.30. A key is read only from the environment. Public endpoint metadata must confirm the route, quantization, parameters and prices before a call. Requests include provider `only`, order, FP8 and fallback restrictions. Returned model/provider metadata is checked, and unverified responses are saved but not selected.

Before a pair, a local stress preflight makes one query per step and one invalid-output retry per interaction, using long outputs. Request bytes/4 × 1.6 provides a padded input-token estimate; every attempt reserves 256 output tokens. Each request reserves its own estimate before dispatch; a shared budget tracks both conditions. Reported costs are retained where supplied, and overruns relative to reservations reduce the remaining budget. Unknown billed amounts remain unknown; an uncertain failed request retains its reservation. These estimates cannot guarantee a provider bill. Preflight GET requests make no inference calls.

## Scoring and analysis

Official scoring is `sim.pm_bench.score_log`, preserved byte for byte. At each step, timely selected actions in the due set contribute TP; selected actions outside it contribute FP; due actions not selected contribute FN. Over a trajectory:

- Precision = TP / (TP + FP).
- Recall = TP / (TP + FN).
- Set-F1 = 2TP / (2TP + FP + FN).

The upstream zero-denominator convention is `n/a`; JSON reports use null/unavailable. A cancellation-only demo may have TP=FP=FN=0 and undefined F1. It must not be displayed as a measured perfect score. Official reports separately count update violations, late actions, dependency violations and duplicate commissions. Some update-error categories are combined upstream; do not claim to distinguish cancellation from reschedule errors solely from the aggregate counter. Per-step annotations support case inspection.

Analysis verifies saved inputs and hashes, reruns the official scorer, and compares reconstructed scores with saved scores. A0/A1 differences are computed for an entire scenario/trajectory. Repeats are averaged within scenario before averaging across scenarios. Days in a carried conversation and sequential steps are not independent samples. Interrupted/incomplete pairs and unpaired runs are listed, not silently discarded. No confidence interval, p-value, or success threshold is invented for the small pilot.

## Provenance and limits

The original frozen development suite is one 20-step, three-day trajectory. The new pilot uses its first eight-step day, selected chronologically before live inference to fit the budget. It is a diagnostic subset with less coverage; cross-day retention and later-day hidden-state performance are not evaluated by this pilot. Full-study preregistration thresholds remain in their original file and do not transfer to the subset.

The six educational demos were authored by Codex during this implementation and are used to develop/test the demo. They are neither an untouched test set nor blind OOD evidence. MOCK uses condition-neutral scripted behavior; its scores prove nothing about the model. RECORDED is only a display mode for genuine saved LIVE runs. Authenticated inference completed for the one frozen pilot pair described below; it did not evaluate the six educational demos.

The released PM-Bench week is preserved, but cannot be described as untouched: recovered tests inspect its identifiers and cues, and historical research notes discuss released-log/scorer audits. This session reran those existing checks; it did not run a final-week model evaluation or tune P1. Earlier exposure cannot be completely reconstructed. PM-Bench and its released results remain upstream work. There is no evidence here of multilingual generalization, independent waking, real-world task execution, SOTA, or an improvement in memory. Student authorship, understanding and supervisor review require the user's own records and defense; software generation does not establish them.

## Earlier authorized preflight, before inference

The user subsequently authorized the frozen small pilot with a total $0.30 ceiling. Local preflight verified unchanged prompt/config/scenario hashes, one scenario, one repeat, A0 then A1 at each of eight steps, 16 minimum model calls, 64 maximum attempts, and a $0.13677592 conservative pair estimate. The command without `--repeats` matches the frozen one-repeat protocol. No experiment was executed: OPENROUTER_API_KEY was unavailable. There are no executed protocol deviations, new model observations, or prompt changes. See `artifacts/verification/authorized-pilot-preflight.json`.

## Retry audit, 2026-09-08 16:39 UTC

Two later saved LIVE startup attempts, `live-pair-8eafb0fb7cc2` and `live-pair-c13c57cee05d`, failed certificate verification in the free public route lookup. Each contains only `pair.json`, with zero completed steps and no condition runs. Inspection of the execution order confirms that this failure precedes model transport construction. These are infrastructure failures, not malformed model responses or task-performance failures. Both records remain byte-for-byte unchanged; their hashes and matching frozen configurations are recorded in `artifacts/verification/pilot-retry-audit-20260908T163833Z.json`.

This audit made no model requests. The public route check passed with `SSL_CERT_FILE` pointing to the installed certifi CA bundle; TLS verification was enabled. The inherited Python trust configuration still failed, so the successful bundle setting must be present in the shell that starts the command. The Novita FP8 route advertised the frozen model, required parameters and prices ($0.27/M input, $1.00/M output); account authentication and a successful generation remain untested. The environment key was unavailable in both Codex execution contexts, so no paid retry started.

The guard checks full-pair headroom before startup and reserves each request estimate before dispatch; it does not atomically debit the entire pair estimate. This suffices for the authorized single sequential pair with no competing consumers, but is a heuristic allowance, not a billing guarantee. The budget is process-local: a new CLI invocation does not automatically inherit prior costs. Here the two saved attempts reached no model calls, so local execution evidence implies $0 inference cost from them; provider-reported and verified billed costs remain unavailable. Future failures after dispatch must retain their costs or uncertain reservations against the same $0.30 authorization. No extra repetition is authorized merely because twice the estimate is below $0.30.

## Executed pilot, 2026-09-08 16:44–16:45 UTC

After the user explicitly identified and authorized reading the local `.env`, only `OPENROUTER_API_KEY` was parsed using the installed python-dotenv parser with interpolation disabled and supplied to the child process environment. No shell code from `.env` was executed and no key was printed, logged or put into tracked files. `SSL_CERT_FILE` pointed to the installed certifi trust bundle; TLS verification remained enabled. This environment setup resolved the previous blocker without changing the experiment implementation.

The exact existing command was executed once: `python3 scripts/run_paired.py --suite pilot --live --budget-usd 0.30`. Default repeat count 1 matched `research/PILOT_PROTOCOL_V1.md`. Pair `live-pair-42433e00474b` started at 16:44:19.395 UTC and finished at 16:45:13.556 UTC. A0 and A1 each completed the same first chronological development day (eight steps), with A0 then A1 at each step, separate histories, seed 20260904 and unchanged frozen prompt hashes/configuration/scenario/scorer. The exact runtime snapshots and raw requests are under `results/kiodai/live-pair-42433e00474b/`. No experimental protocol deviation, prompt change, replacement response, selective rerun or extra repetition occurred. The two earlier pre-inference TLS failures remain recorded as incomplete startup attempts.

All 16 requests returned the pinned `deepseek/deepseek-chat-v3.1` model and `Novita` provider. Each condition made eight calls, no tool queries and no retries; no malformed responses or live transport errors occurred. Every request used the frozen 256-token output allowance, temperature 0, top-p 1, reasoning disabled, FP8 and no provider fallback. Both effective prompt hashes match those listed above. The prospective estimate was $0.13677592 for up to 64 attempts, including queries and retries. The actual request reservations totaled $0.01924624. Sum the 16 raw response costs rather than cumulative budget snapshots: A0's final snapshot precedes A1's last request, and summing snapshots would double-count shared spend.

The saved response-reported costs total $0.00765034 (A0 $0.00336941, A1 $0.00428093). Multiplying actual token counts by uncached frozen list prices gives a separate $0.00944746 estimate. Responses report 4,672 cached input tokens for A0 and 8,640 for A1, accounting for the difference at the advertised cache-read price. No application cache or shared intention state was introduced. Provider caching and single ordered execution limit interpretation of cost/latency differences; account billing was not independently queried, so verified billed cost is unavailable.

Official trajectory scoring gives TP=5, FP=0, FN=0 and precision=recall=Set-F1=1 for each condition; paired differences in those metrics are zero. Task selections match at all eight steps. The incidental ongoing-task choice differs at 08:30 and is not part of the prospective-memory score. A1 used 5,360 more input tokens. This exploratory pilot found no accuracy improvement and has a ceiling result in the baseline; it establishes neither general equivalence nor general superiority. No query behavior, hidden-state capability or cross-day retention was demonstrated. Reproduce the full report without inference using `python3 artifacts/verification/analyze_live_pilot_20260908.py`.

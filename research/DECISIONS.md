# Decision Log

## D-001 — Freeze original implementation and artifacts

- Date: 2026-09-04
- Decision: Protect the released scenario, original Python simulator/evaluator/generators/runners, released results, and browser implementation by individual SHA-256 hashes.
- Reason: The original runtime and evaluator are entangled; editing the file would weaken provenance.

## D-002 — Separate leakage-free runner

- Date: 2026-09-04
- Decision: Build a new runner around imported public environment/scoring primitives. The model-facing selector receives only rendered messages, anonymous handles, and allowed channel names.
- Reason: The original runner replaces exhausted invalid responses with tasks drawn from the evaluator’s due set.

## D-003 — Fail-closed policy

- Date: 2026-09-04
- Decision: After all retries fail, advance with choice `A` and zero task actions. Preserve the raw invalid response and mark the run `completed_with_failures`.
- Reason: This adds no answer information, keeps trajectory length scoreable, and makes the failure count against the method.

## D-004 — No prompt development in guardrail stages

- Date: 2026-09-04
- Decision: Create only a clearly disabled placeholder for the future prospective-memory instruction.
- Reason: Prompt candidate design belongs after the harness and data separation are reviewed.

## D-005 — Configuration format

- Date: 2026-09-04
- Decision: Store configs as JSON documents with `.yaml` extensions; JSON is a YAML 1.2 subset.
- Reason: Avoid adding an unpinned YAML dependency during the integrity stage.

## D-006 — Synthetic smoke fixture and paid-run lock

- Date: 2026-09-04
- Decision: Use a six-step, independently authored laboratory fixture and deterministic mock transport. Non-mock execution requires both a config opt-in and `--allow-paid`; unfinished configs are rejected.
- Result: The official validator accepted the fixture, the mock run completed with six logged model calls and zero network cost, and its output was scored by the unchanged official evaluator.

## D-007 — One prompt candidate only

- Date: 2026-09-04
- Decision: Freeze P1 as the only prompt candidate for the fast falsification experiment.
- Reason: The objective is to determine whether a strong static instruction is sufficient, not optimize repeatedly against development scores.
- Prompt SHA-256: `fcbb7048bb57c0046caeb7246c83470a7980129fe27b4c413a09f80b4200651a`

## D-008 — Independent development suite

- Date: 2026-09-04
- Decision: Freeze one independently authored three-day, 20-step development scenario before any A0/A1 model call.
- Reason: It covers the preregistered lifecycle and precision cases without consulting or modifying released-week answers.
- Scenario SHA-256: `532486afa5c79a902791d6a6bcfb789b6b7b1dcb8a1a60c307b9dc5e1dbcc2a4`

## D-009 — First model and heartbeat policy

- Date: 2026-09-04
- Decision: Recommend `deepseek/deepseek-chat-v3.1` through OpenRouter pinned to provider slug `novita` with the `fp8` quantization filter, with heartbeat disabled identically for A0 and A1.
- Reason: It is inexpensive, supports structured JSON-schema responses and a seed, has sufficient context, and avoids the cheaper DeepInfra FP4 endpoint as a quality confound. The experiment is not an optional-heartbeat reproduction.

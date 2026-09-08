# Preregistration: Fast Static-Skill Falsification

## Question

How much of prospective-memory performance can one fixed model-facing instruction explain without external memory or lifecycle code?

## Hypothesis

Adding frozen prompt P1 to the otherwise identical baseline will substantially increase official Set-F1 and true-positive actions across the three development days without materially increasing false positives or lifecycle violations.

## Frozen inputs

- Development suite: `data/development/prospective_memory_dev_v1.json`
- Scenario SHA-256: `532486afa5c79a902791d6a6bcfb789b6b7b1dcb8a1a60c307b9dc5e1dbcc2a4`
- Skill addendum SHA-256: `fcbb7048bb57c0046caeb7246c83470a7980129fe27b4c413a09f80b4200651a`
- A0 config SHA-256: `2de4e7b9a9f596fa22bcb33861b32eeb1ef7e1dcd1273cc64efd655cc680b27e`
- A1 config SHA-256: `8b6ba7cee65e2f4f274ad18a64e6f2c97ca7a9a8876313f83925e6b774dc9865`
- A0 effective prompt SHA-256: `a92e6af5cfc6bd7839a0b3ffc00022eb6b332a85ac0e292c61629f5c8a663c38`
- A1 effective prompt SHA-256: `3d8cc7b0a81f5d6ddfa56d526d3299d6582365fdf6e5a5515ca62c53ad9a02b4`

## Conditions

- A0: `configs/dev_a0_deepseek_v31.yaml`
- A1: `configs/dev_a1_deepseek_v31.yaml`

The only model-facing difference is the exact P1 addendum. Experiment IDs and condition labels also differ for bookkeeping but are not sent to the model.

Shared settings:

- Provider: OpenRouter
- Pinned provider slug: `novita`
- Required quantization: `fp8`
- Pinned endpoint quantization: FP8
- List price used for budget: $0.27/M input and $1.00/M output tokens
- Route fallbacks: disabled
- Require parameter support: true
- Model: `deepseek/deepseek-chat-v3.1`
- Reasoning: disabled; reasoning content excluded
- Temperature: 0
- Top-p: 1
- Seed: 20260904
- Maximum output: 256 tokens per call
- Context cap: 32,768 estimated tokens
- Invalid-response retries: 1
- Timeout: 120 seconds
- State queries: at most one per step
- Heartbeat: unsupported and disabled in both conditions
- Task legend: disabled

## Calls and cost

There are 20 steps per condition.

- Minimum: 20 calls per condition, 40 total.
- Expected: 21–23 calls per condition, 42–46 total, allowing relevant hidden-state checks.
- Maximum logical calls: 40 per condition, 80 total.
- Maximum billable attempts with one retry: 80 per condition, 160 total.

Local no-query prompt-growth preflight:

| Condition | Calls | Estimated input | Estimated output | Projected list-price cost |
|---|---:|---:|---:|---:|
| A0 | 20 | 57,317 | 320 | $0.0158 |
| A1 | 20 | 75,403 | 320 | $0.0207 |
| Pair | 40 | 132,720 | 640 | $0.0365 |

Expected total with monitoring is approximately $0.04–$0.07. The conservative authorization ceiling is $0.30 for the pair, including maximum configured queries and retries. Exceeding that ceiling requires stopping and renewed approval.

An offline adversarial mock preflight forced one query at every step, one invalid-response retry for every interaction, and 1,024-character invalid outputs. Across the pair it produced the configured maximum 160 billable attempts, an estimated 616,744 input tokens, 22,080 output tokens, and a $0.1886 list-price projection. This is a stress estimate, not a provider bill or a guarantee; $0.30 retains headroom for tokenizer-estimation error.

## Success criterion

The static skill is provisionally useful only if all conditions hold:

1. A1 Set-F1 exceeds A0 by at least 15 absolute percentage points.
2. A1 records at least two additional true-positive task actions.
3. A1 adds no more than one false-positive action.
4. A1 introduces no new cancellation, update, or dependency violation.
5. A1 is no worse on all three days and strictly better on at least two.

If A0 already exceeds 85% Set-F1, the suite has a ceiling problem and the prompt effect is inconclusive rather than successful.

## Failure criterion

The single-skill hypothesis fails this fast screen if the Set-F1 gain is below 10 points, gains occur on only one day, A1 adds two or more false positives, or it creates a new lifecycle violation. A 10–15 point gain is borderline. In either the failure or borderline case, do not tune another prompt; analyze trajectories and proceed to architecture design.

This one-pair development run is a go/no-go screen, not evidence of statistical significance, model-family transfer, PM-Bench test performance, or SOTA.

## Output location

Both configurations write unique run directories below `results/raw/development/`, containing raw requests and responses, actions, failures, official scores, usage, latency, cost, and manifests.

## Execution gate

Do not execute until the user approves paid/network calls and `OPENROUTER_API_KEY` is available. Both config opt-in and the `--allow-paid` CLI flag are required.

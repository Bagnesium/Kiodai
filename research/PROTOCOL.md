# Prospective-Memory Research Protocol

## Questions

The project tests whether one fixed model-facing instruction improves PM-Bench without external memory, how it compares with a faithfully reproduced or approximated Prospective Intention Store (PIS), which failures require deterministic state, and whether any gain transfers beyond the released benchmark week.

## Experimental conditions

- A0: frozen official-style baseline prompt.
- A1: A0 plus exactly one frozen provider-neutral prompt addendum.
- A2: reproduced PIS, or a clearly labeled independent approximation if official code remains unavailable.
- A3: at most one failure-driven extension selected after A0/A1/A2 analysis.

Within a comparison, model, provider route, tool access, context, token limits, retries, timeout, scenario order, and scoring must be identical. The prompt addendum is the only A0/A1 difference.

## Data separation

The released `data/synthetic_week_v9.json` is final in-distribution test data. Prompt development must use separately seeded synthetic development scenarios. Generator-derived data remain template-IID and must not be described as strong OOD evidence. Independently authored generalization fixtures are reserved before method selection.

## Gates

1. No model call until integrity checks, fail-closed behavior, raw logging, and manifests pass locally.
2. No full run until a tiny smoke run succeeds and its measured token/cost projection is reviewed.
3. No released-week evaluation until one prompt candidate is selected on development data and hash-frozen.
4. No SOTA claim without comparable PIS reproduction, repeated trials, uncertainty estimates, and held-out generalization.

## Statistics

Use identical scenario instances for paired comparisons. Report per-run and per-instance differences, mean, median, standard deviation, bootstrap confidence intervals, a justified paired test, and an effect size. Report category regressions and costs even when aggregate F1 improves.

## Failure and exclusion policy

Invalid model output exhaustions produce a no-task fail-closed action that remains in the scored trajectory. Runs are not silently dropped. Technical exclusions require a recorded reason, raw evidence, and counts in the manifest. A completed run containing fail-closed actions is marked `completed_with_failures`.


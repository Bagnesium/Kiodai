# PM-Bench Research Guardrails

## Purpose

This repository evaluates prospective memory in language-model agents. Research changes must improve evidence quality, not merely benchmark scores.

## Protected files

Treat every path recorded in `research/protected_hashes.json` as immutable. This includes the released benchmark, original evaluator and generators, released results, original experiment runners, and browser implementation. Verify them with:

```bash
python scripts/verify_benchmark_integrity.py
```

## Setup and checks

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
scripts/run_smoke_test.sh
```

The repository currently has no separate formatter or linter dependency. Until one is adopted, compile Python files with `python3 -m compileall research_harness scripts tests` and keep code compatible with Python 3.11+.

## Experimental integrity

- Never expose `groundtruth`, evaluator due sets, canonical expected IDs, or protected evaluator state to an evaluated model or action selector.
- Never use expected answers as an invalid-response fallback. Fail closed with no task action and record the failure.
- Never change a benchmark, expected answer, protected evaluator, generator, or released artifact.
- Never tune prompts on the released final week or embed benchmark-specific examples.
- Never silently change models, providers, routes, prompts, budgets, tools, retries, exclusions, or scoring protocols.
- Do not run a paid experiment without a reviewed hypothesis, frozen configuration, estimated cost, success/failure criteria, and output location.

## Required artifacts

Each experiment must preserve raw requests and responses, actions before and after handle mapping, retry and parse failures, official scores, token/latency/cost accounting, and a complete machine-readable manifest under `results/` or a declared external artifact directory.

## Definition of done

Work is done only when protected hashes pass, local tests pass, configurations and prompts are hashed, failures and exclusions are explicit, results are reproducible, and claims do not exceed the evidence recorded in `research/CLAIMS.md`.

# Reproducibility Record

## Initial repository state

- Audit date: 2026-09-04
- Starting branch: `main`
- Starting commit: `e1093c470c8981daf522d4ef047a7c3a71e077d7`
- Research branch: `research/prospective-memory-sota`
- Released scenario SHA-256: `94a45937da1363be19ccfdc2c188d132f23093041e30abd3ec22d64d70da8f24`
- Original `sim/pm_bench.py` SHA-256: `d8ec27d8dcf4679d7a789c52fc305286df460844d47e9f116b81f2400ac254d8`

The authoritative per-file inventory is `research/protected_hashes.json`. It is generated once by `scripts/verify_benchmark_integrity.py --write-manifest` and verified without rewriting thereafter.

- Protected inventory file count: 164
- Protected inventory manifest SHA-256: `f6aed54f4c6b5ff5366b32b9aa59ed5e826e23a1d25bef944f53723a9d65c4cb`

## Environment

The audited machine had Python 3.14.2, OpenAI SDK 2.24.0, Node 24.14.1, and npm 11.11.0. Final experiments should use a newly pinned Python 3.11 environment; current `requirements.txt` is not locked.

## Reproduction commands

```bash
python3 scripts/verify_benchmark_integrity.py
python3 -m unittest discover -s tests -v
scripts/run_smoke_test.sh
```

The smoke scenario and mock responses are synthetic and must not contain released-week task text, cues, IDs, or answers.

The frozen A0/A1 preregistration, input hashes, model route, and local normal/adversarial cost preflights are recorded in `research/EXPERIMENT_PREREGISTRATION_A0_A1.md` and `research/a0_a1_freeze_manifest.json`. No network model call had been made when the freeze manifest was written.

## Artifact requirements

Every run directory contains an official-compatible action log, raw call JSONL, failure JSONL, score JSON, and manifest JSON. Raw call records include every request, response, retry, parse error, timing, reported model, and usage object. The manifest records hashes, resolved settings, paths, cost accounting, status, and exclusions.

#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root"

python3 scripts/verify_benchmark_integrity.py
python3 scripts/run_leakage_free.py --config configs/smoke_test.yaml "$@"

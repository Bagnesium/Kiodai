#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from research_harness.runner import run_experiment


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the leakage-free PM-Bench harness.")
    parser.add_argument("--config", required=True, help="JSON-compatible YAML config path.")
    parser.add_argument(
        "--output-root",
        default=None,
        help="Optional output-root override, primarily for tests and local smoke runs.",
    )
    parser.add_argument(
        "--live", "--allow-paid", dest="allow_paid",
        action="store_true",
        help="Required in addition to execution.allow_paid=true for non-mock providers.",
    )
    parser.add_argument("--budget-usd", type=float, default=None, help="Explicit maximum budget, at most 0.30 USD.")
    args = parser.parse_args()
    manifest = run_experiment(
        Path(args.config),
        allow_paid=args.allow_paid,
        budget_usd=args.budget_usd,
        output_root_override=args.output_root,
    )
    print(manifest)
    import json
    return 0 if json.loads(manifest.read_text())["status"].startswith("completed") else 1


if __name__ == "__main__":
    raise SystemExit(main())

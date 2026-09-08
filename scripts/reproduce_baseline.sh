#!/usr/bin/env bash
set -euo pipefail
echo "Blocked: live baseline execution is not approved in Stages 1-3." >&2
echo "Review configs/baseline.yaml and the research gates before enabling it." >&2
exit 2


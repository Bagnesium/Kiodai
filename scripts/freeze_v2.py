#!/usr/bin/env python3
"""Explicit one-time pre-inference freeze; refuses to overwrite an existing freeze."""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_v2 import ROOT, FREEZE, protocol_files, preflight
from kiodai_v2.common import digest, dump
from research_harness.model_gateway import utc_now


def main():
    if FREEZE.exists():
        raise SystemExit('Already frozen; a method change requires a separately named development version.')
    config, cases, estimate = preflight(False)
    FREEZE.parent.mkdir(parents=True, exist_ok=True)
    dump(FREEZE, {'evaluation': 'kiodai-v2-exploratory-12-v1', 'frozen_at_utc': utc_now(),
         'hashes': {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in protocol_files()},
         'cases': cases, 'config': config, 'estimate': estimate,
         'failure_policy': 'One schema/semantic-validation retry, then fail closed for that step. Any transport failure stops the whole study with unknown charge retained. No automatic resume or replacement run.',
         'context': 'Full received history for all methods; shared documented simulator receipts; no heartbeat.',
         'primary': 'Whole-trajectory official TP/FP/FN, precision, recall, Set-F1 and paired A2-A0/A2-B_ledger differences.',
         'hypothesis': 'A2 obtains relevant hidden evidence more reliably than B_ledger, increasing end-to-end Set-F1; this is unproven and may incur overhead.',
         'decision_rule': 'Report mean per-trajectory A2 minus B_ledger Set-F1 only when all 12 pairs are complete; A2 minus A0 is the reference contrast. Positive, zero and negative differences are all publishable. A positive mean is descriptive evidence on this exposed suite, not general superiority. Invalid extraction remains in the end-to-end score; infrastructure interruption yields no complete-study primary conclusion.',
         'exposure': 'All synthetic templates and local mock traces inspected during development. No independent held-out or blind claim. Existing follow-up is regression material.',
         'output': 'results/v2/live-frozen-v2', 'new_live_inference_authorized': False})
    print(FREEZE)


if __name__ == '__main__':
    main()

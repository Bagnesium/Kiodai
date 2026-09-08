#!/usr/bin/env python3
"""Prepare or explicitly authorize ONE frozen follow-up; default is offline."""
import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from research_harness.followup import FREEZE, preflight, authorize
from research_harness.hashing import sha256_file
from research_harness.model_gateway import RunStopped, safe_error, utc_now
from research_harness.paired import Pair
from research_harness.session import write_json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--preflight', action='store_true', help='Offline validation and estimates only (default).')
    mode.add_argument('--live', action='store_true', help='Explicitly authorize the new frozen $0.70 study.')
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--env-file', type=Path, help='For LIVE only: parse only OPENROUTER_API_KEY, never execute the file.')
    args = parser.parse_args()
    try:
        study, cfgs, estimate = preflight()
        if not args.live:
            if args.budget_usd is not None or args.env_file is not None:
                raise RunStopped('--budget-usd/--env-file require --live; preflight never reads credentials.')
            print(json.dumps({'status': 'prepared_not_run', 'paid_inference': False,
                              'evaluation_id': study['evaluation_id'], 'scenario_count': 1,
                              'days': 3, 'steps_per_condition': 20, 'repeats': 1,
                              'usage_informed_estimate': study['usage_informed_estimate'],
                              'conservative_estimate': estimate,
                              'proposed_budget_usd': study['proposed_budget_usd']}, indent=2))
            return 0
        root, budget = authorize(study, cfgs, estimate, live=args.live, budget_usd=args.budget_usd)
        if args.env_file:
            from dotenv import dotenv_values
            key = dotenv_values(args.env_file, interpolate=False).get('OPENROUTER_API_KEY')
            if not key:
                raise RunStopped('The requested local file has no nonempty OPENROUTER_API_KEY.')
            os.environ['OPENROUTER_API_KEY'] = key
        if not os.environ.get('OPENROUTER_API_KEY'):
            raise RunStopped('OPENROUTER_API_KEY is unavailable; no inference started.')
        # The same verified CA setup used in pilot 1; never disable TLS checks.
        import certifi
        os.environ.setdefault('SSL_CERT_FILE', certifi.where())
        root.mkdir(parents=True, exist_ok=False)  # atomic one-invocation gate
        write_json(root / 'protocol_snapshot.json', study)
        execution = {'evaluation_id': study['evaluation_id'], 'mode': 'LIVE', 'status': 'preparing',
                     'started_at_utc': utc_now(), 'protocol_sha256': sha256_file(FREEZE),
                     'authorization_usd': args.budget_usd, 'previous_pilot_pooled': False,
                     'planned_repeats': 1, 'budget': budget.snapshot(), 'pair_id': None}
        write_json(root / 'study.json', execution)
        pair = None
        try:
            pair = Pair(suite='development', mode='LIVE', live=True, output_root=root,
                        budget_usd=args.budget_usd, budget=budget, repeat=0)
            execution['pair_id'] = pair.pair_id
            while pair.plan['status'] == 'running':
                pair.advance()
                execution.update(status=pair.plan['status'], budget=budget.snapshot())
                write_json(root / 'study.json', execution)
            return 0 if pair.plan['status'] == 'completed' else 1
        except (Exception, KeyboardInterrupt) as exc:
            if pair:
                pair.interrupt(safe_error(exc))
            execution.update(status='interrupted', error=safe_error(exc))
            return 1
        finally:
            execution.update(finished_at_utc=utc_now(), budget=budget.snapshot())
            if pair:
                execution.update(status=pair.plan['status'], pair_id=pair.pair_id)
            else:
                execution['startup_pair_artifacts'] = [str(p.relative_to(root)) for p in root.glob('*/pair.json')]
            write_json(root / 'study.json', execution)
            print(json.dumps(execution, indent=2))
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())

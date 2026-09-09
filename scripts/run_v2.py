#!/usr/bin/env python3
"""Offline v2 preflight, MOCK verification, saved reporting, or explicit paid opt-in."""
import argparse
import json
import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import dump, digest
from kiodai_v2.gateway import Accounting
from kiodai_v2.runner import run_case
from kiodai_v2.report import report
from research_harness.model_gateway import RunStopped, safe_error, utc_now
from sim import pm_bench as PM

ROOT = Path(__file__).resolve().parents[1]
FREEZE = ROOT/'research/v2/freeze.json'
LIVE_ROOT = ROOT/'results/v2/live-frozen-v2'


def protocol_files():
    paths = [ROOT/'configs/v2.json', ROOT/'scripts/run_v2.py', ROOT/'scripts/generate_v2_cases.py',
             ROOT/'scripts/freeze_v2.py', ROOT/'prompts/baseline_system.txt', ROOT/'prompts/prospective_memory_system.txt',
             ROOT/'sim/pm_bench.py', ROOT/'scripts/local_v2_smoke.py', ROOT/'scripts/v2_cooling_regression.py',
             ROOT/'scripts/serve_v2.py', ROOT/'scripts/estimate_v2_cost.py',
             ROOT/'research/v2/legacy_state.json', ROOT/'research/v2/cost_projection.json',
             ROOT/'research/v2/source_inventory.json']
    for directory, pattern in [('kiodai_v2','*.py'), ('prompts/v2','*.txt'), ('data/v2','*.json'),
                               ('research_harness','*.py'), ('tests','test_v2*.py')]:
        paths += list((ROOT/directory).glob(pattern))
    return sorted(set(paths))


def preflight(require_freeze=True):
    config = json.loads((ROOT/'configs/v2.json').read_text())
    catalog = json.loads((ROOT/'data/v2/catalog.json').read_text())['cases']
    for manifest_path in ('research/protected_hashes.json','research/pilot1_preservation_v1.json','research/followup_preservation_v1.json'):
        saved = json.loads((ROOT/manifest_path).read_text())
        if saved.get('archive') and digest((ROOT/saved['archive']).read_bytes()) != saved['archive_sha256']:
            raise RunStopped('Historical preservation archive changed')
        for name, expected in saved['files'].items():
            # Pilot-era shared METHOD/defense documents were legitimately updated by
            # the completed follow-up. Their original bytes remain in the pilot archive.
            if manifest_path.endswith('pilot1_preservation_v1.json') and not name.startswith('results/'):
                continue
            expected = expected['sha256'] if isinstance(expected,dict) else expected
            if digest((ROOT/name).read_bytes()) != expected:
                raise RunStopped('Preserved historical file changed: '+name)
    legacy = json.loads((ROOT/'research/v2/legacy_state.json').read_text())
    for name, record in legacy['files'].items():
        content = (ROOT/name).read_bytes()
        if record['policy'] == 'append_only':
            content = content[:record['bytes']]
        if digest(content) != record['sha256']:
            raise RunStopped('Historical baseline changed: '+name)
    if require_freeze:
        frozen = json.loads(FREEZE.read_text())
        actual = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in protocol_files()}
        if actual != frozen['hashes']:
            raise RunStopped('Frozen v2 implementation, prompts, scenarios or checks changed')
    steps = 0
    for case in catalog:
        scenario = json.loads((ROOT/case['path']).read_text())
        errors, warnings = PM.validate_scenario(scenario)
        if errors or warnings:
            raise RunStopped('Scenario validation: ' + str(errors or warnings))
        steps += sum(len(d['steps']) for d in scenario['days'])
    # Worst case at EVERY step, including a full corrective retry at every internal call.
    input_allowance = (config['max_request_bytes']+1024)*config['model']['pricing_usd_per_million_tokens']['input']/1e6
    out = config['output_tokens']; price = config['model']['pricing_usd_per_million_tokens']['output']/1e6
    per_step = {'A0': 4*(input_allowance+out['baseline']*price),
                'B_ledger': 2*(input_allowance+out['extract']*price)+4*(input_allowance+out['select']*price),
                'A2': 2*(input_allowance+out['extract']*price)+2*(input_allowance+out['select']*price)}
    allowance = steps * sum(per_step[m] for m in config['methods'])
    if allowance > config['cap_usd']:
        raise RunStopped('The frozen complete evaluation exceeds its proposed budget')
    return config, catalog, {'status': 'prepared_no_new_model_evidence', 'paid_inference': False,
        'trajectories': len(catalog), 'families': len(set(c['family'] for c in catalog)), 'steps_per_method': steps,
        'methods': config['methods'], 'repetitions': 1, 'maximum_attempts': steps*14,
        'conservative_allowance_usd': allowance, 'proposed_budget_usd': config['cap_usd'],
        'per_trajectory_reservation_usd': allowance/len(catalog),
        'preflight_model_calls': 0, 'route_metadata_requests_billable': False}


def execute(root, config, catalog, *, live=False, budget_usd=None):
    root = Path(root)
    root.mkdir(parents=True, exist_ok=False)  # refuses overwrite, repeated paid starts, or selective reruns
    mode = 'LIVE' if live else 'MOCK'
    study = {'mode': mode, 'status': 'starting', 'started_at_utc': utc_now(), 'methods': config['methods'],
             'runs': [], 'repeat': 1, 'exposure': 'same-process synthetic development; four template families',
             'no_pooling_with_historical_studies': True}
    dump(root/'study.json', study)
    dump(root/'config.json', config)
    if FREEZE.exists():
        (root/'freeze.json').write_bytes(FREEZE.read_bytes())
    accounting = None
    try:
        if live:
            from research_harness.live import verify_route
            from research_harness.model_gateway import OpenAICompatibleTransport
            accounting = Accounting(root/'accounting.sqlite', budget_usd, config)
            route = verify_route(config)
            dump(root/'route_preflight.json', route)
            transport = OpenAICompatibleTransport(os.environ['OPENROUTER_API_KEY'], config['model']['base_url'])
        study['status'] = 'running'
        for i, case in enumerate(catalog):
            methods = config['methods'][i % len(config['methods']):] + config['methods'][:i % len(config['methods'])]
            if accounting:
                # Reserve feasibility for the entire matched triple before its first call.
                steps = sum(len(d['steps']) for d in json.loads((ROOT/case['path']).read_text())['days'])
                required = steps*(4*accounting.bound(config['output_tokens']['baseline']) +
                                 4*accounting.bound(config['output_tokens']['extract']) +
                                 6*accounting.bound(config['output_tokens']['select']))
                if accounting.snapshot()['reserved_usd'] + required > budget_usd + 1e-10:
                    raise RunStopped('Insufficient cumulative allowance for complete matched trajectory')
            for method in methods:
                if not live:
                    from kiodai_v2.fixture import FixtureTransport
                    transport = FixtureTransport()
                name = Path(case['path']).stem + '/' + method
                study['runs'].append({'trajectory': Path(case['path']).stem, 'family': case['family'], 'folder': name, 'method': method})
                dump(root/'study.json', study)
                run_case(ROOT/case['path'], method, root/name, config, transport, mode, accounting)
                if accounting:
                    study['budget'] = accounting.snapshot()
                dump(root/'study.json', study)
        study['status'] = 'completed'
    except BaseException as exc:
        study.update(status='interrupted', blocker=safe_error(exc))
        raise
    finally:
        if accounting:
            study['budget'] = accounting.snapshot()
        study['finished_at_utc'] = utc_now()
        dump(root/'study.json', study)
        report(root)
    return root


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument('--preflight', action='store_true')
    modes.add_argument('--mock', action='store_true')
    modes.add_argument('--live', action='store_true')
    modes.add_argument('--report', type=Path)
    parser.add_argument('--output', type=Path, help='MOCK only; new path required')
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--budget-usd', type=float)
    args = parser.parse_args()
    if args.report:
        if args.env_file or args.budget_usd is not None or args.output:
            raise RunStopped('Saved reporting cannot enable inference')
        report(args.report)
        print(args.report/'report.md')
        return
    config, catalog, estimate = preflight()
    if not args.live and (args.env_file or args.budget_usd is not None):
        raise RunStopped('Credentials and budget flags require explicit --live')
    if args.live:
        if args.output:
            raise RunStopped('LIVE has one fixed study path; cannot reset spending via another output directory')
        if args.budget_usd != config['cap_usd']:
            raise RunStopped('Explicit frozen budget required: --budget-usd '+str(config['cap_usd']))
        if LIVE_ROOT.exists():
            raise RunStopped('This frozen live study already has an attempt. Preserve it; no fresh spending allowance or restart is permitted.')
        if args.env_file:
            from dotenv import dotenv_values
            key = dotenv_values(args.env_file, interpolate=False).get('OPENROUTER_API_KEY')
            if not key:
                raise RunStopped('No OPENROUTER_API_KEY in the specified local env file')
            os.environ['OPENROUTER_API_KEY'] = key
        if not os.environ.get('OPENROUTER_API_KEY'):
            raise RunStopped('Set OPENROUTER_API_KEY in untracked .env; pass --env-file .env. Never send the key in chat.')
        import certifi
        os.environ.setdefault('SSL_CERT_FILE', certifi.where())
        print(execute(LIVE_ROOT, config, catalog, live=True, budget_usd=args.budget_usd))
    elif args.mock:
        print(execute(args.output or ROOT/'results/v2/mock-verification-v2', config, catalog))
    else:
        print(json.dumps(estimate, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr)
        raise SystemExit(2)

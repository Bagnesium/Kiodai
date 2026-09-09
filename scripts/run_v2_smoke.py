#!/usr/bin/env python3
"""One authorized DeepSeek A2 development trajectory; reuses the frozen engine."""
import argparse
import json
import math
import os
import ssl
import subprocess
import sys
from pathlib import Path
from urllib.request import Request, urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.run_v2 import ROOT, FREEZE as FULL_FREEZE, preflight as full_preflight, protocol_files
from kiodai_v2.common import digest, dump
from kiodai_v2.gateway import Accounting
from kiodai_v2.runner import run_case
from kiodai_v2.report import report
from research_harness.live import verify_route, ENDPOINT_URL
from research_harness.model_gateway import OpenAICompatibleTransport, RunStopped, safe_error, utc_now

CONFIG = ROOT/'configs/v2_deepseek_smoke_v1.json'
FREEZE = ROOT/'research/v2/deepseek_smoke_v1_freeze.json'
LIVE_ROOT = ROOT/'results/v2/deepseek-smoke-v1'
SCENARIO = ROOT/'data/v2/v2_hidden_91320.json'


def smoke_files():
    return sorted(set(protocol_files() + [FULL_FREEZE, CONFIG, Path(__file__).resolve(),
        ROOT/'research/v2/deepseek_smoke_failure_audit.json',
        ROOT/'research/v2/deepseek_smoke_estimate.json',
        ROOT/'docs/v2/DEEPSEEK_SMOKE_PROTOCOL.md',
        ROOT/'tests/test_development_smoke.py']))


def preflight(check_freeze=True):
    original, _, full = full_preflight()
    config = json.loads(CONFIG.read_text())
    expected = {**original, 'version': 'v2.0-deepseek-smoke-v1', 'methods': ['A2'],
                'order': 'one complete v2_hidden_91320 A2 trajectory', 'cap_usd': 1.0}
    if config != expected:
        raise RunStopped('Smoke may change only study scope metadata and cap; frozen agent configuration required')
    scenario = json.loads(SCENARIO.read_text())
    checkpoints = sum(len(d['steps']) for d in scenario['days'])
    if checkpoints != 8:
        raise RunStopped('The intact smoke scenario must have eight checkpoints')
    # Same Accounting.bound formula, at the hard byte limit even for all later contexts.
    accounting = Accounting(':memory:', config['cap_usd'], config)
    extract = accounting.bound(config['output_tokens']['extract'])
    select = accounting.bound(config['output_tokens']['select'])
    accounting.db.close()
    required = checkpoints * (2 * extract + 2 * select)
    if required > config['cap_usd']:
        raise RunStopped('Complete smoke exceeds its cumulative authorization')
    hashes = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in smoke_files()}
    if check_freeze and hashes != json.loads(FREEZE.read_text())['hashes']:
        raise RunStopped('Smoke code, inputs, checks or protocol changed after freezing')
    return config, {'checkpoints': checkpoints, 'method': 'A2', 'repetitions': 1,
        'maximum_model_attempts': checkpoints * 4, 'maximum_tool_queries': checkpoints,
        'extract_attempt_allowance_usd': extract, 'select_attempt_allowance_usd': select,
        'conservative_allowance_usd': required, 'authorized_cap_usd': config['cap_usd'],
        'full_study_conservative_allowance_usd': full['conservative_allowance_usd'],
        'preflight_model_calls': 0, 'hashes': hashes}


def remote_preflight(config, required):
    """GET metadata only. Never persist a key, key label or authorization header."""
    import certifi
    ctx = ssl.create_default_context(cafile=certifi.where())
    with urlopen(ENDPOINT_URL, context=ctx, timeout=20) as response:
        route = verify_route(config, json.load(response))
    for endpoint in route['endpoints']:
        if 'structured_outputs' not in endpoint['supported_parameters']:
            raise RunStopped('Pinned endpoint does not advertise JSON-schema structured outputs')
    request = Request(config['model']['base_url'] + '/key',
                      headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY']})
    with urlopen(request, context=ctx, timeout=20) as response:
        data = json.load(response)['data']
    remaining = data.get('limit_remaining')
    if data.get('limit') is not None:
        if type(remaining) not in (int, float) or not math.isfinite(remaining) or remaining < required:
            raise RunStopped('Reported key allowance cannot cover the complete conservative smoke')
    return {'utc': utc_now(), 'credential_available': True, 'model_calls': 0,
        'metadata_requests_billable': False, 'route': route,
        'key_allowance': {k: data.get(k) for k in ('limit', 'limit_remaining', 'limit_reset', 'usage', 'is_free_tier', 'expires_at')},
        'account_credit_balance': None, 'independently_verified_billing': None,
        'structured_outputs_note': 'Advertised JSON-schema support is not a semantic guarantee; client validation remains enforced.'}


def execute(config, checks):
    # Fixed, exclusive directory is the one-shot gate, including failed preflight attempts.
    LIVE_ROOT.mkdir(parents=True, exist_ok=False)
    case = SCENARIO.stem
    study = {'mode': 'LIVE', 'status': 'starting', 'started_at_utc': utc_now(),
        'methods': ['A2'], 'planned_trajectories': 1, 'repeat': 1, 'runs': [],
        'purpose': 'one development integration smoke; no condition comparison',
        'exposure': 'existing synthetic hidden development case, previously inspected and tested locally',
        'no_pooling_with_historical_studies': True,
        'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()}
    dump(LIVE_ROOT/'study.json', study)
    dump(LIVE_ROOT/'config.json', config)
    dump(LIVE_ROOT/'preflight.json', checks)
    (LIVE_ROOT/'freeze.json').write_bytes(FREEZE.read_bytes())
    accounting = Accounting(LIVE_ROOT/'accounting.sqlite', config['cap_usd'], config)
    try:
        if accounting.snapshot()['reserved_usd'] + checks['conservative_allowance_usd'] > config['cap_usd']:
            raise RunStopped('Insufficient cumulative allowance for the complete A2 trajectory')
        remote = remote_preflight(config, checks['conservative_allowance_usd'])
        dump(LIVE_ROOT/'route_and_key_preflight.json', remote)
        transport = OpenAICompatibleTransport(os.environ['OPENROUTER_API_KEY'], config['model']['base_url'])
        study.update(status='running', runs=[{'folder': case+'/A2', 'method': 'A2', 'family': 'hidden', 'trajectory': case}])
        dump(LIVE_ROOT/'study.json', study)
        run_case(SCENARIO, 'A2', LIVE_ROOT/case/'A2', config, transport, 'LIVE', accounting)
        study['status'] = 'completed'
    except BaseException as exc:
        study.update(status='interrupted', blocker=safe_error(exc))
        raise
    finally:
        study.update(budget=accounting.snapshot(), finished_at_utc=utc_now())
        accounting.db.close()
        dump(LIVE_ROOT/'study.json', study)
        if study['runs'] and (LIVE_ROOT/study['runs'][0]['folder']/'manifest.json').exists():
            report(LIVE_ROOT)
    return LIVE_ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight', action='store_true')
    modes.add_argument('--live', action='store_true')
    parser.add_argument('--env-file', type=Path)
    parser.add_argument('--budget-usd', type=float)
    args = parser.parse_args()
    config, checks = preflight()
    if args.preflight:
        if args.env_file or args.budget_usd is not None:
            raise RunStopped('Offline preflight does not accept credentials or a live budget')
        print(json.dumps({k: v for k, v in checks.items() if k != 'hashes'}, indent=2))
        return
    if args.budget_usd != 1.0:
        raise RunStopped('This one authorized smoke requires --budget-usd 1.00')
    if LIVE_ROOT.exists():
        raise RunStopped('Smoke already has an attempt; no restart, new directory or fresh allowance')
    if args.env_file:
        from dotenv import dotenv_values
        key = dotenv_values(args.env_file, interpolate=False).get('OPENROUTER_API_KEY')
        if not key:
            raise RunStopped('OPENROUTER_API_KEY missing from the specified untracked env file')
        os.environ['OPENROUTER_API_KEY'] = key
    if not os.environ.get('OPENROUTER_API_KEY'):
        raise RunStopped('Set OPENROUTER_API_KEY in untracked .env and pass --env-file .env; never send it in chat')
    import certifi
    os.environ.setdefault('SSL_CERT_FILE', certifi.where())
    print(execute(config, checks))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr)
        raise SystemExit(2)

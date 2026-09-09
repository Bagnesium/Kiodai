#!/usr/bin/env python3
"""Offline v2.1 preflight or one freshly authorized A2 smoke; existing execution engine."""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest
from kiodai_v2.contract import EXTRACTION, VERSION
from kiodai_v2.gateway import Accounting
from research_harness.model_gateway import RunStopped, safe_error
from scripts.run_v2 import ROOT, preflight as historical_preservation
from scripts.run_v2_smoke import execute, SCENARIO
from scripts.verify_saved_smoke import verify, verify_sources, INVENTORY

CONFIG = ROOT/'configs/v21_deepseek_smoke_v1.json'
MANIFEST = ROOT/'research/v2_1/smoke_v1.json'
LIVE_ROOT = ROOT/'results/v2_1/deepseek-smoke-v1'
AUTHORIZATION = 'v2.1-deepseek-smoke-v1'


def implementation_files():
    paths = [CONFIG, SCENARIO, Path(__file__), ROOT/'scripts/run_v2_smoke.py',
             ROOT/'scripts/run_v2.py', ROOT/'scripts/verify_saved_smoke.py',
             ROOT/'scripts/verify_v21_offline.py', ROOT/'prompts/baseline_system.txt',
             ROOT/'sim/pm_bench.py', ROOT/'tests/test_saved_smoke_integrity.py',
             ROOT/'tests/test_development_smoke.py']
    for directory, pattern in [('kiodai_v2', '*.py'), ('research_harness', '*.py'),
                               ('prompts/v2_1', '*.txt'), ('tests', 'test_v2*.py'),
                               ('tests/fixtures', 'v21*.json')]:
        paths.extend((ROOT/directory).glob(pattern))
    return sorted(set(paths))


def preflight(check_manifest=True):
    original, _, _ = historical_preservation(require_freeze=False)
    config = json.loads(CONFIG.read_text())
    expected = {**original, 'version': AUTHORIZATION, 'methods': ['A2'],
                'order': 'one complete v2_hidden_91320 A2 trajectory', 'cap_usd': 1.0}
    if config != expected:
        raise RunStopped('Only version, scope and candidate cap may differ from the pinned v2 settings')
    saved = verify()
    execution_commit = json.loads((ROOT/INVENTORY).read_text())['execution_commit']
    sources = verify_sources(ROOT, execution_commit)
    scenario = json.loads(SCENARIO.read_text())
    archived = ROOT/'results/v2/deepseek-smoke-v1/v2_hidden_91320/A2/scenario.json'
    if scenario != json.loads(archived.read_text()):
        raise RunStopped('Smoke must preserve the complete historical scenario')
    checkpoints = sum(len(day['steps']) for day in scenario['days'])
    account = Accounting(':memory:', config['cap_usd'], config)
    try:
        allowance = checkpoints * 2 * sum(account.bound(config['output_tokens'][k]) for k in ('extract', 'select'))
    finally:
        account.db.close()
    if allowance > config['cap_usd']:
        raise RunStopped('Complete smoke exceeds candidate ceiling')
    hashes = {str(p.relative_to(ROOT)): digest(p.read_bytes()) for p in implementation_files()}
    schema_hash = digest(json.dumps(EXTRACTION, sort_keys=True).encode())
    if check_manifest:
        manifest = json.loads(MANIFEST.read_text())
        if manifest['hashes'] != hashes or manifest['extraction_schema_sha256'] != schema_hash:
            raise RunStopped('v2.1 source/schema/configuration differs from its smoke manifest')
        for name, expected_hash in hashes.items():
            content = subprocess.check_output(['git', 'show', f'{manifest["implementation_commit"]}:{name}'], cwd=ROOT)
            if digest(content) != expected_hash:
                raise RunStopped('Manifest source commit does not contain the prepared implementation')
        if manifest['output'] != str(LIVE_ROOT.relative_to(ROOT)) or manifest['configuration'] != config:
            raise RunStopped('Manifest scope/output/configuration mismatch')
    return config, {'status': 'prepared_requires_fresh_authorization', 'preflight_model_calls': 0,
        'contract_version': VERSION, 'checkpoints': checkpoints, 'method': 'A2', 'repetitions': 1,
        'maximum_model_attempts': checkpoints * 4, 'maximum_tool_queries': checkpoints,
        'conservative_allowance_usd': allowance, 'candidate_ceiling_usd': config['cap_usd'],
        'historical_archive_files': saved['archive_files'], 'historical_source_files': sources,
        'historical_source_commit': execution_commit, 'hashes': hashes,
        'extraction_schema_sha256': schema_hash}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight', action='store_true')
    modes.add_argument('--live', action='store_true')
    parser.add_argument('--authorize-new-smoke', choices=[AUTHORIZATION])
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--env-file', type=Path)
    args = parser.parse_args()
    if args.preflight and (args.authorize_new_smoke or args.budget_usd is not None or args.env_file):
        raise RunStopped('Offline preflight accepts no authorization, budget or credentials')
    if args.live and (args.authorize_new_smoke != AUTHORIZATION or args.budget_usd != 1.0):
        raise RunStopped('Fresh authorization requires --authorize-new-smoke v2.1-deepseek-smoke-v1 --budget-usd 1.00')
    config, checks = preflight()
    if args.preflight:
        print(json.dumps({k: v for k, v in checks.items() if k != 'hashes'}, indent=2))
        return
    if LIVE_ROOT.exists():
        raise RunStopped('This smoke already has an attempt; no restart or new allowance')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip():
        raise RunStopped('Commit intended changes and preserve unrelated edits before live execution')
    if args.env_file:
        from dotenv import dotenv_values
        key = dotenv_values(args.env_file, interpolate=False).get('OPENROUTER_API_KEY')
        if not key:
            raise RunStopped('No OPENROUTER_API_KEY in the specified untracked env file')
        os.environ['OPENROUTER_API_KEY'] = key
    if not os.environ.get('OPENROUTER_API_KEY'):
        raise RunStopped('Supply the key locally using --env-file .env; never send it in chat')
    import certifi
    os.environ.setdefault('SSL_CERT_FILE', certifi.where())
    print(execute(config, checks, live_root=LIVE_ROOT, scenario_path=SCENARIO, freeze_path=MANIFEST))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr)
        raise SystemExit(2)

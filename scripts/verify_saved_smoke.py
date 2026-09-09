#!/usr/bin/env python3
"""Read-only integrity, official-score and accounting checks for the saved smoke."""
import json
import argparse
import math
import sqlite3
import sys
import subprocess
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest, rows
from kiodai_v2.report import analyze_case

ROOT = Path(__file__).resolve().parents[1]
SMOKE = Path('results/v2/deepseek-smoke-v1')
INVENTORY = Path('research/v2/deepseek_smoke_artifact_inventory.json')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def inside(root, name, scope):
    path = (root/name).resolve()
    require(path.is_relative_to((root/scope).resolve()), 'Path outside evidence scope: '+name)
    return path


def verify_files(root):
    """Check existing files only; missing evidence is never silently restored."""
    root = Path(root).resolve()
    inventory = json.loads((root/INVENTORY).read_text())
    archive = inside(root, inventory['archive'], Path('artifacts/verification'))
    require(digest(archive.read_bytes()) == inventory['archive_sha256'], 'Archive hash mismatch')
    with zipfile.ZipFile(archive) as saved:
        names = saved.namelist()
        require(len(names) == len(set(names)), 'Duplicate archive members')
        require(set(names) == set(inventory['files']), 'Archive membership mismatch')
        for name, expected in inventory['files'].items():
            path = inside(root, name, SMOKE)
            require(digest(saved.read(name)) == expected, 'Archived evidence changed: '+name)
            require(path.is_file(), 'Missing evidence; use scripts/restore_deepseek_smoke.py: '+name)
            require(digest(path.read_bytes()) == expected, 'Local evidence changed: '+name)
    for name, expected in inventory['posthoc_files'].items():
        path = inside(root, name, Path('.'))
        require(digest(path.read_bytes()) == expected, 'Preserved post-hoc source changed: '+name)
    return inventory


def equal_number(actual, expected, message):
    require(type(actual) in (int, float) and type(expected) in (int, float)
            and math.isfinite(actual) and math.isfinite(expected)
            and math.isclose(actual, expected, rel_tol=0, abs_tol=1e-10), message)


def verify_sources(root, source_commit=None):
    """Verify frozen sources without requiring unrelated historical run directories."""
    root = Path(root).resolve()
    checked = set()
    for name in ('research/v2/freeze.json', 'research/v2/deepseek_smoke_v1_freeze.json'):
        content = (root/name).read_bytes()
        if source_commit is not None:
            original = subprocess.check_output(['git', 'show', f'{source_commit}:{name}'], cwd=root)
            require(content == original, 'Historical freeze itself changed: '+name)
        frozen = json.loads(content)
        for source, expected in frozen['hashes'].items():
            path = inside(root, source, Path('.'))
            content = path.read_bytes() if source_commit is None else subprocess.check_output(
                ['git', 'show', f'{source_commit}:{source}'], cwd=root)
            require(digest(content) == expected, 'Frozen source changed: '+source)
            checked.add(source)
    return len(checked)


def verify_accounting(root, case_folder):
    """Reconcile saved response costs, not independent provider billing."""
    root = Path(root)
    study = json.loads((root/'study.json').read_text())
    config = json.loads((root/'config.json').read_text())
    events = rows(case_folder/'calls.jsonl')
    requests = [r for r in events if r['event'] == 'request']
    responses = [r for r in events if r['event'] == 'response']
    identifiers = [r['reservation'] for r in requests]
    require(len(identifiers) == len(set(identifiers)), 'Duplicate request reservations')
    by_id = {r['reservation']: r for r in responses}
    require(len(by_id) == len(responses) == len(requests)
            and set(by_id) == set(identifiers), 'Requests and responses do not match')
    # Read-only immutable mode cannot create a journal or update this evidence file.
    uri = (root/'accounting.sqlite').resolve().as_uri() + '?mode=ro&immutable=1'
    connection = sqlite3.connect(uri, uri=True)
    try:
        ceilings = connection.execute('SELECT ceiling FROM account').fetchall()
        entries = connection.execute('SELECT id,reserved,reported,state FROM attempts ORDER BY id').fetchall()
    finally:
        connection.close()
    require(len(ceilings) == 1 and len(entries) == len(requests), 'Ledger cardinality mismatch')
    budget = study['budget']
    equal_number(ceilings[0][0], config['cap_usd'], 'Ledger/config ceiling mismatch')
    equal_number(ceilings[0][0], budget['ceiling_usd'], 'Ledger/study ceiling mismatch')
    prices = config['model']['pricing_usd_per_million_tokens']
    requests_by_id = {r['reservation']: r for r in requests}
    for identifier, reserved, reported, state in entries:
        require(identifier in requests_by_id, 'Unknown ledger reservation')
        request = requests_by_id[identifier]
        response = by_id[identifier]
        require(all(request[k] == response[k] for k in ('checkpoint', 'kind', 'attempt')),
                'Reservation attached to a different internal call')
        require(request['mode'] == response['mode'] == 'LIVE', 'Non-LIVE call in genuine smoke')
        require(response['reported_model'] == config['model']['model_id']
                and response['provider']['provider_reported'].lower() == config['model']['route'],
                'Saved response route mismatch')
        bound = ((config['max_request_bytes']+1024)*prices['input']
                 + request['request']['max_tokens']*prices['output'])/1e6
        equal_number(reserved, bound, 'Per-attempt reservation mismatch')
        equal_number(reported, response['provider']['cost_usd_reported'], 'Ledger/API cost mismatch')
        require(state == 'response_received' and 0 <= reported <= reserved, 'Unresolved or exceeded reservation')
    reserved = sum(e[1] for e in entries)
    reported = sum(e[2] for e in entries)
    require(reserved <= ceilings[0][0], 'Cumulative budget exceeded')
    equal_number(reserved, budget['reserved_usd'], 'Reserved subtotal mismatch')
    equal_number(reported, budget['api_response_cost_usd'], 'Reported cost total mismatch')
    equal_number(reported, budget['reported_subtotal_usd'], 'Reported subtotal mismatch')
    require(budget['attempts'] == len(requests) and budget['unknown_cost_attempts'] == 0,
            'Study accounting completeness mismatch')
    require(budget['verified_billed_cost_usd'] is None, 'Unsupported independently verified billing claim')
    return {'attempts': len(requests), 'reserved_usd': reserved,
            'api_response_cost_usd': reported, 'verified_billed_cost_usd': None}


def verify(root=ROOT):
    root = Path(root).resolve()
    inventory = verify_files(root)
    study_root = root/SMOKE
    study = json.loads((study_root/'study.json').read_text())
    require(study['mode'] == 'LIVE' and study['status'] == 'completed'
            and study['methods'] == ['A2'] and study['repeat'] == 1 and len(study['runs']) == 1,
            'Expected one complete A2-only live smoke')
    require(study['code_commit'] == inventory['execution_commit'], 'Execution commit mismatch')
    folder = inside(root, str(SMOKE/study['runs'][0]['folder']), SMOKE)
    actual = analyze_case(folder)  # Pure saved-artifact analysis; no report writer or gateway.
    saved = json.loads((study_root/'report.json').read_text())
    require(len(saved['cases']) == 1 and saved['matched_differences'] == [], 'Incorrect comparison scope')
    for name, value in actual.items():
        if name != 'path':  # Archival absolute paths may belong to another checkout.
            require(saved['cases'][0][name] == value, 'Saved report does not reproduce: '+name)
    accounting = verify_accounting(study_root, folder)
    equal_number(accounting['api_response_cost_usd'], inventory['api_response_cost_usd'], 'Inventory cost mismatch')
    return {'status': 'verified_without_writes_or_inference', 'archive_files': len(inventory['files']),
            'completed_checkpoints': actual['completed_steps'],
            'tp': actual['tp'], 'fp': actual['fp'], 'fn': actual['fn'],
            'set_f1': actual['set_f1'], **accounting}


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser(description=__doc__)
        parser.add_argument('--historical-sources', action='store_true',
                            help='Verify original code at the recorded execution commit, not current HEAD')
        args = parser.parse_args()
        commit = json.loads((ROOT/INVENTORY).read_text())['execution_commit'] if args.historical_sources else None
        source_count = verify_sources(ROOT, commit)
        print(json.dumps({**verify(), 'frozen_source_files': source_count,
                          'source_commit': commit or 'working tree'}, indent=2))
    except (ValueError, OSError, KeyError, sqlite3.Error, zipfile.BadZipFile) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(2)

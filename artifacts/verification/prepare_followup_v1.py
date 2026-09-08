"""Offline solvability/visibility witnesses and pilot-calibrated cost projection.

These are explicit software fixtures, never genuine model evidence. No key or
network is used. The witness reads only the request's legitimate visible text.
It is NOT installed in, or imported by, the live execution path.
"""
from pathlib import Path
from datetime import datetime, timezone
import copy
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from research_harness.analysis import rows, verify_run, score_artifacts
from research_harness.hashing import sha256_file
from research_harness.model_gateway import TransportResponse
from research_harness.paired import configs, estimate_pair
from research_harness.session import RunSession, write_json

OUT = ROOT / 'artifacts/verification/followup-v1'


class VisibleWitness:
    mode = 'MOCK'

    def __init__(self, query_hidden=True):
        self.query_hidden = query_hidden

    def invoke(self, request, timeout_seconds):
        users = [m['content'] for m in request['messages'] if m['role'] == 'user']
        step = next(s for s in reversed(users) if 'Step action menu:' in s)
        header = next(s for s in reversed(users) if s.startswith('=== '))
        history = '\n'.join(users)
        day = header.split('===')[1].strip()
        clock = re.findall(r'Time: (\d\d:\d\d)', step)[-1]
        menu = {text: handle for handle, text in re.findall(r'^- (task_\d+): (.+)$', step, re.M)}
        action = {'action': 'choose', 'choice': 'A', 'task_ids': [], 'channel': 'NONE'}
        if (day == 'Tuesday' and self.query_hidden and users[-1] == step
                and ('cooling is reported as nearly stable' in step or 'cooling process continues out of sight' in step)):
            action.update(action='query_state', choice='NONE', channel='sensor_board')
        else:
            selected = []
            if day == 'Monday':
                if 'The loading bell rings.' in step:
                    selected.append('Seal the copper case.')
                if clock == '09:40':
                    assert 'Log the room humidity at 09:40.' in history
                    selected.append('Log the room humidity.')
                if 'The requested blue hexagon appears' in step:
                    selected.append('Release the sample envelope.')
                if clock == '11:20':
                    assert 'later correction clearly replaces that time with 11:20' in history
                    selected += ['Inspect the pressure gauge.', 'Send the corrected status note.']
            elif day == 'Tuesday':
                if 'The safety chime sounds.' in step:
                    selected.append('Lock the test chamber.')
                if 'The chamber review window opens' in step:
                    assert 'The safety chime sounds.' in history
                    selected.append('Sign the chamber record.')
                if users[-1].startswith('State [sensor_board]:') and 'Cooling is now fully stable.' in users[-1]:
                    selected.append('Acknowledge stable cooling.')
                if 'The violet approval appears.' in step:
                    assert 'publish the manifest only when the violet approval appears' in history
                    selected.append('Publish the corrected manifest.')
                if clock == '16:00':
                    assert 'Call the calibration desk at 16:00.' in history
                    selected.append('Call the calibration desk.')
            elif day == 'Wednesday':
                if 'The east gate opens for visitors.' in step:
                    assert 'On Wednesday, Hang the visitor badge when the east gate opens.' in history
                    selected.append('Hang the visitor badge.')
                if 'The brass cabinet finally clicks' in step:
                    assert 'On Wednesday, File the blue archive card when the brass cabinet clicks.' in history
                    selected.append('File the blue archive card.')
            action['task_ids'] = [menu[text] for text in selected]
        raw = json.dumps(action, indent=4)  # matches pilot's observed presentation style
        return TransportResponse(raw, {'mock': True, 'fixture': 'visible-solvability-witness', 'content': raw},
                                 {}, 'mock/solvability-witness', {'network': False})


def run_fixture(cfg, name, query_hidden=True, scenario_path=None):
    folder = OUT / name
    folder.mkdir()
    cfg = copy.deepcopy(cfg)
    cfg['model']['provider'] = 'mock'
    cfg['execution']['allow_paid'] = False
    if scenario_path:
        cfg['scenario'] = str(scenario_path)
    path = folder / 'fixture-config.json'
    write_json(path, cfg)
    session = RunSession(path, output_root=folder, transport=VisibleWitness(query_hidden))
    while session.status == 'running':
        session.advance()
    assert session.status == 'completed', session.manifest.get('failure_records')
    verify_run(session.run_dir)
    return session


def request_bytes(request):
    request = copy.deepcopy(request)
    request['provider'] = 'openrouter'
    return len(json.dumps(request, ensure_ascii=False).encode())


def main():
    OUT.mkdir(parents=True, exist_ok=False)
    cfgs, _ = configs('development', None, 'LIVE')
    real = ROOT / 'results/kiodai/live-pair-42433e00474b'
    pilot = json.loads((real / 'pair.json').read_text())
    witnesses = {c: run_fixture(cfg, c + '-visible-witness') for c, cfg in cfgs.items()}
    estimates = {}
    for c, session in witnesses.items():
        assert session.manifest['aggregate_metrics']['set_tp'] == 12
        assert session.manifest['aggregate_metrics']['set_fp'] == session.manifest['aggregate_metrics']['set_fn'] == 0
        verify_run(real / pilot['runs'][c])
        pilot_calls = rows(real / pilot['runs'][c] / 'raw_model_calls.jsonl')
        ratio = sum(x['usage']['input_tokens'] for x in pilot_calls) / sum(request_bytes(x['request']) for x in pilot_calls)
        mean_output = sum(x['usage']['output_tokens'] for x in pilot_calls) / len(pilot_calls)
        calls = rows(session.run_dir / 'raw_model_calls.jsonl')
        input_tokens = sum(math.ceil(request_bytes(x['request']) * ratio) for x in calls)
        output_tokens = math.ceil(mean_output * len(calls))
        estimates[c] = {'pilot_tokens_per_serialized_request_byte': ratio, 'pilot_mean_output_tokens': mean_output,
                        'projected_calls': len(calls), 'projected_input_tokens': input_tokens,
                        'projected_output_tokens': output_tokens,
                        'uncached_list_price_estimate_usd': (input_tokens * .27 + output_tokens) / 1e6,
                        'request_growth_source': str(session.run_dir.relative_to(ROOT))}
    no_query = run_fixture(cfgs['A0'], 'A0-no-query-control', False)
    nq_score = no_query.manifest['aggregate_metrics']
    assert (nq_score['set_tp'], nq_score['set_fp'], nq_score['set_fn']) == (11, 0, 1)

    # Paired visibility check only: not a new evaluation scenario, never LIVE.
    counterfactual = json.loads((ROOT / cfgs['A0']['scenario']).read_text())
    step = next(s for s in counterfactual['days'][1]['steps'] if s['id'] == 'dev_t_s5')
    step['state_events']['sensor_board'] = [{'id': 'audit_only_cooling_not_stable', 'text': 'Cooling is still settling; stabilization is not complete.'}]
    cf_path = OUT / 'counterfactual-visibility-only.json'
    write_json(cf_path, counterfactual)
    cf_no_query = run_fixture(cfgs['A0'], 'A0-counterfactual-no-query', False, cf_path)
    assert [c['request'] for c in rows(no_query.run_dir / 'raw_model_calls.jsonl')] == [c['request'] for c in rows(cf_no_query.run_dir / 'raw_model_calls.jsonl')]
    cf_query = run_fixture(cfgs['A0'], 'A0-counterfactual-query', True, cf_path)
    original_calls = rows(witnesses['A0'].run_dir / 'raw_model_calls.jsonl')
    changed_calls = rows(cf_query.run_dir / 'raw_model_calls.jsonl')
    target = lambda calls, interaction: next(c for c in calls if c['call_context']['step_id'] == 'dev_t_s5' and c['call_context']['interaction_index'] == interaction)
    assert target(original_calls, 1)['request'] == target(changed_calls, 1)['request']
    assert target(original_calls, 2)['request'] != target(changed_calls, 2)['request']
    assert 'Cooling is now fully stable.' in target(original_calls, 2)['request']['messages'][-1]['content']

    audit = {'created_at_utc': datetime.now(timezone.utc).isoformat(), 'mode': 'OFFLINE_SOFTWARE_VALIDATION',
             'network_calls': 0, 'model_inference': False, 'scenario_file': cfgs['A0']['scenario'],
             'scenario_sha256': sha256_file(ROOT / cfgs['A0']['scenario']),
             'selection': 'Complete existing scenario chosen for coverage before any follow-up inference; no slicing or new evaluated cases.',
             'witnesses': {c: {'path': str(s.run_dir.relative_to(ROOT)), 'official_score': s.manifest['aggregate_metrics'],
                               'steps': s.total_steps, 'mode': 'MOCK'} for c, s in witnesses.items()},
             'no_query_control': {'path': str(no_query.run_dir.relative_to(ROOT)), 'tp': 11, 'fp': 0, 'fn': 1},
             'hidden_visibility': {'all_no_query_requests_identical_under_hidden_state_change': True,
                                   'pre_query_request_identical': True, 'permitted_query_reveals_changed_state': True,
                                   'positive_query_step': 'Tuesday/dev_t_s5',
                                   'counterfactual_is_evaluation_case': False,
                                   'limitation': 'Official scoring does not require a query; a lucky action can earn a hit. Report query-supported hidden hits separately from task hits.'},
             'usage_informed_estimate': {'conditions': estimates,
                 'total_usd': round(sum(e['uncached_list_price_estimate_usd'] for e in estimates.values()), 8),
                 'assumptions': 'Pilot-calibrated input-token/request-byte ratio by condition; fresh complete 20-step histories with two relevant queries per condition (44 calls total), no malformed responses/retries, mean 33.625 output tokens per call. No cache discount assumed. A projection, not new model evidence or a cap.'},
             'conservative_estimate': estimate_pair(cfgs),
             'proposed_explicit_budget_usd': .70,
             'fixtures_warning': 'Hand-authored visible-input software witness, not an autonomous model or performance measurement. Live runner never imports it.'}
    write_json(OUT / 'audit.json', audit)
    (OUT / 'README.md').write_text('# Offline follow-up validation only\n\nAll run traces here are MOCK software fixtures, not model-performance evidence. The counterfactual is only a visibility check and is not in the frozen evaluation. No key or network was used. See audit.json.\n')
    print(json.dumps({'usage_informed_estimate': audit['usage_informed_estimate'], 'conservative_estimate': audit['conservative_estimate'], 'hidden_visibility': audit['hidden_visibility']}, indent=2))


if __name__ == '__main__':
    main()

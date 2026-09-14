#!/usr/bin/env python3
"""Offline costing, exposure audit, full MOCK verification and comparison freeze."""
import argparse
import json
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest, dump, rows
from kiodai_v2.dashboard import Viewer
from research_harness.model_gateway import OpenAICompatibleTransport
from scripts import run_v21_comparison as study
from scripts.report_v21_comparison import analyze
from scripts.analyze_v21_smoke import analyze as verify_smokes

ROOT = study.ROOT
MOCK = ROOT/'results/v2_1/comparison-preparation-v1'
PRIOR_A0 = ROOT/'results/followup_v1/live-pair-bdf241965f35/live-A0-20260909T131935-b7f6531a/raw_model_calls.jsonl'
SMOKE = ROOT/'results/v2_1/deepseek-smoke-v1/v2_hidden_91320/A2/calls.jsonl'


def size(value):
    return len(json.dumps(value, ensure_ascii=False).encode())


def calibration():
    calls = rows(SMOKE)
    requests = [r for r in calls if r['event'] == 'request']
    responses = [r for r in calls if r['event'] == 'response']
    baseline = rows(PRIOR_A0)
    result = {}
    for kind in ('extract', 'select', 'baseline'):
        source_q = [r for r in requests if r['kind'] == kind] if kind != 'baseline' else baseline
        source_a = [r for r in responses if r['kind'] == kind] if kind != 'baseline' else baseline
        result[kind] = {
            'observed_calls': len(source_q),
            'input_tokens_per_request_byte': sum(r['usage']['input_tokens'] for r in source_a)/sum(size(r['request']) for r in source_q),
            'output_tokens_per_response_byte': sum(r['usage']['output_tokens'] for r in source_a)/sum(len(r['raw_text'].encode()) for r in source_a),
            'mean_observed_output_tokens': sum(r['usage']['output_tokens'] for r in source_a)/len(source_a)}
    return result


def estimate(root):
    spec = study.specification()
    config = spec['config']
    rates = calibration()
    prices = config['model']['pricing_usd_per_million_tokens']
    result = {'calibration': rates, 'assumptions': {
        'input_growth_margin': 1.35, 'output_growth_margin': 1.20,
        'expected_retry_rates_per_initial_call': {'extract': 0, 'select': 1/8, 'baseline': 0},
        'expected_query_policy': 'Actual full-study MOCK query frequency and own-history growth, separately per method/trajectory; not an assumption of identical histories.',
        'expected_outputs': 'Full MOCK response byte sizes times kind-specific observed token/byte ratio and 1.20 margin, bounded by unchanged output caps.',
        'retry_padding': 'Previous response allowance 8 bytes/output token plus 2048 feedback bytes. Requests above byte gate stop; capped sensitivity is financial planning, not a completion guarantee.',
        'sensitivity_queries': 'One query at every checkpoint for A0/B_ledger, plus one retry at every internal call; A2 still one selection cycle.',
        'extra_query_frame_bytes': 1280, 'cache_discount': 0,
        'limitations': 'Successful smoke calibrates ledger calls only; historical A0 calibrates baseline. B_ledger has no genuine v2.1 trajectory. Fixture language/ledger/query behavior and tokenizers may differ; no probabilistic expected-value guarantee.'},
        'methods': {}, 'by_trajectory': [], 'source_hashes': {
            str(SMOKE.relative_to(ROOT)): digest(SMOKE.read_bytes()),
            str(PRIOR_A0.relative_to(ROOT)): digest(PRIOR_A0.read_bytes())}}
    def cost(inp, out):
        return (inp*prices['input']+out*prices['output'])/1e6
    for block in spec['schedule']:
        for method in block['methods']:
            source = Path(root)/block['trajectory']/method/'calls.jsonl'
            calls = rows(source)
            initial = [r for r in calls if r['event'] == 'request' and r['attempt'] == 1]
            by_id = {r['request_id']: r for r in calls if r['event'] == 'response'}
            expected_in = expected_out = expected_calls = 0
            sensitivity_in = sensitivity_out = sensitivity_calls = 0
            oversize = 0
            for request in initial:
                kind = request['kind']; ratio = rates[kind]
                limit = config['output_tokens'][kind]
                request_bytes = size(request['request'])
                output = min(limit, len(by_id[request['request_id']]['raw_text'].encode())*
                             ratio['output_tokens_per_response_byte']*1.20)
                retry_bytes = request_bytes + 8*limit + 2048
                retry_input = min(retry_bytes, config['max_request_bytes'])*ratio['input_tokens_per_request_byte']*1.35
                retry_rate = result['assumptions']['expected_retry_rates_per_initial_call'][kind]
                expected_in += request_bytes*ratio['input_tokens_per_request_byte']*1.35 + retry_rate*retry_input
                expected_out += output + retry_rate*output
                expected_calls += 1+retry_rate
                sensitivity_in += request_bytes*ratio['input_tokens_per_request_byte']*1.35 + retry_input
                sensitivity_out += 2*limit
                sensitivity_calls += 2
                oversize += retry_bytes > config['max_request_bytes']
            if method != 'A2':
                for checkpoint in range(1, block['checkpoint_count']+1):
                    decisions = [r for r in initial if r['checkpoint'] == checkpoint and r['kind'] != 'extract']
                    if len(decisions) == 1:
                        request = decisions[0]; kind = request['kind']; limit = config['output_tokens'][kind]
                        ratio = rates[kind]['input_tokens_per_request_byte']
                        query_bytes = size(request['request'])+1280
                        retry_bytes = query_bytes+8*limit+2048
                        sensitivity_in += (min(query_bytes,48000)+min(retry_bytes,48000))*ratio*1.35
                        sensitivity_out += 2*limit; sensitivity_calls += 2
                        oversize += retry_bytes > 48000
            row = {'trajectory': block['trajectory'], 'family': block['family'], 'method': method,
                   'mock_initial_calls': len(initial), 'expected_calls_including_retry_fraction': expected_calls,
                   'expected_input_tokens': expected_in, 'expected_output_tokens': expected_out,
                   'usage_informed_expected_usd': cost(expected_in, expected_out),
                   'retry_heavy_attempts': sensitivity_calls,
                   'retry_heavy_usd': cost(sensitivity_in,sensitivity_out),
                   'padded_sensitivity_requests_above_byte_gate': oversize}
            result['by_trajectory'].append(row)
            result['source_hashes'][str(source.relative_to(ROOT))] = digest(source.read_bytes())
    for method in spec['methods']:
        selected = [r for r in result['by_trajectory'] if r['method'] == method]
        result['methods'][method] = {key: sum(r[key] for r in selected) for key in
            ('mock_initial_calls','expected_calls_including_retry_fraction','expected_input_tokens',
             'expected_output_tokens','usage_informed_expected_usd','retry_heavy_attempts','retry_heavy_usd',
             'padded_sensitivity_requests_above_byte_gate')}
        result['methods'][method]['conservative_allowance_usd'] = spec['budget_guard']['by_method'][method]
    result['usage_informed_expected_usd'] = sum(r['usage_informed_expected_usd'] for r in result['methods'].values())
    result['retry_heavy_usd'] = sum(r['retry_heavy_usd'] for r in result['methods'].values())
    result['conservative_allowance_usd'] = spec['budget_guard']['complete_study_allowance_usd']
    result['recommended_authorization_usd'] = config['cap_usd']
    return result


def exposure():
    sources = [ROOT/'results/v2/development/initial-mechanics/study.json',
               ROOT/'results/v2/development/verified-mechanics/study.json',
               ROOT/'results/v2/mock-verification-v2/study.json',
               ROOT/'results/v2/local-smoke-v2/study.json',
               ROOT/'results/v2/deepseek-smoke-v1/study.json',
               ROOT/'results/v2_1/offline-repair-v1/study.json',
               ROOT/'results/v2_1/deepseek-smoke-v1/study.json']
    records = []
    for block in study.specification()['schedule']:
        overlaps = []
        for source in sources:
            saved = study.read(source)
            runs = [r for r in saved['runs'] if r['trajectory'] == block['trajectory']]
            if runs:
                for run in runs:
                    scenario = source.parent/run['folder']/'scenario.json'
                    if digest(scenario.read_bytes()) != block['scenario_sha256']:
                        raise ValueError('Historical scenario with same identifier differs: '+str(scenario))
                overlaps.append({'study': str(source.relative_to(ROOT)), 'mode': saved['mode'],
                    'status': saved['status'], 'methods': [r['method'] for r in runs], 'same_scenario_bytes': True})
        records.append({'trajectory': block['trajectory'], 'family': block['family'],
                        'implementation_development': True, 'independently_held_out': False, 'overlaps': overlaps})
    return {'trajectories': records, 'source_hashes': {str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in sources},
            'interpretation': 'All 12 were authored/inspected and used in MOCK development. Hidden 91320 additionally appears in both network smokes and interrupted local-model smoke. Remaining 11 are still exposed; four templates, not 12 independent families.'}


def verify_mock(root):
    root = Path(root)
    report = analyze(root)
    if report['mode'] != 'MOCK' or report['status'] != 'completed' or len(report['cases']) != 36:
        raise ValueError('Expected full 36-method-trajectory MOCK study')
    expected_runs = [(b['trajectory'], m) for b in study.specification()['schedule'] for m in b['methods']]
    actual_runs = [(r['trajectory'],r['method']) for r in study.read(root/'study.json')['runs']]
    if actual_runs != expected_runs:
        raise ValueError('Executor did not follow frozen balanced order')
    request_count = response_count = queries = checkpoints = 0
    for case in report['cases']:
        folder = root/case['trajectory']/case['method']
        if not case['primary_usable']:
            raise ValueError('MOCK case incomplete')
        checkpoints += case['completed_steps']; queries += case['tool_queries']
        calls = rows(folder/'calls.jsonl')
        requests = [r for r in calls if r['event']=='request']; responses = [r for r in calls if r['event']=='response']
        request_count += len(requests); response_count += len(responses)
        if len(requests) != len(responses) or any(q['request_id'] != a['request_id'] for q,a in zip(requests,responses)):
            raise ValueError('MOCK request accounting mismatch')
        frames = rows(folder/'agent.jsonl')
        if len(frames[0]['frame']['messages']) != 3 or frames[0]['frame']['receipts']:
            raise ValueError('History/receipt state was not reset')
        if case['method'] == 'A0':
            if any(r['kind']=='extract' for r in requests): raise ValueError('Baseline unexpectedly extracted')
            if study.read(folder/'memory.json'): raise ValueError('Baseline unexpectedly acquired intentions')
        else:
            payload = json.loads(requests[0]['request']['messages'][1]['content'])
            if payload['intentions']: raise ValueError('Ledger not reset')
            for request in requests:
                if request['kind']=='extract':
                    if request['request']['messages'][0]['content'] != (ROOT/'prompts/v2_1/extract.txt').read_text():
                        raise ValueError('Stale extraction prompt')
                    if request['request']['response_format']['json_schema']['schema'] != study.EXTRACTION:
                        raise ValueError('Stale extraction schema')
                elif not request['request']['messages'][0]['content'].endswith((ROOT/'prompts/v2_1/select.txt').read_text()):
                    raise ValueError('Stale selection prompt')
        for request in requests:
            serialized = json.dumps(request['request'])
            if any(marker in serialized for marker in ('groundtruth','due_task_ids','private_913','private_step_')):
                raise ValueError('Evaluator identifier/metadata leaked')
            if request['mode'] != 'MOCK': raise ValueError('Mislabelled fixture')
        for frame in frames:
            if any(o['checkpoint'] > frame['checkpoint'] for o in frame['frame']['observations'].values()):
                raise ValueError('Future observation leaked')
        if case['api_response_cost_usd'] is not None or case['input_tokens'] is not None:
            raise ValueError('MOCK imputed a real resource metric')
        for step in rows(folder/'steps.jsonl'):
            if len(step['tools']) > 1 or step['action']['heartbeat_enabled']:
                raise ValueError('Unequal extra checkpoint/query opportunity')
        viewer = Viewer(root)
        if viewer.catalog()['mode'] != 'MOCK' or viewer.inspect(case['trajectory'],case['method'],0)['inference_enabled']:
            raise ValueError('Incorrect MOCK replay boundary')
    return {'mode':'MOCK','purpose':'Software verification only; fixture unchanged, no model inference.',
        'method_trajectories':36, 'checkpoints':checkpoints, 'mock_requests':request_count,
        'mock_responses':response_count, 'tool_queries':queries,
        'all_current_candidate_hashes_match': all(
            digest((ROOT/p).read_bytes()) == h for p,h in study.read(ROOT/'research/v2_1/smoke_v1.json')['hashes'].items()),
        'balanced_order_verified':True,'shared_v21_prompts_schemas_verified':True,
        'isolated_state_and_public_payloads_verified':True, 'model_inference_calls':0,
        'api_response_cost_usd':None,'semantic_correctness':'Not established by fixture outcomes'}


def freeze(root=MOCK):
    verification = verify_mock(root)
    verify_smokes()
    spec = study.specification()
    if study.read(Path(root)/'comparison_specification.json') != spec:
        raise ValueError('Verified design differs from final specification')
    commit = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    hashes = study.source_hashes()
    for name, expected in hashes.items():
        if digest(subprocess.check_output(['git','show',commit+':'+name],cwd=ROOT)) != expected:
            raise ValueError('Commit intended support files before freezing: '+name)
    budget = estimate(root)
    history = exposure()
    inventory_path = ROOT/'research/v2_1/live_smoke_v1_inventory.json'
    inventory = study.read(inventory_path)
    frozen = {'status':'prepared_not_authorized_not_executed', 'support_commit':commit,
        'specification':spec,'hashes':hashes,'budget':budget,'exposure_audit':history,
        'provenance_evidence_hashes': {**budget['source_hashes'], **history['source_hashes'], **inventory['files'],
            str(inventory_path.relative_to(ROOT)):digest(inventory_path.read_bytes()),
            inventory['archive']:inventory['archive_sha256']},
        'offline_verification':verification,
        'preparation_evidence_hashes':{str(p.relative_to(ROOT)):digest(p.read_bytes())
            for p in sorted(Path(root).rglob('*')) if p.is_file()},
        'preflight_command':'python3 scripts/run_v21_comparison.py --preflight',
        'proposed_live_command':'python3 scripts/run_v21_comparison.py --live --authorize-study v2.1-comparison-v1 --budget-usd 20.00 --env-file .env',
        'authorization_message':'I authorize exactly v2.1-comparison-v1 once, with a cumulative paid-inference ceiling of $20.00, following its frozen 12-trajectory A0/B_ledger/A2 protocol. Run the existing preflight first. No prompt or configuration changes, selective reruns, or additional experiments afterward. Preserve all outputs and interrupted attempts.'}
    if study.MANIFEST.exists():
        raise ValueError('Comparison manifest already exists; do not silently overwrite a freeze')
    dump(study.MANIFEST,frozen)
    return frozen


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-mock', action='store_true')
    parser.add_argument('--freeze', action='store_true')
    args=parser.parse_args()
    if args.freeze:
        print(json.dumps(freeze()['budget']['methods'],indent=2))
    elif args.verify_mock:
        print(json.dumps(verify_mock(MOCK),indent=2))
    else:
        raise SystemExit('Choose --verify-mock or --freeze; no inference mode exists here')

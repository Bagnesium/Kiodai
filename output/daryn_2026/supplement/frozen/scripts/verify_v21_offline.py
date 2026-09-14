#!/usr/bin/env python3
"""MOCK-only full-pipeline check and usage-informed planning; never invokes a model."""
import argparse
import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest, dump, rows
from kiodai_v2.fixture import FixtureTransport
from kiodai_v2.runner import run_case, verify_case
from kiodai_v2.report import analyze_case
from research_harness.model_gateway import OpenAICompatibleTransport
from scripts.run_v21_smoke import ROOT, CONFIG, SCENARIO


def estimate(folder, config):
    source = ROOT/'results/v2/deepseek-smoke-v1/v2_hidden_91320/A2/calls.jsonl'
    old = rows(source)
    old_requests = [r for r in old if r['event'] == 'request']
    old_responses = [r for r in old if r['event'] == 'response']
    ratio = sum(r['usage']['input_tokens'] for r in old_responses) / sum(
        len(json.dumps(r['request'], ensure_ascii=False).encode()) for r in old_requests)
    requests = [r for r in rows(folder/'calls.jsonl') if r['event'] == 'request']
    # Full populated-ledger/history request sizes; no truncation, no cache discounts.
    input_tokens = sum(len(json.dumps(r['request'], ensure_ascii=False).encode()) for r in requests) * ratio * 1.35
    output_tokens = sum(750 if r['kind'] == 'extract' else 256 for r in requests)
    prices = config['model']['pricing_usd_per_million_tokens']
    cost = (input_tokens * prices['input'] + output_tokens * prices['output']) / 1e6
    # Sensitivity: one retry at every call, including a maximal prior response in history.
    retry_bytes = sum(len(json.dumps(r['request'], ensure_ascii=False).encode()) +
                      8 * config['output_tokens'][r['kind']] + 2048 for r in requests)
    retry_input = retry_bytes * ratio * 1.35
    retry_output = sum(config['output_tokens'][r['kind']] for r in requests)
    return {'usage_informed_projection_usd': cost, 'projected_calls_without_retries': len(requests),
            'projected_input_tokens': round(input_tokens), 'projected_output_tokens': output_tokens,
            'all_calls_retry_sensitivity_usd': cost + (retry_input * prices['input'] + retry_output * prices['output']) / 1e6,
            'maximum_actual_mock_request_bytes': max(len(json.dumps(r['request'], ensure_ascii=False).encode()) for r in requests),
            'input_token_per_request_byte_ratio': ratio, 'input_growth_margin': 1.35,
            'output_assumptions': {'extract': 750, 'select': 256},
            'retry_sensitivity_assumptions': {'extra_attempts_per_call': 1, 'previous_output_bytes_per_token': 8,
                                             'feedback_framing_bytes': 2048, 'retry_output': config['output_tokens']},
            'sources': {str(source.relative_to(ROOT)): digest(source.read_bytes()),
                        str(folder/'calls.jsonl'): digest((folder/'calls.jsonl').read_bytes())},
            'caveat': 'Planning only. Token/byte ratio comes from the failed live smoke; populated-ledger sizes come from a restricted-language mock. No live extraction improvement or tokenizer upper bound is inferred.'}


def verify(output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=False)
    config = json.loads(CONFIG.read_text())
    with patch.object(OpenAICompatibleTransport, 'invoke', side_effect=AssertionError('No inference permitted')):
        folder = run_case(SCENARIO, 'A2', output/'v2_hidden_91320/A2', config, FixtureTransport(), 'MOCK')
    manifest = verify_case(folder)
    result = analyze_case(folder)
    steps = rows(folder/'steps.jsonl')
    calls = rows(folder/'calls.jsonl')
    responses = [r for r in calls if r['event'] == 'response']
    requests = [r for r in calls if r['event'] == 'request']
    assert manifest['completed_steps'] == 8 and result['invalid_responses'] == 0
    assert 'not complete' in steps[0]['tools'][0]['observation']
    assert steps[0]['action']['selected_handles_validated'] == []
    assert 'fully stable' in steps[6]['tools'][0]['observation']
    assert all(r['status'] == 'completed' for r in json.loads((folder/'memory.json').read_text()).values())
    assert len(requests) == len(responses) == len({r['request_id'] for r in requests})
    assert all(q['request_id'] == a['request_id'] for q, a in zip(requests, responses))
    summary = {'mode': 'MOCK', 'new_model_inference': False,
               'purpose': 'Full-pipeline mechanics only; fixture knows the authored public grammar.',
               'checkpoints': 8, 'model_requests': len(requests), 'tool_queries': result['tool_queries'],
               'accepted_operations_responses': sum(r['outcome'] == 'accepted_operations' for r in responses),
               'accepted_empty_updates': sum(r['outcome'] == 'accepted_empty_update' for r in responses),
               'validation_failures': sum(bool(r['validation_error']) for r in responses),
               'completed_intentions': len(json.loads((folder/'memory.json').read_text())),
               'official_mock_score': {k: result[k] for k in ('tp', 'fp', 'fn', 'set_f1')},
               'usage_projection': estimate(folder, config)}
    dump(output/'verification.json', summary)
    dump(output/'study.json', {'mode': 'MOCK', 'status': 'completed', 'methods': ['A2'],
         'planned_trajectories': 1, 'repeat': 1, 'runs': [{'folder': 'v2_hidden_91320/A2',
         'method': 'A2', 'family': 'hidden', 'trajectory': 'v2_hidden_91320'}]})
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True, help='New MOCK artifact directory; refuses overwrite')
    args = parser.parse_args()
    print(json.dumps(verify(args.output), indent=2))

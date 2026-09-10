#!/usr/bin/env python3
"""Frozen v2.1 study scope around the unchanged v2 executor; offline by default."""
import argparse
import json
import os
import random
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest, dump
from kiodai_v2.contract import EXTRACTION
from kiodai_v2.agent import BINDING
from kiodai_v2.gateway import Accounting
from research_harness.model_gateway import RunStopped, action_schema, safe_error
from research_harness.runner import render_prompt
from sim import pm_bench as PM
from scripts import run_v2 as executor
from scripts.run_v21_smoke import preflight as smoke_preflight

ROOT = Path(__file__).resolve().parents[1]
IDENTIFIER = 'v2.1-comparison-v1'
SEED = 20260910
CANDIDATE_COMMIT = '959db38dac8b68f63ecf79420dcd53bea2278cf2'
CONFIG = ROOT/'configs/v21_comparison_v1.json'
MANIFEST = ROOT/'research/v2_1/comparison_v1.json'
LIVE_ROOT = ROOT/'results/v2_1/comparison-v1'
ORDER = 'seed 20260910: shuffled family blocks and within-family variants; cyclic method order'


def read(path):
    return json.loads(Path(path).read_text())


def normalized_hash(value):
    return digest(json.dumps(value, sort_keys=True).encode())


def design():
    rng = random.Random(SEED)
    methods = ['A0', 'B_ledger', 'A2']
    rng.shuffle(methods)
    original = read(ROOT/'data/v2/catalog.json')['cases']
    families = list(dict.fromkeys(c['family'] for c in original))
    if len(original) != 12 or len(families) != 4 or any(
            sum(c['family'] == f for c in original) != 3 for f in families):
        raise RunStopped('Expected all 12 existing trajectories, three per each of four families')
    rng.shuffle(families)
    catalog = []
    for family in families:
        variants = [c for c in original if c['family'] == family]
        rng.shuffle(variants)
        catalog.extend(variants)
    config = read(CONFIG)
    expected = {**read(ROOT/'configs/v2.json'), 'version': IDENTIFIER, 'methods': methods,
                'order': ORDER, 'cap_usd': 20.0}
    if config != expected:
        raise RunStopped('Comparison changes only version and predeclared ordering from pinned settings')
    return config, catalog


def specification():
    config, catalog = design()
    account = Accounting(':memory:', config['cap_usd'], config)
    by_method = {'A0': {}, 'B_ledger': {}, 'A2': {}}
    schedule = []
    try:
        for index, case in enumerate(catalog):
            scenario = read(ROOT/case['path'])
            count = sum(len(d['steps']) for d in scenario['days'])
            methods = config['methods'][index % 3:] + config['methods'][:index % 3]
            prompt, _ = render_prompt(ROOT/'prompts/baseline_system.txt', None,
                                      PM.list_state_channels(scenario), False)
            bounds = {
                'A0': count * 4 * account.bound(config['output_tokens']['baseline']),
                'B_ledger': count * (2 * account.bound(config['output_tokens']['extract']) +
                                    4 * account.bound(config['output_tokens']['select'])),
                'A2': count * (2 * account.bound(config['output_tokens']['extract']) +
                              2 * account.bound(config['output_tokens']['select'])),
            }
            for method, bound in bounds.items():
                by_method[method][Path(case['path']).stem] = bound
            schedule.append({**case, 'trajectory': Path(case['path']).stem, 'checkpoint_count': count,
                'days': len(scenario['days']), 'instructed_obligations': sum(len(d['tasks']) for d in scenario['days']),
                'scenario_sha256': digest((ROOT/case['path']).read_bytes()), 'methods': methods,
                'rendered_baseline_system_prompt_sha256': digest(prompt.encode()),
                'rendered_ledger_selection_system_prompt_sha256': digest(
                    (prompt+'\n'+(ROOT/'prompts/v2_1/select.txt').read_text()).encode()),
                'prior_network_smoke': Path(case['path']).stem == 'v2_hidden_91320',
                'block_conservative_allowance_usd': sum(bounds.values())})
    finally:
        account.db.close()
    total_steps = sum(s['checkpoint_count'] for s in schedule)
    return {'identifier': IDENTIFIER, 'candidate_implementation_commit': CANDIDATE_COMMIT,
        'config': config, 'order_seed': SEED, 'schedule': schedule, 'methods': ['A0', 'B_ledger', 'A2'],
        'primary_contrast': 'A2 minus B_ledger', 'secondary_contrast': 'A2 minus A0',
        'trajectories': 12, 'families': 4, 'repetitions': 1, 'method_trajectories': 36,
        'checkpoints_per_method': total_steps, 'total_checkpoints': 3*total_steps,
        'maximum_model_attempts': 14*total_steps, 'maximum_queries': 3*total_steps,
        'budget_guard': {'by_method_and_trajectory': by_method,
            'by_method': {m: sum(v.values()) for m, v in by_method.items()},
            'complete_study_allowance_usd': sum(sum(v.values()) for v in by_method.values()),
            'recommended_authorization_usd': config['cap_usd'],
            'policy': 'Preflight requires the full conservative allowance. Executor checks feasibility for each matched block, then durably reserves each attempt. Reservations are never refunded; no resume or restart is supported.'},
        'prompt_schema_policy': {
            'A0': 'Original rendered baseline system prompt and action_schema, no explicit intention extraction; baseline output cap 256.',
            'B_ledger_and_A2': 'Same Agent, Store, Gateway, extract/select prompt files and extraction schema; only monitoring/query policy differs.',
            'extraction_schema_sha256': normalized_hash(EXTRACTION),
            'binding_template_sha256': normalized_hash(BINDING),
            'action_schema_empty_interface_sha256': normalized_hash(action_schema((), ())),
            'dynamic_schemas': 'Allowed handle/channel enums and eligible ledger ID/version constraints derive from each method own current public frame. Every exact request schema is logged.',
            'full_history': 'Shared initial instructions and checkpoint schedule; complete own history with receipts. Later observations diverge legitimately. No cross-run sharing. Unchanged 65536 runtime context limit and 48000 serialized request-byte gate, no truncation.',
            'not_compute_matched': 'A0 256 output tokens; ledger selection 1536 and extraction 3072. A0/B_ledger may need an extra selection after a query; count all calls.',
            'tools': 'Same available channels/actions and one query per checkpoint; heartbeat off; no between-checkpoint A2 opportunities.'},
        'analysis_policy': {
            'headline': 'Arithmetic mean of the 12 per-trajectory A2 minus B_ledger Set-F1 differences; require all declared pairs and completed study, otherwise null. A2 minus A0 separately.',
            'secondary_tables': 'Every declared method-trajectory; each template family; previous network-smoke case versus other 11 exposed cases; descriptive micro TP/FP/FN totals and rates.',
            'missing': 'Unstarted/interrupted/unusable units remain present with null primary metrics. Completed-pair diagnostics labeled separately; no imputation, selective exclusions or reruns.',
            'semantic': 'Separate manual-review queue for both ledger methods: required fields/prerequisites, triggers, bindings, unsupported intentions, quarantine and repairing revisions; timing relative to recorded first due. A0 not applicable. Pending review is not zero errors.',
            'hidden': 'Relevant same-checkpoint query-supported hits, other visible-supported hits, unsupported-evidence hits, misses and false actions. Query counts and necessity review; no immediate hit does not prove an unnecessary query.',
            'dependencies': 'Unique instructed, ever-due, dependency-blocked at a trigger opportunity, unfinished and canceled obligations, alongside unchanged official scores.',
            'units': '12 matched blocks from four dependent template families; checkpoints/calls/renamed variants are not independent replications. No significance, superiority, equivalence or held-out claim from preparation.'},
        'output': str(LIVE_ROOT.relative_to(ROOT)), 'exposure': 'All 12 are exposed synthetic development cases; no held-out benchmark.',
        'interruption_policy': 'Any transport or runner interruption stops the entire study; preserve partial output and reservations. Validation uses existing one retry, then recorded fail-closed action. No supported resume; a fresh path cannot be supplied to LIVE.',
        'new_model_inference_authorized': False}


def source_hashes():
    # No additions inside candidate module directories or historical freeze globs.
    paths = set(read(ROOT/'research/v2_1/smoke_v1.json')['hashes'])
    paths.update(c['path'] for c in read(ROOT/'data/v2/catalog.json')['cases'])
    paths.update(['data/v2/catalog.json', 'configs/v2.json', 'configs/v21_comparison_v1.json',
                  'scripts/run_v21_comparison.py', 'scripts/report_v21_comparison.py',
                  'scripts/prepare_v21_comparison.py', 'scripts/analyze_v21_smoke.py',
                  'tests/test_comparison_preparation.py'])
    return {name: digest((ROOT/name).read_bytes()) for name in sorted(paths)}


def preflight(require_manifest=True):
    _, smoke = smoke_preflight()  # offline, verifies candidate and historical preservation
    spec = specification()
    if spec['budget_guard']['complete_study_allowance_usd'] > spec['config']['cap_usd']:
        raise RunStopped('Complete study exceeds the frozen candidate ceiling')
    if require_manifest:
        frozen = read(MANIFEST)
        if frozen['specification'] != spec or frozen['hashes'] != source_hashes():
            raise RunStopped('Comparison specification or source hashes changed')
        for name, expected in frozen['hashes'].items():
            content = subprocess.check_output(['git', 'show', frozen['support_commit']+':'+name], cwd=ROOT)
            if digest(content) != expected:
                raise RunStopped('Frozen support commit mismatch: '+name)
        for name, expected in {**frozen['preparation_evidence_hashes'], **frozen['provenance_evidence_hashes']}.items():
            if digest((ROOT/name).read_bytes()) != expected:
                raise RunStopped('Preparation evidence changed: '+name)
    return spec, {'status': 'prepared_requires_fresh_authorization', 'preflight_model_calls': 0,
                  'preflight_network_requests': 0, 'candidate_frozen_files': len(smoke['hashes']),
                  'checkpoints': spec['total_checkpoints'], 'method_trajectories': 36,
                  'conservative_allowance_usd': spec['budget_guard']['complete_study_allowance_usd']}


def execute(output, *, live=False, require_manifest=True):
    if live and not require_manifest:
        raise RunStopped('LIVE cannot bypass the comparison manifest')
    spec, checks = preflight(require_manifest)
    output = Path(output).resolve()
    if live and output != LIVE_ROOT.resolve():
        raise RunStopped('LIVE only permits the frozen output path')
    if not live and output == LIVE_ROOT.resolve():
        raise RunStopped('MOCK cannot occupy the genuine study path')
    if output.exists():
        raise RunStopped('This study already has an attempt; no overwrite or restart')
    config, catalog = design()
    provenance = {'code_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
                  'source_hashes': source_hashes(), 'candidate_commit': CANDIDATE_COMMIT,
                  'mode': 'LIVE' if live else 'MOCK', 'verification_before_final_manifest': not require_manifest}
    prior_freeze = executor.FREEZE
    # Existing execute exposes its manifest location as a module constant. Rebind
    # only this metadata input, then restore it; do not replace any run/agent logic.
    executor.FREEZE = MANIFEST if require_manifest else ROOT/'research/v2_1/not-yet-frozen.json'
    try:
        return executor.execute(output, config, catalog, live=live,
                                budget_usd=config['cap_usd'] if live else None)
    finally:
        executor.FREEZE = prior_freeze
        if output.exists():
            dump(output/'comparison_specification.json', spec)
            dump(output/'comparison_preflight.json', checks)
            dump(output/'execution_provenance.json', provenance)
            if (output/'study.json').exists():
                from scripts.report_v21_comparison import write_report
                write_report(output)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument('--preflight', action='store_true')
    modes.add_argument('--mock', action='store_true')
    modes.add_argument('--live', action='store_true')
    parser.add_argument('--output', type=Path, help='MOCK only, fresh directory')
    parser.add_argument('--authorize-study', choices=[IDENTIFIER])
    parser.add_argument('--budget-usd', type=float)
    parser.add_argument('--env-file', type=Path)
    args = parser.parse_args()
    if not args.live and (args.authorize_study or args.budget_usd is not None or args.env_file):
        raise RunStopped('Offline modes reject authorization, budget and credential flags')
    if args.live and (args.authorize_study != IDENTIFIER or args.budget_usd != 20.0 or args.output):
        raise RunStopped('LIVE requires exact named authorization and --budget-usd 20.00; no alternate output')
    if args.preflight and args.output:
        raise RunStopped('Preflight cannot write a study output')
    if args.live and LIVE_ROOT.exists():
        raise RunStopped('This study already has an attempt; no restart or reset allowance')
    spec, checks = preflight()
    if args.preflight:
        print(json.dumps({**checks, 'identifier': IDENTIFIER, 'budget': read(MANIFEST)['budget']}, indent=2))
    elif args.mock:
        if not args.output:
            raise RunStopped('MOCK requires an explicit fresh --output')
        print(execute(args.output))
    else:
        if subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT, text=True).strip():
            raise RunStopped('A clean committed checkout is required before LIVE')
        if args.env_file:
            from dotenv import dotenv_values
            key = dotenv_values(args.env_file, interpolate=False).get('OPENROUTER_API_KEY')
            if not key:
                raise RunStopped('No key in local env file; never send it in chat')
            os.environ['OPENROUTER_API_KEY'] = key
        if not os.environ.get('OPENROUTER_API_KEY'):
            raise RunStopped('Supply a local key only after authorization')
        import certifi
        os.environ.setdefault('SSL_CERT_FILE', certifi.where())
        print(execute(LIVE_ROOT, live=True))


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(safe_error(exc), file=sys.stderr)
        raise SystemExit(2)

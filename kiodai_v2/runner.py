"""Environment-side adapter: the only v2 module that handles private PM state."""
import json
import re
from pathlib import Path
from sim import pm_bench as PM
from research_harness.runner import iter_environment, render_prompt
from research_harness.model_gateway import ModelAction, SelectionResult
from .agent import Agent
from .gateway import Gateway
from .common import append, dump, digest, rows

ROOT = Path(__file__).resolve().parents[1]


class Adapter:
    def __init__(self, agent, trace):
        self.agent, self.trace = agent, trace
        self.checkpoint = 0
        self.observations, self.receipts = {}, []
        self.seen = 0
        self.last = None

    def select_action(self, *, messages, allowed_handles, allowed_channels, call_context):
        # Private day and step IDs stop here. Controller gets its own sequential counter.
        if call_context['interaction_index'] == 1:
            self.checkpoint += 1
        current_refs = []
        for index in range(self.seen, len(messages)):
            message = messages[index]
            if message['role'] == 'user':
                ref = f'm{index}'
                text = message['content']
                self.observations[ref] = {'text': text, 'kind': 'query' if text.startswith('State [') else 'visible',
                                          'checkpoint': self.checkpoint}
                current_refs.append(ref)
        self.seen = len(messages)
        visible = next((m['content'] for m in reversed(messages) if 'Step action menu' in m['content'] and m['role'] == 'user'), '')
        frame = {'checkpoint': self.checkpoint, 'messages': messages, 'observations': self.observations,
                 'current_refs': current_refs, 'channels': list(allowed_channels), 'handles': list(allowed_handles),
                 'menu': dict(re.findall(r'^- ([^:]+): (.+)$', visible, re.M)), 'receipts': self.receipts}
        serialized = json.dumps(frame, ensure_ascii=False)
        self.agent.receive(serialized)
        decision = self.agent.decide()
        append(self.trace, {'checkpoint': self.checkpoint, 'frame': json.loads(serialized),
                            'decision': decision, 'intentions': self.agent.store.records()})
        self.last = decision
        plain = {k: decision[k] for k in ('action', 'choice', 'task_ids', 'channel')}
        return SelectionResult(ModelAction(plain['action'], plain['choice'], tuple(plain['task_ids']), plain['channel']),
                               bool(decision.get('blocked')), 1, tuple(plain['task_ids']), json.dumps(plain), decision.get('blocked'))

    def execution(self, public_receipts):
        # No canonical IDs, due flags or hidden state enter receipt handling.
        mapped = []
        for receipt in public_receipts:
            outcome = 'success' if receipt['outcome'] == 'simulator_completed' else 'failed'
            self.receipts.append({'checkpoint': self.checkpoint, 'handle': receipt['handle'], 'outcome': outcome})
            for binding in self.last.get('bindings', []):
                if binding['handle'] == receipt['handle']:
                    mapped.append({'execution_id': binding['execution_id'], 'outcome': outcome})
        self.agent.receipt(json.dumps(mapped))


def run_case(scenario_path, method, folder, config, transport, mode='MOCK', accounting=None):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=False)
    for name in ('calls.jsonl', 'agent.jsonl', 'steps.jsonl', 'actions.jsonl', 'failures.jsonl'):
        (folder/name).touch()
    scenario = json.loads(Path(scenario_path).read_text())
    dump(folder/'scenario.json', scenario)
    dump(folder/'config.json', config)
    prompt, metadata = render_prompt(ROOT/'prompts/baseline_system.txt',
                                    ROOT/'prompts/prospective_memory_system.txt' if method == 'A1' else None,
                                    PM.list_state_channels(scenario), False)
    (folder/'system_prompt.txt').write_text(prompt)
    manifest = {'mode': mode, 'method': method, 'status': 'running', 'prompt': metadata,
                'scenario_sha256': digest(Path(scenario_path).read_bytes()),
                'heartbeat_enabled': False, 'context': 'matched full history, shared documented receipts',
                'independent_unit': 'complete trajectory', 'repeat': 1, 'excluded': False}
    dump(folder/'manifest.json', manifest)
    gateway = Gateway(transport, config, folder/'calls.jsonl', mode, accounting)
    agent = Agent(method, folder/'memory.sqlite', gateway)
    adapter = Adapter(agent, folder/'agent.jsonl')
    runtime = {'execution': {'daily_header_lines': [], 'show_task_legend': False},
               'limits': {'max_context_tokens': 65536, 'max_tool_calls_per_step': 1}}
    actions = []
    try:
        for step in iter_environment(scenario=scenario, system_prompt=prompt, selector=adapter, config=runtime,
                allowed_channels=PM.list_state_channels(scenario), state_visibility=PM.normalize_state_visibility(scenario),
                state_channels=PM.normalize_state_channels(scenario), failure_path=folder/'failures.jsonl'):
            adapter.execution(json.loads(json.dumps(step['execution'])))
            # These artifacts are evaluator-side, separate from the agent request log.
            step['checkpoint'] = adapter.checkpoint
            step['intentions_after_receipt'] = agent.store.records()
            append(folder/'steps.jsonl', step)
            actions.append(step['action'])
            append(folder/'actions.jsonl', step['action'])
        manifest['status'] = 'completed'
    except BaseException as exc:
        from research_harness.model_gateway import safe_error
        manifest.update(status='interrupted', blocker=safe_error(exc))
        raise
    finally:
        dump(folder/'score.json', PM.score_log(scenario, actions))
        manifest['completed_steps'] = len(actions)
        manifest['planned_steps'] = sum(len(day['steps']) for day in scenario['days'])
        dump(folder/'memory.json', agent.store.records())
        agent.store.close()
        manifest['files'] = {p.name: digest(p.read_bytes()) for p in folder.iterdir() if p.is_file() and p.name != 'manifest.json'}
        dump(folder/'manifest.json', manifest)
    return folder


def verify_case(folder):
    folder = Path(folder)
    manifest = json.loads((folder/'manifest.json').read_text())
    for name, expected in manifest['files'].items():
        if Path(name).name != name or digest((folder/name).read_bytes()) != expected:
            raise ValueError('Artifact changed: ' + name)
    return manifest

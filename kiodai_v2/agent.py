"""Public agent controller. Input is serialized observations only, never an environment."""
import json
import re
from pathlib import Path
from .common import obj, array, CITATION, STRING, citations_valid, validate
from .store import Store, EXTRACTION
from .contract import VERSION
from research_harness.model_gateway import action_schema, parse_action

ROOT = Path(__file__).resolve().parents[1]
FRAME_KEYS = {'checkpoint', 'messages', 'observations', 'current_refs', 'channels', 'handles', 'menu', 'receipts'}
BINDING = obj({'handle': STRING, 'intention': STRING, 'version': {'type': 'integer'},
               'evidence': array(CITATION)})


class Agent:
    def __init__(self, method, store_path, gateway):
        if method not in ('A0', 'A1', 'B_ledger', 'A2'):
            raise ValueError('Unknown method')
        self.method, self.store, self.gateway = method, Store(store_path), gateway
        self.last_checkpoint = -1
        self.blocked = False
        self.decisions = []

    def receive(self, serialized_frame):
        frame = json.loads(serialized_frame)
        if set(frame) != FRAME_KEYS:
            raise ValueError('Agent boundary accepts only public frame fields')
        if type(frame['checkpoint']) is not int or frame['checkpoint'] < 1:
            raise ValueError('Invalid public checkpoint')
        for message in frame['messages']:
            if set(message) != {'role', 'content'} or message['role'] not in ('system', 'user', 'assistant') or not isinstance(message['content'], str):
                raise ValueError('Private or malformed message metadata')
        for receipt in frame['receipts']:
            if set(receipt) != {'checkpoint', 'handle', 'outcome'}:
                raise ValueError('Private receipt metadata')
        if not isinstance(frame['menu'], dict) or any(not isinstance(k, str) or not isinstance(v, str) for k,v in frame['menu'].items()):
            raise ValueError('Malformed public action menu')
        if any(not isinstance(x, str) for x in frame['handles'] + frame['channels'] + frame['current_refs']):
            raise ValueError('Malformed public interface')
        # Exact observation shape keeps private metadata out of persistent state.
        for source in frame['observations'].values():
            if set(source) != {'text', 'kind', 'checkpoint'} or source['kind'] not in ('visible', 'query'):
                raise ValueError('Private or malformed observation metadata')
        checkpoint = frame['checkpoint']
        if checkpoint < self.last_checkpoint:
            raise ValueError('Cannot rewind an agent')
        first = checkpoint != self.last_checkpoint
        self.last_checkpoint = checkpoint
        self.frame = frame
        if first:
            self.blocked = False
            self.queries = 0
            if self.method in ('B_ledger', 'A2'):
                payload = {'observations': frame['observations'], 'new_refs': frame['current_refs'],
                           'intentions': self.store.records(), 'channels': frame['channels'],
                           'contract_version': VERSION}
                def apply(value):
                    self.store.apply(value, frame['observations'], checkpoint, frame['channels'])
                value = self.gateway.call('extract', [
                    {'role': 'system', 'content': (ROOT/'prompts/v2_1/extract.txt').read_text()},
                    {'role': 'user', 'content': json.dumps(payload, ensure_ascii=False)}],
                    EXTRACTION, checkpoint, apply)
                self.blocked = value is None
        for ref in frame['current_refs']:
            source = frame['observations'][ref]
            if source['kind'] == 'query':
                for channel in frame['channels']:
                    if source['text'].startswith(f'State [{channel}]') or (channel == 'clock' and source['text'].startswith('Time:')):
                        self.store.query_received(channel, {'ref': ref, **source}, checkpoint)
        return first

    def decide(self):
        frame = self.frame
        checkpoint = frame['checkpoint']
        empty = {'action': 'choose', 'choice': 'A', 'task_ids': [], 'channel': 'NONE'}
        if self.blocked:
            return {**empty, 'blocked': 'invalid_extraction', 'bindings': []}
        if self.method == 'A2' and self.queries == 0:
            visible_clock = any(re.search(r'\bTime: \d\d:\d\d', frame['observations'][ref]['text'])
                                for ref in frame['current_refs'])
            tickets = self.store.monitor(checkpoint, frame['channels'], 1, clock_visible=visible_clock)
            if tickets and self.store.check_valid(tickets[0]):
                self.queries += 1
                return {'action': 'query_state', 'choice': 'NONE', 'task_ids': [],
                        'channel': tickets[0]['channel'], 'bindings': [], 'policy_ticket': tickets[0]}
        schema = action_schema(tuple(frame['handles']), tuple(frame['channels']))
        messages = json.loads(json.dumps(frame['messages']))
        # Every method sees the same documented execution receipts from its own actions.
        if frame['receipts']:
            messages.append({'role': 'user', 'content': 'Simulator execution receipts (with checkpoints): ' + json.dumps(frame['receipts'])})
        structured = self.method in ('B_ledger', 'A2')
        if structured:
            binding_schema = json.loads(json.dumps(BINDING))
            eligible = [key for key, item in self.store.records().items()
                        if self.store.eligible(key, item['version'])]
            if eligible:
                binding_schema['properties']['intention']['enum'] = eligible
            binding_schema['properties']['handle']['enum'] = list(frame['handles']) or ['NONE']
            schema['properties']['bindings'] = array(binding_schema, 8 if eligible else 0)
            if not eligible:
                schema['properties']['task_ids']['maxItems'] = 0
            schema['required'].append('bindings')
            messages[0]['content'] += '\n' + (ROOT/'prompts/v2_1/select.txt').read_text()
            messages.append({'role': 'user', 'content': json.dumps({
                'intentions': self.store.records(), 'observations': frame['observations'],
                'contract_version': VERSION,
                'current_checkpoint': checkpoint, 'query_remaining': 1 - self.queries,
                'query_decision': 'controller; choose now' if self.method == 'A2' else 'model may query',
            }, ensure_ascii=False)})
        if self.queries >= 1 or self.method == 'A2':
            schema['properties']['action']['enum'] = ['choose']
        def check(value):
            plain = {k: value[k] for k in ('action', 'choice', 'task_ids', 'channel')}
            parse_action(json.dumps(plain), tuple(frame['handles']), tuple(frame['channels']))
            if not structured:
                return
            bindings = value['bindings']
            if sorted(b['handle'] for b in bindings) != sorted(value['task_ids']):
                raise ValueError('One binding required per selected handle')
            if len({b['intention'] for b in bindings}) != len(bindings):
                raise ValueError('Cannot execute one intention twice')
            for binding in bindings:
                if not self.store.eligible(binding['intention'], binding['version']):
                    raise ValueError('bindings.intention/version: use an eligible ledger ID and its current version, not an action description')
                item = self.store.records()[binding['intention']]
                # The LLM supplies semantic action mapping. Record exact menu text for audit.
                # Citation validity is structural, not proof of semantic truth.
                citations_valid(binding['evidence'], frame['observations'], current=checkpoint)
                if item['trigger'] == 'hidden':
                    relevant = [frame['observations'][c['ref']] for c in binding['evidence']]
                    if not any(s['kind'] == 'visible' or s['text'].startswith(f"State [{item['channel']}]") for s in relevant):
                        raise ValueError('No current relevant channel or visible evidence')
        value = self.gateway.call('select' if structured else 'baseline', messages, schema, checkpoint, check)
        if value is None:
            return {**empty, 'blocked': 'invalid_selection', 'bindings': []}
        value.setdefault('bindings', [])
        if value['action'] != 'choose':
            self.queries += 1
        for binding in value['bindings']:
            binding['menu_text'] = frame['menu'].get(binding['handle'])
            binding['execution_id'] = self.store.select(binding['intention'], binding['version'],
                                                        binding['handle'], checkpoint, binding['evidence'])
            self.store.attempted(binding['execution_id'])
        self.decisions.append(value)
        return value

    def receipt(self, serialized_receipts):
        receipts = json.loads(serialized_receipts)
        for receipt in receipts:
            if set(receipt) != {'execution_id', 'outcome'}:
                raise ValueError('Receipt contains private fields')
            self.store.receipt(receipt['execution_id'], receipt['outcome'])

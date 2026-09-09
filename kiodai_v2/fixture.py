"""MOCK-only restricted language fixture. No scenario imports or expected-answer input.

This recognizer understands the authored template grammar, not unrestricted language.
All methods receive the same competent fixture policy; no baseline is scripted to lose.
It is never imported by the LIVE launcher path.
"""
import json
import re
from research_harness.model_gateway import TransportResponse


def cite(ref, quote):
    return {'ref': ref, 'quote': quote}


def record(action, trigger, condition, channel, when, source, ref, dependencies=None):
    values = dict(action=action, trigger=trigger, condition=condition, channel=channel,
                  when=when, dependencies=dependencies or [])
    return {**values, 'evidence': {key: [cite(ref, source)] if value not in (None, []) else []
                                  for key, value in values.items()}}


def interpret(observations):
    """Parse only observed source text into fixture semantic records."""
    records = {}
    for ref, source in observations.items():
        text = source['text']
        for m in re.finditer(r'At (\d\d:\d\d) on (\w+), ([A-Z][^.]+\.)', text):
            records[m[3]] = record(m[3], 'time', m[0], None, m[2]+' '+m[1], m[0], ref)
        for m in re.finditer(r'(?:On (\w+) )?When you see "([^"]+)", ([A-Z][^.]+\.)', text, re.I):
            records[m[3]] = record(m[3], 'event', m[2], None, m[1], m[0], ref)
        for m in re.finditer(r'When (\w+) reports "([^"]+)", ([A-Z][^.]+\.)', text):
            records[m[3]] = record(m[3], 'hidden', m[2], m[1], None, m[0], ref)
        for m in re.finditer(r'Change of schedule: "([^"]+)" is now due at (\d\d:\d\d) on (\w+)', text):
            if m[1] in records:
                records[m[1]] = record(m[1], 'time', m[0], None, m[3]+' '+m[2], m[0], ref)
        for m in re.finditer(r'For "([^"]+)" replace the earlier cue with "([^"]+)"', text):
            if m[1] in records:
                records[m[1]] = record(m[1], 'event', m[2], None, None, m[0], ref)
        for m in re.finditer(r'Do not carry out "([^"]+)"; that request has been canceled\.', text):
            if m[1] in records:
                records[m[1]]['canceled'] = cite(ref, m[0])
    return records


class FixtureTransport:
    is_mock = True
    def invoke(self, request, timeout_seconds):
        del timeout_seconds
        kind = request['response_format']['json_schema']['name']
        schema = request['response_format']['json_schema']['schema']
        messages = request['messages']
        if kind == 'extract':
            data = json.loads(messages[-1]['content'])
            semantic = interpret(data['observations'])
            existing = {r['action']: r for r in data['intentions'].values()}
            operations = []
            for action, rec in semantic.items():
                for ref, source in data['observations'].items():
                    dependency = re.search(re.escape(action) + r' Only after "([^"]+)" succeeds\.', source['text'])
                    if dependency and dependency[1] in existing:
                        rec['dependencies'] = [existing[dependency[1]]['id']]
                        rec['evidence']['dependencies'] = [cite(ref, dependency[0])]
                    elif dependency:
                        # v2.1 fixture contract: a new prerequisite has no ID until
                        # after this atomic batch. Quarantine until the next update.
                        rec['trigger'] = 'unknown'
                        rec['condition'] += '; unresolved prerequisite: ' + dependency[1]
                        rec['evidence']['condition'] = [cite(ref, dependency[0])]
                previous = existing.get(action)
                if previous and previous['status'] in ('completed', 'canceled', 'uncertain', 'attempted'):
                    continue
                canceled = rec.pop('canceled', None)
                if canceled and previous:
                    operations.append(dict(kind='cancel', target=previous['id'], expected_version=previous['version'], record=None, sources=[canceled]))
                elif not previous or any(previous[key] != rec[key] for key in ('condition', 'when', 'channel', 'action', 'dependencies')):
                    operations.append(dict(kind='revise' if previous else 'create', target=previous['id'] if previous else None,
                                           expected_version=previous['version'] if previous else None, record=rec, sources=rec['evidence']['action']))
            value = {'operations': operations}
        else:
            structured = kind == 'select'
            if structured:
                data = next(json.loads(m['content']) for m in reversed(messages) if m['role'] == 'user' and m['content'].startswith('{"intentions"'))
                obs, records = data['observations'], data['intentions']
                checkpoint = data['current_checkpoint']
            else:
                obs = {f'm{i}': {'text': m['content'], 'kind': 'query' if m['content'].startswith('State [') else 'visible', 'checkpoint': i}
                       for i, m in enumerate(messages) if m['role'] == 'user' and not m['content'].startswith('Simulator execution receipts')}
                semantic = interpret(obs)
                records = {str(i): {**r, 'status': 'canceled' if 'canceled' in r else 'pending'} for i, r in enumerate(semantic.values())}
                checkpoint = max((s['checkpoint'] for s in obs.values() if 'Step action menu' in s['text']), default=0)
                for source in obs.values():
                    if source['checkpoint'] >= checkpoint:
                        source['checkpoint'] = checkpoint
            current = {ref: s for ref, s in obs.items() if s['checkpoint'] == checkpoint}
            narrative = '\n'.join(s['text'] for s in current.values())
            # Latest visible menu identifies the current decision, even following a query.
            menu_source = next(m['content'] for m in reversed(messages) if 'Step action menu' in m['content'] and m['role'] == 'user' and not m['content'].startswith('{'))
            menu = dict(re.findall(r'^- ([^:]+): (.+)$', menu_source, re.M))
            day_matches = re.findall(r'=== (\w+) ===', '\n'.join(m['content'] for m in messages if not m['content'].startswith('{')))
            day = day_matches[-1] if day_matches else ''
            time_match = re.findall(r'Time: (\d\d:\d\d)', menu_source)
            visible_time = time_match[-1] if time_match else None
            if visible_time is None:
                clock_times = re.findall(r'State \[clock\]: Time (\d\d:\d\d)', narrative)
                visible_time = clock_times[-1] if clock_times else None
            can_query = 'query_state' in schema['properties']['action']['enum']
            value = {'action': 'choose', 'choice': 'A', 'task_ids': [], 'channel': 'NONE'}
            bindings = []
            for key, item in records.items():
                if item['status'] not in ('pending', 'failed'):
                    continue
                handle = next((h for h, a in menu.items() if a == item['action']), None)
                if not handle:
                    continue
                if item['trigger'] == 'hidden' and can_query and not any(s['text'].startswith(f"State [{item['channel']}]") for s in current.values()):
                    value = {'action': 'query_state', 'choice': 'NONE', 'task_ids': [], 'channel': item['channel']}
                    bindings = []
                    break
                support = []
                for ref, source in current.items():
                    text = source['text']
                    if item['trigger'] == 'time':
                        satisfied = item['when'] == f'{day} {visible_time}' and ('Step action menu' in text or text.startswith('State [clock]'))
                    else:
                        # Ignore the initial instruction/menu when finding a present cue.
                        scene = text.split('A)')[0]
                        satisfied = (item['condition'] in scene and not any(x in scene for x in ('When ', 'when you see', 'not a ', 'reports "', 'replace the earlier cue'))
                                     and (not item['when'] or item['when'] == day))
                    if satisfied:
                        support = [cite(ref, text)]
                        break
                if support:
                    value['task_ids'].append(handle)
                    if structured:
                        bindings.append({'handle': handle, 'intention': key, 'version': item['version'], 'evidence': support})
            if structured:
                value['bindings'] = bindings
        raw = json.dumps(value, ensure_ascii=False)
        return TransportResponse(raw, {'mock': True, 'fixture': 'restricted visible-language grammar', 'content': value},
                                 {'input_tokens': len(json.dumps(request)) // 4, 'output_tokens': len(raw) // 4},
                                 'mock-fixture', {'transport': 'MOCK', 'cost_usd_reported': None})

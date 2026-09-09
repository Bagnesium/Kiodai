"""Agent-side SQLite intention ledger. Never reads a scenario or an evaluator."""
import json
import sqlite3
from .common import array, obj, STRING, NULL_STRING, CITATION, citations_valid, digest, validate

FIELDS = {'action': STRING, 'trigger': {'type': 'string', 'enum': ['time', 'event', 'hidden', 'unknown']},
          'condition': STRING, 'channel': NULL_STRING, 'when': NULL_STRING,
          'dependencies': array(STRING)}
RECORD = obj({**FIELDS, 'evidence': obj({key: array(CITATION) for key in FIELDS})})
EXTRACTION = obj({'operations': array(obj({
    'kind': {'type': 'string', 'enum': ['create', 'revise', 'cancel', 'ambiguous']},
    'target': NULL_STRING, 'expected_version': {'type': ['integer', 'null']},
    'record': {**RECORD, 'type': ['object', 'null']}, 'sources': array(CITATION)}))})


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS state (key TEXT PRIMARY KEY, value TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS events (seq INTEGER PRIMARY KEY, body TEXT NOT NULL)')
        self.db.commit()

    def close(self):
        self.db.close()

    def get(self, key, default=None):
        row = self.db.execute('SELECT value FROM state WHERE key=?', (key,)).fetchone()
        return json.loads(row[0]) if row else default

    def put(self, key, value):
        self.db.execute('INSERT OR REPLACE INTO state VALUES (?,?)', (key, json.dumps(value)))

    def event(self, kind, **values):
        self.db.execute('INSERT INTO events(body) VALUES (?)', (json.dumps({'kind': kind, **values}),))

    def records(self):
        return self.get('intentions', {})

    def apply(self, payload, observations, checkpoint, channels):
        validate(payload, EXTRACTION)
        # Atomic batch: malformed output must not leave half-applied revisions.
        with self.db:
            records = self.records()
            for op in payload['operations']:
                citations_valid(op['sources'], observations)
                kind, target = op['kind'], op['target']
                if kind == 'ambiguous':
                    self.event('ambiguous_update', checkpoint=checkpoint, operation=op)
                    # Quarantine all live intentions: no arbitrary target is chosen.
                    for item in records.values():
                        if item['status'] not in ('completed', 'canceled'):
                            item['status'] = 'quarantined'
                    continue
                if kind != 'create':
                    if target not in records or records[target]['version'] != op['expected_version']:
                        raise ValueError('Unknown or stale revision target')
                    if records[target]['status'] in ('completed', 'canceled', 'uncertain', 'attempted'):
                        raise ValueError('Terminal or unresolved execution cannot be revised')
                if kind == 'cancel':
                    if op['record'] is not None:
                        raise ValueError('Cancel has no replacement record')
                    records[target]['status'] = 'canceled'
                    records[target]['version'] += 1
                    records[target]['update_evidence'] = op['sources']
                else:
                    record = op['record']
                    if record is None or not record['action'] or not record['condition']:
                        raise ValueError('Missing intention content')
                    for field in FIELDS:
                        if record[field] not in (None, [], 'unknown'):
                            citations_valid(record['evidence'][field], observations)
                    if record['channel'] is not None and record['channel'] not in channels:
                        raise ValueError('Unavailable channel')
                    if record['trigger'] == 'hidden' and not record['channel']:
                        raise ValueError('Hidden trigger requires a legitimate channel')
                    if any(dep not in records or dep == target for dep in record['dependencies']):
                        raise ValueError('Unknown or self dependency')
                    if kind == 'create':
                        if target is not None or op['expected_version'] is not None:
                            raise ValueError('Create cannot nominate an evaluator ID')
                        target = 'i_' + digest(json.dumps([op['sources'], record['action']], sort_keys=True).encode())[:16]
                        if target in records:
                            raise ValueError('Duplicate creation')
                        version = 1
                    else:
                        version = records[target]['version'] + 1
                    records[target] = {**record, 'id': target, 'version': version, 'status': 'pending',
                                       'update_evidence': op['sources'], 'last_query': None,
                                       'attempt_id': None, 'receipt': None}
                self.event(kind, checkpoint=checkpoint, id=target, record=records[target])
            # Cyclic dependencies would deadlock the ledger; reject the entire batch.
            def visit(key, chain):
                if key in chain:
                    raise ValueError('Cyclic dependencies')
                for dep in records[key]['dependencies']:
                    visit(dep, chain | {key})
            for key in records:
                visit(key, set())
            self.put('intentions', records)

    def eligible(self, identifier, version):
        records = self.records()
        item = records.get(identifier)
        return bool(item and item['version'] == version and item['status'] in ('pending', 'failed')
                    and all(records[d]['status'] == 'completed' for d in item['dependencies']))

    def monitor(self, checkpoint, channels, remaining, clock_visible=True):
        records = self.records()
        candidates = {}
        for key, item in records.items():
            channel = item['channel']
            if channel is None and item['trigger'] == 'time' and not clock_visible:
                channel = 'clock'
            if self.eligible(key, item['version']) and channel in channels:
                candidates.setdefault(channel, []).append([key, item['version']])
        last = self.get('channel_checks', {})
        ordered = sorted(candidates, key=lambda channel: (last.get(channel, -1), channel))
        chosen = ordered[:max(0, remaining)]
        with self.db:
            self.event('monitor', checkpoint=checkpoint, selected=chosen,
                       unavailable=[c for c in ordered if c not in chosen], remaining=remaining)
        return [{'channel': channel, 'versions': candidates[channel]} for channel in chosen]

    def check_valid(self, ticket):
        return any(self.eligible(key, version) and (self.records()[key]['channel'] == ticket['channel'] or
                   (ticket['channel'] == 'clock' and self.records()[key]['trigger'] == 'time' and self.records()[key]['channel'] is None))
                   for key, version in ticket['versions'])

    def query_received(self, channel, observation, checkpoint):
        with self.db:
            checks = self.get('channel_checks', {})
            checks[channel] = checkpoint
            self.put('channel_checks', checks)
            records = self.records()
            for item in records.values():
                if item['channel'] == channel and item['status'] in ('pending', 'failed'):
                    item['last_query'] = {'observation': observation, 'checkpoint': checkpoint,
                                          'version': item['version']}
            self.put('intentions', records)
            self.event('query_received', channel=channel, observation=observation, checkpoint=checkpoint)

    def select(self, identifier, version, handle, checkpoint, evidence):
        if not self.eligible(identifier, version):
            raise ValueError('Canceled, stale, completed, unresolved, or dependency-blocked action')
        records = self.records()
        # One logical side effect per intention version, stable across process restarts.
        execution_id = 'exec_' + digest(f'{identifier}:{version}'.encode())[:20]
        with self.db:
            records[identifier].update(status='selected', attempt_id=execution_id)
            self.put('intentions', records)
            self.event('selected', id=identifier, version=version, handle=handle,
                       execution_id=execution_id, checkpoint=checkpoint, evidence=evidence)
        return execution_id

    def attempted(self, execution_id):
        with self.db:
            records = self.records()
            for item in records.values():
                if item['attempt_id'] == execution_id and item['status'] == 'selected':
                    item['status'] = 'attempted'
            self.put('intentions', records)
            self.event('attempted', execution_id=execution_id)

    def receipt(self, execution_id, outcome):
        if outcome not in ('success', 'failed', 'uncertain'):
            raise ValueError('Undocumented execution outcome')
        with self.db:
            records = self.records()
            matched = [r for r in records.values() if r['attempt_id'] == execution_id]
            if not matched:
                raise ValueError('Unknown execution receipt')
            for item in matched:
                if item['status'] not in ('attempted', 'failed', 'uncertain', 'completed'):
                    raise ValueError('Receipt requires an attempted execution')
                if item['status'] == 'completed':
                    if outcome != 'success':
                        raise ValueError('Contradictory receipt')
                    continue
                item['status'] = 'completed' if outcome == 'success' else outcome
                item['receipt'] = {'execution_id': execution_id, 'outcome': outcome}
            self.put('intentions', records)
            self.event('receipt', execution_id=execution_id, outcome=outcome)


class LocalExecutor:
    """Separate lifecycle simulator, not PM-Bench. SQLite side effect + receipt are atomic."""
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS executions (id TEXT PRIMARY KEY, outcome TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS effects (id TEXT PRIMARY KEY)')
        self.db.commit()

    def execute(self, identifier, outcome='success'):
        if outcome not in ('success', 'failed', 'uncertain'):
            raise ValueError('Unknown simulator outcome')
        with self.db:
            prior = self.db.execute('SELECT outcome FROM executions WHERE id=?', (identifier,)).fetchone()
            if prior and prior[0] in ('success', 'uncertain'):
                return prior[0]
            if outcome == 'success':
                self.db.execute('INSERT OR IGNORE INTO effects VALUES (?)', (identifier,))
            self.db.execute('INSERT OR REPLACE INTO executions VALUES (?,?)', (identifier, outcome))
        return outcome

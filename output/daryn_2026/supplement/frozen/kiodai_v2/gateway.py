"""All internal inference crosses this logged, bounded gateway."""
import json
import math
import sqlite3
import time
from .common import append, parse
from research_harness.model_gateway import RunStopped, safe_error, utc_now, OpenAICompatibleTransport


class Accounting:
    """Durable reservations never refunded, including unknown transport outcomes."""
    def __init__(self, path, ceiling, config):
        if not math.isfinite(ceiling) or ceiling <= 0:
            raise RunStopped('A finite positive explicit budget is required')
        self.config = config
        self.db = sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS account (ceiling REAL NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS attempts (id INTEGER PRIMARY KEY, reserved REAL, reported REAL, state TEXT)')
        saved = self.db.execute('SELECT ceiling FROM account').fetchone()
        if saved and saved[0] != ceiling:
            self.db.close()
            raise RunStopped('Cannot reset or change this study budget')
        if not saved:
            self.db.execute('INSERT INTO account VALUES (?)', (ceiling,))
        self.db.commit()
        self.ceiling = ceiling

    def bound(self, output_tokens):
        prices = self.config['model']['pricing_usd_per_million_tokens']
        # Upper allowance: one token per serialized UTF-8 byte plus 1024 framing tokens.
        # No cache discounts, no average-output assumption in the budget guard.
        return ((self.config['max_request_bytes'] + 1024) * prices['input'] +
                output_tokens * prices['output']) / 1e6

    def snapshot(self):
        values = self.db.execute('SELECT reserved, reported, state FROM attempts').fetchall()
        return {'ceiling_usd': self.ceiling, 'reserved_usd': sum(x[0] for x in values),
                'attempts': len(values), 'api_response_cost_usd': sum(x[1] for x in values) if values and all(x[1] is not None for x in values) else None,
                'reported_subtotal_usd': sum(x[1] for x in values if x[1] is not None),
                'unknown_cost_attempts': sum(x[1] is None for x in values),
                'verified_billed_cost_usd': None}

    def reserve(self, request):
        if len(json.dumps(request, ensure_ascii=False).encode()) > self.config['max_request_bytes']:
            raise RunStopped('Request exceeds the frozen byte allowance; no truncation or inference')
        amount = self.bound(request['max_tokens'])
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            if self.snapshot()['reserved_usd'] + amount > self.ceiling + 1e-10:
                raise RunStopped('Cumulative reservation would exceed the authorized budget')
            cursor = self.db.execute('INSERT INTO attempts(reserved,state) VALUES (?,?)', (amount, 'reserved_before_send'))
        return cursor.lastrowid

    def finish(self, identifier, response):
        cost = (response.provider_metadata or {}).get('cost_usd_reported')
        valid = type(cost) in (float, int) and math.isfinite(cost) and cost >= 0
        with self.db:
            self.db.execute('UPDATE attempts SET reported=?,state=? WHERE id=?',
                            (cost if valid else None, 'response_received', identifier))
        if valid and cost > self.db.execute('SELECT reserved FROM attempts WHERE id=?', (identifier,)).fetchone()[0] + 1e-10:
            raise RunStopped('Reported charge exceeds reservation; stop and audit billing')


class Gateway:
    def __init__(self, transport, config, log, mode, accounting=None):
        if mode not in ('MOCK', 'LOCAL_MODEL', 'LIVE'):
            raise ValueError('Replay is not an inference mode')
        if mode == 'LOCAL_MODEL' and not getattr(transport, 'is_local', False):
            raise ValueError('LOCAL_MODEL requires the loopback-only local transport')
        if mode == 'LIVE' and (accounting is None or type(transport) is not OpenAICompatibleTransport):
            raise ValueError('LIVE requires durable accounting and a real transport')
        self.transport, self.config, self.log, self.mode = transport, config, log, mode
        self.accounting = accounting
        self.sequence = 0

    def call(self, kind, messages, schema, checkpoint, validator=None):
        config, model = self.config, self.config['model']
        messages = json.loads(json.dumps(messages))
        for attempt in (1, 2):
            request = {'provider': model['provider'], 'provider_route': model['route'],
                       'route_fallbacks_allowed': False, 'provider_require_parameters': True,
                       'provider_quantizations': model['quantizations'], 'model': model['model_id'],
                       **config['sampling'], 'reasoning': model['reasoning'],
                       'messages': messages, 'max_tokens': config['output_tokens'][kind],
                       'response_format': {'type': 'json_schema', 'json_schema':
                                           {'name': kind, 'strict': True, 'schema': schema}}}
            if len(json.dumps(request, ensure_ascii=False).encode()) > config['max_request_bytes']:
                raise RunStopped('Request byte limit exceeded before inference')
            reservation = self.accounting.reserve(request) if self.accounting else None
            self.sequence += 1
            request_id = f'call_{self.sequence:04d}'
            # Persist exact request before send, so a process interruption leaves evidence.
            started = time.perf_counter()
            append(self.log, {'event': 'request', 'mode': self.mode, 'kind': kind,
                              'request_id': request_id,
                              'checkpoint': checkpoint, 'attempt': attempt, 'reservation': reservation,
                              'utc': utc_now(), 'request': request})
            response = None
            error = None
            value = None
            stage = 'transport'
            try:
                response = self.transport.invoke(request, config['timeout_seconds'])
                stage = 'structure'
                value = parse(response.raw_text, schema)
                if validator:
                    stage = 'application'
                    validator(value)
            except Exception as exc:
                error = safe_error(exc)
            if response is None:
                outcome = 'transport_failure'
            elif error:
                outcome = 'retry_exhausted' if attempt == 2 else 'validation_failure'
            elif kind == 'extract':
                outcome = 'accepted_operations' if value['operations'] else 'accepted_empty_update'
            else:
                outcome = 'accepted_selection'
            append(self.log, {'event': 'response', 'mode': self.mode, 'kind': kind,
                              'request_id': request_id,
                              'checkpoint': checkpoint, 'attempt': attempt, 'reservation': reservation,
                              'utc': utc_now(), 'latency_seconds': time.perf_counter() - started,
                              'raw_text': response.raw_text if response else None,
                              'raw_response': response.raw_response if response else None,
                              'usage': response.usage if response and self.mode in ('LIVE', 'LOCAL_MODEL') else None,
                              'mock_token_estimates': response.usage if response and self.mode == 'MOCK' else None,
                              'provider': response.provider_metadata if response else None,
                              'reported_model': response.reported_model if response else None,
                              'validation_stage': stage if error else None,
                              'outcome': outcome,
                              'validation_error': error if response else None,
                              'transport_error': error if response is None else None})
            if response is None:
                # Unknown server-side execution: no automatic transport retry.
                raise RunStopped('Transport interrupted; preserve study and unknown charge: ' + str(error))
            if self.accounting:
                self.accounting.finish(reservation, response)
                provider = (response.provider_metadata or {}).get('provider_reported', '')
                if response.reported_model != model['model_id'] or provider.lower() != model['route']:
                    raise RunStopped('Returned model/provider differs from pinned route')
            if error is None:
                return value
            if attempt == 1:
                messages += [{'role': 'assistant', 'content': response.raw_text or ''},
                             {'role': 'user', 'content': 'Validation failed (' + stage + '): ' + error +
                              '\nThe rejected batch/action was not applied. Correct this problem using only offered observations, IDs and current versions. Return the same requested JSON schema. Do not invent evidence. An empty operations list is valid only when no supported update is needed; rejection does not mean the instructions disappeared.'}]
        return None

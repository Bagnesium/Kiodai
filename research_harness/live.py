"""Explicit paid gate, public route preflight and a shared conservative budget."""
from __future__ import annotations
import json
import math
import os
from pathlib import Path
from urllib.request import urlopen
from .model_gateway import RunStopped, OpenAICompatibleTransport

MODEL = 'deepseek/deepseek-chat-v3.1'
ENDPOINT_URL = f'https://openrouter.ai/api/v1/models/{MODEL}/endpoints'
CEILING = 0.30


def request_bound(request, prices):
    # Heuristic, intentionally padded. This is NOT an actual tokenizer or bill.
    tokens = math.ceil(len(json.dumps(request, ensure_ascii=False).encode()) / 4 * 1.6)
    return (tokens * prices['input'] + int(request['max_tokens']) * prices['output']) / 1_000_000


class Budget:
    def __init__(self, ceiling, prices, *, protocol_ceiling=CEILING):
        # Existing pilot/dashboard callers retain the $0.30 cap. A separately
        # frozen study may pass its reviewed cap; --live and explicit budget
        # approval are still required by its launcher. Estimation is unchanged.
        if (not isinstance(protocol_ceiling, (float, int)) or isinstance(protocol_ceiling, bool)
                or not math.isfinite(protocol_ceiling) or protocol_ceiling <= 0):
            raise RunStopped('A finite positive protocol ceiling is required.')
        if (not isinstance(ceiling, (float, int)) or isinstance(ceiling, bool)
                or not math.isfinite(ceiling) or not 0 < ceiling <= protocol_ceiling):
            raise RunStopped(f'An explicit budget in (0, {protocol_ceiling:.2f}] USD is required.')
        self.ceiling = float(ceiling)
        self.prices = prices
        self.reserved = 0.0
        self.reported = 0.0
        self.unreported = 0
        self.attempts = 0

    def require(self, amount):
        if not math.isfinite(amount) or amount < 0 or self.reserved + amount > self.ceiling + 1e-12:
            raise RunStopped(f'Insufficient budget: estimated reservation {amount:.6f}, remaining {self.ceiling-self.reserved:.6f} USD.')

    def reserve(self, request):
        amount = request_bound(request, self.prices)
        self.require(amount)
        self.reserved += amount
        self.attempts += 1
        return amount

    def snapshot(self):
        return {'ceiling_usd': self.ceiling, 'reserved_estimate_usd': self.reserved,
                'reported_cost_usd': self.reported if self.unreported == 0 else None,
                'reported_cost_subtotal_usd': self.reported,
                'unreported_attempts': self.unreported, 'attempts': self.attempts,
                'policy': 'Reservations are conservative estimates, not a guaranteed billing cap; missing costs remain unavailable.'}


def verify_route(config, payload=None):
    model = config['model']
    if (model['provider'] != 'openrouter' or model['model_id'] != MODEL or
        model.get('route') != 'novita' or model.get('quantizations') != ['fp8'] or
        model.get('allow_route_fallbacks') is not False or model.get('require_parameters') is not True or
        model.get('base_url') != 'https://openrouter.ai/api/v1' or
        model.get('api_key_env') != 'OPENROUTER_API_KEY'):
        raise RunStopped('The frozen OpenRouter / DeepSeek V3.1 / novita / fp8 route is required.')
    if payload is None:
        with urlopen(ENDPOINT_URL, timeout=20) as response:
            payload = json.load(response)
    endpoints = payload.get('data', {}).get('endpoints', [])
    candidates = [e for e in endpoints if
                  (e.get('tag', '').lower().split('/')[0] == 'novita' or e.get('provider_name', '').lower() == 'novita')
                  and str(e.get('quantization', '')).lower() == 'fp8'
                  and e.get('status', 0) == 0]
    if not candidates:
        raise RunStopped('Pinned novita fp8 endpoint unavailable in public route metadata; no substitution allowed.')
    required = {'response_format', 'temperature', 'top_p', 'max_tokens', 'seed', 'reasoning'}
    candidates = [e for e in candidates if required <= set(e.get('supported_parameters', []))]
    if not candidates:
        raise RunStopped('Pinned endpoint does not advertise all frozen request parameters; no inference attempted.')
    prices = model['pricing_usd_per_million_tokens']
    for endpoint in candidates:
        pricing = endpoint.get('pricing', {})
        for source, key in [('prompt', 'input'), ('completion', 'output')]:
            try:
                price = float(pricing[source]) * 1_000_000
            except (KeyError, ValueError, TypeError):
                raise RunStopped('Pinned route pricing is unavailable.')
            if not math.isfinite(price) or price < 0 or price > prices[key] + 1e-9:
                raise RunStopped('Current endpoint price exceeds frozen pricing; budget/protocol review required.')
    return {'url': ENDPOINT_URL, 'billable': False, 'endpoints': candidates}


class BudgetedTransport:
    mode = 'LIVE'
    def __init__(self, config, budget):
        key = os.environ.get('OPENROUTER_API_KEY')
        if not key:
            raise RunStopped('OPENROUTER_API_KEY is missing from the local environment.')
        self.inner = OpenAICompatibleTransport(key, config['model']['base_url'])
        self.budget = budget

    def invoke(self, request, timeout_seconds):
        reserved = self.budget.reserve(request)
        try:
            response = self.inner.invoke(request, timeout_seconds)
        except Exception:
            self.budget.unreported += 1
            raise
        cost = (response.provider_metadata or {}).get('cost_usd_reported')
        if isinstance(cost, (int, float)) and math.isfinite(cost) and cost >= 0:
            self.budget.reported += cost
            self.budget.reserved += max(0.0, cost - reserved)
        else:
            self.budget.unreported += 1
        # Preserve mismatched raw responses for audit; stop before selecting any action.
        provider = (response.provider_metadata or {}).get('provider_reported')
        if response.reported_model != MODEL or not provider or provider.lower() != 'novita':
            response.provider_metadata['route_error'] = 'Returned route/model could not be verified; pair interrupted.'
        return response

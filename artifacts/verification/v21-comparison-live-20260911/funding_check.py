import json, math, ssl, sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
import certifi
from dotenv import dotenv_values

root = Path('/Users/bagnesium/Documents/GitHub/Kiodai')
config = json.loads((root / 'configs/v21_comparison_v1.json').read_text())
base = config['model']['base_url']
if base != 'https://openrouter.ai/api/v1':
    raise SystemExit('Unexpected API base URL; no request sent')
key = dotenv_values(root / '.env', interpolate=False).get('OPENROUTER_API_KEY')
if not key:
    raise SystemExit('Local key unavailable; no request sent')
ctx = ssl.create_default_context(cafile=certifi.where())
required = 19.95251712
report = {'study': 'v2.1-comparison-v1', 'checked_at_utc': datetime.now(timezone.utc).isoformat(),
          'required_conservative_allowance_usd': required, 'authorized_local_ceiling_usd': 20.0,
          'http_method': 'GET', 'tls_verification': True, 'model_calls': 0,
          'settings_changed': False, 'independently_verified_study_billing': None}
for endpoint, fields in [('/key', ('limit', 'limit_remaining', 'limit_reset', 'usage', 'is_free_tier', 'expires_at')),
                         ('/credits', ('total_credits', 'total_usage'))]:
    entry = {'url': base + endpoint}
    request = Request(base + endpoint, headers={'Authorization': 'Bearer ' + key}, method='GET')
    try:
        with urlopen(request, context=ctx, timeout=20) as response:
            data = json.load(response).get('data', {})
            entry.update({'http_status': response.status, 'data': {f: data.get(f) for f in fields}})
    except HTTPError as exc:
        entry.update({'http_status': exc.code, 'available': False, 'error': 'HTTP request denied or failed; response body not persisted'})
    except Exception as exc:
        entry.update({'available': False, 'error_type': type(exc).__name__})
    report[endpoint[1:]] = entry
kd = report['key'].get('data', {})
cd = report['credits'].get('data', {})
def numeric(value):
    return type(value) in (int, float) and math.isfinite(value)
remaining = kd.get('limit_remaining')
limit = kd.get('limit')
report['key_allowance_covers_required'] = (remaining >= required if numeric(remaining) else
    True if report['key'].get('http_status') == 200 and limit is None else None)
if numeric(cd.get('total_credits')) and numeric(cd.get('total_usage')):
    balance = cd['total_credits'] - cd['total_usage']
    report['account_credit_balance_usd'] = balance
    report['account_credit_covers_required'] = balance >= required
else:
    report['account_credit_balance_usd'] = None
    report['account_credit_covers_required'] = None
report['decision'] = ('stop_before_inference' if report['key_allowance_covers_required'] is not True
                       or report['account_credit_covers_required'] is False else 'funding_checks_permit_start')
path = Path('/tmp/kiodai-v21-comparison-funding-authorized-20260911.json')
path.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))

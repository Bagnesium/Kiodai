"""Read-only loopback checks for the existing viewer; no model transport."""
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.parse import urlencode
base='http://127.0.0.1:8772'
def get(path):
 with urlopen(base+path,timeout=10) as response:
  assert response.status==200
  return json.load(response)
catalog=get('/api/catalog'); assert catalog['mode']=='RECORDED' and catalog['source_mode']=='LIVE' and catalog['status']=='completed' and catalog['inference_enabled'] is False
assert len(catalog['trajectories'])==12 and set(catalog['methods'])=={'A0','B_ledger','A2'}
checked=[]
for trajectory in catalog['trajectories']:
 for method in catalog['methods']:
  for index in (0,7):
   value=get('/api/step?'+urlencode(dict(trajectory=trajectory,method=method,index=index)))
   assert value['status']=='completed' and value['completed_steps']==8 and value['checkpoint']==index+1 and value['inference_enabled'] is False and 'evaluator' not in value
   checked.append([trajectory,method,index+1])
value=get('/api/step?'+urlencode(dict(trajectory='v2_hidden_91322',method='A2',index=6)))
assert len(value['queries'])==1 and len(value['execution_receipts'])==2 and all(r['outcome']=='simulator_completed' for r in value['execution_receipts'])
evaluator=get('/api/evaluator?'+urlencode(dict(trajectory='v2_hidden_91322',method='A2',index=6)));assert evaluator['label']=='EVALUATOR ONLY · after selection'
print(json.dumps(dict(base_url=base,catalog=catalog,first_and_last_step_checks=checked,step_checks_passed=len(checked),successful_trace_query_and_receipts_verified=True,evaluator_separate=True,inference_enabled=False),indent=2))

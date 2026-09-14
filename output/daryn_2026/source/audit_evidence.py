"""Read-only audit of the frozen Kiodai comparison; no model calls or writes to evidence."""
import csv, hashlib, json, subprocess, sys
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
def read(p): return json.loads((ROOT/p).read_text())
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p): return [json.loads(s) for s in p.read_text().splitlines() if s.strip()]
manifest=read('research/v2_1/comparison_v1.json')
inventory=read('research/v2_1/live_comparison_v1_inventory.json')
checks={}
for name,mapping in [('frozen',manifest['hashes']),('raw',inventory['files']),('preparation',manifest['preparation_evidence_hashes']),('provenance',manifest['provenance_evidence_hashes'])]:
 bad=[p for p,h in mapping.items() if not (ROOT/p).is_file() or sha(ROOT/p)!=h]
 checks[name]={'files':len(mapping),'mismatches':bad}; assert not bad,(name,bad)
checks['archive_sha256']=sha(ROOT/inventory['archive']);assert checks['archive_sha256']==inventory['archive_sha256']
commit=inventory['execution_commit']
core=['kiodai_v2/agent.py','kiodai_v2/store.py','kiodai_v2/runner.py','kiodai_v2/report.py','sim/pm_bench.py','research_harness/runner.py','scripts/report_v21_comparison.py','prompts/v2_1/extract.txt','prompts/v2_1/select.txt','prompts/baseline_system.txt']
for p in core:
 b=subprocess.check_output(['git','show',commit+':'+p],cwd=ROOT)
 assert b==(ROOT/p).read_bytes(),p
checks['evaluated_code_matches']=core
from sim import pm_bench as PM
from kiodai_v2.report import analyze_case
from scripts.report_v21_comparison import obligation_diagnostics
cfg=manifest['specification']['config']; path=ROOT/'results/v2_1/comparison-v1'
review=read('results/v2_1/comparison-v1/comparison_report_reviewed.json')
review_idx={(c['trajectory'],c['method']):c for c in review['cases']}
case_results=[];totals={}
for entry in manifest['specification']['schedule']:
 trajectory=entry['trajectory']
 for method in ['A0','B_ledger','A2']:
  folder=path/trajectory/method
  sc=json.loads((folder/'scenario.json').read_text());ac=rows(folder/'actions.jsonl');st=rows(folder/'steps.jsonl');calls=rows(folder/'calls.jsonl')
  assert len(st)==len(ac)==8
  official=json.loads(json.dumps(PM.score_log(sc,ac))); assert official==json.loads((folder/'score.json').read_text())
  counts=[official[0]['set_'+k] for k in ['tp','fp','fn']];tp,fp,fn=counts;den=2*tp+fp+fn;f1=2*tp/den if den else None
  assert f1==review_idx[(trajectory,method)]['set_f1']
  requests=[r for r in calls if r['event']=='request'];responses=[r for r in calls if r['event']=='response'];assert len(requests)==len(responses)
  for r in requests:
   q=r['request'];assert q['model']==cfg['model']['model_id']; assert q['temperature']==0 and q['top_p']==1 and q['seed']==20260904
   assert q['max_tokens']==cfg['output_tokens'][r['kind']]
   assert q['provider_route']=='novita' and q['route_fallbacks_allowed']==False
   assert q['provider']=='openrouter' and q['provider_quantizations']==['fp8']
   assert q['provider_require_parameters'] is True
   assert q['reasoning']=={'enabled':False,'exclude':True}
  for r in responses:
   assert r['reported_model']=='deepseek/deepseek-chat-v3.1'
   assert r['provider']['provider_reported']=='Novita' and not r['transport_error']
  ob=obligation_diagnostics(sc,st)
  record=dict(trajectory=trajectory,family=entry['family'],method=method,tp=tp,fp=fp,fn=fn,set_f1=f1,model_calls=len(requests),input_tokens=sum(r['usage']['input_tokens'] for r in responses),output_tokens=sum(r['usage']['output_tokens'] for r in responses),api_cost_usd=str(sum((Decimal(str(r['provider']['cost_usd_reported'])) for r in responses),Decimal(0))),board_queries=sum(q['channel']!='clock' for s in st for q in s['tools']),executions=sum(len(s['execution']) for s in st),successful_receipts=sum(e['outcome']=='simulator_completed' for s in st for e in s['execution']),selection_validation_failures=sum(bool(r['validation_error']) and r['kind'] in ['select','baseline'] for r in responses),**{k:v for k,v in ob.items() if k not in ['obligations','coverage']})
  for k in ['total_instructed_obligations','unique_obligations_ever_due','unique_obligations_blocked_at_trigger','canceled_obligations','unfinished_not_canceled']:
   assert record[k]==review_idx[(trajectory,method)]['diagnostics']['obligations'][k]
  base=analyze_case(folder)
  record["query_supported_successes"]=sum(h["category"]=="query_supported_hit" for h in base["hidden_opportunities"])
  assert record["query_supported_successes"]==sum(h["category"]=="query_supported_hit" for h in review_idx[(trajectory,method)]["hidden_opportunities"])
  case_results.append(record)
for method in ['A0','B_ledger','A2']:
 cs=[r for r in case_results if r['method']==method];t={k:sum(r[k] for r in cs) for k in cs[0] if isinstance(cs[0][k],(int,float)) and k!='set_f1'}
 t['mean_trajectory_set_f1']=sum(c['set_f1'] for c in cs)/12;t['micro_set_f1']=2*t['tp']/(2*t['tp']+t['fp']+t['fn']);t['api_cost_usd']=str(sum((Decimal(c['api_cost_usd']) for c in cs),Decimal(0)))
 totals[method]=t
checks['checkpoints']=288;checks['method_trajectories']=len(case_results)
contrasts={k:sum(next(r['set_f1'] for r in case_results if r['trajectory']==t['trajectory'] and r['method']=='A2')-next(r['set_f1'] for r in case_results if r['trajectory']==t['trajectory'] and r['method']==k) for t in manifest['specification']['schedule'])/12 for k in ['B_ledger','A0']}
cost_ratio=Decimal(totals['A2']['api_cost_usd'])/Decimal(totals['A0']['api_cost_usd'])
result={'audit_date':'2026-09-12','execution_commit':commit,'candidate_commit':manifest['specification']['candidate_implementation_commit'],'manifest_sha256':sha(ROOT/'research/v2_1/comparison_v1.json'),'checks':checks,'totals':totals,'mean_paired_contrasts':contrasts,'a2_to_a0_api_cost_ratio':str(cost_ratio),'cases':case_results}
(OUT/'data/audit_results.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
with (OUT/'data/trajectory_scores.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=list(case_results[0]));w.writeheader();w.writerows(case_results)
with (OUT/'data/method_summary.csv').open('w') as f:
 w=csv.DictWriter(f,fieldnames=['method']+list(totals['A0']));w.writeheader();w.writerows(dict(method=k,**v) for k,v in totals.items())
print(json.dumps({k:v for k,v in result.items() if k!='cases'},ensure_ascii=False,indent=2))

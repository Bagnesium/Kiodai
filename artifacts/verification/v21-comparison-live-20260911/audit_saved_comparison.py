"""Read-only audit of a finished genuine comparison; no provider/transport calls."""
import hashlib, json, sqlite3, sys, zipfile
from collections import Counter
from datetime import datetime
from pathlib import Path
ROOT=Path.cwd().resolve()
assert (ROOT/'research/v2_1/comparison_v1.json').exists(), 'Run from the repository root'
sys.path.insert(0,str(ROOT))
from scripts.report_v21_comparison import analyze

def read(p): return json.loads(Path(p).read_text())
def rows(p): return [json.loads(s) for s in Path(p).read_text().splitlines()]
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
root=ROOT/'results/v2_1/comparison-v1'
study=read(root/'study.json')
assert study['status'] != 'running', 'Wait until runner finishes; do not snapshot an active study'
original=read(ROOT/'research/v2_1/live_comparison_v1_inventory.json')
assert digest(ROOT/original['archive'])==original['archive_sha256']
with zipfile.ZipFile(ROOT/original['archive']) as archive:
    assert set(archive.namelist())==set(original['files'])
    for name,value in original['files'].items():
        assert digest(ROOT/name)==value, 'Original recording changed: '+name
        assert hashlib.sha256(archive.read(name)).hexdigest()==value
prior_name='artifacts/verification/v21-comparison-funding-block-20260911/inventory.json'
with zipfile.ZipFile(ROOT/'artifacts/verification/v21-comparison-live-20260911/prior_funding_block_original.zip') as archive:
    assert archive.read(prior_name)==(ROOT/prior_name).read_bytes()
    prior=json.loads(archive.read(prior_name))
    for name,value in prior['files'].items(): assert hashlib.sha256(archive.read(name)).hexdigest()==value
frozen=read(ROOT/'research/v2_1/comparison_v1.json')
for name,value in frozen['hashes'].items(): assert digest(ROOT/name)==value,name
for name,value in {**frozen['preparation_evidence_hashes'],**frozen['provenance_evidence_hashes']}.items(): assert digest(ROOT/name)==value,name
assert read(root/'comparison_specification.json')==frozen['specification']
assert read(root/'config.json')==frozen['specification']['config']
assert read(root/'execution_provenance.json')['source_hashes']==frozen['hashes']
annotation=Path(sys.argv[1]) if len(sys.argv)>1 else None
report=analyze(root,annotation)
config=frozen['specification']['config']
request_ids=[];response_ids=[];response_costs={};kinds=Counter();all_responses=[];failures=[];request_bytes=[]
case_details=[]
for case in report['cases']:
    folder=root/case['trajectory']/case['method']
    if not (folder/'calls.jsonl').exists(): continue
    requests=[];responses=[]
    scenario=read(folder/'scenario.json')
    private_ids=[t['id'] for day in scenario['days'] for t in day['tasks']]+[z['id'] for day in scenario['days'] for z in day['steps']]
    def private_values(value):
        if isinstance(value,dict):
            for item in value.values(): yield from private_values(item)
        elif isinstance(value,list):
            for item in value: yield from private_values(item)
        elif isinstance(value,str) and value.startswith('private_'): yield value
    private_ids=list(set(private_ids+list(private_values(scenario))))
    for lineno,r in enumerate(rows(folder/'calls.jsonl'),1):
        if r['event']=='request':
            q=r['request'];request_ids.append(r['reservation']); requests.append(r);kinds[r['kind']]+=1
            assert r['mode']=='LIVE'
            serialized=json.dumps(q,ensure_ascii=False)
            assert all(identifier not in serialized for identifier in private_ids), 'Private evaluator identifier in model request'
            assert all(token not in serialized for token in ('due_task_ids','selected_task_ids','task_id_evaluator_only')), 'Private evaluator fields in model request'
            assert q['model']==config['model']['model_id'] and q['provider_route']==config['model']['route']
            assert q['provider_quantizations']==config['model']['quantizations']
            assert q['route_fallbacks_allowed'] is False and q['provider_require_parameters'] is True
            assert q['reasoning']==config['model']['reasoning']
            assert all(q[k]==v for k,v in config['sampling'].items())
            assert q['max_tokens']==config['output_tokens'][r['kind']]
            n=len(json.dumps(q,ensure_ascii=False).encode());request_bytes.append(n);assert n<=config['max_request_bytes']
            assert r['attempt'] in (1,2)
        else:
            responses.append(r);all_responses.append(r);response_ids.append(r['reservation'])
            cost=(r.get('provider') or {}).get('cost_usd_reported');response_costs[r['reservation']]=cost
            if r.get('raw_response') is not None:
                assert r['reported_model']==config['model']['model_id']
                assert r['provider']['provider_reported'].lower()==config['model']['route']
            if r['validation_error'] or r['transport_error']:
                failures.append({'trajectory':case['trajectory'],'method':case['method'],'checkpoint':r['checkpoint'],'kind':r['kind'],'attempt':r['attempt'],'stage':r['validation_stage'],'outcome':r['outcome'],'validation_error':r['validation_error'],'transport_error':r['transport_error'],'source':str((folder/'calls.jsonl').relative_to(ROOT))+':'+str(lineno)})
    case_details.append({'trajectory':case['trajectory'],'method':case['method'],'requests':len(requests),'responses':len(responses),'extract_responses':sum(r['kind']=='extract' for r in responses),'extract_attempts':sum(r['kind']=='extract' for r in requests),'selection_attempts':sum(r['kind'] in ('select','baseline') for r in requests),'outcomes':dict(Counter(r['outcome'] for r in responses))})
c=sqlite3.connect((root/'accounting.sqlite').resolve().as_uri()+'?mode=ro&immutable=1',uri=True)
account=c.execute('select ceiling from account').fetchall();attempts=c.execute('select id,reserved,reported,state from attempts order by id').fetchall();c.close()
assert account==[(20.0,)]
assert len(response_ids)==len(set(response_ids)) and set(response_ids)<=set(request_ids)
if study['status']=='completed': assert sorted(response_ids)==sorted(request_ids)
assert sorted(request_ids)==[r[0] for r in attempts] and len(request_ids)==len(set(request_ids))
for identifier,reserved,reported,state in attempts:
    expected=response_costs.get(identifier)
    assert reported==expected,(identifier,reported,expected)
    assert reported is None or reported <= reserved+1e-10
assert sum(a[1] for a in attempts)<=20+1e-10
assert len(report['cases'])==36
planned=[(b['trajectory'],m) for b in frozen['specification']['schedule'] for m in b['methods']]
observed=[(r['trajectory'],r['method']) for r in study['runs']]
assert observed==planned[:len(observed)], 'Unexpected method order or duplicate'
if study['status']=='completed':
    assert observed==planned
    assert all(c['primary_usable'] and c['completed_steps']==8 for c in report['cases'])
summary={}
for method in ('A0','B_ledger','A2'):
    cs=[c for c in report['cases'] if c['method']==method];usable=[c for c in cs if c.get('primary_usable')]
    x={'completed':len(usable),'mean_trajectory_set_f1':sum(c['set_f1'] for c in usable)/12 if len(usable)==12 else None,'micro':report['overall']['micro_aggregates'][method]['complete_case_micro_totals']}
    for key in ('model_calls','retries','invalid_responses','transport_errors','tool_queries','latency_seconds'):
        x[key]=sum(c.get(key,0) for c in cs)
    for key in ('input_tokens','output_tokens','api_response_cost_usd'):
        values=[c.get(key) for c in cs];x[key]=sum(values) if all(v is not None for v in values) else None
        method_responses=[r for c in cs for r in (rows(root/c['trajectory']/method/'calls.jsonl') if (root/c['trajectory']/method/'calls.jsonl').exists() else []) if r['event']=='response']
        x['known_'+key+'_subtotal']=sum((r.get('provider') or {}).get('cost_usd_reported') or 0 for r in method_responses) if key=='api_response_cost_usd' else sum((r.get('usage') or {}).get(key) or 0 for r in method_responses)
    for key in ('total_instructed_obligations','unique_obligations_ever_due','unique_obligations_blocked_at_trigger','completed_obligations','unfinished_including_canceled','unfinished_not_canceled','canceled_obligations'):
        values=[c.get('diagnostics',{}).get('obligations',{}).get(key) for c in cs]
        x[key]=sum(values) if all(v is not None for v in values) else None
    for key in ('extraction_accepted_empty_updates','extraction_accepted_operation_responses','task_executions','successful_simulator_receipts','failed_simulator_receipts','final_unresolved_intentions'):
        x[key]=sum(c.get('diagnostics',{}).get(key,0) for c in cs)
    x['validation_failure_stages']=dict(Counter(r['kind']+'/'+r['stage'] for r in failures if r['method']==method))
    x['retry_kinds']=dict(Counter(r['kind'] for c in cs for r in (rows(root/c['trajectory']/method/'calls.jsonl') if (root/c['trajectory']/method/'calls.jsonl').exists() else []) if r['event']=='request' and r['attempt']>1))
    x['semantic_finding_layers']=dict(Counter(f.get('layer','unspecified') for c in cs for f in c.get('diagnostics',{}).get('semantic_review',{}).get('findings',[])))
    x['query_channels']=dict(Counter(q['channel'] for c in cs for q in c.get('diagnostics',{}).get('queries',[])))
    x['hidden_categories']=dict(sum((Counter(c.get('diagnostics',{}).get('hidden_categories',{})) for c in cs),Counter()))
    x['fail_closed_checkpoints']=sum(len(c.get('diagnostics',{}).get('fail_closed_checkpoints',[])) for c in cs)
    x['semantic_reviewed_cases']=sum(c['diagnostics']['semantic_review'].get('status')=='reviewed' for c in cs)
    x['semantic_review_findings']=dict(sum((Counter(f['category'] for f in c['diagnostics']['semantic_review'].get('findings',[])) for c in cs),Counter()))
    x['quarantined_case_count']=sum(bool(c.get('diagnostics',{}).get('quarantined_snapshots',[])) for c in cs)
    x['quarantined_snapshots']=sum(len(c.get('diagnostics',{}).get('quarantined_snapshots',[])) for c in cs)
    x['created_intentions']=sum(sum(e['kind']=='create' for e in c.get('diagnostics',{}).get('ledger_changes',[])) for c in cs)
    summary[method]=x
output={'status':study['status'],'started_at_utc':study['started_at_utc'],'finished_at_utc':study.get('finished_at_utc'),'matched_blocks':sum(all(next(c for c in report['cases'] if c['trajectory']==b['trajectory'] and c['method']==m).get('primary_usable') for m in b['methods']) for b in frozen['specification']['schedule']), 'verification':{'original_recording_files':len(original['files']),'original_archive_and_tree_unchanged':True,'prior_funding_record_archive_verified':True,'frozen_files':len(frozen['hashes']),'preparation_files':len(frozen['preparation_evidence_hashes']),'provenance_files':len(frozen['provenance_evidence_hashes']),'request_accounting_reconciles':True,'pinned_requests_and_responses_verified':True,'official_scores_and_case_hashes_reproduce':True,'frozen_order_verified':True,'maximum_request_bytes':max(request_bytes,default=0)},'methods':summary,'paired':report['overall']['comparisons'],'families':report['families'],'smoke_overlap':report['smoke_overlap'],'request_kinds':dict(kinds),'case_call_details':case_details,'failures':failures,'accounting':{'ceiling_usd':20,'attempts':len(attempts),'reserved_usd':sum(r[1] for r in attempts),'api_reported_subtotal_usd':sum(r[2] for r in attempts if r[2] is not None),'unknown_cost_attempts':sum(r[2] is None for r in attempts),'verified_billed_cost_usd':None},'limitations':'Saved-response cost reconciles with study ledger, not independent billing. Semantic review is AI-assisted; no independent annotator. Exposed development cases, four dependent families, one repeat, non-compute-matched; descriptive contrasts only.'}
print(json.dumps(output,indent=2))

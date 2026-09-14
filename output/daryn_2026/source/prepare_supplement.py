import csv,json,hashlib,shutil,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3];OUT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from sim import pm_bench as PM
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rows(p):return [json.loads(x) for x in p.read_text().splitlines() if x.strip()]
manifest=json.loads((ROOT/'research/v2_1/comparison_v1.json').read_text())
for p,sha in manifest['hashes'].items():
 src=ROOT/p;assert h(src)==sha;dest=OUT/'supplement/frozen'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
for p in ['research/v2_1/comparison_v1.json','research/v2_1/live_comparison_v1_inventory.json','research/v2_1/extraction.schema.json']:
 dest=OUT/'supplement'/p;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/p,dest)
historical=[]
for f in ['RESULTS.json','FOLLOWUP_RESULTS.json']:
 for r in json.loads((ROOT/f).read_text())['runs']:
  folder=Path(r['_path']).parent;mf=json.loads((folder/'manifest.json').read_text());bad=[name for name,sha in mf['artifact_sha256'].items() if h(folder/name)!=sha];assert not bad
  sc=json.loads((folder/'scenario.json').read_text());score=json.loads(json.dumps(PM.score_log(sc,rows(folder/'actions.jsonl'))));saved=json.loads((folder/'score.json').read_text())
  assert score[0]==saved["summary"] and score[1]==saved["per_day"] and score[2]==saved["summary_steps"]
  z=score[0];tp,fp,fn=[z['set_'+k] for k in ['tp','fp','fn']]
  historical.append({'summary':f,'method':r['condition'],'folder':str(folder.relative_to(ROOT)),'artifact_hashes_verified':len(mf['artifact_sha256']),'tp':tp,'fp':fp,'fn':fn,'set_f1':2*tp/(2*tp+fp+fn),'input_tokens':r['token_usage']['input_tokens']})
smoke=ROOT/'results/v2_1/deepseek-smoke-v1/v2_hidden_91320/A2'
s=json.loads((smoke/'scenario.json').read_text());score=json.loads(json.dumps(PM.score_log(s,rows(smoke/'actions.jsonl'))));assert score==json.loads((smoke/'score.json').read_text());steps=rows(smoke/'steps.jsonl')
historical.append({'study':'v2.1 development smoke','official_counts':{k:score[0]['set_'+k] for k in ['tp','fp','fn']},'queries':sum(len(s['tools']) for s in steps),'successful_receipts':sum(e['outcome']=='simulator_completed' for s in steps for e in s['execution'])})
(OUT/'data/historical_audit.json').write_text(json.dumps(historical,ensure_ascii=False,indent=2))
claims=[
('Registered title and identity','author-provided; original manuscript','Downloads/Kiodai_Bagdat_Beimzhan.docx; current request','Title page','Preserved; no independent school registration verification'),
('Formatting limits','direct source','Downloads/Telegram Desktop/1_Правила_оформления_научных_проектов_для_учащихся_—_копия_1.docx','Entire document','Font and margins are editorial choices'),
('PM-Bench environment and existing ledger','original publication verified','https://arxiv.org/abs/2607.12385v1; PDF sections 3–4','1, 2.1','Borrowed environment; local scenarios are exposed'),
('Virtual Week paradigm','publisher record verified','https://onlinelibrary.wiley.com/doi/10.1002/acp.770','2.1','Issue 2000; online 2001; no human/LLM causal equivalence'),
('TriggerBench matched controls','original publication verified','https://arxiv.org/html/2606.23459v1 sections 3–4','2.2','Different metrics; no head-to-head score comparison'),
('MemoryAgentBench four abilities','original abstract verified','https://arxiv.org/abs/2507.05257v4','2.2','Not MemBench 2506.21605'),
('PIS operators','original paper verified','https://arxiv.org/pdf/2609.01272v1 section 3','2.2','Reconstruction, not faithful replication'),
('Shared B_ledger/A2 lifecycle','evaluated code verified','kiodai_v2/agent.py:54–146; kiodai_v2/store.py:94–174 at cd0ce89','3','Difference is query policy; meaning not fully enforced'),
('Frozen model, counts and settings','raw records and manifest verified','research/v2_1/comparison_v1.json; calls.jsonl in 36 folders','4.1','Provider execution not independently observable'),
('Fail-closed boundary','evaluated code and records verified','kiodai_v2/agent.py; kiodai_v2/gateway.py; research_harness/runner.py','4.2','Not universal proof of zero leakage'),
('Primary and micro scores','independent deterministic recalculation','data/audit_results.json; source/audit_evidence.py; raw score.json/actions.jsonl','5.2','No uncertainty estimate or significance claim'),
('Primary and secondary paired differences','recomputed from full trajectory values','data/trajectory_scores.csv; data/audit_results.json','5.2','Not subtracted from rounded means'),
('Historical A0/A1 equality','raw scores replayed; artifact hashes verified','data/historical_audit.json; RESULTS.json; FOLLOWUP_RESULTS.json','5.1','Separate pilots, baseline ceiling, exposed follow-up'),
('Successful development smoke','raw scores and steps verified','results/v2_1/deepseek-smoke-v1/v2_hidden_91320/A2','5.1','One functionality check, not superiority'),
('API resources and 4.91 cost ratio','raw usage/cost sums verified','calls.jsonl; data/audit_results.json','5.3','API-reported, not independent billed cost'),
('Query-supported hits','record-based post-run diagnostic','comparison_report_reviewed.json hidden_opportunities; kiodai_v2/report.py','5.3','Evidence support is not causal proof'),
('27 versus 24 reconciliation','evaluator state replay verified','scenario.json/steps.jsonl; obligation_diagnostics; data/audit_results.json','5.3','Three official cancellations; erroneous ledger cancels differ'),
('A0 blocked count 0','new deterministic calculation on old records','data/audit_results.json','5.3','Replaces missing summary cell, not assumed zero'),
('Missing prereq and failed positive selection','key raw trace verified, semantic annotation assisted','v2_hidden_91320/A2/calls.jsonl:2,4,6,8,10,14; steps.jsonl:1–7','6','No independent human review'),
('Stored correct day; wrong execution','key raw trace verified','v2_cross_day_91331/A2/steps.jsonl:3,7; calls.jsonl:16,18','6','Observed noncompletion, not proof failed status alone prevents retry'),
('Stale deadline accepted','key raw trace verified','v2_revision_91300/A2/steps.jsonl:6–7; calls.jsonl:22,24,26,28','6','All 16 validation flags clear'),
('Superseded visible trigger returns','reported AI semantic annotation','semantic_review.json for A2 visible_events_91310 and B_ledger visible_events','6 table 7','Not a new independent semantic reannotation'),
('Semantic error propagation','interpretation','Cases above; hypothesis in discussion','6.2','No causal intervention performed'),
('Author contribution and AI assistance','author manuscript plus interaction record','Original manuscript; project requests; semantic review metadata','Abstracts, 7','Independence not certified by git metadata'),
('Reference extraction diagnostic','unperformed proposal','Conclusion of this manuscript','8','Only information revealed so far; not deployable or upper bound'),
]
with (OUT/'data/source_claims.csv').open('w') as f:
 w=csv.writer(f);w.writerow(['claim','evidence_status','source_or_locator','manuscript_location','limit']);w.writerows(claims)
index={'copied_frozen_files':manifest['hashes'],'execution_commit':'cd0ce89e10d036918d1af06e5f5f2140930a0981','candidate_commit':manifest['specification']['candidate_implementation_commit'],'note':'Exact unmodified files. Historical status/authorization fields in copied manifest are preserved. Actual completion established by original inventory and raw run. No credentials included.'}
(OUT/'supplement/index.json').write_text(json.dumps(index,ensure_ascii=False,indent=2))
print('Historical and smoke audit verified; copied',len(manifest['hashes']),'frozen files; claims',len(claims))

#!/usr/bin/env python3
"""Usage-informed projection; no requests, credentials or inference."""
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import rows,dump,digest
from scripts.run_v2 import ROOT,preflight


def estimate(study):
    config,_,guard=preflight(False)
    pilot=ROOT/'results/kiodai/live-pair-42433e00474b'
    calls=[r for p in pilot.glob('live-*/raw_model_calls.jsonl') for r in rows(p)]
    inputs=sum(r['usage']['input_tokens'] for r in calls)
    request_bytes=sum(len(json.dumps(r['request'],ensure_ascii=False).encode()) for r in calls)
    ratio=inputs/request_bytes
    baseline_output=sum(r['usage']['output_tokens'] for r in calls)/len(calls)
    source=Path(study).resolve()
    result={'source_pilot':str(pilot.relative_to(ROOT)),'pilot_input_tokens':inputs,'pilot_request_bytes':request_bytes,
            'pilot_tokens_per_request_byte':ratio,'baseline_output_tokens_per_call':baseline_output,
            'assumptions':{'input_growth_margin':1.35,'extraction_output_tokens_per_call':750,
                           'structured_selection_output_tokens_per_call':256,'validation_retries_in_projection':0,
                           'extra_model_query_cycles_per_comparator':3,'extra_query_request_bytes':12000,
                           'cache_discount':0,'longer_scenario_policy':'Uses actual v2 mock request sizes, not pilot per-trajectory cost.'},
            'methods':{},'conservative_allowance_usd':guard['conservative_allowance_usd'],
            'proposed_budget_usd':guard['proposed_budget_usd'],'api_response_cost_usd':None,'verified_billed_cost_usd':None}
    for method in config['methods']:
        requests=[r for p in source.glob('*/'+method+'/calls.jsonl') for r in rows(p) if r['event']=='request']
        projected_input=sum(len(json.dumps(r['request'],ensure_ascii=False).encode()) for r in requests)*ratio*1.35
        projected_output=sum(750 if r['kind']=='extract' else 256 if r['kind']=='select' else baseline_output for r in requests)
        extras=3 if method in ('A0','B_ledger') else 0
        projected_input+=extras*12000*ratio*1.35
        projected_output+=extras*(baseline_output if method=='A0' else 256)
        price=config['model']['pricing_usd_per_million_tokens']
        result['methods'][method]={'projected_calls':len(requests)+extras,'projected_input_tokens':round(projected_input),
                                  'projected_output_tokens':round(projected_output),
                                  'projected_uncached_cost_usd':(projected_input*price['input']+projected_output*price['output'])/1e6}
    result['usage_informed_projection_usd']=sum(v['projected_uncached_cost_usd'] for v in result['methods'].values())
    result['projection_input_artifact_hashes']={str(p.relative_to(ROOT)):digest(p.read_bytes()) for p in source.glob('*/*/calls.jsonl')}
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--study',type=Path,default=Path('results/v2/development/verified-mechanics'))
    args=parser.parse_args();result=estimate(args.study)
    dump(ROOT/'research/v2/cost_projection.json',result)
    print(json.dumps(result,indent=2))

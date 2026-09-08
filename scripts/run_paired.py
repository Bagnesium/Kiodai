#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research_harness.paired import Pair, catalog, configs, estimate_pair
from research_harness.live import Budget
from research_harness.model_gateway import safe_error


def main():
    p=argparse.ArgumentParser(description='Matched Kiodai pilot. Defaults to zero-cost MOCK.')
    p.add_argument('--suite',choices=['demo','pilot','development'],default='demo')
    p.add_argument('--scenario',default='time',help='Demo scenario ID, or all')
    p.add_argument('--live',action='store_true');p.add_argument('--budget-usd',type=float)
    p.add_argument('--repeats',type=int,default=1);p.add_argument('--preflight',action='store_true')
    p.add_argument('--output-root',default='results/kiodai')
    args=p.parse_args()
    if not 1<=args.repeats<=3:p.error('Use 1–3 repeats for this small pilot.')
    mode='LIVE' if args.live else 'MOCK'
    ids=[s['id'] for s in catalog()] if args.suite=='demo' and args.scenario=='all' else [args.scenario]
    try:
        if args.preflight:
            cfg,_=configs(args.suite,ids[0],'LIVE')
            print(json.dumps(estimate_pair(cfg),indent=2));return 0
        budget=Budget(args.budget_usd,configs(args.suite,ids[0],'LIVE')[0]['A0']['model']['pricing_usd_per_million_tokens']) if args.live else None
        for scenario in ids:
            for repeat in range(args.repeats):
                pair=Pair(suite=args.suite,scenario_id=scenario,mode=mode,live=args.live,budget_usd=args.budget_usd,budget=budget,repeat=repeat,output_root=args.output_root)
                try:
                    while pair.plan['status']=='running':pair.advance()
                except KeyboardInterrupt:pair.interrupt('KeyboardInterrupt')
                print(f'{mode} {pair.plan["status"]}: {pair.path / "pair.json"}')
                if pair.plan['status']!='completed':return 1
        return 0
    except Exception as exc:
        print(safe_error(exc),file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())

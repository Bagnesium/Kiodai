#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from research_harness.analysis import analyze, report


def main():
    p=argparse.ArgumentParser(description='Reconstruct official results from saved artifacts; never pool mock and live.')
    p.add_argument('--root',default='results/kiodai');p.add_argument('--mode',choices=['MOCK','LIVE'],default='LIVE')
    p.add_argument('--output',default=None);a=p.parse_args()
    result=analyze(a.root,a.mode)
    output=Path(a.output or ('RESULTS.md' if a.mode=='LIVE' else 'MOCK_RESULTS.md'))
    output.write_text(report(result));output.with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
    print(output.resolve())
if __name__=='__main__':main()

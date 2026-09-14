#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kiodai_v2.dashboard import serve

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Read-only v2 extension of the Kiodai dashboard; makes no inference calls.')
    parser.add_argument('--study',type=Path,default=Path('results/v2/mock-verification-v2'))
    parser.add_argument('--port',type=int,default=8767)
    args=parser.parse_args()
    serve(args.study,args.port)

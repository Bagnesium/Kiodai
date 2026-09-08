#!/usr/bin/env python3
"""Save real command output and exit nonzero on any failed required local check."""
import json
import subprocess
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'artifacts/verification'
OUT.mkdir(parents=True,exist_ok=True)
checks=[
 ('integrity.txt',[sys.executable,'scripts/verify_benchmark_integrity.py']),
 ('development-integrity.txt',[sys.executable,'scripts/verify_development_suite.py']),
 ('tests.txt',[sys.executable,'-m','unittest','discover','-s','tests','-v']),
 ('compile.txt',[sys.executable,'-m','compileall','-q','research_harness','scripts','tests']),
 ('smoke.txt',['bash','scripts/run_smoke_test.sh']),
 ('demo-cli.txt',[sys.executable,'scripts/run_paired.py','--suite','demo','--scenario','all']),
 ('pilot-mock.txt',[sys.executable,'scripts/run_paired.py','--suite','pilot']),
 ('pilot-preflight.json',[sys.executable,'scripts/run_paired.py','--suite','pilot','--preflight']),
 ('development-preflight.json',[sys.executable,'scripts/run_paired.py','--suite','development','--preflight']),
 ('mock-analysis.txt',[sys.executable,'scripts/analyze_results.py','--root','results/kiodai','--mode','MOCK','--output','MOCK_RESULTS.md']),
 ('live-analysis.txt',[sys.executable,'scripts/analyze_results.py','--root','results/kiodai','--mode','LIVE','--output','RESULTS.md']),
]
summary=[]
for filename,command in checks:
    result=subprocess.run(command,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (OUT/filename).write_text(result.stdout)
    summary.append({'command':command,'exit_code':result.returncode,'output':filename})
    print(f'{filename}: {"PASS" if result.returncode==0 else "FAIL"}',flush=True)
    if result.returncode:break
(OUT/'commands.json').write_text(json.dumps(summary,indent=2)+'\n')
raise SystemExit(int(any(c['exit_code'] for c in summary)))

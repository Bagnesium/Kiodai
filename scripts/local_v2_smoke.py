#!/usr/bin/env python3
"""One real local development smoke, separately labeled; never a paid-model substitute."""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kiodai_v2.local import LocalTransport, MODEL
from kiodai_v2.runner import run_case, ROOT
from kiodai_v2.common import dump
from kiodai_v2.report import report


def main():
    root=ROOT/'results/v2/local-smoke-v2'
    root.mkdir(parents=True,exist_ok=False)
    config=json.loads((ROOT/'configs/v2.json').read_text())
    config['model']={**config['model'],'provider':'ollama-local','model_id':MODEL,'route':'localhost',
                     'base_url':'http://127.0.0.1:11434','api_key_env':None}
    # One intact existing development trajectory; no condition comparison or repetition.
    case='v2_hidden_91320'
    study={'mode':'LOCAL_MODEL','status':'starting','methods':['A2'],
           'runs':[{'folder':case+'/A2','method':'A2','family':'hidden','trajectory':case}],
           'purpose':'real local development smoke; exposed case; not the frozen research backend'}
    dump(root/'study.json',study)
    try:
        transport=LocalTransport()
        dump(root/'local_backend.json',transport.metadata)
        run_case(ROOT/f'data/v2/{case}.json','A2',root/case/'A2',config,transport,'LOCAL_MODEL')
        study['status']='completed'
    except BaseException as exc:
        study.update(status='interrupted',blocker=str(exc))
        raise
    finally:
        dump(root/'study.json',study)
        report(root)
    print(root/'report.md')


if __name__=='__main__':main()

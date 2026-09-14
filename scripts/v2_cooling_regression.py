#!/usr/bin/env python3
"""MOCK-only known cooling regression over the intact original 20-step development story.

This deliberately narrow semantic fixture extracts only the cooling intention. Other
tasks remain in the environment and are scored, including misses. It is not a method
comparison or a full-competence language model.
"""
import json
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kiodai_v2.fixture import FixtureTransport, record
from kiodai_v2.common import dump
from kiodai_v2.runner import ROOT, run_case
from kiodai_v2.report import report
from research_harness.model_gateway import TransportResponse


class CoolingFixture(FixtureTransport):
    def invoke(self, request, timeout_seconds):
        if request['response_format']['json_schema']['name'] != 'extract':
            return super().invoke(request, timeout_seconds)
        data=json.loads(request['messages'][-1]['content'])
        operations=[]
        if not data['intentions']:
            for ref, source in data['observations'].items():
                for line in source['text'].splitlines():
                    if line == '- Acknowledge cooling only when the sensor board reports fully stable cooling.':
                        rec=record('Acknowledge stable cooling.','hidden','Cooling is now fully stable.','sensor_board',None,line,ref)
                        operations.append({'kind':'create','target':None,'expected_version':None,
                                           'record':rec,'sources':[{'ref':ref,'quote':line}]})
        value={'operations':operations};raw=json.dumps(value)
        return TransportResponse(raw,{'mock':True,'fixture':'known-cooling-only-regression','content':value},
                                 {'input_tokens':len(json.dumps(request))//4,'output_tokens':len(raw)//4},
                                 'mock-fixture',{'transport':'MOCK','cost_usd_reported':None})


def main():
    root=ROOT/'results/v2/known-cooling-regression-v2'
    root.mkdir(parents=True,exist_ok=False)
    config=json.loads((ROOT/'configs/v2.json').read_text())
    config['max_request_bytes']=96000  # MOCK development allowance; never used by the frozen LIVE study
    study={'mode':'MOCK','status':'running','methods':['A2'],
           'runs':[{'trajectory':'known-original-followup','family':'inspected-historical-regression',
                    'method':'A2','folder':'original/A2'}],
           'scope':'Intact original 20-step story. Cooling-only mocked semantics; all other errors retained. Not a comparator result.'}
    dump(root/'study.json',study)
    try:
        run_case(ROOT/'data/development/prospective_memory_dev_v1.json','A2',root/'original/A2',config,CoolingFixture())
        study['status']='completed'
    finally:
        dump(root/'study.json',study)
        report(root)
    print(root/'report.md')


if __name__=='__main__':main()

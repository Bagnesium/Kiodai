#!/usr/bin/env python3
"""Exercise the already-running loopback demo API in MOCK mode only."""
import io
import json
import zipfile
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
BASE='http://127.0.0.1:8765'
OUT=Path(__file__).resolve().parents[1]/'artifacts/verification'
OUT.mkdir(parents=True,exist_ok=True)

def call(endpoint,payload=None):
    headers={'Content-Type':'application/json','X-Kiodai-Demo':'1'}
    data=json.dumps(payload).encode() if payload is not None else None
    with urlopen(Request(BASE+'/api/'+endpoint,data=data,headers=headers),timeout=10) as response:
        return json.load(response)

def main():
    if call('state')['live_enabled']:
        raise SystemExit('Use the default offline server for this verification script.')
    evidence=[]
    for item in call('catalog')['scenarios']:
        state=call('start',{'mode':'MOCK','scenario':item['id']})
        try:call('reveal',{'index':0});raise AssertionError('Premature reveal was accepted')
        except HTTPError as error:assert error.code==400
        while state['status']=='running':state=call('next',{})
        assert state['status']=='completed',state
        evaluation=call('reveal',{'index':state['visible_steps']-1})
        assert evaluation['mode']=='MOCK'
        evidence.append({'scenario':item['id'],'pair_id':state['pair_id'],'steps':state['visible_steps'],'status':state['status'],'reveal_gate':'passed'})
    with urlopen(BASE+'/api/export') as response:blob=response.read()
    archive=zipfile.ZipFile(io.BytesIO(blob))
    assert b'MOCK' in archive.read('EXPORT_MODE.txt')
    assert not any(name.endswith(('.pages','.docx')) for name in archive.namelist())
    (OUT/'demo-export.zip').write_bytes(blob)
    state=call('reset',{});assert state['has_run'] is False
    try:call('start',{'mode':'LIVE','scenario':'time','confirm_live':True});raise AssertionError('Unenabled live call accepted')
    except HTTPError as error:assert error.code==400
    result={'mode':'MOCK','scenarios':evidence,'export_bytes':len(blob),'export_files':len(archive.namelist()),'reset':'passed','live_disabled_gate':'passed','genuine_recordings':len(call('state')['recordings'])}
    (OUT/'http-demo.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()

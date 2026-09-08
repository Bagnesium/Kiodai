"""Explicit scripted software fixture, identical for A0 and A1; no evaluator access."""
import json
import re
from .model_gateway import TransportResponse


class DemoTransport:
    mode = 'MOCK'
    def __init__(self, script):
        self.script = script

    def invoke(self, request, timeout_seconds):
        # Only the supplied agent-visible conversation and action schema are read.
        users=[m['content'] for m in request['messages'] if m['role']=='user']
        step=next((s for s in reversed(users) if 'Step action menu' in s),'')
        menu=dict((text.strip(),handle) for handle,text in re.findall(r'^- (task_\d+): (.+)$',step,re.M))
        times=re.findall(r'Time: (\d\d:\d\d)',step)
        clock=times[-1] if times else ''
        output={'action':'choose','choice':'A','task_ids':[], 'channel':'NONE'}
        if 'A new teacher bulletin arrives.' in step and users[-1]==step:
            output.update(action='query_state',choice='NONE',channel='teacher_feed')
        else:
            texts=self.script.get(clock,[])
            if 'ABSTRACT ACCEPTED.' in users[-1] and users[-1]!=step:
                texts=['Submit the revised abstract.']
            output['task_ids']=[menu[text] for text in texts if text in menu]
        raw=json.dumps(output)
        return TransportResponse(raw,{'mock':True,'fixture':'educational-script-v1','content':raw},{},'mock/educational-script-v1',{'network':False,'transport':'scripted-demo'})


class StressTransport:
    """Upper-growth software preflight: query once per step, correct once per call."""
    def __init__(self):self.index=0
    def invoke(self,request,timeout_seconds):
        slot=self.index%4;self.index+=1
        if slot in (0,2):raw='x'*1024
        else:
            channels=request['response_format']['json_schema']['schema']['properties']['channel']['enum']
            channel=next((c for c in channels if c not in ['NONE','clock']),'clock')
            action={'action':'query_state','choice':'NONE','task_ids':[],'channel':channel} if slot==1 else {'action':'choose','choice':'A','task_ids':[],'channel':'NONE'}
            raw=json.dumps(action).ljust(1024)
        return TransportResponse(raw,{'mock':True,'stress_preflight':True,'content':raw},{},'mock/stress-v1',{'network':False})

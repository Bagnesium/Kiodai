"""Loopback-only thin dashboard over Pair/RunSession. No browser credentials."""
from __future__ import annotations
import argparse
import io
import json
import threading
import zipfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .paired import Pair, catalog, ROOT
from .analysis import rows, verify_run
from .live import Budget
from .model_gateway import RunStopped, safe_error

EXPORT_FILES={'manifest.json','config.json','scenario.json','system_prompt.txt','raw_model_calls.jsonl','failures.jsonl','actions.jsonl','steps.jsonl','evaluator.jsonl','score.json','baseline_template.txt','addendum.txt'}


class Dashboard:
    def __init__(self,root=None,live=False,budget_usd=None):
        self.root=Path(root or ROOT/'results/kiodai').resolve();self.root.mkdir(parents=True,exist_ok=True)
        self.live=live;self.budget_usd=budget_usd
        self.budget=Budget(budget_usd,{'input':0.27,'output':1.0}) if live else None
        self.pair=None;self.replay=None;self.cursor=0
        self.lock=threading.Lock()

    def recordings(self):
        results=[]
        for path in sorted(self.root.glob('*/pair.json')):
            plan=json.loads(path.read_text())
            if plan.get('mode')=='LIVE' and plan.get('status')=='completed':
                try:
                    if len(plan['runs'])!=2:continue
                    for name in plan['runs'].values():
                        folder=self.child(path.parent,name);m=verify_run(folder)
                        calls=rows(folder/'raw_model_calls.jsonl')
                        if m['mode']!='LIVE' or not calls or any(c.get('raw_response',{}).get('mock') for c in calls if isinstance(c.get('raw_response'),dict)):
                            raise ValueError('Not a genuine live artifact')
                    results.append({'id':path.parent.name,'title':plan['scenario_id']+' · '+plan['pair_id']})
                except (ValueError,KeyError,FileNotFoundError):continue
        return results

    def child(self,parent,name):
        path=(parent/name).resolve()
        if path.parent!=parent.resolve():raise ValueError('Invalid artifact path')
        return path

    def reset(self):
        if self.pair:self.pair.interrupt('User reset the dashboard')
        self.pair=None;self.replay=None;self.cursor=0

    def start(self,data):
        if data.get('mode')=='LIVE' and (not self.live or data.get('confirm_live') is not True):
            raise RunStopped('LIVE is disabled. Restart the server with --live --budget-usd 0.30, then explicitly opt in in the interface.')
        self.reset()
        self.pair=Pair(suite='demo',scenario_id=data.get('scenario','time'),mode=data.get('mode','MOCK'),
                       output_root=self.root,live=self.live,budget_usd=self.budget_usd,budget=self.budget)

    def load_replay(self,identifier):
        if identifier not in {r['id'] for r in self.recordings()}:raise ValueError('No genuine saved LIVE pair with that ID')
        self.reset();self.replay=self.child(self.root,identifier);self.cursor=0

    def next(self):
        if self.pair:self.pair.advance()
        elif self.replay:self.cursor+=1
        else:raise ValueError('Start or open a run first')

    def current(self):
        if self.pair:return self.pair.path,self.pair.plan,None
        if self.replay:return self.replay,json.loads((self.replay/'pair.json').read_text()),self.cursor
        return None,None,None

    def state(self):
        path,plan,cursor=self.current()
        state={'mode':'RECORDED' if self.replay else self.pair.mode if self.pair else 'MOCK',
               'live_enabled':self.live,'has_run':bool(plan),'recordings':self.recordings(),
               'notice':'No genuine saved A0/A1 runs are available.' if not self.recordings() else '', 'conditions':{}}
        if not plan:return state
        state.update(pair_id=plan['pair_id'],status=plan['status'],source_mode=plan['mode'],scenario=plan['scenario_id'],
                     interruption_reason=plan.get('interruption_reason'),total_steps=0)
        for condition,name in plan['runs'].items():
            folder=self.child(path,name);manifest=json.loads((folder/'manifest.json').read_text())
            steps=rows(folder/'steps.jsonl');calls=rows(folder/'raw_model_calls.jsonl')
            visible=steps if cursor is None else steps[:cursor]
            keys={(s['day'],s['step_id']) for s in visible}
            visible_calls=[c for c in calls if (c['call_context']['day'],c['call_context']['step_id']) in keys]
            # Canonical task IDs are evaluator-only in the dashboard too.
            clean_steps=[]
            for s in visible:
                s=json.loads(json.dumps(s));s['action'].pop('task_ids',None);clean_steps.append(s)
            state['conditions'][condition]={'steps':clean_steps,'calls':visible_calls,'run_id':manifest['run_id'],
                'status':manifest['status'],'prompt_hash':manifest['prompt_hash'],'model':manifest['exact_model_id'],
                'provider':manifest['provider_route'],'reported_cost_usd':manifest['reported_cost_usd'],
                'retry_count':manifest['retry_count'],'invalid_attempt_count':manifest['invalid_attempt_count'],
                'token_usage':manifest['token_usage'],'interruption_reason':manifest.get('interruption_reason')}
            state['total_steps']=max(state['total_steps'],manifest['total_steps'])
        state['visible_steps']=min((len(v['steps']) for v in state['conditions'].values()),default=0)
        if self.replay:state['status']='completed' if state['visible_steps']>=state['total_steps'] else 'replaying'
        return state

    def reveal(self,index):
        path,plan,cursor=self.current()
        if not plan or not isinstance(index,int) or index<0:raise ValueError('Select a completed step')
        result={'mode':'RECORDED' if self.replay else plan['mode'],'label':'Evaluator visualization — not model internal memory','conditions':{}}
        for condition,name in plan['runs'].items():
            evaluations=rows(self.child(path,name)/'evaluator.jsonl')
            if index>=len(evaluations) or (cursor is not None and index>=cursor):raise ValueError('Response is not fixed/visible yet')
            result['conditions'][condition]=evaluations[index]
        return result

    def export(self):
        path,plan,_=self.current()
        if not plan:raise ValueError('No run to export')
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w',zipfile.ZIP_DEFLATED) as archive:
            export_mode='RECORDED' if self.replay else plan['mode']
            archive.writestr('EXPORT_MODE.txt',f'{export_mode}\nSource mode: {plan["mode"]}\nLocal research artifact; contains synthetic scenarios only.\n')
            archive.writestr('pair.json',json.dumps(plan,indent=2))
            for name in plan['runs'].values():
                folder=self.child(path,name)
                for filename in sorted(EXPORT_FILES):
                    file=folder/filename
                    if file.is_file():archive.writestr(name+'/'+filename,file.read_bytes())
        return stream.getvalue()


def serve(host='127.0.0.1',port=8765,**kwargs):
    app=Dashboard(**kwargs)
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args):pass
        def response(self,code,body,kind='application/json'):
            if not isinstance(body,bytes):body=json.dumps(body,ensure_ascii=False).encode()
            self.send_response(code);self.send_header('Content-Type',kind);self.send_header('Content-Length',str(len(body)))
            self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
            self.send_header('Content-Security-Policy',"default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; frame-ancestors 'none'")
            self.end_headers();self.wfile.write(body)
        def trusted(self):
            expected=f'{host}:{self.server.server_port}'
            return self.headers.get('Host')==expected and self.headers.get('Origin',f'http://{expected}')==f'http://{expected}'
        def do_GET(self):
            if not self.trusted():return self.response(403,{'error':'Loopback same-origin requests only'})
            path=urlparse(self.path).path
            try:
                if path=='/api/catalog':return self.response(200,{'scenarios':[{k:v for k,v in s.items() if k in ['id','title','provenance']} for s in catalog()]})
                with app.lock:
                    if path=='/api/state':return self.response(200,app.state())
                    if path=='/api/export':return self.response(200,app.export(),'application/zip')
                files={'/':'index.html','/app.js':'app.js','/style.css':'style.css'}
                if path in files:
                    filename=files[path];kind={'html':'text/html; charset=utf-8','js':'text/javascript; charset=utf-8','css':'text/css; charset=utf-8'}[filename.split('.')[-1]]
                    return self.response(200,(ROOT/'demo'/filename).read_bytes(),kind)
                self.response(404,{'error':'Not found'})
            except Exception as exc:self.response(400,{'error':safe_error(exc)})
        def do_POST(self):
            if not self.trusted() or self.headers.get('X-Kiodai-Demo')!='1' or self.headers.get('Content-Type')!='application/json':
                return self.response(403,{'error':'Same-origin JSON request required'})
            try:
                size=int(self.headers.get('Content-Length','0'))
                if not 0<size<=8192:raise ValueError('Invalid request size')
                data=json.loads(self.rfile.read(size));path=urlparse(self.path).path
                with app.lock:
                    if path=='/api/start':app.start(data)
                    elif path=='/api/next':app.next()
                    elif path=='/api/reset':app.reset()
                    elif path=='/api/replay':app.load_replay(data['id'])
                    elif path=='/api/reveal':return self.response(200,app.reveal(data['index']))
                    else:return self.response(404,{'error':'Not found'})
                    self.response(200,app.state())
            except Exception as exc:self.response(400,{'error':safe_error(exc)})
    server=ThreadingHTTPServer((host,port),Handler)
    print(f'Kiodai local dashboard: http://{host}:{server.server_port} — default MOCK',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:app.reset()
    finally:server.server_close()


def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8765)
    p.add_argument('--live',action='store_true');p.add_argument('--budget-usd',type=float)
    p.add_argument('--output-root',default=None);a=p.parse_args()
    serve(port=a.port,live=a.live,budget_usd=a.budget_usd,root=a.output_root)
if __name__=='__main__':main()

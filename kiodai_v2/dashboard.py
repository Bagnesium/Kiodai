"""Read-only extension of the existing dashboard, using its unchanged stylesheet."""
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs
from .common import rows
from .runner import verify_case, ROOT


class Viewer:
    def __init__(self, study):
        self.root = Path(study).resolve()
        self.study = json.loads((self.root/'study.json').read_text())
        self.runs = {(r['trajectory'], r['method']): r for r in self.study['runs']}

    def catalog(self):
        return {'source_mode': self.study['mode'], 'status': self.study['status'],
                'mode': 'RECORDED' if self.study['mode'] == 'LIVE' else self.study['mode'],
                'methods': self.study['methods'], 'trajectories': list(dict.fromkeys(k[0] for k in self.runs)),
                'inference_enabled': False}

    def inspect(self, trajectory, method, index, evaluator=False):
        item = self.runs[(trajectory, method)]
        folder = (self.root/item['folder']).resolve()
        if not folder.is_relative_to(self.root):
            raise ValueError('Invalid recording path')
        manifest = verify_case(folder)
        steps = rows(folder/'steps.jsonl')
        if index < 0 or index >= len(steps):
            raise ValueError('Only completed steps may be inspected')
        step = steps[index]
        if evaluator:
            return {'label': 'EVALUATOR ONLY · after selection', 'evaluator': step['evaluator']}
        trace = [r for r in rows(folder/'agent.jsonl') if r['checkpoint'] == step['checkpoint']]
        calls = [r for r in rows(folder/'calls.jsonl') if r['checkpoint'] == step['checkpoint']]
        return {'source_mode': manifest['mode'], 'method': method, 'status': manifest['status'],
                'completed_steps': len(steps), 'checkpoint': step['checkpoint'], 'time': step['time'],
                'agent': trace, 'intentions': step['intentions_after_receipt'],
                'queries': step['tools'], 'execution_receipts': step['execution'],
                'model_attempts': calls, 'inference_enabled': False}


def serve(study, port):
    viewer = Viewer(study)
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urlparse(self.path)
            try:
                if parsed.path == '/api/catalog':
                    value = viewer.catalog()
                elif parsed.path in ('/api/step', '/api/evaluator'):
                    args = parse_qs(parsed.query)
                    value = viewer.inspect(args['trajectory'][0], args['method'][0], int(args['index'][0]), parsed.path == '/api/evaluator')
                elif parsed.path == '/api/report':
                    value = json.loads((viewer.root/'report.json').read_text())
                else:
                    path = {'/': ROOT/'demo/v2/index.html', '/app.js': ROOT/'demo/v2/app.js',
                            '/style.css': ROOT/'demo/style.css'}.get(parsed.path)
                    if path is None:
                        self.send_error(404); return
                    body = path.read_bytes()
                    self.send_response(200)
                    self.send_header('Content-Type', 'text/css' if path.suffix=='.css' else 'text/javascript' if path.suffix=='.js' else 'text/html; charset=utf-8')
                    self.end_headers(); self.wfile.write(body); return
                body = json.dumps(value, ensure_ascii=False).encode()
                self.send_response(200); self.send_header('Content-Type','application/json'); self.end_headers(); self.wfile.write(body)
            except (ValueError, KeyError, FileNotFoundError) as exc:
                self.send_error(400, str(exc))
        def log_message(self, *args):
            pass
    print(f'Kiodai v2 read-only viewer: http://127.0.0.1:{port}/', flush=True)
    ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()

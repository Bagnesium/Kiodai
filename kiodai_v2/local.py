"""Optional already-installed local development model. No pull, cloud route or API key."""
import json
from urllib.request import Request, urlopen
from research_harness.model_gateway import TransportResponse

MODEL = 'llama3.2:latest'
BASE = 'http://127.0.0.1:11434'


class LocalTransport:
    is_local = True
    def __init__(self):
        with urlopen(BASE+'/api/tags', timeout=5) as response:
            models = json.load(response)['models']
        self.metadata = next((m for m in models if m['name'] == MODEL and m.get('size', 0) > 100_000_000), None)
        if self.metadata is None:
            raise RuntimeError('The declared local llama3.2 model is not installed; no download attempted')

    def invoke(self, request, timeout_seconds):
        payload = {'model': MODEL, 'messages': request['messages'], 'stream': False,
                   'format': request['response_format']['json_schema']['schema'],
                   'options': {'temperature': 0, 'seed': 20260909, 'num_ctx': 16384,
                               'num_predict': request['max_tokens']}, 'keep_alive': '5m'}
        with urlopen(Request(BASE+'/api/chat', data=json.dumps(payload).encode(),
                             headers={'Content-Type': 'application/json'}), timeout=timeout_seconds) as response:
            raw = json.load(response)
        if raw.get('model') != MODEL:
            raise RuntimeError('Unexpected local backend model')
        return TransportResponse(raw['message']['content'], raw,
                                 {'input_tokens': raw.get('prompt_eval_count'), 'output_tokens': raw.get('eval_count')},
                                 MODEL, {'transport': 'Ollama loopback', 'digest': self.metadata['digest'],
                                         'cost_usd_reported': None})

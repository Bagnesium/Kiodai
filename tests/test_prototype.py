from __future__ import annotations
import copy
import io
import json
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch
from research_harness.paired import Pair, configs, catalog
from research_harness.session import RunSession, write_json
from research_harness.demo_transport import DemoTransport
from research_harness.model_gateway import ActionSelector, MockTransport, RunStopped, parse_action, ActionValidationError, safe_error
from research_harness.live import Budget, verify_route, request_bound, MODEL
from research_harness.analysis import rows, analyze, report, verify_run, rates
from research_harness.dashboard import Dashboard
from research_harness.hashing import sha256_file
from sim import pm_bench as PM

ROOT=Path(__file__).resolve().parents[1]
EMPTY='{"action":"choose","choice":"A","task_ids":[],"channel":"NONE"}'
QUERY='{"action":"query_state","choice":"NONE","task_ids":[],"channel":"teacher_feed"}'


class PrototypeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
    def tearDown(self):self.temp.cleanup()
    def session(self,scenario='time',transport=None,condition='A0',modify=None):
        config,spec=configs('demo',scenario,'MOCK');cfg=config[condition]
        if modify:modify(cfg)
        path=self.root/f'{condition}-{scenario}.json';write_json(path,cfg)
        return RunSession(path,output_root=self.root/'runs',transport=transport or DemoTransport(spec['script']))
    def finish(self,session):
        while session.status=='running':session.advance()
        self.assertTrue(session.status.startswith('completed'),session.manifest)
        return session
    def test_all_six_demo_scenarios_shared_runner(self):
        for item in catalog():
            pair=Pair(scenario_id=item['id'],output_root=self.root)
            while pair.plan['status']=='running':pair.advance()
            self.assertEqual(pair.plan['status'],'completed')
            a,b=[pair.sessions[c] for c in ['A0','A1']]
            self.assertEqual(a.manifest['aggregate_metrics'],b.manifest['aggregate_metrics'])
            self.assertEqual(a.manifest['aggregate_metrics']['set_fp'],0)
            self.assertEqual(a.manifest['aggregate_metrics']['set_fn'],0)
    def test_exact_request_parity_except_addendum(self):
        a=self.session(condition='A0');b=self.session(condition='A1');a.advance();b.advance()
        ra=rows(a.run_dir/'raw_model_calls.jsonl')[0]['request'];rb=rows(b.run_dir/'raw_model_calls.jsonl')[0]['request']
        p0=ra['messages'][0].pop('content');p1=rb['messages'][0].pop('content')
        self.assertEqual(p1,p0+'\n\n'+(ROOT/'prompts/prospective_memory_system.txt').read_text().strip())
        self.assertEqual(ra,rb)
    def test_no_future_observation_in_requests(self):
        session=self.session();self.finish(session)
        calls=rows(session.run_dir/'raw_model_calls.jsonl')
        future='The class starts another discussion.'
        for c in calls[:-1]:self.assertNotIn(future,json.dumps(c['request']))
        self.assertIn(future,json.dumps(calls[-1]['request']))
    def test_hidden_channel_future_result_isolated(self):
        session=self.session('hidden');self.finish(session)
        calls=rows(session.run_dir/'raw_model_calls.jsonl')
        # The instruction may state the trigger. Its actual future result must not arrive early.
        prior=[c for c in calls if c['call_context']['step_index']<3]
        for c in prior:
            self.assertNotIn('demo_abstract_accepted',json.dumps(c['request']))
        tool_steps=[s for s in session.steps if s['tools']]
        self.assertEqual(len(tool_steps),2)
        self.assertIn('UNDER REVIEW',tool_steps[0]['tools'][0]['observation'])
        self.assertNotIn('ACCEPTED',tool_steps[0]['tools'][0]['observation'])
        self.assertIn('ACCEPTED',tool_steps[1]['tools'][0]['observation'])
    def test_run_state_isolation(self):
        a=self.finish(self.session());b=self.session();b.advance()
        self.assertEqual(a.steps[0],b.steps[0]);self.assertNotEqual(a.run_id,b.run_id)
        self.assertEqual(len(b.actions),1)
    def test_query_budget_counts_only_executed_queries(self):
        session=self.session('hidden',MockTransport([QUERY,QUERY]));session.advance()
        action=session.actions[0]
        self.assertEqual(action['state_queries'],{'teacher_feed':1})
        self.assertEqual(action['state_query_attempts'],{'teacher_feed':2})
        self.assertEqual(action['task_ids'],[])
        self.assertTrue(action['invalid_response_failure'])
    def test_invalid_output_has_only_one_corrective_retry(self):
        s=self.session(transport=MockTransport(['bad','bad',EMPTY]));s.advance()
        calls=rows(s.run_dir/'raw_model_calls.jsonl')
        self.assertEqual(len(calls),2);self.assertEqual(s.actions[0]['task_ids'],[])
        self.assertIn('Invalid response.',calls[1]['request']['messages'][-1]['content'])
        self.assertEqual(s.manifest['invalid_attempt_count'],2)
    def test_transport_failure_interrupts_and_preserves_attempts(self):
        s=self.session(transport=MockTransport([RuntimeError('network down'),RuntimeError('network down')]))
        s.advance();self.assertEqual(s.status,'interrupted')
        self.assertEqual(s.manifest['transport_error_count'],2)
        self.assertEqual(s.manifest['invalid_attempt_count'],0)
        self.assertIsNone(s.manifest['aggregate_metrics'])
        self.assertEqual(len(rows(s.run_dir/'raw_model_calls.jsonl')),2)
    def test_context_limit_fails_closed_without_transport(self):
        s=self.session(modify=lambda c:c['limits'].update(max_context_tokens=1));s.advance()
        self.assertEqual(rows(s.run_dir/'raw_model_calls.jsonl'),[])
        self.assertEqual(s.actions[0]['task_ids'],[])
        self.assertTrue(s.actions[0]['invalid_response_failure'])
    def test_object_duplicate_keys_and_unknown_handles(self):
        with self.assertRaises(ActionValidationError):parse_action(EMPTY.replace('"choice":"A"','"choice":"B","choice":"A"'),(),('clock',))
        with self.assertRaises(ActionValidationError):parse_action(EMPTY.replace('[]','["task_999"]'),('task_1',),('clock',))
    def test_unavailable_channel_rejected(self):
        with self.assertRaises(ActionValidationError):parse_action(QUERY,(),('clock',))
    def test_missing_usage_is_unavailable_not_zero(self):
        s=self.finish(self.session());self.assertIsNone(s.manifest['token_usage']['input_tokens'])
        self.assertIsNone(s.manifest['model_latency_seconds']);self.assertEqual(s.manifest['reported_cost_usd'],0.0)
    def test_budget_invalid_limits(self):
        for n in [None,0,-1,.31,float('nan'),float('inf')]:
            with self.assertRaises(RunStopped):Budget(n,{'input':.27,'output':1})
    def test_budget_request_reservation_and_exhaustion(self):
        b=Budget(.001,{'input':.27,'output':1});req={'max_tokens':256,'messages':[{'content':'a'*4000}]}
        amount=request_bound(req,b.prices);b.reserve(req)
        self.assertAlmostEqual(b.reserved,amount)
        with self.assertRaises(RunStopped):b.require(.001)
    def test_live_gate_before_any_network(self):
        with patch('research_harness.paired.verify_route') as route:
            with self.assertRaises(RunStopped):Pair(mode='LIVE',output_root=self.root)
            route.assert_not_called()
    def test_frozen_route_rejects_substitution(self):
        c=configs('demo','time','LIVE')[0]['A0'];c['model']['route']='another-provider'
        with self.assertRaises(RunStopped):verify_route(c,{})
    def test_route_preflight_parameters_and_prices(self):
        c=configs('demo','time','LIVE')[0]['A0']
        endpoint={'tag':'novita','quantization':'fp8','status':0,'supported_parameters':['response_format','temperature','top_p','max_tokens','seed','reasoning'],'pricing':{'prompt':'0.00000027','completion':'0.000001'}}
        payload={'data':{'endpoints':[endpoint]}}
        self.assertFalse(verify_route(c,payload)['billable'])
        endpoint['pricing']['completion']='0.1'
        with self.assertRaises(RunStopped):verify_route(c,payload)
    def test_reports_reconstruct_from_saved_logs(self):
        pair=Pair(output_root=self.root)
        while pair.plan['status']=='running':pair.advance()
        result=analyze(self.root,'MOCK');self.assertEqual(len(result['pairs']),1)
        self.assertEqual(result['mean_paired_difference'],0)
        self.assertEqual(report(result),report(analyze(self.root,'MOCK')))
        self.assertEqual(analyze(self.root,'LIVE')['runs'],[])
        session=pair.sessions['A0'];verify_run(session.run_dir)
        score=json.loads((session.run_dir/'score.json').read_text());score['summary']['set_tp']=99
        write_json(session.run_dir/'score.json',score)
        with self.assertRaises(ValueError):verify_run(session.run_dir)
    def test_repeat_averaging_at_scenario_level(self):
        for repeat in range(2):
            pair=Pair(output_root=self.root,repeat=repeat)
            while pair.plan['status']=='running':pair.advance()
        result=analyze(self.root,'MOCK');self.assertEqual(len(result['pairs']),2)
        self.assertEqual(len(result['scenario_averages']),1)
        self.assertEqual(result['scenario_averages'][0]['paired_repeats'],2)
    def test_reset_keeps_interrupted_pair(self):
        app=Dashboard(self.root);app.start({'mode':'MOCK','scenario':'time'});path=app.pair.path
        app.next();app.reset();plan=json.loads((path/'pair.json').read_text())
        self.assertEqual(plan['status'],'interrupted')
        self.assertEqual(len(analyze(self.root,'MOCK')['incomplete_pairs']),1)
    def test_dashboard_evaluator_reveal_gate(self):
        app=Dashboard(self.root);app.start({'mode':'MOCK','scenario':'time'})
        with self.assertRaises(ValueError):app.reveal(0)
        app.next();self.assertNotIn('due_task_ids',json.dumps(app.state()))
        self.assertNotIn('demo_submit',json.dumps(app.state()))
        self.assertIn('due_task_ids',json.dumps(app.reveal(0)))
        with self.assertRaises(ValueError):app.reveal(1)
    def test_dashboard_live_and_recorded_cannot_fallback_to_mock(self):
        app=Dashboard(self.root)
        with self.assertRaises(RunStopped):app.start({'mode':'LIVE','confirm_live':True})
        app.start({'mode':'MOCK','scenario':'time'});identifier=app.pair.pair_id
        while app.pair.plan['status']=='running':app.next()
        self.assertEqual(app.recordings(),[])
        with self.assertRaises(ValueError):app.load_replay(identifier)
    def test_export_whitelist_mode_and_no_private_manuscript(self):
        app=Dashboard(self.root);app.start({'mode':'MOCK','scenario':'time'});app.next()
        (app.pair.path/'private-source.txt').write_text('PRIVATE_SENTINEL')
        archive=zipfile.ZipFile(io.BytesIO(app.export()))
        self.assertIn(b'MOCK',archive.read('EXPORT_MODE.txt'))
        self.assertFalse(any('private-source' in n or n.endswith('.pages') for n in archive.namelist()))
        self.assertNotIn(b'PRIVATE_SENTINEL',b''.join(archive.read(n) for n in archive.namelist()))
    def test_frozen_demo_hashes(self):
        frozen=json.loads((ROOT/'research/demo_freeze_v1.json').read_text())
        for path,digest in frozen['files'].items():self.assertEqual(sha256_file(ROOT/path),digest)
    def test_official_zero_denominator(self):
        self.assertEqual(PM.format_set_f1(0,0,0),'n/a')
        self.assertEqual(rates({'set_tp':0,'set_fp':0,'set_fn':0}),{'precision':None,'recall':None,'set_f1':None})
    def test_error_redacts_environment_key(self):
        with patch.dict('os.environ',{'OPENROUTER_API_KEY':'secret-fixture-key'}):
            self.assertNotIn('secret-fixture-key',safe_error(RuntimeError('header secret-fixture-key')))


class PilotAndArtifactTests(unittest.TestCase):
    setUp = PrototypeTests.setUp
    tearDown = PrototypeTests.tearDown
    session = PrototypeTests.session
    finish = PrototypeTests.finish
    def test_pilot_is_exact_first_day_and_frozen(self):
        original=json.loads((ROOT/'data/development/prospective_memory_dev_v1.json').read_text())
        pilot=json.loads((ROOT/'data/pilot/first_development_day_v1.json').read_text())
        self.assertEqual(pilot['days'],original['days'][:1])
        frozen=json.loads((ROOT/'research/pilot_freeze_v1.json').read_text())
        for name,digest in frozen['files'].items():self.assertEqual(sha256_file(ROOT/name),digest)
    def test_saved_raw_response_tampering_detected(self):
        s=self.finish(self.session());(s.run_dir/'raw_model_calls.jsonl').write_text('')
        with self.assertRaises(ValueError):verify_run(s.run_dir)
    def test_route_mismatch_logs_response_before_interrupt(self):
        from research_harness.model_gateway import TransportResponse
        class ChangedRoute:
            def invoke(self,request,timeout_seconds):
                return TransportResponse(EMPTY,{'model':'wrong-model'},{},'wrong-model',{'route_error':'route mismatch'})
        s=self.session(transport=ChangedRoute());s.advance()
        self.assertEqual(s.status,'interrupted');self.assertEqual(len(rows(s.run_dir/'raw_model_calls.jsonl')),1)
        self.assertEqual(s.actions,[])
    def test_live_mode_rejects_injected_mock_transport(self):
        cfg=configs('pilot',None,'LIVE')[0]['A0'];path=self.root/'live.json';write_json(path,cfg)
        with self.assertRaises(RunStopped):RunSession(path,allow_paid=True,budget_usd=.30,transport=MockTransport(),output_root=self.root)
    def test_empty_interrupted_pair_is_reported(self):
        folder=self.root/'interrupted';folder.mkdir()
        write_json(folder/'pair.json',{'mode':'LIVE','pair_id':'blocked-before-calls','status':'interrupted'})
        result=analyze(self.root,'LIVE');self.assertEqual(result['incomplete_pairs'],['blocked-before-calls'])
    def test_genuine_recording_replay_path_with_explicit_synthetic_test_fixture(self):
        # Temporary fabricated LIVE-shaped fixture solely to exercise replay plumbing.
        # It is never retained, exported as research evidence, or written to real results.
        app=Dashboard(self.root);app.start({'mode':'MOCK','scenario':'time'})
        while app.pair.plan['status']=='running':app.next()
        pair=app.pair
        for s in pair.sessions.values():
            calls=rows(s.run_dir/'raw_model_calls.jsonl')
            for c in calls:c['raw_response']={'test_fixture_only':True,'content':c['raw_text']}
            (s.run_dir/'raw_model_calls.jsonl').write_text('\n'.join(json.dumps(c) for c in calls)+'\n')
            m=json.loads(s.manifest_path.read_text());m['mode']='LIVE';m['artifact_sha256']['raw_model_calls.jsonl']=sha256_file(s.run_dir/'raw_model_calls.jsonl');write_json(s.manifest_path,m)
        pair.plan['mode']='LIVE';pair.save();identifier=pair.pair_id
        self.assertEqual(len(app.recordings()),1)
        app.load_replay(identifier);self.assertEqual(app.state()['mode'],'RECORDED')
        self.assertEqual(app.state()['visible_steps'],0)
        with self.assertRaises(ValueError):app.reveal(0)
        app.next();self.assertEqual(app.state()['visible_steps'],1)
        self.assertEqual(app.reveal(0)['mode'],'RECORDED')

if __name__=='__main__':unittest.main()

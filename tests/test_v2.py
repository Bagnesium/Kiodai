import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kiodai_v2.agent import Agent
from kiodai_v2.common import parse, obj, STRING, rows
from kiodai_v2.fixture import FixtureTransport, record
from kiodai_v2.gateway import Gateway, Accounting
from kiodai_v2.store import Store, LocalExecutor, EXTRACTION
from kiodai_v2.runner import run_case, verify_case
from kiodai_v2.report import analyze_case
from research_harness.model_gateway import MockTransport, RunStopped
from scripts.generate_v2_cases import build

ROOT = Path(__file__).resolve().parents[1]


class V2Tests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.store = Store(self.root/'memory.sqlite')
        self.config = json.loads((ROOT/'configs/v2.json').read_text())
        self.text = 'When board reports "Ready.", Seal the case.'
        self.observations = {'m1': {'text': self.text, 'kind': 'visible', 'checkpoint': 1}}
        self.rec = record('Seal the case.', 'hidden', 'Ready.', 'board', None, self.text, 'm1')
        self.operation = {'kind': 'create', 'target': None, 'expected_version': None,
                          'record': self.rec, 'sources': [{'ref': 'm1', 'quote': self.text}]}

    def tearDown(self):
        self.store.close()
        self.temp.cleanup()

    def create(self):
        self.store.apply({'operations': [self.operation]}, self.observations, 1, ['board'])
        return next(iter(self.store.records()))

    def revise(self, identifier, kind='revise', version=1):
        op = {**self.operation, 'kind': kind, 'target': identifier, 'expected_version': version,
              'record': self.rec if kind == 'revise' else None}
        self.store.apply({'operations': [op]}, self.observations, 2, ['board'])

    def test_schema_rejects_extra_and_duplicate_keys(self):
        for raw in ['{"x":"a","x":"b"}', '{"x":"a","gold":1}', '{"x":1}']:
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                parse(raw, obj({'x': STRING}))

    def test_null_record_and_multiple_creation(self):
        other = copy.deepcopy(self.operation)
        other['record']['action'] = 'Record the reading.'
        self.store.apply({'operations': [self.operation, other]}, self.observations, 1, ['board'])
        self.assertEqual(len(self.store.records()), 2)
        self.assertTrue(all(k.startswith('i_') for k in self.store.records()))

    def test_missing_or_fabricated_source_rejected_atomically(self):
        bad = copy.deepcopy(self.operation)
        bad['record']['evidence']['condition'][0]['quote'] = 'UNQUERIED_SECRET'
        with self.assertRaises(ValueError):
            self.store.apply({'operations': [self.operation, bad]}, self.observations, 1, ['board'])
        self.assertEqual(self.store.records(), {})

    def test_unknown_channel_is_not_manufactured(self):
        with self.assertRaises(ValueError):
            self.store.apply({'operations': [self.operation]}, self.observations, 1, ['clock'])

    def test_ambiguous_update_quarantines_without_arbitrary_target(self):
        key = self.create()
        self.revise(key, 'ambiguous')
        self.assertEqual(self.store.records()[key]['status'], 'quarantined')
        self.assertFalse(self.store.eligible(key, 1))
        self.revise(key)
        self.assertTrue(self.store.eligible(key, 2))

    def test_cancellation_invalidates_scheduled_check(self):
        key = self.create()
        ticket = self.store.monitor(1, ['board'], 1)[0]
        self.revise(key, 'cancel')
        self.assertFalse(self.store.check_valid(ticket))
        with self.assertRaises(ValueError):
            self.store.select(key, 1, 'handle', 2, [])

    def test_revision_invalidates_stale_version(self):
        key = self.create()
        ticket = self.store.monitor(1, ['board'], 1)[0]
        self.revise(key)
        self.assertFalse(self.store.check_valid(ticket))
        self.assertFalse(self.store.eligible(key, 1))
        self.assertTrue(self.store.eligible(key, 2))
        with self.assertRaises(ValueError):
            self.revise(key, version=1)

    def test_negative_does_not_suppress_next_check(self):
        self.create()
        self.store.query_received('board', {'text': 'Not ready.'}, 1)
        self.assertEqual(self.store.monitor(2, ['board'], 1)[0]['channel'], 'board')

    def test_query_budget_exhaustion_and_grouping(self):
        self.test_null_record_and_multiple_creation()
        self.assertEqual(len(self.store.monitor(1, ['board'], 1)), 1)
        self.assertEqual(self.store.monitor(1, ['board'], 0), [])

    def test_fair_channel_rotation(self):
        self.create()
        other = copy.deepcopy(self.operation)
        other['record']['action'] = 'Other action.'
        other['record']['channel'] = 'second'
        self.store.apply({'operations': [other]}, self.observations, 1, ['board', 'second'])
        self.store.query_received('board', {'text': 'Not ready.'}, 1)
        self.assertEqual(self.store.monitor(2, ['board', 'second'], 1)[0]['channel'], 'second')

    def test_dependencies_block_until_receipt(self):
        key = self.create()
        other = copy.deepcopy(self.operation)
        other['record']['action'] = 'Dependent action.'
        other['record']['dependencies'] = [key]
        other['record']['evidence']['dependencies'] = other['sources']
        self.store.apply({'operations': [other]}, self.observations, 1, ['board'])
        dependent = next(k for k in self.store.records() if k != key)
        self.assertFalse(self.store.eligible(dependent, 1))
        eid = self.store.select(key, 1, 'h', 1, [])
        self.assertFalse(self.store.eligible(dependent, 1))
        self.store.attempted(eid)
        self.store.receipt(eid, 'success')
        self.assertTrue(self.store.eligible(dependent, 1))

    def test_selection_is_not_completion(self):
        key = self.create()
        eid = self.store.select(key, 1, 'h', 1, [])
        self.assertEqual(self.store.records()[key]['status'], 'selected')
        self.store.attempted(eid)
        self.assertEqual(self.store.records()[key]['status'], 'attempted')
        self.store.receipt(eid, 'uncertain')
        self.assertEqual(self.store.records()[key]['status'], 'uncertain')
        self.assertFalse(self.store.eligible(key, 1))

    def test_failed_execution_can_retry_same_stable_id(self):
        key = self.create()
        eid = self.store.select(key, 1, 'h', 1, [])
        self.store.attempted(eid)
        self.store.receipt(eid, 'failed')
        self.assertEqual(self.store.select(key, 1, 'renamed_handle', 2, []), eid)

    def test_restart_preserves_completion_and_duplicate_protection(self):
        key = self.create()
        eid = self.store.select(key, 1, 'h', 1, [])
        executor = LocalExecutor(self.root/'effects.sqlite')
        self.store.attempted(eid)
        self.store.receipt(eid, executor.execute(eid))
        executor.db.close()
        self.store.close()
        self.store = Store(self.root/'memory.sqlite')
        executor = LocalExecutor(self.root/'effects.sqlite')
        self.assertEqual(executor.execute(eid), 'success')
        self.assertEqual(executor.db.execute('SELECT count(*) FROM effects').fetchone()[0], 1)
        self.assertFalse(self.store.eligible(key, 1))
        executor.db.close()

    def test_uncertain_simulator_does_not_repeat_side_effect(self):
        executor = LocalExecutor(self.root/'effects.sqlite')
        self.assertEqual(executor.execute('x', 'uncertain'), 'uncertain')
        self.assertEqual(executor.execute('x', 'success'), 'uncertain')
        self.assertEqual(executor.db.execute('SELECT count(*) FROM effects').fetchone()[0], 0)
        executor.db.close()

    def test_full_path_hidden_negative_positive_and_receipt(self):
        path = ROOT/'data/v2/v2_hidden_91320.json'
        folder = run_case(path, 'A2', self.root/'run', self.config, FixtureTransport())
        r = analyze_case(folder)
        self.assertEqual((r['tp'],r['fp'],r['fn']), (3,0,0))
        self.assertEqual(r['hidden_due_opportunities'], 2)
        self.assertTrue(all(h['category']=='query_supported_hit' for h in r['hidden_opportunities']))
        steps = rows(folder/'steps.jsonl')
        self.assertIn('not complete', steps[0]['tools'][0]['observation'])
        self.assertIn('fully stable', steps[6]['tools'][0]['observation'])
        self.assertEqual(steps[0]['action']['selected_handles_validated'], [])
        self.assertTrue(all(r['status']=='completed' for r in json.loads((folder/'memory.json').read_text()).values()))

    def test_full_path_every_family_and_baseline_not_scripted_to_lose(self):
        for family, seed in [('revision',91300), ('visible_events',91310), ('hidden',91320), ('cross_day',91330)]:
            for method in self.config['methods']:
                with self.subTest(family=family, method=method):
                    r=analyze_case(run_case(ROOT/f'data/v2/v2_{family}_{seed}.json', method,
                                           self.root/f'{family}-{method}', self.config, FixtureTransport()))
                    self.assertEqual((r['fp'],r['fn'],r['invalid_responses']), (0,0,0))

    def test_all_components_only_receive_public_history(self):
        scenario = build('hidden', 99991)
        scenario['private_sentinel'] = 'GOLD_SENTINEL'
        scenario['days'][0]['tasks'][0]['private'] = 'TASK_TABLE_SENTINEL'
        scenario['days'][0]['steps'][-1]['text'] += ' FUTURE_SENTINEL'
        path = self.root/'scenario.json'; path.write_text(json.dumps(scenario))
        folder = run_case(path, 'A2', self.root/'run', self.config, FixtureTransport())
        agent_rows = rows(folder/'agent.jsonl')
        for row in agent_rows:
            serialized = json.dumps(row)
            self.assertNotIn('GOLD_SENTINEL', serialized)
            self.assertNotIn('TASK_TABLE_SENTINEL', serialized)
            self.assertNotIn('private_99991', serialized)
            if row['checkpoint'] < 8:
                self.assertNotIn('FUTURE_SENTINEL', serialized)
            if row['checkpoint'] < 7:
                # The instruction quotes the positive condition; the hidden actual positive event is absent.
                self.assertFalse(any(s['kind']=='query' and s['text'].endswith('Cooling is now fully stable.') for s in row['frame']['observations'].values()))

    def test_reject_private_fields_in_full_boundary(self):
        gateway = Gateway(FixtureTransport(), self.config, self.root/'calls.jsonl', 'MOCK')
        agent = Agent('A2', self.root/'agent.sqlite', gateway)
        with self.assertRaises(ValueError):
            agent.receive(json.dumps({'groundtruth': ['secret']}))
        agent.store.close()

    def test_metamorphic_names_handles_channels_and_valid_times(self):
        results = []
        for seed in (981,982):
            case = build('hidden', seed)
            path = self.root/f'{seed}.json'; path.write_text(json.dumps(case))
            r = analyze_case(run_case(path,'A2',self.root/f'run{seed}',self.config,FixtureTransport()))
            results.append((r['tp'],r['fp'],r['fn']))
        self.assertEqual(results, [(3,0,0),(3,0,0)])

    def test_no_agent_module_imports_private_simulator(self):
        import ast
        for filename in ('agent.py','store.py','fixture.py','gateway.py','common.py'):
            tree = ast.parse((ROOT/'kiodai_v2'/filename).read_text())
            imports = [n.module for n in ast.walk(tree) if isinstance(n,ast.ImportFrom)]
            self.assertFalse(any(m and (m.startswith('sim') or m.endswith('runner')) for m in imports))

    def test_state_isolation_between_runs(self):
        self.create()
        other = Store(self.root/'other.sqlite')
        self.assertEqual(other.records(), {})
        other.close()

    def test_internal_retries_counted_and_invalid_fails_closed(self):
        gateway = Gateway(MockTransport(['bad','bad']), self.config, self.root/'calls.jsonl', 'MOCK')
        self.assertIsNone(gateway.call('extract', [], EXTRACTION, 1))
        calls = rows(self.root/'calls.jsonl')
        self.assertEqual(len(calls),4)
        self.assertEqual(sum(r['event']=='response' and bool(r['validation_error']) for r in calls),2)
        self.assertTrue(all(r.get('usage') is None for r in calls))

    def test_transport_failure_never_falls_back_or_retries(self):
        gateway = Gateway(MockTransport([RuntimeError('offline')]),self.config,self.root/'calls.jsonl','MOCK')
        with self.assertRaises(RunStopped):
            gateway.call('baseline',[],obj({'x':STRING}),1)
        self.assertEqual(len(rows(self.root/'calls.jsonl')),2)

    def test_interrupted_trajectory_preserves_artifacts_without_imputation(self):
        folder=self.root/'interrupted'
        with self.assertRaises(RunStopped):
            run_case(ROOT/'data/v2/v2_revision_91300.json','A0',folder,self.config,MockTransport([RuntimeError('offline')]))
        manifest=verify_case(folder)
        self.assertEqual(manifest['status'],'interrupted')
        result=analyze_case(folder)
        self.assertFalse(result['primary_usable'])
        self.assertIsNone(result['tp'])
        self.assertEqual(result['model_calls'],1)
        self.assertEqual(result['completed_steps'],0)

    def test_budget_reservations_survive_restart(self):
        path=self.root/'account.sqlite'; account=Accounting(path,0.1,self.config)
        account.reserve({'max_tokens':256}); first=account.snapshot()['reserved_usd'];account.db.close()
        account=Accounting(path,0.1,self.config)
        self.assertEqual(account.snapshot()['reserved_usd'],first)
        self.assertIsNone(account.snapshot()['api_response_cost_usd'])
        with self.assertRaises(RunStopped):
            Accounting(path,0.2,self.config)
        account.db.close()

    def test_live_cannot_accept_mock_transport_even_with_budget(self):
        account=Accounting(self.root/'account.sqlite',20,self.config)
        with self.assertRaises(ValueError):
            Gateway(MockTransport(),self.config,self.root/'calls.jsonl','LIVE',account)
        self.assertEqual(account.snapshot()['attempts'],0)
        account.db.close()

    def test_budget_rejects_oversized_request_and_insufficient_allowance(self):
        account=Accounting(self.root/'account.sqlite',0.001,self.config)
        with self.assertRaises(RunStopped):account.reserve({'max_tokens':256})
        with self.assertRaises(RunStopped):account.reserve({'max_tokens':256,'text':'x'*50000})
        self.assertEqual(account.snapshot()['attempts'],0)
        account.db.close()

    def test_mode_separation(self):
        for mode in ('RECORDED','LOCAL_MODEL','LIVE'):
            with self.subTest(mode=mode), self.assertRaises(ValueError):
                Gateway(FixtureTransport(),self.config,self.root/'calls.jsonl',mode)

    def test_artifact_tampering_detected(self):
        folder=run_case(ROOT/'data/v2/v2_revision_91300.json','A0',self.root/'run',self.config,FixtureTransport())
        (folder/'actions.jsonl').write_text('[]')
        with self.assertRaises(ValueError):verify_case(folder)

    def test_stale_positive_citation_rejected(self):
        from kiodai_v2.common import citations_valid
        with self.assertRaises(ValueError):
            citations_valid([{'ref':'m1','quote':self.text}],self.observations,current=2)

    def test_hidden_clock_uses_allowed_query_not_evaluator_time(self):
        case=build('revision',777)
        case['time_visible_by_default']=False
        case['state_visibility']['clock']=False
        path=self.root/'hidden-clock.json';path.write_text(json.dumps(case))
        folder=run_case(path,'A2',self.root/'hidden-clock',self.config,FixtureTransport())
        result=analyze_case(folder)
        self.assertEqual((result['tp'],result['fp'],result['fn']),(1,0,0))
        self.assertGreater(result['tool_queries'],0)
        self.assertTrue(all(t['channel']=='clock' for s in rows(folder/'steps.jsonl') for t in s['tools']))

    def test_dashboard_agent_view_excludes_evaluator_fields(self):
        from kiodai_v2.dashboard import Viewer
        from kiodai_v2.common import dump
        folder=run_case(ROOT/'data/v2/v2_revision_91300.json','A0',self.root/'run',self.config,FixtureTransport())
        dump(self.root/'study.json',{'mode':'MOCK','status':'completed','methods':['A0'],
             'runs':[{'trajectory':'x','method':'A0','folder':'run'}]})
        viewer=Viewer(self.root)
        view=viewer.inspect('x','A0',0)
        self.assertNotIn('due_task_ids',json.dumps(view))
        self.assertNotIn('evaluator',view)
        self.assertIn('evaluator',viewer.inspect('x','A0',0,True))
        self.assertFalse(viewer.catalog()['inference_enabled'])
        with self.assertRaises(ValueError):viewer.inspect('x','A0',8)

    def test_a1_remains_runnable(self):
        folder=run_case(ROOT/'data/v2/v2_revision_91300.json','A1',self.root/'a1',self.config,FixtureTransport())
        self.assertTrue(verify_case(folder)['prompt']['addendum_present'])
        self.assertEqual(analyze_case(folder)['fn'],0)

    def test_frozen_budget_includes_all_three_conditions(self):
        from scripts.run_v2 import preflight
        _,_,estimate=preflight(False)
        self.assertEqual(estimate['maximum_attempts'],1344)
        self.assertAlmostEqual(estimate['conservative_allowance_usd'],19.95251712)
        self.assertLessEqual(estimate['conservative_allowance_usd'],20)

    def test_report_pairing_and_complete_study_mean(self):
        from scripts.run_v2 import execute
        root=execute(self.root/'study',self.config,[{'path':'data/v2/v2_revision_91300.json','family':'revision'}])
        result=json.loads((root/'report.json').read_text())
        self.assertEqual(result['complete_study_paired_means']['A2 minus B_ledger']['mean_set_f1_difference'],0)
        self.assertEqual(len(result['matched_differences']),2)
        from kiodai_v2.report import report
        study=json.loads((root/'study.json').read_text());study['planned_trajectories']=2
        (root/'study.json').write_text(json.dumps(study))
        self.assertIsNone(report(root)['complete_study_paired_means']['A2 minus B_ledger']['mean_set_f1_difference'])


if __name__ == '__main__':
    unittest.main()

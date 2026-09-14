"""Offline scope, unchanged candidate, reporting and authorization regressions."""
import copy
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path
from unittest.mock import patch

from kiodai_v2.common import dump, rows
from kiodai_v2.fixture import FixtureTransport
from kiodai_v2.gateway import Accounting
from kiodai_v2.runner import run_case
from research_harness.model_gateway import OpenAICompatibleTransport, RunStopped
from scripts import run_v21_comparison as study
from scripts import report_v21_comparison as report


class ComparisonPreparationTests(unittest.TestCase):
    def test_scope_and_order_are_complete_reproducible_and_balanced_within_families(self):
        spec = study.specification()
        self.assertEqual(spec, study.specification())
        self.assertEqual((spec['method_trajectories'],spec['total_checkpoints']), (36,288))
        self.assertEqual({b['path'] for b in spec['schedule']},
                         {c['path'] for c in study.read(study.ROOT/'data/v2/catalog.json')['cases']})
        for family in {b['family'] for b in spec['schedule']}:
            for position in range(3):
                self.assertEqual(Counter(b['methods'][position] for b in spec['schedule'] if b['family']==family),
                                 Counter(['A0','B_ledger','A2']))
        self.assertEqual(sum(b['prior_network_smoke'] for b in spec['schedule']),1)

    def test_candidate_preflight_is_offline_and_unchanged(self):
        with patch.object(OpenAICompatibleTransport,'invoke',side_effect=AssertionError('network model')), \
                patch('research_harness.live.urlopen',side_effect=AssertionError('network metadata')):
            spec, checks = study.preflight(False)
        self.assertEqual(checks['candidate_frozen_files'],40)
        self.assertEqual(checks['preflight_network_requests'],0)
        self.assertEqual(spec['candidate_implementation_commit'],study.CANDIDATE_COMMIT)

    def test_allowance_counts_all_query_cycles_and_retries(self):
        spec = study.specification()
        self.assertEqual(spec['maximum_model_attempts'],1344)
        self.assertAlmostEqual(spec['budget_guard']['complete_study_allowance_usd'],19.95251712)
        self.assertAlmostEqual(sum(b['block_conservative_allowance_usd'] for b in spec['schedule']),19.95251712)
        self.assertEqual(spec['config']['max_validation_retries'],1)
        self.assertEqual(spec['config']['transport_retries'],0)

    def test_changed_candidate_settings_cannot_hide_inside_new_config(self):
        with tempfile.TemporaryDirectory() as d:
            config = study.read(study.CONFIG)
            config['output_tokens']['baseline'] += 1
            path = Path(d)/'config.json'; dump(path,config)
            with patch.object(study,'CONFIG',path), self.assertRaises(RunStopped): study.design()

    def test_unauthorized_live_and_offline_credentials_fail_before_preflight(self):
        args_list = [ ['--live'], ['--live','--budget-usd','20'],
            ['--live','--authorize-study',study.IDENTIFIER,'--budget-usd','1'],
            ['--live','--authorize-study',study.IDENTIFIER,'--budget-usd','20','--output','/tmp/alternate'],
            ['--preflight','--env-file','.env'], ['--mock','--budget-usd','20'] ]
        for args in args_list:
            with self.subTest(args=args), patch('sys.argv',['launcher',*args]), \
                    patch.object(study,'preflight') as check, self.assertRaises(RunStopped):
                study.main()
            check.assert_not_called()

    def test_existing_live_attempt_refuses_restart_before_credentials(self):
        with tempfile.TemporaryDirectory() as d, patch.object(study,'LIVE_ROOT',Path(d)), \
                patch('sys.argv',['launcher','--live','--authorize-study',study.IDENTIFIER,'--budget-usd','20']), \
                patch.object(study,'preflight') as check, self.assertRaisesRegex(RunStopped,'already has an attempt'):
            study.main()
        check.assert_not_called()

    def test_live_cannot_bypass_manifest_through_preparation_helper(self):
        with patch.object(study,'preflight') as check, self.assertRaisesRegex(RunStopped,'cannot bypass'):
            study.execute(study.LIVE_ROOT,live=True,require_manifest=False)
        check.assert_not_called()

    def test_wrapper_reuses_executor_and_restores_manifest_binding(self):
        original = study.executor.FREEZE
        with tempfile.TemporaryDirectory() as d, patch.object(study,'preflight',return_value=(study.specification(),{})), \
                patch.object(study.executor,'execute',side_effect=RuntimeError('injected before mkdir')) as execute:
            with self.assertRaisesRegex(RuntimeError,'injected'):
                study.execute(Path(d)/'mock',require_manifest=False)
            self.assertEqual(execute.call_count,1)
        self.assertEqual(study.executor.FREEZE,original)

    def test_durable_accounting_keeps_reservations_across_reopen(self):
        config = study.specification()['config']
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'account.sqlite'
            account = Accounting(path,20,config)
            account.reserve({'max_tokens':config['output_tokens']['extract']})
            original=account.snapshot();account.db.close()
            reopened=Accounting(path,20,config)
            self.assertEqual(reopened.snapshot(),original)
            self.assertEqual(reopened.snapshot()['unknown_cost_attempts'],1)
            reopened.db.close()
            with self.assertRaisesRegex(RunStopped,'Cannot reset'): Accounting(path,21,config)

    def test_primary_mean_is_paired_not_micro_and_missing_is_not_zero(self):
        cases=[]
        for trajectory,values in [('x',(.1,.2,.5)),('y',(.9,.8,.6))]:
            for method,f1 in zip(('A0','B_ledger','A2'),values):
                cases.append(dict(trajectory=trajectory,method=method,set_f1=f1,primary_usable=True,tp=1,fp=0,fn=1))
        value=report.group_summary(cases,['x','y'],True)
        self.assertAlmostEqual(value['comparisons']['A2 minus B_ledger']['declared_mean_difference'],.05)
        cases[-1].update(primary_usable=False,set_f1=None)
        value=report.group_summary(cases,['x','y'],False)['comparisons']['A2 minus B_ledger']
        self.assertIsNone(value['declared_mean_difference'])
        self.assertEqual(value['usable_pairs'],1)
        self.assertIsNone(value['per_trajectory'][1]['difference'])

    def test_zero_denominators_remain_undefined(self):
        self.assertEqual(report.metrics(0,0,0), {'tp':0,'fp':0,'fn':0,'precision':None,'recall':None,'set_f1':None})
        self.assertIsNone(report.metrics(0,0,2)['precision'])
        self.assertEqual(report.metrics(0,0,2)['set_f1'],0)

    def test_interrupted_case_and_unstarted_units_remain_in_report(self):
        class BrokenTransport:
            def invoke(self,*args): raise RuntimeError('injected transport failure')
        spec=study.specification();block=spec['schedule'][0];method=block['methods'][0]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);folder=root/block['trajectory']/method
            with self.assertRaises(RunStopped):
                run_case(study.ROOT/block['path'],method,folder,spec['config'],BrokenTransport(),'MOCK')
            dump(root/'comparison_specification.json',spec)
            dump(root/'study.json',{'mode':'MOCK','status':'interrupted','methods':spec['methods'],'runs':[], 'planned_trajectories':12})
            value=report.analyze(root)
            self.assertEqual(len(value['cases']),36)
            self.assertEqual(value['cases'][0]['status'],'interrupted')
            self.assertEqual(value['cases'][0]['model_calls'],1)
            self.assertEqual(sum(c['status']=='not_started' for c in value['cases']),35)
            self.assertIsNone(value['overall']['comparisons']['A2 minus B_ledger']['declared_mean_difference'])
            self.assertIsNone(value['cases'][0]['diagnostics']['obligations']['unfinished_not_canceled'])

    def test_dependency_diagnostics_distinguish_old_and_new_smoke_denominators(self):
        for version,expected in [('v2',(2,1,3)),('v2_1',(3,0,0))]:
            folder=study.ROOT/'results'/version/'deepseek-smoke-v1/v2_hidden_91320/A2'
            value=report.obligation_diagnostics(study.read(folder/'scenario.json'),rows(folder/'steps.jsonl'))
            self.assertEqual(value['total_instructed_obligations'],3)
            self.assertEqual((value['unique_obligations_ever_due'],value['unique_obligations_blocked_at_trigger'],
                              value['unfinished_not_canceled']),expected)

    def test_semantic_review_requires_evidence_and_retains_repaired_defects(self):
        case={'trajectory':'x','method':'A2','primary_usable':True,'planned_steps':8,'diagnostics':{
              'obligations':{'obligations':[{'day':'day','task_id_evaluator_only':'id','first_due_checkpoint':7}]}}}
        value={'cases':[case]}
        annotation={'cases':[{'trajectory':'x','method':'A2','review_status':'reviewed','reviewer':'offline test',
            'notes':'reviewed instructions and all checkpoints','findings':[{'category':'missing_prerequisite',
                'intention_id':'i_test','obligation':'day/id','first_checkpoint':1,'repair_checkpoint':4,
                'source_refs':['m1 exact instruction; ledger checkpoint 1'],'notes':'Missing until revision'}]}]}
        report.apply_reviews(value,annotation)
        audit=case['diagnostics']['semantic_review']
        self.assertEqual(audit['error_count'],1)
        self.assertTrue(audit['findings'][0]['repaired_before_first_due_checkpoint'])
        annotation['cases'][0]['findings'][0]['source_refs']=[]
        with self.assertRaises(ValueError): report.apply_reviews(value,annotation)

    def test_a0_has_no_semantic_zero_and_pending_reviews_are_not_zero(self):
        value={'cases':[{'trajectory':'x','method':m} for m in ('A0','B_ledger','A2')]}
        template=report.review_template(value)
        self.assertEqual([r['method'] for r in template['cases']],['B_ledger','A2'])
        self.assertTrue(all(r['review_status']=='pending' for r in template['cases']))

    def test_manifest_tampering_is_rejected_offline(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'manifest.json'
            dump(path,{'specification':{'changed':True},'hashes':{}})
            with patch.object(study,'MANIFEST',path), patch.object(study,'smoke_preflight',return_value=({}, {'hashes':{}})), \
                    self.assertRaisesRegex(RunStopped,'specification or source hashes'):
                study.preflight()


if __name__=='__main__': unittest.main()

"""Offline preparation, historical verification, and fresh live-gate regressions."""
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import run_v21_smoke as smoke
from scripts import verify_v21_offline as offline
from scripts.verify_saved_smoke import verify_sources
from research_harness.model_gateway import OpenAICompatibleTransport, RunStopped


class SmokePreparationTests(unittest.TestCase):
    def test_offline_preflight_has_no_model_calls_and_covers_every_attempt(self):
        with patch.object(OpenAICompatibleTransport, 'invoke', side_effect=AssertionError('no inference')):
            config, checks = smoke.preflight(False)
        self.assertEqual(config['methods'], ['A2'])
        self.assertEqual(checks['maximum_model_attempts'], 32)
        self.assertEqual(checks['maximum_tool_queries'], 8)
        self.assertAlmostEqual(checks['conservative_allowance_usd'], .49729536)
        self.assertLess(checks['conservative_allowance_usd'], 1)
        self.assertEqual(checks['preflight_model_calls'], 0)
        self.assertEqual(checks['historical_source_files'], 59)

    def test_changed_route_or_resource_settings_fail_before_transport(self):
        original = json.loads(smoke.CONFIG.read_text())
        for key in ('model', 'sampling', 'output_tokens', 'max_request_bytes'):
            with tempfile.TemporaryDirectory() as d:
                config = copy.deepcopy(original)
                config[key] = None
                path = Path(d)/'config.json'
                path.write_text(json.dumps(config))
                with self.subTest(key=key), patch.object(smoke, 'CONFIG', path), self.assertRaises(RunStopped):
                    smoke.preflight(False)

    def test_live_gate_requires_fresh_named_authorization_and_budget(self):
        for args in (['--live'], ['--live', '--budget-usd', '1'],
                     ['--live', '--authorize-new-smoke', smoke.AUTHORIZATION]):
            with self.subTest(args=args), patch.object(sys, 'argv', ['run_v21_smoke.py', *args]), \
                    patch.object(smoke, 'preflight') as preflight, self.assertRaises(RunStopped):
                smoke.main()
            preflight.assert_not_called()

    def test_preflight_rejects_credentials_and_live_flags(self):
        with patch.object(sys, 'argv', ['run_v21_smoke.py', '--preflight', '--env-file', '.env']), \
                patch.object(smoke, 'preflight') as preflight, self.assertRaises(RunStopped):
            smoke.main()
        preflight.assert_not_called()

    def test_existing_attempt_never_opens_credentials_or_executes(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(smoke, 'LIVE_ROOT', Path(d)), patch.object(smoke, 'preflight', return_value=({}, {})), \
                    patch.object(smoke, 'execute') as execute, \
                    patch.object(sys, 'argv', ['run_v21_smoke.py', '--live', '--budget-usd', '1',
                                              '--authorize-new-smoke', smoke.AUTHORIZATION]), \
                    self.assertRaisesRegex(RunStopped, 'already has an attempt'):
                smoke.main()
            execute.assert_not_called()

    def test_historical_sources_verify_at_recorded_commit_without_changing_freezes(self):
        paths = [smoke.ROOT/'research/v2/freeze.json', smoke.ROOT/'research/v2/deepseek_smoke_v1_freeze.json']
        before = [p.read_bytes() for p in paths]
        commit = json.loads((smoke.ROOT/smoke.INVENTORY).read_text())['execution_commit']
        self.assertEqual(verify_sources(smoke.ROOT, commit), 59)
        self.assertEqual([p.read_bytes() for p in paths], before)
        with self.assertRaisesRegex(ValueError, 'Frozen source changed'):
            verify_sources(smoke.ROOT)  # Current v2.1 must not masquerade as the old freeze.

    def test_full_pipeline_negative_later_positive_and_receipts_is_mock_only(self):
        with tempfile.TemporaryDirectory() as d:
            summary = offline.verify(Path(d)/'new-mock')
            self.assertEqual(summary['checkpoints'], 8)
            self.assertEqual(summary['model_requests'], 16)
            self.assertEqual(summary['completed_intentions'], 3)
            self.assertEqual(summary['validation_failures'], 0)
            self.assertFalse(summary['new_model_inference'])
            self.assertLess(summary['usage_projection']['maximum_actual_mock_request_bytes'], 48000)
            self.assertLess(summary['usage_projection']['usage_informed_projection_usd'], .49729536)

    def test_manifest_detects_source_or_schema_changes(self):
        config, checks = smoke.preflight(False)
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'manifest.json'
            path.write_text(json.dumps({'hashes': checks['hashes'], 'extraction_schema_sha256': 'changed'}))
            with patch.object(smoke, 'MANIFEST', path), self.assertRaisesRegex(RunStopped, 'source/schema/configuration'):
                smoke.preflight()

    def test_single_method_report_does_not_claim_a_comparative_study(self):
        from kiodai_v2.report import report
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root/'study.json').write_text(json.dumps({'mode': 'LIVE', 'status': 'starting',
                'methods': ['A2'], 'runs': [], 'planned_trajectories': 1, 'scope': 'One development smoke.'}))
            result = report(root)
            self.assertEqual(result['interpretation'], 'One development smoke.')
            self.assertEqual(result['complete_study_paired_means'], {})


if __name__ == '__main__':
    unittest.main()

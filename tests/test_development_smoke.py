"""Scope and spending regressions for the separate one-shot development launcher."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from scripts import run_v2_smoke as smoke
from research_harness.model_gateway import RunStopped


class DevelopmentSmokeTests(unittest.TestCase):
    def test_complete_allowance_includes_all_retry_attempts(self):
        config, checks = smoke.preflight(False)
        self.assertEqual(config['methods'], ['A2'])
        self.assertEqual(checks['maximum_model_attempts'], 32)
        self.assertAlmostEqual(checks['conservative_allowance_usd'], .49729536)
        self.assertAlmostEqual(checks['full_study_conservative_allowance_usd'], 19.95251712)

    def test_rejects_changed_generation_setting(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d)/'config.json'
            config = json.loads(smoke.CONFIG.read_text())
            config['output_tokens']['extract'] = 2000
            path.write_text(json.dumps(config))
            with patch.object(smoke, 'CONFIG', path), self.assertRaises(RunStopped):
                smoke.preflight(False)

    def test_existing_attempt_stops_before_metadata_or_transport(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(smoke, 'LIVE_ROOT', Path(d)), patch.object(smoke, 'remote_preflight') as remote:
                with self.assertRaises(FileExistsError):
                    smoke.execute({}, {})
                remote.assert_not_called()


if __name__ == '__main__':
    unittest.main()

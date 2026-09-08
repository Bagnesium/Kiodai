import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research_harness.followup import ROOT, FREEZE, preflight, authorize
from research_harness.live import Budget
from research_harness.model_gateway import RunStopped


class FollowupTests(unittest.TestCase):
    def test_existing_pilot_cap_is_not_raised(self):
        with self.assertRaises(RunStopped):
            Budget(.70, {'input': .27, 'output': 1})
        b = Budget(.70, {'input': .27, 'output': 1}, protocol_ceiling=.70)
        b.require(.63708409)
        b.reserve({'max_tokens': 256, 'messages': [{'content': 'x' * 100}]})
        with self.assertRaises(RunStopped):
            b.require(.70)
        with self.assertRaises(RunStopped):
            Budget(.71, b.prices, protocol_ceiling=.70)
        for bad in [float('nan'), float('inf'), -1, True]:
            with self.assertRaises(RunStopped):
                Budget(.70, b.prices, protocol_ceiling=bad)

    def test_preflight_is_offline_and_exact_full_scenario(self):
        with patch('socket.socket.connect', side_effect=AssertionError('No network in preflight')):
            study, cfgs, estimate = preflight()
        scenario = json.loads((ROOT / cfgs['A0']['scenario']).read_text())
        self.assertEqual([len(d['steps']) for d in scenario['days']], [8, 7, 5])
        self.assertEqual(study['repeats'], 1)
        self.assertEqual(estimate['maximum_attempts'], 160)
        self.assertAlmostEqual(estimate['conservative_pair_estimate_usd'], .63708409)
        self.assertTrue(study['planned_after_pilot1_results'])
        self.assertFalse(study['paid_execution_approved_at_freeze'])

    def test_authorization_and_restart_gates(self):
        study, cfgs, estimate = preflight()
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp) / 'single-invocation'
            for live, amount in [(False, .70), (True, None), (True, .30), (True, .71), (True, float('nan'))]:
                with self.assertRaises(RunStopped):
                    authorize(study, cfgs, estimate, live=live, budget_usd=amount, root=root)
            path, budget = authorize(study, cfgs, estimate, live=True, budget_usd=.70, root=root)
            self.assertEqual(path, root)
            self.assertFalse(root.exists())
            self.assertEqual(budget.attempts, 0)
            with self.assertRaises(RunStopped):
                authorize(study, cfgs, {**estimate, 'conservative_pair_estimate_usd': .71},
                          live=True, budget_usd=.70, root=root)
            root.mkdir()
            with self.assertRaises(RunStopped):
                authorize(study, cfgs, estimate, live=True, budget_usd=.70, root=root)

    def test_changed_frozen_input_stops_before_network(self):
        from research_harness.hashing import sha256_file
        scenario = ROOT / 'data/development/prospective_memory_dev_v1.json'
        def digest(path):
            return 'changed' if Path(path) == scenario else sha256_file(path)
        with patch('research_harness.followup.sha256_file', side_effect=digest), \
             patch('socket.socket.connect', side_effect=AssertionError('No network')):
            with self.assertRaisesRegex(RunStopped, 'frozen file changed'):
                preflight()

    def test_cli_default_never_loads_key_or_constructs_pair(self):
        spec = importlib.util.spec_from_file_location('followup_cli_test', ROOT / 'scripts/run_followup.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with patch('sys.argv', ['run_followup.py', '--preflight']), \
             patch.object(module, 'Pair', side_effect=AssertionError('No LIVE or MOCK experiment in preflight')), \
             patch('dotenv.dotenv_values', side_effect=AssertionError('No credentials in preflight')), \
             patch('socket.socket.connect', side_effect=AssertionError('No network')), \
             contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(module.main(), 0)
        self.assertEqual(json.loads(output.getvalue())['status'], 'prepared_not_run')


if __name__ == '__main__':
    unittest.main()

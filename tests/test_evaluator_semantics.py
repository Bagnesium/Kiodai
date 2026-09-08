from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from sim import pm_bench as PM_BENCH


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "tests" / "fixtures" / "smoke_scenario.json"


def empty_actions() -> list[dict]:
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    return [
        {
            "day": day["name"],
            "step_id": step["id"],
            "choice": "A",
            "task_ids": [],
            "state_queries": {},
        }
        for day in scenario["days"]
        for step in day["steps"]
    ]


def score_with_choices(choices: dict[str, list[str]]) -> dict:
    scenario = json.loads(SCENARIO_PATH.read_text(encoding="utf-8"))
    actions = empty_actions()
    for action in actions:
        action["task_ids"] = list(choices.get(action["step_id"], []))
    summary, _, _ = PM_BENCH.score_log(scenario, actions)
    return summary


class EvaluatorSemanticsTests(unittest.TestCase):
    def test_deterministic_fixture_perfect_play(self) -> None:
        choices = {
            "lab_s3": ["lab_seal_amber"],
            "lab_s4": ["lab_label_amber"],
            "lab_s5": ["lab_freezer_log", "lab_send_calibration"],
        }
        first = score_with_choices(choices)
        second = score_with_choices(copy.deepcopy(choices))
        self.assertEqual(first, second)
        self.assertEqual(first["set_tp"], 4)
        self.assertEqual(first["set_fp"], 0)
        self.assertEqual(first["set_fn"], 0)
        self.assertEqual(first["hit"], 4)
        self.assertEqual(first["canceled_total"], 1)
        self.assertEqual(first["update_hit"], 2)
        self.assertEqual(first["update_canceled"], 1)

    def test_cancellation_override_and_reschedule_violations(self) -> None:
        summary = score_with_choices(
            {
                "lab_s3": [
                    "lab_discard_readout",
                    "lab_send_calibration",
                    "lab_freezer_log",
                ]
            }
        )
        self.assertEqual(summary["set_tp"], 0)
        self.assertGreaterEqual(summary["set_fp"], 3)
        self.assertGreaterEqual(summary["update_violation"], 3)

    def test_dependency_violation(self) -> None:
        summary = score_with_choices({"lab_s4": ["lab_label_amber"]})
        self.assertEqual(summary["dependency_violation"], 1)
        self.assertGreaterEqual(summary["false_alarm"], 1)

    def test_duplicate_action_is_commission(self) -> None:
        summary = score_with_choices(
            {
                "lab_s3": ["lab_seal_amber"],
                "lab_s4": ["lab_seal_amber"],
            }
        )
        self.assertEqual(summary["commission"], 1)

    def test_premature_and_late_time_actions(self) -> None:
        premature = score_with_choices({"lab_s4": ["lab_freezer_log"]})
        self.assertGreaterEqual(premature["false_alarm"], 1)
        self.assertEqual(premature["late"], 0)

        late = score_with_choices({"lab_s6": ["lab_freezer_log"]})
        self.assertEqual(late["late"], 1)
        self.assertGreaterEqual(late["set_fn"], 1)
        self.assertGreaterEqual(late["set_fp"], 1)


if __name__ == "__main__":
    unittest.main()


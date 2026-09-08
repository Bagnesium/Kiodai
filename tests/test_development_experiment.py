from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path

from research_harness.hashing import sha256_file
from research_harness.runner import render_prompt


ROOT = Path(__file__).resolve().parents[1]
A0_PATH = ROOT / "configs" / "dev_a0_deepseek_v31.yaml"
A1_PATH = ROOT / "configs" / "dev_a1_deepseek_v31.yaml"
PROMPT_PATH = ROOT / "prompts" / "prospective_memory_system.txt"
EXPECTED_PROMPT_HASH = "fcbb7048bb57c0046caeb7246c83470a7980129fe27b4c413a09f80b4200651a"


def load_suite_verifier():
    path = ROOT / "scripts" / "verify_development_suite.py"
    spec = importlib.util.spec_from_file_location("verify_development_suite", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class DevelopmentExperimentTests(unittest.TestCase):
    def test_frozen_development_suite(self) -> None:
        verifier = load_suite_verifier()
        self.assertEqual(verifier.verify(), [])

    def test_prompt_is_frozen_and_contains_no_released_identifiers(self) -> None:
        self.assertEqual(sha256_file(PROMPT_PATH), EXPECTED_PROMPT_HASH)
        prompt = PROMPT_PATH.read_text(encoding="utf-8")
        released = json.loads(
            (ROOT / "data" / "synthetic_week_v9.json").read_text(encoding="utf-8")
        )
        for day in released["days"]:
            for task in day.get("tasks", []):
                self.assertNotIn(task["id"], prompt)
                self.assertNotIn(task["label"], prompt)
                self.assertNotIn(task["action_text"], prompt)

    def test_a0_a1_settings_differ_only_in_metadata_and_addendum(self) -> None:
        a0 = json.loads(A0_PATH.read_text(encoding="utf-8"))
        a1 = json.loads(A1_PATH.read_text(encoding="utf-8"))
        self.assertEqual(a0["condition"], "A0")
        self.assertEqual(a1["condition"], "A1")
        a1["experiment_id"] = a0["experiment_id"]
        a1["condition"] = a0["condition"]
        a1["prompt"]["addendum_path"] = a0["prompt"]["addendum_path"]
        self.assertEqual(a1, a0)

    def test_a1_effective_prompt_is_exactly_a0_plus_addendum(self) -> None:
        base = ROOT / "prompts" / "baseline_system.txt"
        channels = ["clock", "sensor_board"]
        a0_prompt, _ = render_prompt(base, None, channels, False)
        a1_prompt, _ = render_prompt(base, PROMPT_PATH, channels, False)
        addendum = PROMPT_PATH.read_text(encoding="utf-8").strip()
        self.assertEqual(a1_prompt, a0_prompt + "\n\n" + addendum)

    def test_machine_readable_freeze_manifest_matches_files(self) -> None:
        freeze = json.loads(
            (ROOT / "research" / "a0_a1_freeze_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertFalse(freeze["paid_execution_approved"])
        self.assertEqual(freeze["network_calls_completed"], 0)
        for condition in ("A0", "A1"):
            item = freeze["conditions"][condition]
            self.assertEqual(
                sha256_file(ROOT / item["config_path"]), item["config_sha256"]
            )
        self.assertEqual(
            sha256_file(ROOT / freeze["scenario"]["path"]),
            freeze["scenario"]["sha256"],
        )
        self.assertEqual(
            sha256_file(ROOT / freeze["skill"]["provider_neutral_path"]),
            freeze["skill"]["provider_neutral_sha256"],
        )
        self.assertEqual(
            sha256_file(ROOT / freeze["skill"]["codex_claude_path"]),
            freeze["skill"]["codex_claude_sha256"],
        )


if __name__ == "__main__":
    unittest.main()

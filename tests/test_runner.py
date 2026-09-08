from __future__ import annotations

import copy
import inspect
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from sim import pm_bench as PM_BENCH

from research_harness.hashing import sha256_bytes, sha256_file
from research_harness.config import ConfigError, validate_runtime_config
from research_harness import model_gateway
from research_harness.model_gateway import ActionSelector, MockTransport, TransportResponse
from research_harness.runner import (
    MANIFEST_REQUIRED_FIELDS,
    PROJECT_ROOT,
    render_prompt,
    run_experiment,
)


ROOT = Path(__file__).resolve().parents[1]
SMOKE_CONFIG = ROOT / "configs" / "smoke_test.yaml"
SMOKE_SCENARIO = ROOT / "tests" / "fixtures" / "smoke_scenario.json"


class SpyTransport:
    def __init__(self, banned: list[str], event_order: list[str] | None = None) -> None:
        self.banned = banned
        self.requests: list[dict] = []
        self.event_order = event_order

    def invoke(self, request: dict, timeout_seconds: float) -> TransportResponse:
        del timeout_seconds
        serialized = json.dumps(request, ensure_ascii=False)
        for value in self.banned:
            if value:
                if value in serialized:
                    raise AssertionError(f"Evaluator-only value reached transport: {value}")
        self.requests.append(copy.deepcopy(request))
        if self.event_order is not None:
            self.event_order.append("model")
        raw = '{"action":"choose","choice":"A","task_ids":[],"channel":"NONE"}'
        return TransportResponse(
            raw_text=raw,
            raw_response={"spy": True, "content": raw},
            usage={"input_tokens": 10, "output_tokens": 5},
            reported_model="mock/spy-v1",
            provider_metadata={"network": False},
        )


class FirstHandleTransport:
    def invoke(self, request: dict, timeout_seconds: float) -> TransportResponse:
        del timeout_seconds
        item_schema = request["response_format"]["json_schema"]["schema"]["properties"][
            "task_ids"
        ]["items"]
        handle = item_schema["enum"][0]
        raw = json.dumps(
            {
                "action": "choose",
                "choice": "C",
                "task_ids": [handle],
                "channel": "NONE",
            }
        )
        return TransportResponse(
            raw_text=raw,
            raw_response={"first_handle": handle, "content": raw},
            usage={"input_tokens": 1, "output_tokens": 1},
            reported_model="mock/first-handle-v1",
            provider_metadata={"network": False},
        )


def write_temp_config(tmp: Path, scenario_path: Path) -> Path:
    config = json.loads(SMOKE_CONFIG.read_text(encoding="utf-8"))
    config["scenario"] = str(scenario_path)
    config["prompt"]["base_path"] = str(ROOT / "prompts" / "baseline_system.txt")
    config["output"]["root"] = str(tmp / "configured-output")
    path = tmp / "config.yaml"
    path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    return path


class RunnerTests(unittest.TestCase):
    def test_baseline_prompt_template_matches_original_prompt(self) -> None:
        channels = ["clock", "instrument_feed"]
        rendered, _ = render_prompt(
            ROOT / "prompts" / "baseline_system.txt", None, channels, False
        )
        original = PM_BENCH.build_llm_system_prompt(False, channels)
        self.assertEqual(rendered, original)

    def test_action_selector_signature_has_no_evaluator_state(self) -> None:
        parameters = set(inspect.signature(ActionSelector.select_action).parameters)
        forbidden = {"scenario", "groundtruth", "due_now", "expected_task_ids", "task_states"}
        self.assertTrue(parameters.isdisjoint(forbidden))

    def test_model_gateway_has_no_evaluator_import_or_state_names(self) -> None:
        source = inspect.getsource(model_gateway)
        self.assertNotIn("pm_bench", source)
        self.assertNotIn("groundtruth", source)
        self.assertNotIn("due_now", source)
        self.assertNotIn("expected_task_ids", source)

    def test_groundtruth_canonical_ids_and_due_state_never_reach_selector(self) -> None:
        scenario = json.loads(SMOKE_SCENARIO.read_text(encoding="utf-8"))
        sentinel = "SECRET_GROUNDTRUTH_SENTINEL_7f0e"
        canonical_ids = [
            task["id"] for day in scenario["days"] for task in day.get("tasks", [])
        ]
        for day in scenario["days"]:
            for step in day["steps"]:
                step["groundtruth"] = {
                    "status": sentinel,
                    "actions": [{"id": sentinel, "task_handle": sentinel}],
                }

        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            scenario_path = tmp / "sentinel-scenario.json"
            scenario_path.write_text(json.dumps(scenario), encoding="utf-8")
            config_path = write_temp_config(tmp, scenario_path)
            event_order: list[str] = []
            spy = SpyTransport([sentinel] + canonical_ids, event_order)
            original_compute = PM_BENCH.compute_due_now

            def observed_compute(*args, **kwargs):
                event_order.append("evaluator")
                return original_compute(*args, **kwargs)

            with patch.object(PM_BENCH, "compute_due_now", side_effect=observed_compute):
                manifest_path = run_experiment(
                    config_path, output_root_override=tmp / "runs", transport=spy
                )
            self.assertTrue(manifest_path.is_file())
            self.assertEqual(len(spy.requests), 6)
            self.assertEqual(event_order, ["model", "evaluator"] * 6)
            raw_log = Path(
                json.loads(manifest_path.read_text())["raw_output_locations"][
                    "raw_model_calls"
                ]
            ).read_text(encoding="utf-8")
            self.assertNotIn(sentinel, raw_log)
            for canonical_id in canonical_ids:
                self.assertNotIn(canonical_id, raw_log)

    def test_manifest_hashes_raw_logging_and_official_score_parity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            config_path = write_temp_config(tmp, SMOKE_SCENARIO)
            manifest_path = run_experiment(
                config_path,
                output_root_override=tmp / "runs",
                transport=MockTransport(),
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertTrue(MANIFEST_REQUIRED_FIELDS.issubset(manifest))
            self.assertEqual(manifest["configuration_hash"], sha256_file(config_path))
            self.assertEqual(manifest["git_commit"], _git_head())
            rendered, _ = render_prompt(
                ROOT / "prompts" / "baseline_system.txt",
                None,
                ["clock", "instrument_feed"],
                False,
            )
            self.assertEqual(
                manifest["prompt_hash"], sha256_bytes(rendered.encode("utf-8"))
            )
            raw_records = [
                json.loads(line)
                for line in Path(
                    manifest["raw_output_locations"]["raw_model_calls"]
                ).read_text(encoding="utf-8").splitlines()
            ]
            self.assertEqual(len(raw_records), 6)
            self.assertTrue(all(record["request"] for record in raw_records))
            self.assertTrue(all(record["raw_response"] for record in raw_records))
            actions, _ = PM_BENCH.read_log_with_metadata(
                manifest["raw_output_locations"]["actions"]
            )
            scenario = PM_BENCH.load_scenario(str(SMOKE_SCENARIO))
            direct_summary, _, _ = PM_BENCH.score_log(scenario, actions)
            self.assertEqual(manifest["aggregate_metrics"], direct_summary)

    def test_original_handles_are_logged_before_canonical_mapping(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            config_path = write_temp_config(tmp, SMOKE_SCENARIO)
            manifest_path = run_experiment(
                config_path,
                output_root_override=tmp / "runs",
                transport=FirstHandleTransport(),
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            actions, _ = PM_BENCH.read_log_with_metadata(
                manifest["raw_output_locations"]["actions"]
            )
            first = actions[0]
            self.assertEqual(first["selected_handles_raw"], first["selected_handles_validated"])
            self.assertTrue(first["selected_handles_raw"][0].startswith("task_"))
            self.assertEqual(len(first["task_ids"]), 1)
            self.assertNotEqual(first["task_ids"][0], first["selected_handles_raw"][0])

    def test_non_mock_provider_requires_double_paid_opt_in(self) -> None:
        config = json.loads(SMOKE_CONFIG.read_text(encoding="utf-8"))
        config["model"]["provider"] = "openrouter"
        config["execution"]["allow_paid"] = False
        with self.assertRaises(ConfigError):
            validate_runtime_config(config, allow_paid_cli=True)
        config["execution"]["allow_paid"] = True
        with self.assertRaises(ConfigError):
            validate_runtime_config(config, allow_paid_cli=False)
        config["model"]["route"] = "REQUIRED_PROVIDER_PIN"
        with self.assertRaises(ConfigError):
            validate_runtime_config(config, allow_paid_cli=True)
        config["model"]["route"] = "OpenAI"
        validate_runtime_config(config, allow_paid_cli=True)

    def test_end_to_end_invalid_response_is_scored_and_not_replaced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_name:
            tmp = Path(tmp_name)
            config_path = write_temp_config(tmp, SMOKE_SCENARIO)
            transport = MockTransport(["invalid-1", "invalid-2", "invalid-3"])
            manifest_path = run_experiment(
                config_path, output_root_override=tmp / "runs", transport=transport
            )
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(manifest["status"], "completed_with_failures")
            self.assertEqual(manifest["failed_run_count"], 1)
            self.assertEqual(manifest["failed_action_count"], 1)
            self.assertEqual(manifest["invalid_attempt_count"], 3)
            actions, _ = PM_BENCH.read_log_with_metadata(
                manifest["raw_output_locations"]["actions"]
            )
            self.assertEqual(actions[0]["action_source"], "fail_closed")
            self.assertEqual(actions[0]["task_ids"], [])
            failures = Path(manifest["raw_output_locations"]["failures"]).read_text()
            self.assertIn("invalid JSON", failures)

    def test_smoke_fixture_identifiers_do_not_overlap_released_benchmark(self) -> None:
        smoke = json.loads(SMOKE_SCENARIO.read_text(encoding="utf-8"))
        released = json.loads(
            (ROOT / "data" / "synthetic_week_v9.json").read_text(encoding="utf-8")
        )
        smoke_task_ids = {
            task["id"] for day in smoke["days"] for task in day.get("tasks", [])
        }
        released_task_ids = {
            task["id"] for day in released["days"] for task in day.get("tasks", [])
        }
        smoke_cues = {
            cue
            for day in smoke["days"]
            for step in day["steps"]
            for cue in step.get("cues", [])
        }
        released_cues = {
            cue
            for day in released["days"]
            for step in day["steps"]
            for cue in step.get("cues", [])
        }
        self.assertTrue(smoke_task_ids.isdisjoint(released_task_ids))
        self.assertTrue(smoke_cues.isdisjoint(released_cues))
        self.assertNotIn("groundtruth", json.dumps(smoke))


def _git_head() -> str:
    import subprocess

    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


if __name__ == "__main__":
    unittest.main()

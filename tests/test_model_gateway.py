from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from research_harness.model_gateway import (
    ActionSelector,
    ActionValidationError,
    MockTransport,
    parse_action,
)


class ModelGatewayTests(unittest.TestCase):
    def settings(self) -> tuple[dict, dict, dict]:
        return (
            {
                "provider": "mock",
                "route": "local-deterministic",
                "allow_route_fallbacks": False,
                "model_id": "mock/test-v1",
            },
            {"temperature": 0.0, "top_p": 1.0},
            {"max_retries": 2, "max_output_tokens": 64, "timeout_seconds": 1},
        )

    def test_invalid_responses_retry_then_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "raw.jsonl"
            model, sampling, limits = self.settings()
            transport = MockTransport(
                [
                    "not json",
                    '{"action":"choose","choice":"A","task_ids":["task_999"],"channel":"NONE"}',
                    '{"action":"choose","choice":"A","task_ids":["task_1","task_1"],"channel":"NONE"}',
                ]
            )
            selector = ActionSelector(transport, log_path, model, sampling, limits)
            result = selector.select_action(
                messages=[{"role": "system", "content": "visible only"}],
                allowed_handles=("task_1",),
                allowed_channels=("clock",),
                call_context={"day": "D", "step_id": "S"},
            )
            self.assertTrue(result.failed_closed)
            self.assertEqual(result.action.task_ids, ())
            self.assertEqual(result.action.choice, "A")
            self.assertEqual(result.attempts, 2)
            records = [json.loads(line) for line in log_path.read_text().splitlines()]
            self.assertEqual(len(records), 2)
            self.assertEqual([record["attempt"] for record in records], [1, 2])
            self.assertTrue(all(record["parse_error"] for record in records))
            self.assertEqual(records[0]["raw_response"]["content"], "not json")
            self.assertEqual(result.raw_selected_handles, ("task_999",))

    def test_transport_exception_is_logged_as_a_retry(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "raw.jsonl"
            model, sampling, limits = self.settings()
            limits["max_retries"] = 1
            selector = ActionSelector(
                MockTransport(
                    [
                        RuntimeError("synthetic transport failure"),
                        '{"action":"choose","choice":"B","task_ids":[],"channel":"NONE"}',
                    ]
                ),
                log_path,
                model,
                sampling,
                limits,
            )
            result = selector.select_action(
                messages=[{"role": "user", "content": "public prompt"}],
                allowed_handles=(),
                allowed_channels=("clock",),
                call_context={"day": "D", "step_id": "S"},
            )
            self.assertFalse(result.failed_closed)
            self.assertEqual(result.action.choice, "B")
            records = [json.loads(line) for line in log_path.read_text().splitlines()]
            self.assertIn("synthetic transport failure", records[0]["transport_error"])
            self.assertIsNone(records[1]["parse_error"])

    def test_strict_parser_rejects_trailing_or_duplicate_content(self) -> None:
        with self.assertRaises(ActionValidationError):
            parse_action(
                '{"action":"choose","choice":"A","task_ids":[],"channel":"NONE"} trailing',
                (),
                ("clock",),
            )
        with self.assertRaises(ActionValidationError):
            parse_action(
                '{"action":"choose","choice":"A","task_ids":["task_1","task_1"],"channel":"NONE"}',
                ("task_1",),
                ("clock",),
            )

    def test_request_records_provider_and_quantization_pin(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            log_path = Path(tmp) / "raw.jsonl"
            model, sampling, limits = self.settings()
            model.update(
                {
                    "provider": "openrouter",
                    "route": "novita",
                    "quantizations": ["fp8"],
                    "require_parameters": True,
                }
            )
            selector = ActionSelector(MockTransport(), log_path, model, sampling, limits)
            selector.select_action(
                messages=[{"role": "user", "content": "public prompt"}],
                allowed_handles=(),
                allowed_channels=("clock",),
                call_context={"day": "D", "step_id": "S"},
            )
            request = json.loads(log_path.read_text().splitlines()[0])["request"]
            self.assertEqual(request["provider_route"], "novita")
            self.assertEqual(request["provider_quantizations"], ["fp8"])
            self.assertFalse(request["route_fallbacks_allowed"])
            self.assertTrue(request["provider_require_parameters"])


if __name__ == "__main__":
    unittest.main()

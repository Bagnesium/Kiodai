#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from research_harness.hashing import sha256_file
from sim import pm_bench as PM_BENCH


MANIFEST_PATH = PROJECT_ROOT / "research" / "development_suite_manifest.json"
RELEASED_PATH = PROJECT_ROOT / "data" / "synthetic_week_v9.json"
REQUIRED_CASES = {
    "simple_time_trigger",
    "simple_event_trigger",
    "long_delay_intention",
    "cancellation",
    "rescheduling",
    "multiple_reschedules",
    "override",
    "conflicting_instructions",
    "irrelevant_distraction",
    "similar_false_trigger",
    "multiple_simultaneous_intentions",
    "hidden_state_monitoring",
    "must_not_execute",
    "duplicate_execution_trap",
    "cross_day_intention",
}


def verify() -> list[str]:
    errors: list[str] = []
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    cases = manifest.get("required_cases", [])
    if set(cases) != REQUIRED_CASES or len(cases) != len(REQUIRED_CASES):
        errors.append("development coverage list is incomplete or duplicated")

    scenarios = []
    for relative, metadata in manifest.get("files", {}).items():
        path = PROJECT_ROOT / relative
        if not path.is_file():
            errors.append(f"development file missing: {relative}")
            continue
        actual_hash = sha256_file(path)
        if actual_hash != metadata.get("sha256"):
            errors.append(
                f"development hash mismatch: {relative}: expected "
                f"{metadata.get('sha256')}, got {actual_hash}"
            )
        scenario = json.loads(path.read_text(encoding="utf-8"))
        scenarios.append(scenario)
        if _contains_key(scenario, "groundtruth"):
            errors.append(f"embedded groundtruth found: {relative}")
        validation_errors, _ = PM_BENCH.validate_scenario(scenario)
        errors.extend(f"{relative}: {error}" for error in validation_errors)
        report = PM_BENCH.compute_scenario_groundtruth(scenario)
        if not report["solvable"]:
            errors.append(f"development scenario is not solvable: {relative}")

    counts = {
        "scenario_count": len(scenarios),
        "day_count": sum(len(scenario.get("days", [])) for scenario in scenarios),
        "step_count": sum(
            len(day.get("steps", []))
            for scenario in scenarios
            for day in scenario.get("days", [])
        ),
        "task_count": sum(
            len(day.get("tasks", []))
            for scenario in scenarios
            for day in scenario.get("days", [])
        ),
    }
    for field, actual in counts.items():
        if manifest.get(field) != actual:
            errors.append(f"{field} mismatch: expected {manifest.get(field)}, got {actual}")

    released = json.loads(RELEASED_PATH.read_text(encoding="utf-8"))
    for field in ("id", "label", "action_text"):
        dev_values = _task_values(scenarios, field)
        released_values = _task_values([released], field)
        overlap = sorted(dev_values & released_values)
        if overlap:
            errors.append(f"released-week {field} overlap: {overlap}")
    return errors


def _contains_key(value, key: str) -> bool:
    if isinstance(value, dict):
        return key in value or any(_contains_key(item, key) for item in value.values())
    if isinstance(value, list):
        return any(_contains_key(item, key) for item in value)
    return False


def _task_values(scenarios: list[dict], field: str) -> set[str]:
    return {
        task[field]
        for scenario in scenarios
        for day in scenario.get("days", [])
        for task in day.get("tasks", [])
        if task.get(field)
    }


def main() -> int:
    errors = verify()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    print(
        "Development-suite integrity OK: "
        f"{manifest['scenario_count']} scenario, {manifest['day_count']} days, "
        f"{manifest['step_count']} steps, {len(manifest['required_cases'])} cases"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


from __future__ import annotations

import json
import os
import subprocess
import time
import uuid
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from sim import pm_bench as PM_BENCH

from .config import load_config, validate_runtime_config
from .hashing import sha256_bytes, sha256_file
from .model_gateway import (
    ActionSelector,
    MockTransport,
    ModelAction,
    ModelTransport,
    OpenAICompatibleTransport,
    SelectionResult,
    utc_now,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PLACEHOLDER_MARKER = "UNFROZEN_PLACEHOLDER"
MANIFEST_REQUIRED_FIELDS = {
    "schema_version",
    "experiment_id",
    "run_id",
    "status",
    "git_commit",
    "git_dirty",
    "benchmark_commit",
    "benchmark_hash",
    "evaluator_hash",
    "configuration_hash",
    "resolved_configuration_hash",
    "prompt_hash",
    "model_provider",
    "provider_route",
    "route_fallbacks_allowed",
    "provider_require_parameters",
    "provider_quantizations",
    "exact_model_id",
    "model_reported_versions",
    "started_at_utc",
    "finished_at_utc",
    "temperature",
    "top_p",
    "maximum_output_tokens",
    "context_limit",
    "random_seed",
    "retry_settings",
    "timeout_seconds",
    "tool_permissions",
    "benchmark_split",
    "scenario_ids",
    "raw_output_locations",
    "aggregate_metrics",
    "token_usage",
    "estimated_cost_usd",
    "failed_run_count",
    "failed_action_count",
    "invalid_attempt_count",
    "excluded_run_count",
    "exclusion_reasons",
}


def render_prompt(
    base_path: Path,
    addendum_path: Path | None,
    state_channels: list[str],
    show_task_legend: bool,
) -> tuple[str, dict[str, Any]]:
    # Normalize the tracked template's editor newline to the single trailing
    # newline emitted by the protected baseline prompt builder.
    template = base_path.read_text(encoding="utf-8").rstrip("\n") + "\n"
    menu_line = (
        "A daily action-handle legend is shown at the start of each day."
        if show_task_legend
        else "A step-level action menu is shown before each choice."
    )
    replacements = {
        "{{MENU_LINE}}": menu_line,
        "{{STATE_CHANNELS}}": ", ".join(state_channels) if state_channels else "clock",
        "{{MAX_ACTION_TASK_IDS}}": str(PM_BENCH.MAX_ACTION_TASK_IDS),
    }
    rendered = template
    for token, value in replacements.items():
        rendered = rendered.replace(token, value)
    unresolved = [token for token in replacements if token in rendered]
    if unresolved:
        raise ValueError(f"Unresolved prompt tokens: {unresolved}")

    addendum_text = None
    addendum_hash = None
    if addendum_path is not None:
        addendum_text = addendum_path.read_text(encoding="utf-8").strip()
        if PLACEHOLDER_MARKER in addendum_text:
            raise ValueError("Refusing to inject the unfrozen prompt placeholder.")
        if not addendum_text:
            raise ValueError("Prompt addendum must not be empty when configured.")
        rendered = rendered + "\n\n" + addendum_text
        addendum_hash = sha256_file(addendum_path)
    metadata = {
        "base_prompt_path": str(base_path),
        "base_prompt_file_sha256": sha256_file(base_path),
        "addendum_path": str(addendum_path) if addendum_path else None,
        "addendum_file_sha256": addendum_hash,
        "effective_prompt_sha256": sha256_bytes(rendered.encode("utf-8")),
        "addendum_present": addendum_text is not None,
    }
    return rendered, metadata


def build_transport(config: dict[str, Any]) -> ModelTransport:
    model = config["model"]
    provider = model["provider"]
    if provider == "mock":
        responses_path = model.get("mock_responses_path")
        responses = None
        if responses_path:
            path = Path(responses_path)
            if not path.is_absolute():
                path = PROJECT_ROOT / path
            responses = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(responses, list):
                raise ValueError("Mock responses must be a JSON list.")
        return MockTransport(responses)
    if provider == "openrouter" and not model.get("route"):
        raise ValueError("OpenRouter execution requires an explicit pinned provider route.")
    key_env = model.get("api_key_env")
    api_key = os.environ.get(key_env or "")
    if not api_key:
        raise ValueError(f"Missing API credential in environment variable {key_env!r}.")
    return OpenAICompatibleTransport(api_key, base_url=model.get("base_url"))


def run_experiment(config_path, *, allow_paid=False, output_root_override=None, transport=None, budget_usd=None):
    from .session import RunSession
    session = RunSession(config_path, allow_paid=allow_paid, output_root=output_root_override,
                         transport=transport, budget_usd=budget_usd)
    while session.status == "running":
        session.advance()
    return session.manifest_path


def iter_environment(
    *,
    scenario: dict[str, Any],
    system_prompt: str,
    selector: ActionSelector,
    config: dict[str, Any],
    allowed_channels: list[str],
    state_visibility: dict[str, bool],
    state_channels: dict[str, dict[str, Any]],
    failure_path: Path,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    for header_line in config["execution"].get("daily_header_lines", []):
        messages.append({"role": "user", "content": str(header_line)})
    updates_by_day = PM_BENCH.build_updates_by_day(scenario)
    actions: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for day_index, day in enumerate(scenario.get("days", [])):
        day_start_minutes = PM_BENCH.build_day_start_minutes(day)
        tasks = day.get("tasks", [])
        lure_catalog = PM_BENCH.normalize_lure_catalog(day.get("lures", []))
        task_states = {task["id"]: PM_BENCH.init_task_state(task) for task in tasks}
        active_task_ids: set[str] = set()
        for task in tasks:
            encoding_type, _ = PM_BENCH.normalize_encoding(task["encoding"])
            if encoding_type == "start":
                active_task_ids.add(task["id"])
                task_states[task["id"]]["active"] = True
        day_updates = updates_by_day.get(day["name"], {"pre": [], "by_step": {}})
        for update in day_updates.get("pre", []):
            task_id = update.get("task_id")
            if task_id in task_states:
                PM_BENCH.apply_task_update(task_states[task_id], update, task_states=task_states)

        id_to_handle, _ = PM_BENCH.build_day_handle_maps(
            task_states, lure_catalog, seed_key=f"{day['name']}:handles"
        )
        day_header = "\n".join([f"=== {day['name']} ==="] + day.get("start_instructions", []))
        messages.append({"role": "user", "content": day_header})
        if config["execution"].get("show_task_legend", False):
            legend_entries = []
            for task_id, state in sorted(task_states.items()):
                if state["active"]:
                    legend_entries.append(
                        {
                            "id": task_id,
                            "handle": id_to_handle[task_id],
                            "action_text": PM_BENCH.runtime_task_action_text(state),
                        }
                    )
            for lure in lure_catalog:
                legend_entries.append(
                    {
                        "id": lure["id"],
                        "handle": id_to_handle[lure["id"]],
                        "action_text": lure["action_text"],
                    }
                )
            messages.append(
                {
                    "role": "user",
                    "content": PM_BENCH.format_action_menu(
                        legend_entries, header="Daily action-handle legend"
                    ),
                }
            )

        last_query_step_by_channel: dict[str, int] = {}
        last_snapshot_item_by_channel: dict[str, dict[str, Any]] = {}
        for step_index, step in enumerate(day.get("steps", [])):
            for update in day_updates.get("by_step", {}).get(step["id"], []):
                task_id = update.get("task_id")
                if task_id in task_states:
                    PM_BENCH.apply_task_update(
                        task_states[task_id], update, task_states=task_states
                    )
            for task in tasks:
                encoding_type, encoding_step = PM_BENCH.normalize_encoding(task["encoding"])
                if encoding_type == "step" and encoding_step == step["id"]:
                    active_task_ids.add(task["id"])
                    task_states[task["id"]]["active"] = True

            menu_entries, handle_to_id = PM_BENCH.build_step_action_menu(
                task_states,
                active_task_ids,
                lure_catalog,
                id_to_handle,
                day["name"],
                step["id"],
            )
            menu_text = PM_BENCH.format_action_menu(menu_entries, header="Step action menu")
            time_line = ""
            if state_visibility.get("clock", False):
                step_minutes = PM_BENCH.time_to_minutes(step["time"])
                time_line = (
                    f"\nTime: {step['time']} | Stopwatch: "
                    f"{step_minutes - day_start_minutes} min"
                )
            visible_step_prompt = (
                f"{step['text']}\n"
                + "\n".join(step["options"])
                + "\n"
                + menu_text
                + "\n"
                + time_line
            )
            messages.append({"role": "user", "content": visible_step_prompt})

            query_counts: dict[str, int] = {}
            query_attempts: dict[str, int] = {}
            tool_results = []
            step_messages = json.loads(json.dumps(messages))
            interaction_index = 0
            final_selection: SelectionResult | None = None
            while final_selection is None:
                interaction_index += 1
                context_estimate = PM_BENCH.estimate_input_tokens(messages)
                if context_estimate > int(config["limits"]["max_context_tokens"]):
                    selection = SelectionResult(
                        action=ModelAction("choose", "A", (), "NONE"),
                        failed_closed=True,
                        attempts=0,
                        raw_selected_handles=(),
                        last_raw_text=None,
                        failure_reason=(
                            f"context limit exceeded: estimated {context_estimate} > "
                            f"{config['limits']['max_context_tokens']}"
                        ),
                    )
                else:
                    selection = selector.select_action(
                        messages=messages,
                        allowed_handles=tuple(sorted(handle_to_id)),
                        allowed_channels=tuple(allowed_channels),
                        call_context={
                            "day": day["name"],
                            "day_index": day_index,
                            "step_id": step["id"],
                            "step_index": step_index,
                            "interaction_index": interaction_index,
                        },
                    )
                if selection.failed_closed:
                    _record_failure(
                        failure_path,
                        failures,
                        day["name"],
                        step["id"],
                        interaction_index,
                        selection,
                    )
                    if selection.last_raw_text is not None:
                        messages.append(
                            {"role": "assistant", "content": selection.last_raw_text}
                        )
                    messages.append(
                        {
                            "role": "user",
                            "content": (
                                "Harness notice: the previous response was invalid after all "
                                "configured attempts. No task action was executed for this step."
                            ),
                        }
                    )
                    final_selection = selection
                    break

                action = selection.action
                messages.append(
                    {
                        "role": "assistant",
                        "content": selection.last_raw_text
                        or json.dumps(asdict(action), ensure_ascii=False),
                    }
                )
                if action.action in ("query_state", "check_time"):
                    channel = "clock" if action.action == "check_time" else action.channel
                    query_attempts[channel] = query_attempts.get(channel, 0) + 1
                    if sum(query_attempts.values()) > int(
                        config["limits"]["max_tool_calls_per_step"]
                    ):
                        capped = SelectionResult(
                            action=ModelAction("choose", "A", (), "NONE"),
                            failed_closed=True,
                            attempts=selection.attempts,
                            raw_selected_handles=selection.raw_selected_handles,
                            last_raw_text=selection.last_raw_text,
                            failure_reason="maximum tool calls per step exceeded",
                        )
                        _record_failure(
                            failure_path,
                            failures,
                            day["name"],
                            step["id"],
                            interaction_index,
                            capped,
                        )
                        messages.append(
                            {
                                "role": "user",
                                "content": (
                                    "Harness notice: the per-step tool-call limit was exceeded. "
                                    "No task action was executed for this step."
                                ),
                            }
                        )
                        final_selection = capped
                        break
                    query_counts[channel] = query_counts.get(channel, 0) + 1
                    items = PM_BENCH.resolve_state_query_items(
                        channel,
                        day["steps"],
                        step_index,
                        day["name"],
                        day_start_minutes,
                        state_channels,
                        last_query_step_by_channel,
                        last_snapshot_item_by_channel,
                    )
                    observation = PM_BENCH.format_state_query_display(channel, items)
                    messages.append({"role": "user", "content": observation})
                    tool_results.append({"channel": channel, "observation": observation})
                    continue
                final_selection = selection

            assert final_selection is not None
            original_handles = list(final_selection.raw_selected_handles)
            validated_handles = list(final_selection.action.task_ids)
            canonical_task_ids: list[str] = []
            for handle in validated_handles:
                mapped_id = handle_to_id.get(handle)
                if mapped_id is not None and mapped_id not in canonical_task_ids:
                    canonical_task_ids.append(mapped_id)

            # Evaluator-only due state is computed only after the model action is fixed
            # and handles are mapped. It is never passed to ActionSelector or transport.
            step_minutes = PM_BENCH.time_to_minutes(step["time"])
            evaluator_due_task_ids = PM_BENCH.compute_due_now(
                task_states,
                active_task_ids,
                step,
                step_index,
                step_minutes,
                day_start_minutes,
            )
            previous_completed = {key for key, value in task_states.items() if value["completed"]}
            PM_BENCH.apply_runtime_completions(
                task_states,
                canonical_task_ids,
                evaluator_due_task_ids,
                step,
                step_index,
                step_minutes,
                day_start_minutes,
            )
            actions.append(
                {
                    "day": day["name"],
                    "step_id": step["id"],
                    "choice": final_selection.action.choice,
                    "task_ids": canonical_task_ids,
                    "selected_handles_raw": original_handles,
                    "selected_handles_validated": validated_handles,
                    "action_source": (
                        "fail_closed" if final_selection.failed_closed else "model"
                    ),
                    "invalid_response_failure": final_selection.failed_closed,
                    "attempts_for_final_interaction": final_selection.attempts,
                    "check_time": query_counts.get("clock", 0),
                    "state_queries": query_counts,
                    "state_query_attempts": query_attempts,
                    "heartbeat_enabled": False,
                    "heartbeat_interval_minutes": None,
                    "heartbeat_prompted": False,
                }
            )
            completed_now = {key for key, value in task_states.items() if value["completed"]} - previous_completed
            selected = set(canonical_task_ids)
            yield {
                "day": day["name"], "step_id": step["id"], "time": step["time"],
                "agent_messages": step_messages,
                "tools": tool_results,
                "action": actions[-1],
                "execution": [{"handle": id_to_handle[key], "outcome": "simulator_completed" if key in completed_now else "simulator_not_completed"} for key in canonical_task_ids],
                "evaluator": {
                    "due_task_ids": sorted(evaluator_due_task_ids),
                    "selected_task_ids": canonical_task_ids,
                    "missed": sorted(evaluator_due_task_ids - selected),
                    "false": sorted(selected - evaluator_due_task_ids),
                    "tp": len(selected & evaluator_due_task_ids),
                    "fp": len(selected - evaluator_due_task_ids),
                    "fn": len(evaluator_due_task_ids - selected),
                    "tasks": [{"id": key, "action": PM_BENCH.runtime_task_action_text(value), "status": "completed" if value["completed"] else "canceled" if value["canceled"] else "pending" if value["active"] else "not_encoded", "updated": value["updated"]} for key, value in task_states.items() if value["active"]],
                },
            }
    return actions, failures


def _record_failure(
    path: Path,
    failures: list[dict[str, Any]],
    day: str,
    step_id: str,
    interaction_index: int,
    selection: SelectionResult,
) -> None:
    record = {
        "record_type": "fail_closed_action",
        "timestamp_utc": utc_now(),
        "day": day,
        "step_id": step_id,
        "interaction_index": interaction_index,
        "attempts": selection.attempts,
        "raw_selected_handles": list(selection.raw_selected_handles),
        "last_raw_text": selection.last_raw_text,
        "reason": selection.failure_reason,
        "executed_task_ids": [],
    }
    failures.append(record)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _summarize_call_log(path: Path) -> dict[str, Any]:
    input_tokens = 0
    output_tokens = 0
    attempts = 0
    invalid_attempts = 0
    reported_models: set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            record = json.loads(line)
            attempts += 1
            usage = record.get("usage") or {}
            input_tokens += int(usage.get("input_tokens", 0) or 0)
            output_tokens += int(usage.get("output_tokens", 0) or 0)
            if record.get("parse_error") or record.get("transport_error"):
                invalid_attempts += 1
            if record.get("reported_model"):
                reported_models.add(record["reported_model"])
    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "attempts": attempts,
        "invalid_attempts": invalid_attempts,
        "reported_models": sorted(reported_models),
    }


def _git_state(project_root: Path) -> tuple[str, bool]:
    commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    status = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return commit, bool(status.strip())

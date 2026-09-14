from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .hashing import sha256_file, sha256_json


class ConfigError(ValueError):
    """Raised when an experiment configuration is incomplete or unsafe."""


REQUIRED_TOP_LEVEL = {
    "schema_version",
    "experiment_id",
    "condition",
    "benchmark_split",
    "scenario",
    "prompt",
    "model",
    "sampling",
    "limits",
    "execution",
    "output",
}


def load_config(path: Path, project_root: Path) -> tuple[dict[str, Any], dict[str, str]]:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"{path} must be a JSON document (valid YAML 1.2 subset): {exc}"
        ) from exc
    if not isinstance(raw, dict):
        raise ConfigError("Experiment config must be an object.")
    missing = sorted(REQUIRED_TOP_LEVEL - set(raw))
    if missing:
        raise ConfigError(f"Missing config fields: {', '.join(missing)}")

    resolved = json.loads(json.dumps(raw))
    resolved["scenario"] = str(_resolve_project_path(project_root, raw["scenario"]))
    prompt = resolved["prompt"]
    if not isinstance(prompt, dict) or "base_path" not in prompt:
        raise ConfigError("prompt.base_path is required.")
    prompt["base_path"] = str(_resolve_project_path(project_root, prompt["base_path"]))
    addendum = prompt.get("addendum_path")
    if addendum:
        prompt["addendum_path"] = str(_resolve_project_path(project_root, addendum))
    output = resolved["output"]
    if not isinstance(output, dict) or "root" not in output:
        raise ConfigError("output.root is required.")
    output["root"] = str(_resolve_project_path(project_root, output["root"]))

    hashes = {
        "config_file_sha256": sha256_file(path),
        "resolved_config_sha256": sha256_json(resolved),
    }
    return resolved, hashes


def _resolve_project_path(project_root: Path, value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = project_root / path
    return path.resolve()


def validate_runtime_config(config: dict[str, Any], allow_paid_cli: bool) -> None:
    status = config.get("status")
    if status in {"not-implemented", "locked-until-prompt-freeze", "locked-until-method-selection"}:
        raise ConfigError(f"Configuration is intentionally disabled: {status}")
    provider = config["model"].get("provider")
    allow_paid_config = bool(config["execution"].get("allow_paid", False))
    if provider != "mock" and not (allow_paid_config and allow_paid_cli):
        raise ConfigError(
            "Non-mock execution requires both execution.allow_paid=true and "
            "the explicit --allow-paid CLI flag."
        )
    if provider == "openrouter":
        route = config["model"].get("route")
        if not route or str(route).startswith("REQUIRED_"):
            raise ConfigError("OpenRouter execution requires a real pinned provider route.")
    if config["prompt"].get("addendum_path"):
        addendum_path = Path(config["prompt"]["addendum_path"])
        text = addendum_path.read_text(encoding="utf-8")
        if "UNFROZEN_PLACEHOLDER" in text:
            raise ConfigError("The prospective-memory prompt is an unfrozen placeholder.")
    if int(config["limits"].get("max_retries", 0)) < 0:
        raise ConfigError("limits.max_retries must be non-negative.")
    if int(config["limits"].get("max_tool_calls_per_step", 0)) < 0:
        raise ConfigError("limits.max_tool_calls_per_step must be non-negative.")

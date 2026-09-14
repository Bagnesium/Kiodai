from __future__ import annotations

import json
import os
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Protocol


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace(
        "+00:00", "Z"
    )


@dataclass(frozen=True)
class TransportResponse:
    raw_text: str | None
    raw_response: Any
    usage: dict[str, int]
    reported_model: str | None = None
    provider_metadata: dict[str, Any] | None = None


class ModelTransport(Protocol):
    def invoke(self, request: dict[str, Any], timeout_seconds: float) -> TransportResponse:
        ...


@dataclass(frozen=True)
class ModelAction:
    action: str
    choice: str
    task_ids: tuple[str, ...]
    channel: str


@dataclass(frozen=True)
class SelectionResult:
    action: ModelAction
    failed_closed: bool
    attempts: int
    raw_selected_handles: tuple[Any, ...]
    last_raw_text: str | None
    failure_reason: str | None


class TransportFailure(RuntimeError):
    """A request failed after the shared transport retry policy."""


class RunStopped(RuntimeError):
    """Budget or route gate stopped a run; never retry or substitute mock output."""


def safe_error(exc):
    text = f"{type(exc).__name__}: {exc}"
    key = os.environ.get("OPENROUTER_API_KEY")
    return text.replace(key, "[REDACTED]") if key else text


class ActionValidationError(ValueError):
    pass


def action_schema(allowed_handles: tuple[str, ...], allowed_channels: tuple[str, ...]) -> dict[str, Any]:
    item_schema: dict[str, Any] = {"type": "string"}
    if allowed_handles:
        item_schema["enum"] = list(allowed_handles)
    return {
        "type": "object",
        "properties": {
            "action": {"type": "string", "enum": ["choose", "query_state", "check_time"]},
            "choice": {"type": "string", "enum": ["A", "B", "C", "NONE"]},
            "task_ids": {
                "type": "array",
                "items": item_schema,
                "maxItems": min(8, len(allowed_handles)),
            },
            "channel": {
                "type": "string",
                "enum": sorted(set(allowed_channels + ("NONE",))),
            },
        },
        "required": ["action", "choice", "task_ids", "channel"],
        "additionalProperties": False,
    }


def extract_raw_handles(raw_text: str | None) -> tuple[Any, ...]:
    if raw_text is None:
        return ()
    try:
        payload = json.loads(raw_text)
    except (TypeError, json.JSONDecodeError):
        return ()
    if not isinstance(payload, dict) or not isinstance(payload.get("task_ids"), list):
        return ()
    return tuple(payload["task_ids"])


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ActionValidationError("duplicate JSON object field")
        result[key] = value
    return result


def parse_action(
    raw_text: str | None,
    allowed_handles: tuple[str, ...],
    allowed_channels: tuple[str, ...],
) -> ModelAction:
    if raw_text is None or not raw_text.strip():
        raise ActionValidationError("empty response")
    try:
        payload = json.loads(raw_text, object_pairs_hook=_unique_object)
    except json.JSONDecodeError as exc:
        raise ActionValidationError(f"invalid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise ActionValidationError("response must be a JSON object")
    expected_keys = {"action", "choice", "task_ids", "channel"}
    if set(payload) != expected_keys:
        missing = sorted(expected_keys - set(payload))
        extra = sorted(set(payload) - expected_keys)
        raise ActionValidationError(f"wrong fields; missing={missing}, extra={extra}")

    action = payload["action"]
    choice = payload["choice"]
    task_ids = payload["task_ids"]
    channel = payload["channel"]
    if action not in ("choose", "query_state", "check_time"):
        raise ActionValidationError(f"unsupported action: {action!r}")
    if not isinstance(task_ids, list) or not all(isinstance(item, str) for item in task_ids):
        raise ActionValidationError("task_ids must be a list of strings")
    if len(task_ids) > 8:
        raise ActionValidationError("too many task handles")
    if len(task_ids) != len(set(task_ids)):
        raise ActionValidationError("duplicate task handles are invalid")
    unknown_handles = [item for item in task_ids if item not in allowed_handles]
    if unknown_handles:
        raise ActionValidationError(f"unknown task handles: {unknown_handles}")

    if action == "choose":
        if choice not in ("A", "B", "C"):
            raise ActionValidationError("choose requires choice A, B, or C")
        if channel != "NONE":
            raise ActionValidationError("choose requires channel NONE")
    else:
        if choice != "NONE" or task_ids:
            raise ActionValidationError(f"{action} requires choice NONE and no task handles")
        normalized_channel = "clock" if action == "check_time" else channel
        if normalized_channel not in allowed_channels:
            raise ActionValidationError(f"unavailable channel: {normalized_channel!r}")
        channel = normalized_channel
    return ModelAction(action, choice, tuple(task_ids), channel)


class ActionSelector:
    """Model boundary accepting only agent-visible content and anonymous handles."""

    def __init__(
        self,
        transport: ModelTransport,
        raw_log_path: Path,
        model_settings: dict[str, Any],
        sampling: dict[str, Any],
        limits: dict[str, Any],
    ) -> None:
        self.transport = transport
        self.raw_log_path = raw_log_path
        self.model_settings = dict(model_settings)
        self.sampling = dict(sampling)
        self.limits = dict(limits)

    def select_action(
        self,
        *,
        messages: list[dict[str, str]],
        allowed_handles: tuple[str, ...],
        allowed_channels: tuple[str, ...],
        call_context: dict[str, Any],
    ) -> SelectionResult:
        max_retries = min(1, max(0, int(self.limits.get("max_retries", 0))))
        max_attempts = max_retries + 1
        last_raw_text = None
        last_handles: tuple[Any, ...] = ()
        last_error = None
        retry_messages = json.loads(json.dumps(messages))
        for attempt in range(1, max_attempts + 1):
            request = self._build_request(retry_messages, allowed_handles, allowed_channels)
            started = utc_now()
            start_perf = time.perf_counter()
            response = None
            transport_error = None
            try:
                response = self.transport.invoke(
                    request, float(self.limits.get("timeout_seconds", 120))
                )
                last_raw_text = response.raw_text
                last_handles = extract_raw_handles(last_raw_text)
                parsed = parse_action(last_raw_text, allowed_handles, allowed_channels)
                parse_error = None
            except RunStopped:
                raise
            except Exception as exc:  # transport failures are separate from malformed output
                parsed = None
                parse_error = safe_error(exc)
                last_error = parse_error
                if response is None:
                    transport_error = parse_error
                    parse_error = None
            record = {
                "record_type": "model_call_attempt",
                "call_context": dict(call_context),
                "attempt": attempt,
                "max_attempts": max_attempts,
                "started_at_utc": started,
                "finished_at_utc": utc_now(),
                "latency_seconds": round(time.perf_counter() - start_perf, 6),
                "request": request,
                "raw_text": response.raw_text if response else None,
                "raw_response": response.raw_response if response else None,
                "usage": response.usage if response else {},
                "reported_model": response.reported_model if response else None,
                "provider_metadata": response.provider_metadata if response else None,
                "parse_error": parse_error,
                "transport_error": transport_error,
                "parsed_action": asdict(parsed) if parsed else None,
            }
            self._append_record(record)
            if response and (response.provider_metadata or {}).get("route_error"):
                raise RunStopped(response.provider_metadata["route_error"])
            if transport_error and attempt == max_attempts:
                raise TransportFailure(transport_error)
            if parse_error and attempt < max_attempts:
                retry_messages.extend([
                    {"role": "assistant", "content": last_raw_text or ""},
                    {"role": "user", "content": "Invalid response. Return exactly one JSON object matching the supplied schema. Use only offered action handles and channels; no extra fields or duplicate keys."},
                ])
            if parsed is not None:
                return SelectionResult(
                    action=parsed,
                    failed_closed=False,
                    attempts=attempt,
                    raw_selected_handles=last_handles,
                    last_raw_text=last_raw_text,
                    failure_reason=None,
                )

        return SelectionResult(
            action=ModelAction("choose", "A", (), "NONE"),
            failed_closed=True,
            attempts=max_attempts,
            raw_selected_handles=last_handles,
            last_raw_text=last_raw_text,
            failure_reason=last_error or "unknown invalid-response failure",
        )

    def _build_request(
        self,
        messages: list[dict[str, str]],
        allowed_handles: tuple[str, ...],
        allowed_channels: tuple[str, ...],
    ) -> dict[str, Any]:
        request = {
            "provider": self.model_settings["provider"],
            "provider_route": self.model_settings.get("route"),
            "route_fallbacks_allowed": bool(
                self.model_settings.get("allow_route_fallbacks", False)
            ),
            "provider_require_parameters": bool(
                self.model_settings.get("require_parameters", False)
            ),
            "provider_quantizations": list(
                self.model_settings.get("quantizations", [])
            ),
            "model": self.model_settings["model_id"],
            "messages": json.loads(json.dumps(messages)),
            "temperature": self.sampling.get("temperature"),
            "top_p": self.sampling.get("top_p"),
            "seed": self.sampling.get("seed"),
            "max_tokens": self.limits.get("max_output_tokens"),
            "reasoning": self.model_settings.get("reasoning"),
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "pm_action",
                    "strict": True,
                    "schema": action_schema(allowed_handles, allowed_channels),
                },
            },
        }
        return request

    def _append_record(self, record: dict[str, Any]) -> None:
        with self.raw_log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


class MockTransport:
    """Deterministic local transport; it performs no network operations."""

    def __init__(self, responses: list[Any] | None = None) -> None:
        self.responses = list(responses or [])
        self.index = 0

    def invoke(self, request: dict[str, Any], timeout_seconds: float) -> TransportResponse:
        del timeout_seconds
        if self.index < len(self.responses):
            item = self.responses[self.index]
            self.index += 1
        else:
            item = '{"action":"choose","choice":"A","task_ids":[],"channel":"NONE"}'
        if isinstance(item, Exception):
            raise item
        if isinstance(item, dict) and "raw_text" in item:
            raw_text = item.get("raw_text")
            raw_response = item.get("raw_response", {"mock": True, "content": raw_text})
            usage = item.get("usage", {})
            reported_model = item.get("reported_model", request["model"])
        else:
            raw_text = str(item) if item is not None else None
            raw_response = {"mock": True, "content": raw_text}
            request_chars = len(json.dumps(request, ensure_ascii=False))
            usage = {
                "input_tokens": (request_chars + 3) // 4,
                "output_tokens": (len(raw_text or "") + 3) // 4,
            }
            reported_model = request["model"]
        return TransportResponse(
            raw_text=raw_text,
            raw_response=raw_response,
            usage=usage,
            reported_model=reported_model,
            provider_metadata={"transport": "deterministic-mock", "network": False},
        )


class OpenAICompatibleTransport:
    """Lazy OpenAI-compatible transport with optional OpenRouter route pinning."""

    def __init__(self, api_key: str, base_url: str | None = None) -> None:
        from openai import OpenAI

        self.client = OpenAI(api_key=api_key, base_url=base_url, max_retries=0)

    def invoke(self, request: dict[str, Any], timeout_seconds: float) -> TransportResponse:
        kwargs: dict[str, Any] = {
            "model": request["model"],
            "messages": request["messages"],
            "temperature": request["temperature"],
            "top_p": request["top_p"],
            "max_tokens": request["max_tokens"],
            "response_format": request["response_format"],
            "timeout": timeout_seconds,
        }
        if request.get("seed") is not None:
            kwargs["seed"] = request["seed"]
        if request["provider"] == "openrouter" and request.get("provider_route"):
            extra_body: dict[str, Any] = {
                "provider": {
                    "order": [request["provider_route"]],
                    "only": [request["provider_route"]],
                    "allow_fallbacks": bool(request["route_fallbacks_allowed"]),
                    "require_parameters": bool(request["provider_require_parameters"]),
                    "quantizations": list(request.get("provider_quantizations", [])),
                },
            }
            if request.get("reasoning") is not None:
                extra_body["reasoning"] = request["reasoning"]
            kwargs["extra_body"] = extra_body
        response = self.client.chat.completions.create(**kwargs)
        raw_dump = response.model_dump(mode="json")
        raw_text = None
        if response.choices:
            raw_text = response.choices[0].message.content
        usage = {}
        if response.usage is not None:
            usage = {
                "input_tokens": int(response.usage.prompt_tokens or 0),
                "output_tokens": int(response.usage.completion_tokens or 0),
                "total_tokens": int(response.usage.total_tokens or 0),
            }
        return TransportResponse(
            raw_text=raw_text,
            raw_response=raw_dump,
            usage=usage,
            reported_model=getattr(response, "model", None),
            provider_metadata={"route_requested": request.get("provider_route"),
                               "provider_reported": raw_dump.get("provider"),
                               "cost_usd_reported": (raw_dump.get("usage") or {}).get("cost")},
        )

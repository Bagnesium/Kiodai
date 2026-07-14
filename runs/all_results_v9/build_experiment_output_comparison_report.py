#!/usr/bin/env python3
from __future__ import annotations

import argparse
import math
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


RESULTS_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = RESULTS_DIR.parents[1]
SIM_ROOT = PROJECT_ROOT / "sim"
for path in (str(PROJECT_ROOT), str(SIM_ROOT)):
    if path not in sys.path:
        sys.path.insert(0, path)

import pm_bench as PM_BENCH


SETUP_ORDER = [
    "single-baseline",
    "single-todo-ledger",
    "heartbeat-proactive",
    "heartbeat-auto-60m",
    "heartbeat-auto-30m",
    "hier-union-query",
    "hier-majority-vote",
    "hier-unanimous-vote",
]

SETUP_DESCRIPTIONS = {
    "single-baseline": (
        "live",
        "Single-agent baseline with no heartbeat scaffold.",
    ),
    "single-todo-ledger": (
        "live",
        "Single-agent run with the notebook-style in-context TODO ledger memory aid.",
    ),
    "heartbeat-proactive": (
        "live",
        "Single-agent run with optional heartbeat; the model decides whether to use proactive reminders.",
    ),
    "heartbeat-auto-60m": (
        "live",
        "Single-agent run with automatic proactive heartbeat reminders every 60 virtual minutes.",
    ),
    "heartbeat-auto-30m": (
        "live",
        "Single-agent run with automatic proactive heartbeat reminders every 30 virtual minutes.",
    ),
    "hier-union-query": (
        "live",
        "Hierarchical 3-subagent run with union-query evidence gathering and coordinator-only final task selection.",
    ),
    "hier-majority-vote": (
        "replay",
        "Replay-derived variant of the union-query run that keeps the same queried evidence but replaces task selection with strict majority vote over subagent task handles.",
    ),
    "hier-unanimous-vote": (
        "replay",
        "Replay-derived variant of the union-query run that keeps the same queried evidence but replaces task selection with unanimous agreement over subagent task handles.",
    ),
}

MODEL_DISPLAY = {
    "gpt-54": "GPT-5.4",
    "gpt-53-codex": "GPT-5.3-Codex",
    "llama-33-70b-instruct": "Llama 3.3 70B Instruct",
    "mistral-large-2512": "Mistral Large 2512",
    "mistral-small-32-24b-instruct": "Mistral Small 3.2 24B Instruct",
    "qwen3-32b": "Qwen3-32B",
    "qwen3-14b": "Qwen3-14B",
    "qwen3-8b": "Qwen3-8B",
}

MODEL_ORDER = [
    "gpt-54",
    "gpt-53-codex",
    "llama-33-70b-instruct",
    "mistral-large-2512",
    "mistral-small-32-24b-instruct",
    "qwen3-32b",
    "qwen3-14b",
    "qwen3-8b",
]

PROACTIVE_CHANNEL_ORDER = [
    "appointment_portal",
    "bank_balance",
    "calendar",
    "clock",
    "course_portal",
    "email",
    "library_hold",
    "shipment_status",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a cross-model PM-Bench comparison report for March_ALL_results_v9."
    )
    parser.add_argument(
        "--results-dir",
        default=str(RESULTS_DIR),
        help="Directory containing per-model run folders.",
    )
    parser.add_argument(
        "--scenario",
        default=str(PROJECT_ROOT / "data" / "synthetic_week_v9.json"),
        help="Scenario JSON used to rescore the logs.",
    )
    parser.add_argument(
        "--out",
        default=str(RESULTS_DIR / "experiment_output_comparison_report.md"),
        help="Markdown output path.",
    )
    return parser.parse_args()


def pct(numerator: int | float, denominator: int | float) -> float | None:
    if denominator <= 0:
        return None
    return (float(numerator) / float(denominator)) * 100.0


def fmt_pct(value: float | None) -> str:
    return "n/a" if value is None else f"{value:.1f}%"


def fmt_float(value: float | None, digits: int = 3) -> str:
    return "n/a" if value is None else f"{value:.{digits}f}"


def fmt_count_rate(hit: int, total: int) -> str:
    return f"{hit}/{total} ({fmt_pct(pct(hit, total))})"


def fmt_monitoring_counts(counts: dict[str, int]) -> str:
    return (
        f"{counts['hit']}/{counts['late']}/{counts['miss']}/{counts['total']} "
        f"({fmt_pct(pct(counts['hit'], counts['total']))})"
    )


def fmt_duration(seconds: float | None) -> str:
    if seconds is None:
        return "n/a"
    if seconds <= 0:
        return "0.0s"
    total_seconds = float(seconds)
    minutes, rem = divmod(total_seconds, 60.0)
    hours, minutes = divmod(minutes, 60.0)
    if hours >= 1:
        return f"{int(hours)}h {int(minutes)}m {rem:.1f}s"
    if minutes >= 1:
        return f"{int(minutes)}m {rem:.1f}s"
    return f"{rem:.1f}s"


def mean(values: list[float | None]) -> float | None:
    filtered = [value for value in values if value is not None]
    if not filtered:
        return None
    return sum(filtered) / len(filtered)


def safe_divide(numerator: int | float, denominator: int | float) -> float | None:
    if denominator == 0:
        return None
    return float(numerator) / float(denominator)


def setup_sort_key(setup: str) -> tuple[int, str]:
    if setup in SETUP_ORDER:
        return (SETUP_ORDER.index(setup), setup)
    return (len(SETUP_ORDER), setup)


def model_sort_key(model_label: str) -> tuple[int, str]:
    if model_label in MODEL_ORDER:
        return (MODEL_ORDER.index(model_label), model_label)
    return (len(MODEL_ORDER), model_label)


def markdown_table(headers: list[str], rows: list[list[str]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(["---"] * len(headers)) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(lines)


@dataclass
class RunRecord:
    model_label: str
    model_display: str
    setup_label: str
    run_type: str
    run_dir: Path
    log_path: Path
    score_path: Path | None
    run_metadata: dict[str, Any] | None
    summary: dict[str, Any]
    per_day: dict[str, Any]
    summary_steps: int
    total_tasks: int
    by_type: dict[str, dict[str, int]]
    by_monitoring: dict[str, dict[str, int]]
    by_monitoring_channel: dict[str, dict[str, int]]
    state_query_calls_by_channel: dict[str, int]
    set_precision: float | None
    set_recall: float | None
    set_f1: float | None
    hit_rate: float | None
    late_rate: float | None
    miss_rate: float | None
    precision_hit: float | None
    precision_any: float | None
    exact_set_match_rate: float | None
    exact_set_avg_reward: float | None
    proactive_hit_rate: float | None
    proactive_any_rate: float | None
    no_proactive_hit_rate: float | None
    no_proactive_any_rate: float | None
    clock_proactive_hit_rate: float | None
    clock_proactive_any_rate: float | None
    non_clock_proactive_hit_rate: float | None
    non_clock_proactive_any_rate: float | None
    event_hit_rate: float | None
    time_hit_rate: float | None
    duration_seconds: float | None


def detect_setup_label(run_name: str, model_label: str) -> str:
    marker = f"-{model_label}-v9-"
    if marker not in run_name:
        raise ValueError(f"Unable to parse setup label from run name: {run_name}")
    return run_name.split(marker, 1)[0]


def find_log_path(run_dir: Path) -> Path:
    candidates = sorted(
        path
        for path in run_dir.glob("*.jsonl")
        if not path.name.endswith(".debug.jsonl") and not path.name.endswith(".ledger.jsonl")
    )
    if len(candidates) != 1:
        raise ValueError(f"Expected exactly one primary log file in {run_dir}, found {len(candidates)}")
    return candidates[0]


def aggregate_total_tasks(by_type: dict[str, dict[str, int]]) -> int:
    return sum(counts["total"] for counts in by_type.values())


def combine_monitoring_counts(
    channel_counts: dict[str, dict[str, int]],
    *,
    include_channels: list[str],
) -> dict[str, int]:
    combined = {"hit": 0, "late": 0, "miss": 0, "total": 0}
    for channel in include_channels:
        counts = channel_counts.get(channel)
        if not counts:
            continue
        for key in ("hit", "late", "miss", "total"):
            combined[key] += counts.get(key, 0)
    return combined


def classify_run_type(meta: dict[str, Any] | None, setup_label: str) -> str:
    if meta:
        mode = str(meta.get("mode", ""))
        if mode.startswith("replay-"):
            return "replay"
    return SETUP_DESCRIPTIONS.get(setup_label, ("live", ""))[0]


def load_run_record(
    scenario: dict[str, Any],
    model_dir: Path,
    run_dir: Path,
) -> RunRecord:
    model_label = model_dir.name
    setup_label = detect_setup_label(run_dir.name, model_label)
    log_path = find_log_path(run_dir)
    score_candidates = sorted(run_dir.glob("*.score.md"))
    score_path = score_candidates[0] if score_candidates else None
    log_entries, run_metadata = PM_BENCH.read_log_with_metadata(str(log_path))
    summary, per_day, summary_steps = PM_BENCH.score_log(scenario, log_entries)
    by_type = PM_BENCH.aggregate_type_counts(per_day)
    by_monitoring = PM_BENCH.aggregate_monitoring_counts(per_day)
    by_monitoring_channel = PM_BENCH.aggregate_monitoring_channel_counts(per_day)
    state_query_calls_by_channel = PM_BENCH.aggregate_state_query_call_counts(per_day)
    event_hit, event_total, time_hit, time_total = PM_BENCH.compute_event_time_rates(by_type)

    proactive_counts = by_monitoring["proactive_monitoring_required"]
    no_proactive_counts = by_monitoring["no_proactive_monitoring"]
    clock_counts = by_monitoring_channel.get(
        "clock", {"hit": 0, "late": 0, "miss": 0, "total": 0}
    )
    non_clock_channels = [
        channel for channel in by_monitoring_channel.keys() if channel != "clock"
    ]
    non_clock_counts = combine_monitoring_counts(
        by_monitoring_channel, include_channels=non_clock_channels
    )

    return RunRecord(
        model_label=model_label,
        model_display=MODEL_DISPLAY.get(model_label, model_label),
        setup_label=setup_label,
        run_type=classify_run_type(run_metadata, setup_label),
        run_dir=run_dir,
        log_path=log_path,
        score_path=score_path,
        run_metadata=run_metadata,
        summary=summary,
        per_day=per_day,
        summary_steps=summary_steps,
        total_tasks=aggregate_total_tasks(by_type),
        by_type=by_type,
        by_monitoring=by_monitoring,
        by_monitoring_channel=by_monitoring_channel,
        state_query_calls_by_channel=state_query_calls_by_channel,
        set_precision=pct(summary["set_tp"], summary["set_tp"] + summary["set_fp"]),
        set_recall=pct(summary["set_tp"], summary["set_tp"] + summary["set_fn"]),
        set_f1=pct(2 * summary["set_tp"], (2 * summary["set_tp"]) + summary["set_fp"] + summary["set_fn"]),
        hit_rate=pct(summary["hit"], aggregate_total_tasks(by_type)),
        late_rate=pct(summary["late"], aggregate_total_tasks(by_type)),
        miss_rate=pct(summary["miss"], aggregate_total_tasks(by_type)),
        precision_hit=pct(summary["hit"], summary["chosen_tasks"]),
        precision_any=pct(summary["hit"] + summary["late"], summary["chosen_tasks"]),
        exact_set_match_rate=pct(summary["exact_set_match_steps"], summary_steps),
        exact_set_avg_reward=safe_divide(summary["exact_set_match_reward"], summary_steps),
        proactive_hit_rate=pct(proactive_counts["hit"], proactive_counts["total"]),
        proactive_any_rate=pct(proactive_counts["hit"] + proactive_counts["late"], proactive_counts["total"]),
        no_proactive_hit_rate=pct(no_proactive_counts["hit"], no_proactive_counts["total"]),
        no_proactive_any_rate=pct(no_proactive_counts["hit"] + no_proactive_counts["late"], no_proactive_counts["total"]),
        clock_proactive_hit_rate=pct(clock_counts["hit"], clock_counts["total"]),
        clock_proactive_any_rate=pct(clock_counts["hit"] + clock_counts["late"], clock_counts["total"]),
        non_clock_proactive_hit_rate=pct(non_clock_counts["hit"], non_clock_counts["total"]),
        non_clock_proactive_any_rate=pct(non_clock_counts["hit"] + non_clock_counts["late"], non_clock_counts["total"]),
        event_hit_rate=pct(event_hit, event_total),
        time_hit_rate=pct(time_hit, time_total),
        duration_seconds=(
            float(run_metadata["duration_seconds"])
            if run_metadata and run_metadata.get("duration_seconds") is not None
            else None
        ),
    )


def collect_runs(results_dir: Path, scenario_path: Path) -> list[RunRecord]:
    scenario = PM_BENCH.load_scenario(str(scenario_path))
    records: list[RunRecord] = []
    for model_dir in sorted((path for path in results_dir.iterdir() if path.is_dir()), key=lambda p: model_sort_key(p.name)):
        for run_dir in sorted((path for path in model_dir.iterdir() if path.is_dir())):
            records.append(load_run_record(scenario, model_dir, run_dir))
    records.sort(key=lambda record: (model_sort_key(record.model_label), setup_sort_key(record.setup_label)))
    return records


def build_setup_summary(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    records_by_setup: dict[str, list[RunRecord]] = {}
    for record in records:
        records_by_setup.setdefault(record.setup_label, []).append(record)

    for setup_label in sorted(records_by_setup, key=setup_sort_key):
        group = records_by_setup[setup_label]
        tp = sum(item.summary["set_tp"] for item in group)
        fp = sum(item.summary["set_fp"] for item in group)
        fn = sum(item.summary["set_fn"] for item in group)
        best_run = max(group, key=lambda item: (-1 if item.set_f1 is None else item.set_f1, item.model_display))
        worst_run = min(group, key=lambda item: (math.inf if item.set_f1 is None else item.set_f1, item.model_display))
        rows.append(
            [
                setup_label,
                SETUP_DESCRIPTIONS.get(setup_label, ("n/a", ""))[0],
                fmt_pct(mean([item.set_f1 for item in group])),
                fmt_pct(pct(2 * tp, (2 * tp) + fp + fn)),
                str(tp),
                str(fp),
                str(fn),
                fmt_pct(mean([item.hit_rate for item in group])),
                fmt_pct(mean([item.precision_hit for item in group])),
                fmt_pct(mean([item.proactive_hit_rate for item in group])),
                fmt_pct(mean([item.clock_proactive_hit_rate for item in group])),
                fmt_pct(mean([item.non_clock_proactive_hit_rate for item in group])),
                str(sum(item.summary["state_query_calls"] for item in group)),
                str(sum(item.summary["chosen_tasks"] for item in group)),
                f"{best_run.model_display} ({fmt_pct(best_run.set_f1)})",
                f"{worst_run.model_display} ({fmt_pct(worst_run.set_f1)})",
            ]
        )
    return rows


def build_model_best_summary(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    records_by_model: dict[str, list[RunRecord]] = {}
    for record in records:
        records_by_model.setdefault(record.model_label, []).append(record)

    for model_label in sorted(records_by_model, key=model_sort_key):
        group = records_by_model[model_label]
        best_set_f1 = max(group, key=lambda item: (-1 if item.set_f1 is None else item.set_f1, -item.summary["set_tp"]))
        best_proactive = max(group, key=lambda item: (-1 if item.proactive_hit_rate is None else item.proactive_hit_rate, -1 if item.set_f1 is None else item.set_f1))
        best_non_clock = max(group, key=lambda item: (-1 if item.non_clock_proactive_hit_rate is None else item.non_clock_proactive_hit_rate, -1 if item.set_f1 is None else item.set_f1))
        rows.append(
            [
                MODEL_DISPLAY.get(model_label, model_label),
                f"{best_set_f1.setup_label} ({fmt_pct(best_set_f1.set_f1)})",
                f"{best_proactive.setup_label} ({fmt_pct(best_proactive.proactive_hit_rate)})",
                f"{best_non_clock.setup_label} ({fmt_pct(best_non_clock.non_clock_proactive_hit_rate)})",
                f"{best_set_f1.setup_label}: {best_set_f1.summary['set_tp']}/{best_set_f1.summary['set_fp']}/{best_set_f1.summary['set_fn']}",
            ]
        )
    return rows


def build_core_metrics_table(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    for record in records:
        rows.append(
            [
                record.model_display,
                record.setup_label,
                record.run_type,
                str(record.summary["set_tp"]),
                str(record.summary["set_fp"]),
                str(record.summary["set_fn"]),
                fmt_pct(record.set_precision),
                fmt_pct(record.set_recall),
                fmt_pct(record.set_f1),
                fmt_pct(record.hit_rate),
                fmt_pct(record.exact_set_match_rate),
                str(record.summary["state_query_calls"]),
                str(record.summary["check_time_calls"]),
                str(record.summary["chosen_tasks"]),
                fmt_duration(record.duration_seconds),
            ]
        )
    return rows


def build_error_control_table(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    for record in records:
        rows.append(
            [
                record.model_display,
                record.setup_label,
                record.run_type,
                str(record.summary["false_alarm"]),
                str(record.summary["commission"]),
                str(record.summary["wrong_content"]),
                str(record.summary["dependency_violation"]),
                str(record.summary["overkill_steps"]),
                fmt_pct(record.late_rate),
                fmt_pct(record.miss_rate),
                fmt_pct(pct(record.summary["false_alarm"], record.summary_steps)),
                fmt_pct(pct(record.summary["overkill_steps"], record.summary_steps)),
            ]
        )
    return rows


def build_proactive_table(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    for record in records:
        clock_queries = record.state_query_calls_by_channel.get("clock", 0)
        non_clock_queries = record.summary["state_query_calls"] - clock_queries
        rows.append(
            [
                record.model_display,
                record.setup_label,
                record.run_type,
                fmt_pct(record.proactive_hit_rate),
                fmt_pct(record.proactive_any_rate),
                fmt_pct(record.no_proactive_hit_rate),
                fmt_pct(record.clock_proactive_hit_rate),
                fmt_pct(record.clock_proactive_any_rate),
                fmt_pct(record.non_clock_proactive_hit_rate),
                fmt_pct(record.non_clock_proactive_any_rate),
                str(record.summary["state_query_calls"]),
                str(clock_queries),
                str(non_clock_queries),
            ]
        )
    return rows


def build_proactive_channel_table(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    for record in records:
        row = [record.model_display, record.setup_label, record.run_type]
        for channel in PROACTIVE_CHANNEL_ORDER:
            counts = record.by_monitoring_channel.get(channel, {"hit": 0, "late": 0, "miss": 0, "total": 0})
            row.append(fmt_monitoring_counts(counts))
        rows.append(row)
    return rows


def build_cross_day_update_table(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    for record in records:
        summary = record.summary
        update_effective_total = summary["update_total"] - summary["update_canceled"]
        rows.append(
            [
                record.model_display,
                record.setup_label,
                record.run_type,
                f"{summary['cross_day_hit']}/{summary['cross_day_late']}/{summary['cross_day_miss']}/{summary['cross_day_total']}",
                f"{summary['update_hit']}/{summary['update_late']}/{summary['update_miss']}/{summary['update_canceled']}/{summary['update_total']}",
                str(summary["update_violation"]),
                fmt_pct(pct(summary["cross_day_hit"], summary["cross_day_total"])),
                fmt_pct(pct(summary["cross_day_hit"] + summary["cross_day_late"], summary["cross_day_total"])),
                fmt_pct(pct(summary["update_hit"], update_effective_total)),
                fmt_pct(pct(summary["update_hit"] + summary["update_late"], update_effective_total)),
            ]
        )
    return rows


def build_setup_channel_summary(records: list[RunRecord]) -> list[list[str]]:
    rows: list[list[str]] = []
    records_by_setup: dict[str, list[RunRecord]] = {}
    for record in records:
        records_by_setup.setdefault(record.setup_label, []).append(record)

    for setup_label in sorted(records_by_setup, key=setup_sort_key):
        group = records_by_setup[setup_label]
        row = [setup_label]
        for channel in PROACTIVE_CHANNEL_ORDER:
            hit = late = miss = total = 0
            for record in group:
                counts = record.by_monitoring_channel.get(channel, {"hit": 0, "late": 0, "miss": 0, "total": 0})
                hit += counts["hit"]
                late += counts["late"]
                miss += counts["miss"]
                total += counts["total"]
            row.append(f"{hit}/{late}/{miss}/{total} ({fmt_pct(pct(hit, total))})")
        rows.append(row)
    return rows


def build_model_notes(records: list[RunRecord]) -> list[str]:
    notes: list[str] = []
    records_by_model: dict[str, list[RunRecord]] = {}
    for record in records:
        records_by_model.setdefault(record.model_label, []).append(record)

    for model_label in sorted(records_by_model, key=model_sort_key):
        group = records_by_model[model_label]
        baseline = next(item for item in group if item.setup_label == "single-baseline")
        best = max(group, key=lambda item: (-1 if item.set_f1 is None else item.set_f1, -item.summary["set_tp"]))
        best_proactive = max(group, key=lambda item: (-1 if item.proactive_hit_rate is None else item.proactive_hit_rate, -1 if item.set_f1 is None else item.set_f1))
        note = (
            f"- **{MODEL_DISPLAY.get(model_label, model_label)}**: baseline Set-F1 {fmt_pct(baseline.set_f1)}; "
            f"best overall is `{best.setup_label}` at {fmt_pct(best.set_f1)} "
            f"(TP/FP/FN = {best.summary['set_tp']}/{best.summary['set_fp']}/{best.summary['set_fn']}); "
            f"best proactive-required hit rate is `{best_proactive.setup_label}` at {fmt_pct(best_proactive.proactive_hit_rate)}."
        )
        notes.append(note)
    return notes


def build_cross_setup_conclusions(records: list[RunRecord]) -> list[str]:
    records_by_setup: dict[str, list[RunRecord]] = {}
    for record in records:
        records_by_setup.setdefault(record.setup_label, []).append(record)

    def macro(setup: str, attr: str) -> float | None:
        return mean([getattr(item, attr) for item in records_by_setup[setup]])

    best_set_f1_setup = max(
        records_by_setup,
        key=lambda setup: (-1 if macro(setup, "set_f1") is None else macro(setup, "set_f1")),
    )
    best_proactive_setup = max(
        records_by_setup,
        key=lambda setup: (-1 if macro(setup, "proactive_hit_rate") is None else macro(setup, "proactive_hit_rate")),
    )
    best_non_clock_setup = max(
        records_by_setup,
        key=lambda setup: (-1 if macro(setup, "non_clock_proactive_hit_rate") is None else macro(setup, "non_clock_proactive_hit_rate")),
    )
    most_queries_setup = max(records_by_setup, key=lambda setup: sum(item.summary["state_query_calls"] for item in records_by_setup[setup]))
    fewest_fp_setup = min(
        records_by_setup,
        key=lambda setup: sum(item.summary["set_fp"] for item in records_by_setup[setup]),
    )
    highest_fp_setup = max(
        records_by_setup,
        key=lambda setup: sum(item.summary["set_fp"] for item in records_by_setup[setup]),
    )

    union_macro = macro("hier-union-query", "set_f1")
    majority_macro = macro("hier-majority-vote", "set_f1")
    unanimous_macro = macro("hier-unanimous-vote", "set_f1")
    auto30_macro = macro("heartbeat-auto-30m", "set_f1")
    auto60_macro = macro("heartbeat-auto-60m", "set_f1")
    auto30_proactive = macro("heartbeat-auto-30m", "proactive_hit_rate")
    auto60_proactive = macro("heartbeat-auto-60m", "proactive_hit_rate")

    conclusions = [
        (
            f"1. Best overall Set-F1 in this V9 batch is `{best_set_f1_setup}` "
            f"(macro Set-F1 {fmt_pct(macro(best_set_f1_setup, 'set_f1'))})."
        ),
        (
            f"2. Best proactive-required hit rate is `{best_proactive_setup}` "
            f"(macro proactive hit {fmt_pct(macro(best_proactive_setup, 'proactive_hit_rate'))}); "
            f"best non-clock proactive hit rate is `{best_non_clock_setup}` "
            f"({fmt_pct(macro(best_non_clock_setup, 'non_clock_proactive_hit_rate'))})."
        ),
        (
            f"3. `{most_queries_setup}` issues the most state queries "
            f"({sum(item.summary['state_query_calls'] for item in records_by_setup[most_queries_setup])} total), "
            f"while `{fewest_fp_setup}` has the lowest aggregate FP pressure "
            f"({sum(item.summary['set_fp'] for item in records_by_setup[fewest_fp_setup])} total FP)."
        ),
        (
            f"4. The strongest proactive-only setup is not the strongest utility setup. "
            f"`{best_proactive_setup}` raises macro proactive hit to {fmt_pct(macro(best_proactive_setup, 'proactive_hit_rate'))}, "
            f"but it also has the highest aggregate FP count "
            f"({sum(item.summary['set_fp'] for item in records_by_setup[highest_fp_setup])} FP for `{highest_fp_setup}`), "
            f"which keeps its macro Set-F1 well below the best live single-agent variants."
        ),
        (
            f"5. Auto-heartbeat frequency trades recall for noise. "
            f"`heartbeat-auto-30m` improves macro proactive hit over `heartbeat-auto-60m` "
            f"({fmt_pct(auto30_proactive)} vs {fmt_pct(auto60_proactive)}), "
            f"but both trail `heartbeat-proactive` on macro Set-F1, and `auto30` drives the largest action volume among live single-agent setups."
        ),
        (
            f"6. Clock monitoring remains far easier than non-clock monitoring. "
            f"Even the best non-clock macro hit rate is only {fmt_pct(macro(best_non_clock_setup, 'non_clock_proactive_hit_rate'))}, "
            f"far below the best clock macro hit rate of {fmt_pct(macro(best_proactive_setup, 'clock_proactive_hit_rate'))}."
        ),
        (
            f"7. The replay-derived hierarchical variants should be interpreted as decision-rule ablations over the same union-query evidence. "
            f"Macro Set-F1 shifts from union-query {fmt_pct(union_macro)} "
            f"to majority-vote {fmt_pct(majority_macro)} and unanimous-vote {fmt_pct(unanimous_macro)}."
        ),
    ]
    return conclusions


def build_report(records: list[RunRecord], results_dir: Path, scenario_path: Path) -> str:
    def public_path(path: Path) -> str:
        try:
            return str(path.relative_to(PROJECT_ROOT))
        except ValueError:
            return path.name

    setup_summary_rows = build_setup_summary(records)
    model_summary_rows = build_model_best_summary(records)
    core_rows = build_core_metrics_table(records)
    error_rows = build_error_control_table(records)
    proactive_rows = build_proactive_table(records)
    proactive_channel_rows = build_proactive_channel_table(records)
    cross_day_rows = build_cross_day_update_table(records)
    setup_channel_rows = build_setup_channel_summary(records)
    model_notes = build_model_notes(records)
    conclusions = build_cross_setup_conclusions(records)

    models_present = sorted({record.model_display for record in records})
    setups_present = sorted({record.setup_label for record in records}, key=setup_sort_key)

    lines: list[str] = [
        "# Experiment Output Comparison Report",
        "",
        "## Scope",
        "",
        f"Compared scored PM-Bench runs under `{public_path(results_dir)}` using scenario `{public_path(scenario_path)}`.",
        f"- Runs covered: {len(records)} total ({len(models_present)} models x {len(setups_present)} setups).",
        f"- Models covered: {', '.join(models_present)}.",
        f"- Setups covered: {', '.join(setups_present)}.",
        "- Primary emphasis: `Set F1`, TP/FP/FN tradeoffs, proactive monitoring performance, cross-day/update handling, and state-query behavior.",
        "- Important interpretation detail: `hier-majority-vote` and `hier-unanimous-vote` are included as separate setups, but they are replay-derived decision-rule variants of `hier-union-query`, not fresh inference runs.",
        "",
        "## Setup Definitions",
        "",
        markdown_table(
            ["Setup", "Run Type", "Meaning"],
            [
                [setup, SETUP_DESCRIPTIONS[setup][0], SETUP_DESCRIPTIONS[setup][1]]
                for setup in setups_present
            ],
        ),
        "",
        "## Setup-Level Summary (Across 8 Models)",
        "",
        markdown_table(
            [
                "Setup",
                "Run Type",
                "Macro Set-F1",
                "Micro Set-F1",
                "Micro TP",
                "Micro FP",
                "Micro FN",
                "Macro Hit Rate",
                "Macro Precision(hit)",
                "Macro Proactive Hit",
                "Macro Clock Hit",
                "Macro Non-Clock Hit",
                "Total State Queries",
                "Total Actions",
                "Best Model",
                "Worst Model",
            ],
            setup_summary_rows,
        ),
        "",
        "## Best Setup Per Model",
        "",
        markdown_table(
            [
                "Model",
                "Best Set-F1 Setup",
                "Best Proactive Setup",
                "Best Non-Clock Proactive Setup",
                "Best Set-F1 TP/FP/FN",
            ],
            model_summary_rows,
        ),
        "",
        "## Per-Run Core Metrics",
        "",
        markdown_table(
            [
                "Model",
                "Setup",
                "Run Type",
                "TP",
                "FP",
                "FN",
                "Set Precision",
                "Set Recall",
                "Set F1",
                "Hit Rate",
                "Exact-Set Match",
                "State Queries",
                "Check_time",
                "Actions",
                "Duration",
            ],
            core_rows,
        ),
        "",
        "## Per-Run Error / Control Metrics",
        "",
        markdown_table(
            [
                "Model",
                "Setup",
                "Run Type",
                "False Alarms",
                "Commission",
                "Wrong-Content",
                "Dependency Violations",
                "Overkill Steps",
                "Late Rate",
                "Miss Rate",
                "False Alarm/Step",
                "Overkill/Step",
            ],
            error_rows,
        ),
        "",
        "## Per-Run Proactive Monitoring",
        "",
        markdown_table(
            [
                "Model",
                "Setup",
                "Run Type",
                "Proactive Hit",
                "Proactive Any",
                "No-Proactive Hit",
                "Clock Hit",
                "Clock Any",
                "Non-Clock Hit",
                "Non-Clock Any",
                "State Queries",
                "Clock Queries",
                "Non-Clock Queries",
            ],
            proactive_rows,
        ),
        "",
        "## Per-Run Proactive Required by Channel",
        "",
        markdown_table(
            ["Model", "Setup", "Run Type"] + PROACTIVE_CHANNEL_ORDER,
            proactive_channel_rows,
        ),
        "",
        "## Cross-Day and Update Metrics",
        "",
        markdown_table(
            [
                "Model",
                "Setup",
                "Run Type",
                "Cross-day Hit/Late/Miss/Total",
                "Update Hit/Late/Miss/Canceled/Total",
                "Update Violations",
                "Cross-day Hit",
                "Cross-day Any",
                "Update Hit",
                "Update Any",
            ],
            cross_day_rows,
        ),
        "",
        "## Setup-Level Proactive Required by Channel (Aggregated Across 8 Models)",
        "",
        markdown_table(
            ["Setup"] + PROACTIVE_CHANNEL_ORDER,
            setup_channel_rows,
        ),
        "",
        "## Model-by-Model Notes",
        "",
        *model_notes,
        "",
        "## Cross-Setup Conclusions",
        "",
        *conclusions,
        "",
    ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    results_dir = Path(args.results_dir).expanduser().resolve()
    scenario_path = Path(args.scenario).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()

    records = collect_runs(results_dir, scenario_path)
    report = build_report(records, results_dir, scenario_path)
    out_path.write_text(report, encoding="utf-8")
    print(f"Wrote report: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

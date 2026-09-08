#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST = PROJECT_ROOT / "research" / "protected_hashes.json"

PROTECTED_EXACT = {
    "data/synthetic_week_v9.json": "released_benchmark",
    "webapp/frontend/public/scenarios/synthetic_week_v9.json": "browser_benchmark_copy",
}
PROTECTED_TREES = {
    "sim": "original_runtime_evaluator_generator",
    "runs/all_results_v9": "released_results",
    "webapp/frontend/src": "browser_scoring_implementation",
}
PROTECTED_FRONTEND_FILES = {
    "webapp/frontend/package.json": "browser_scoring_environment",
    "webapp/frontend/package-lock.json": "browser_scoring_environment",
    "webapp/frontend/eslint.config.js": "browser_scoring_environment",
    "webapp/frontend/tsconfig.app.json": "browser_scoring_environment",
    "webapp/frontend/tsconfig.json": "browser_scoring_environment",
    "webapp/frontend/tsconfig.node.json": "browser_scoring_environment",
    "webapp/frontend/vite.config.ts": "browser_scoring_environment",
}


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_protected_files() -> dict[str, str]:
    categories = dict(PROTECTED_EXACT)
    categories.update(PROTECTED_FRONTEND_FILES)
    for relative_root, category in PROTECTED_TREES.items():
        root = PROJECT_ROOT / relative_root
        if not root.is_dir():
            raise FileNotFoundError(f"Protected directory is missing: {relative_root}")
        for path in root.rglob("*"):
            if not path.is_file():
                continue
            if "__pycache__" in path.parts or path.suffix in {".pyc", ".pyo"}:
                continue
            relative = path.relative_to(PROJECT_ROOT).as_posix()
            categories[relative] = category
    missing = [relative for relative in categories if not (PROJECT_ROOT / relative).is_file()]
    if missing:
        raise FileNotFoundError(f"Protected files are missing: {missing}")
    return dict(sorted(categories.items()))


def current_commit() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=PROJECT_ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def create_manifest() -> dict:
    categories = discover_protected_files()
    files = {
        relative: {
            "sha256": sha256_file(PROJECT_ROOT / relative),
            "bytes": (PROJECT_ROOT / relative).stat().st_size,
            "category": category,
        }
        for relative, category in categories.items()
    }
    return {
        "schema_version": 1,
        "created_at_utc": datetime.now(timezone.utc)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        "baseline_git_commit": current_commit(),
        "policy": {
            "exact_paths": sorted(PROTECTED_EXACT),
            "protected_trees": sorted(PROTECTED_TREES),
            "browser_environment_files": sorted(PROTECTED_FRONTEND_FILES),
        },
        "file_count": len(files),
        "files": files,
    }


def verify_manifest(manifest_path: Path) -> list[str]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected = manifest.get("files", {})
    discovered = discover_protected_files()
    errors: list[str] = []
    expected_paths = set(expected)
    discovered_paths = set(discovered)
    for relative in sorted(expected_paths - discovered_paths):
        errors.append(f"protected file missing: {relative}")
    for relative in sorted(discovered_paths - expected_paths):
        errors.append(f"unrecorded protected file: {relative}")
    for relative in sorted(expected_paths & discovered_paths):
        path = PROJECT_ROOT / relative
        actual_hash = sha256_file(path)
        recorded_hash = expected[relative].get("sha256")
        if actual_hash != recorded_hash:
            errors.append(
                f"hash mismatch: {relative}: expected {recorded_hash}, got {actual_hash}"
            )
        actual_size = path.stat().st_size
        if actual_size != expected[relative].get("bytes"):
            errors.append(
                f"size mismatch: {relative}: expected {expected[relative].get('bytes')}, "
                f"got {actual_size}"
            )
        if discovered[relative] != expected[relative].get("category"):
            errors.append(f"category mismatch: {relative}")
    if manifest.get("file_count") != len(expected):
        errors.append("manifest file_count does not match files object")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify immutable PM-Bench files.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--write-manifest",
        action="store_true",
        help="Create the initial manifest. Refuses to overwrite an existing file.",
    )
    args = parser.parse_args()
    manifest_path = args.manifest.resolve()
    if args.write_manifest:
        if manifest_path.exists():
            print(f"Refusing to overwrite existing integrity manifest: {manifest_path}")
            return 2
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        payload = create_manifest()
        manifest_path.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote {payload['file_count']} protected hashes to {manifest_path}")
        return 0

    if not manifest_path.is_file():
        print(f"Integrity manifest not found: {manifest_path}")
        return 2
    errors = verify_manifest(manifest_path)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(f"Protected-file integrity OK: {manifest['file_count']} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


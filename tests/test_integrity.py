from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERIFY_PATH = ROOT / "scripts" / "verify_benchmark_integrity.py"


def load_verify_module():
    spec = importlib.util.spec_from_file_location("verify_benchmark_integrity", VERIFY_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


class ProtectedFileIntegrityTests(unittest.TestCase):
    def test_all_recorded_protected_hashes_match(self) -> None:
        verifier = load_verify_module()
        errors = verifier.verify_manifest(ROOT / "research" / "protected_hashes.json")
        self.assertEqual(errors, [])

    def test_manifest_covers_every_discovered_protected_file(self) -> None:
        verifier = load_verify_module()
        manifest = json.loads(
            (ROOT / "research" / "protected_hashes.json").read_text(encoding="utf-8")
        )
        self.assertEqual(set(manifest["files"]), set(verifier.discover_protected_files()))
        self.assertEqual(manifest["file_count"], 164)


if __name__ == "__main__":
    unittest.main()


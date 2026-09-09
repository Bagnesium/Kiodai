"""Restoring the committed smoke must preserve pre-existing local evidence."""
import contextlib
import io
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from kiodai_v2.common import digest
from scripts import restore_deepseek_smoke as restore


class SmokeRestorationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name).resolve()
        name = 'research/v2/deepseek_smoke_artifact_inventory.json'
        self.inventory = json.loads((restore.ROOT/name).read_text())
        for source in (name, self.inventory['archive']):
            path = self.root/source
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(restore.ROOT/source, path)

    def run_restore(self):
        with patch.object(restore, 'ROOT', self.root), contextlib.redirect_stdout(io.StringIO()):
            restore.main()

    def test_missing_artifacts_restore_and_second_invocation_preserves_bytes(self):
        self.run_restore()
        for name, expected in self.inventory['files'].items():
            self.assertEqual(digest((self.root/name).read_bytes()), expected)
        before = {name: (self.root/name).stat().st_mtime_ns for name in self.inventory['files']}
        self.run_restore()
        self.assertEqual(before, {name: (self.root/name).stat().st_mtime_ns for name in before})

    def test_one_conflict_prevents_partial_restoration(self):
        name = next(iter(self.inventory['files']))
        conflict = self.root/name
        conflict.parent.mkdir(parents=True, exist_ok=True)
        conflict.write_bytes(b'local evidence must survive')
        with self.assertRaisesRegex(SystemExit, 'Preserving different local artifact'):
            self.run_restore()
        self.assertEqual(conflict.read_bytes(), b'local evidence must survive')
        self.assertEqual([p for p in (self.root/'results').rglob('*') if p.is_file()], [conflict])

    def test_corrupt_archive_creates_no_result_directory(self):
        with (self.root/self.inventory['archive']).open('ab') as stream:
            stream.write(b'corrupt')
        with self.assertRaisesRegex(SystemExit, 'Archive hash mismatch'):
            self.run_restore()
        self.assertFalse((self.root/'results').exists())


if __name__ == '__main__':
    unittest.main()

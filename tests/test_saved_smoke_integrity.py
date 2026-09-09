"""Saved evidence must verify without inference, mutation, or invented accounting."""
import json
import shutil
import sqlite3
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from kiodai_v2.common import digest
from kiodai_v2.gateway import Gateway
from scripts import verify_saved_smoke as verify


class SavedSmokeIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        inventory = json.loads((verify.ROOT/verify.INVENTORY).read_text())
        for name in [str(verify.INVENTORY), inventory['archive'], *inventory['posthoc_files']]:
            target = self.root/name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(verify.ROOT/name, target)
        with zipfile.ZipFile(self.root/inventory['archive']) as archive:
            for name in archive.namelist():
                target = verify.inside(self.root, name, verify.SMOKE)
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.read(name))
        self.study = self.root/verify.SMOKE
        self.case = self.study/'v2_hidden_91320/A2'

    def test_relocated_copy_verifies_without_writes_or_inference(self):
        def snapshot():
            return {str(p.relative_to(self.root)): digest(p.read_bytes())
                    for p in self.root.rglob('*') if p.is_file()}
        before = snapshot()
        with patch.object(Gateway, 'call', side_effect=AssertionError('No inference during verification')):
            result = verify.verify(self.root)
        self.assertEqual((result['tp'], result['fp'], result['fn']), (0, 0, 2))
        self.assertEqual(result['attempts'], 24)
        self.assertIsNone(result['verified_billed_cost_usd'])
        self.assertEqual(snapshot(), before)

    def test_altered_report_is_rejected_without_regenerating_it(self):
        path = self.study/'report.json'
        report = json.loads(path.read_text())
        report['cases'][0]['tp'] = 3
        path.write_text(json.dumps(report))
        changed = path.read_bytes()
        with self.assertRaisesRegex(ValueError, 'Local evidence changed'):
            verify.verify(self.root)
        self.assertEqual(path.read_bytes(), changed)

    def test_missing_response_log_is_not_restored_by_verification(self):
        path = self.case/'calls.jsonl'
        path.unlink()
        with self.assertRaisesRegex(ValueError, 'Missing evidence'):
            verify.verify(self.root)
        self.assertFalse(path.exists())

    def test_modified_archive_is_rejected(self):
        archive = next((self.root/'artifacts/verification').glob('*.zip'))
        with archive.open('ab') as stream:
            stream.write(b'corruption')
        with self.assertRaisesRegex(ValueError, 'Archive hash mismatch'):
            verify.verify(self.root)

    def test_cost_reconciliation_rejects_ledger_api_disagreement(self):
        with sqlite3.connect(self.study/'accounting.sqlite') as database:
            database.execute('UPDATE attempts SET reported=0 WHERE id=1')
        with self.assertRaisesRegex(ValueError, 'Ledger/API cost mismatch'):
            verify.verify_accounting(self.study, self.case)

    def test_unavailable_billing_cannot_be_reclassified_as_verified(self):
        path = self.study/'study.json'
        study = json.loads(path.read_text())
        study['budget']['verified_billed_cost_usd'] = .01525668
        path.write_text(json.dumps(study))
        with self.assertRaisesRegex(ValueError, 'Unsupported independently verified billing'):
            verify.verify_accounting(self.study, self.case)

    def test_frozen_source_check_does_not_require_other_live_runs(self):
        for name in ('research/v2/freeze.json', 'research/v2/deepseek_smoke_v1_freeze.json'):
            frozen = json.loads((verify.ROOT/name).read_text())
            for source in [name, *frozen['hashes']]:
                target = self.root/source
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(verify.ROOT/source, target)
        self.assertFalse((self.root/'results/kiodai').exists())
        self.assertFalse((self.root/'results/followup_v1').exists())
        self.assertGreater(verify.verify_sources(self.root), 0)
        path = self.root/'prompts/v2/extract.txt'
        path.write_text(path.read_text()+'\nchanged prompt\n')
        with self.assertRaisesRegex(ValueError, 'Frozen source changed'):
            verify.verify_sources(self.root)


if __name__ == '__main__':
    unittest.main()

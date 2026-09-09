#!/usr/bin/env python3
"""Restore missing archived v2 artifacts; refuse to overwrite different local evidence."""
import json
import sys
import zipfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import digest
ROOT=Path(__file__).resolve().parents[1]


def main():
    inventory=json.loads((ROOT/'research/v2/artifact_inventory.json').read_text())
    archive=ROOT/inventory['archive']
    if digest(archive.read_bytes())!=inventory['archive_sha256']:
        raise SystemExit('Archive hash mismatch')
    with zipfile.ZipFile(archive) as z:
        if set(z.namelist())!=set(inventory['files']):
            raise SystemExit('Archive membership mismatch')
        for name, expected in inventory['files'].items():
            path=(ROOT/name).resolve()
            if not path.is_relative_to(ROOT/'results/v2') or digest(z.read(name))!=expected:
                raise SystemExit('Unsafe or modified archive member')
            if path.exists() and digest(path.read_bytes())!=expected:
                raise SystemExit('Preserving different local artifact: '+name)
        for name in z.namelist():
            path=ROOT/name
            if not path.exists():
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(z.read(name))
    print('Archived v2 artifacts verified; missing files restored without overwriting evidence.')


if __name__=='__main__':main()

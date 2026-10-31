#!/usr/bin/env python3
"""Refresh sha256 and row_count in every data/<dataset>.manifest.json from its CSV.
Optional: --version X.Y.Z sets the version in every manifest.

Usage: python3 scripts/regen_manifests.py [--version X.Y.Z]
"""
import csv
import hashlib
import json
import os
import sys

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = os.path.join(root, 'data')
version = sys.argv[sys.argv.index('--version') + 1] if '--version' in sys.argv else None

for name in sorted(os.listdir(data)):
    if not name.endswith('.manifest.json'):
        continue
    key = name[: -len('.manifest.json')]
    path = os.path.join(data, name)
    manifest = json.load(open(path, encoding='utf-8'))
    raw = open(os.path.join(data, key + '.csv'), 'rb').read()
    manifest['sha256'] = hashlib.sha256(raw).hexdigest()
    manifest['row_count'] = len(list(csv.DictReader(raw.decode('utf-8').splitlines())))
    if version:
        manifest['version'] = version
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
        f.write('\n')
    print(f"{key}: {manifest['row_count']} rows")

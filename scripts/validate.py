#!/usr/bin/env python3
"""Validate every dataset in data/: manifest present and complete, sha256 and row_count match the CSV,
required columns present and non-blank, `active` is 0/1, natural keys unique. Exit 1 on any problem.

Usage: python3 scripts/validate.py [repo root]
"""
import csv
import hashlib
import json
import os
import re
import sys

root = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = os.path.join(root, 'data')
with open(os.path.join(root, 'schema.json'), encoding='utf-8') as f:
    schema = json.load(f)['datasets']

MANIFEST_KEYS = ['name', 'version', 'source', 'source_url', 'as_of', 'row_count', 'sha256']
problems = []
seen = set()

for name in sorted(os.listdir(data)):
    if not name.endswith('.manifest.json'):
        continue
    key = name[: -len('.manifest.json')]
    seen.add(key)
    with open(os.path.join(data, name), encoding='utf-8') as f:
        manifest = json.load(f)
    for k in MANIFEST_KEYS:
        if manifest.get(k) in (None, ''):
            problems.append(f'{key}: manifest misses {k}')
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(manifest.get('as_of', ''))):
        problems.append(f'{key}: as_of must be YYYY-MM-DD')
    if key not in schema:
        problems.append(f'{key}: not declared in schema.json')
        continue
    path = os.path.join(data, key + '.csv')
    if not os.path.exists(path):
        problems.append(f'{key}: {key}.csv missing')
        continue
    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xef\xbb\xbf'):
        problems.append(f'{key}: CSV has a BOM')
    if hashlib.sha256(raw).hexdigest() != manifest.get('sha256'):
        problems.append(f'{key}: sha256 does not match the CSV')
    rows = list(csv.DictReader(raw.decode('utf-8').splitlines()))
    if len(rows) != manifest.get('row_count'):
        problems.append(f'{key}: row_count {manifest.get("row_count")} but CSV has {len(rows)} rows')
    header = rows[0].keys() if rows else []
    spec = schema[key]
    for col in spec['required'] + ['active']:
        if col not in header:
            problems.append(f'{key}: missing column {col}')
    keys = set()
    for i, row in enumerate(rows, start=2):
        for col in spec['required']:
            if not (row.get(col) or '').strip():
                problems.append(f'{key} line {i}: blank {col}')
        if row.get('active') not in ('0', '1'):
            problems.append(f'{key} line {i}: active must be 0 or 1')
        for col in ('effective_from', 'effective_to'):
            v = (row.get(col) or '').strip()
            if v and not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
                problems.append(f'{key} line {i}: {col} must be YYYY-MM-DD')
        nk = tuple((row.get(c) or '').strip().lower() for c in spec['key'])
        if nk in keys:
            problems.append(f'{key} line {i}: duplicate key {nk}')
        keys.add(nk)

for key in sorted(set(f[:-4] for f in os.listdir(data) if f.endswith('.csv')) - seen):
    problems.append(f'{key}: CSV without a manifest')

if problems:
    print('\n'.join(problems))
    sys.exit(1)
print(f'OK: {len(seen)} datasets valid')

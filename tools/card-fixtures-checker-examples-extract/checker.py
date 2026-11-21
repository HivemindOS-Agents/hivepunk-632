#!/usr/bin/env python3
"""Card-fixtures checker. Stdlib only, no network.
Checks a fixture package holding card.json, checksums.txt, data/*.csv:
 - card-coverage:       card files == CSV files on disk (and card.json self-entry if present)
 - checksum-integrity:  SHA256 in checksums.txt recomputed for every entry
 - row-consistency:     CSV data rows (excluding header) == rows declared in card.json
Usage: python3 checker.py <dir> [--json]
Prints RESULT=pass|fail and EXIT=0|1. Untested in the step that wrote it.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def count_rows(path):
    with open(path, newline='', encoding='utf-8') as fh:
        rows = list(csv.reader(fh))
    return max(0, len(rows) - 1) if rows else 0


def _card_files(card):
    files = []
    raw = card.get('files', [])
    if isinstance(raw, dict):
        raw = list(raw.keys())
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, str):
                files.append(item)
            elif isinstance(item, dict) and isinstance(item.get('path'), str):
                files.append(item['path'])
    declared = {}
    raw_rows = card.get('rows', {})
    if isinstance(raw_rows, dict):
        for k, v in raw_rows.items():
            if isinstance(v, int):
                declared[k] = v
    if isinstance(raw, list):
        for item in raw:
            if isinstance(item, dict) and isinstance(item.get('path'), str) and isinstance(item.get('rows'), int):
                declared[item['path']] = item['rows']
    return files, declared


def load_card(directory):
    card_path = Path(directory) / 'card.json'
    card = json.loads(card_path.read_text(encoding='utf-8'))
    if not isinstance(card, dict):
        raise ValueError('card.json must hold a JSON object')
    return card


def load_checksums(directory):
    path = Path(directory) / 'checksums.txt'
    entries = {}
    order = []
    for line in path.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        parts = line.split()
        if len(parts) < 2:
            entries.setdefault('', []).append(line)
            continue
        digest, rel = parts[0].lower(), parts[-1].lstrip('*')
        if rel in entries:
            entries[rel].append(digest)
        else:
            entries[rel] = [digest]
            order.append(rel)
    return entries, order


def evaluate(directory):
    d = Path(directory)
    findings = []
    summary = {'card_coverage': 'pass', 'checksum_integrity': 'pass', 'row_consistency': 'pass'}
    def fail(kind, msg):
        findings.append(kind + ':' + msg)
        summary[kind.replace('-', '_')] = 'fail'
    try:
        card = load_card(d)
    except Exception as exc:
        return {'ok': False, 'findings': ['card-coverage:unreadable-card:%s' % exc], 'summary': summary, 'files': [], 'rows': {}}
    card_files, declared = _card_files(card)
    if not card_files:
        fail('card-coverage', 'empty-card-files')
    if len(card_files) != len(set(card_files)):
        for f in sorted(set(card_files)):
            if card_files.count(f) > 1:
                fail('card-coverage', 'duplicate-card-file:' + f)
    # CSVs on disk under data/ (and at top level if any)
    disk_csvs = sorted(str(p.relative_to(d)) for p in d.rglob('*.csv'))
    card_set = set(card_files)
    for f in disk_csvs:
        if f not in card_set:
            fail('card-coverage', 'disk-file-not-in-card:' + f)
    for f in sorted(card_set):
        if not (d / f).is_file():
            fail('card-coverage', 'card-file-missing-on-disk:' + f)
    # Checksums
    try:
        entries, order = load_checksums(d)
    except Exception as exc:
        fail('checksum-integrity', 'unreadable-checksums:%s' % exc)
        entries, order = {}, []
    for rel in order:
        target = d / rel
        if not target.is_file():
            fail('checksum-integrity', 'missing-file:' + rel)
            continue
        actual = sha256_file(target)
        for digest in entries[rel]:
            if digest != actual:
                fail('checksum-integrity', 'mismatch:' + rel)
    for f in disk_csvs:
        if f not in entries:
            fail('checksum-integrity', 'no-checksum-for:' + f)
    # Rows
    rows = {}
    for f in disk_csvs:
        try:
            rows[f] = count_rows(d / f)
        except Exception as exc:
            fail('row-consistency', 'unreadable-csv:%s:%s' % (f, exc))
    for f, expected in sorted(declared.items()):
        if f not in rows:
            fail('row-consistency', 'no-csv-for-declared-rows:' + f)
        elif rows[f] != expected:
            fail('row-consistency', 'row-count:%s:card=%d:actual=%d' % (f, expected, rows[f]))
    for f in disk_csvs:
        if f not in declared:
            fail('row-consistency', 'no-declared-rows:' + f)
    return {'ok': not findings, 'findings': findings, 'summary': summary, 'files': sorted(card_set), 'rows': rows}


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    as_json = '--json' in args
    dirs = [a for a in args if a != '--json']
    if not dirs:
        print('usage: python3 checker.py <dir> [--json]')
        print('RESULT=fail')
        print('EXIT=1')
        return 1
    try:
        out = evaluate(dirs[0])
    except Exception as exc:
        print('checker: %s: %s' % (type(exc).__name__, exc))
        print('RESULT=fail')
        print('EXIT=1')
        return 1
    if as_json:
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        for kind, state in sorted(out['summary'].items()):
            print(kind + '=' + state)
        for f in out['findings']:
            print('FINDING ' + f)
        print('files=%d findings=%d' % (len(out['files']), len(out['findings'])))
    print('RESULT=' + ('pass' if out['ok'] else 'fail'))
    print('EXIT=' + ('0' if out['ok'] else '1'))
    return 0 if out['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())

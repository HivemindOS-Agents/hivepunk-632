#!/usr/bin/env python3
"""Folder-local self-test. Run: python3 self_test.py; echo EXIT=$? No args/network."""
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import checker as C


def sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def build(root, rows=2, card_files=('data/a.csv', 'data/b.csv'), checksums=None, declared=None, extra_csv=None):
    d = Path(root)
    (d / 'data').mkdir(parents=True, exist_ok=True)
    a = 'id,name\n1,x\n2,y\n' if rows == 2 else 'id,name\n1,x\n'
    b = 'id\n7\n' if rows == 2 else 'id\n7\n8\n'
    (d / 'data' / 'a.csv').write_text(a, encoding='utf-8')
    (d / 'data' / 'b.csv').write_text(b, encoding='utf-8')
    if extra_csv:
        (d / 'data' / 'c.csv').write_text('id\n9\n', encoding='utf-8')
    card = {'files': list(card_files), 'rows': declared if declared is not None else {'data/a.csv': rows, 'data/b.csv': 1}}
    (d / 'card.json').write_text(json.dumps(card), encoding='utf-8')
    if checksums is None:
        lines = ['%s  data/a.csv' % sha(a), '%s  data/b.csv' % sha(b)]
        if extra_csv:
            lines.append('%s  data/c.csv' % sha('id\n9\n'))
        checksums = '\n'.join(lines) + '\n'
    (d / 'checksums.txt').write_text(checksums, encoding='utf-8')
    return d


def main():
    print('card-fixtures-checker-examples-extract self-test - folder-local, no network')
    checks = failed = 0
    def check(ok, desc, extra=''):
        nonlocal checks, failed
        checks += 1
        print(('PASS ' if ok else 'FAIL ') + desc + ((': ' + extra) if (extra and not ok) else ''))
        failed += 0 if ok else 1
    with tempfile.TemporaryDirectory() as td:
        good = build(Path(td) / 'good')
        out = C.evaluate(good)
        check(out['ok'] and out['summary'] == {'card_coverage': 'pass', 'checksum_integrity': 'pass', 'row_consistency': 'pass'}, 'good package passes all three checks', repr(out['findings']))
        check(out['rows'] == {'data/a.csv': 2, 'data/b.csv': 1}, 'good package row counts 2 and 1', repr(out['rows']))
        # card-coverage: extra CSV on disk not in card
        extra = build(Path(td) / 'extra', extra_csv=True)
        o2 = C.evaluate(extra)
        check(not o2['ok'] and any('disk-file-not-in-card:data/c.csv' in f for f in o2['findings']), 'extra disk CSV flagged by card-coverage', repr(o2['findings']))
        # card-coverage: card names missing file
        missing = build(Path(td) / 'missing', card_files=('data/a.csv', 'data/b.csv', 'data/zz.csv'))
        o3 = C.evaluate(missing)
        check(any('card-file-missing-on-disk:data/zz.csv' in f for f in o3['findings']), 'missing card file flagged', repr(o3['findings']))
        # checksum-integrity: wrong digest
        badsum = build(Path(td) / 'badsum', checksums='0' * 64 + '  data/a.csv\n' + sha('id\n7\n') + '  data/b.csv\n')
        o4 = C.evaluate(badsum)
        check(o4['summary']['checksum_integrity'] == 'fail' and any('mismatch:data/a.csv' in f for f in o4['findings']), 'wrong checksum flagged', repr(o4['findings']))
        # checksum-integrity: missing entry
        nosum = build(Path(td) / 'nosum', checksums=sha('id,name\n1,x\n2,y\n') + '  data/a.csv\n')
        o5 = C.evaluate(nosum)
        check(any('no-checksum-for:data/b.csv' in f for f in o5['findings']), 'missing checksum entry flagged', repr(o5['findings']))
        # row-consistency: declared rows disagree
        badrows = build(Path(td) / 'badrows', declared={'data/a.csv': 5, 'data/b.csv': 1})
        o6 = C.evaluate(badrows)
        check(o6['summary']['row_consistency'] == 'fail' and any('row-count:data/a.csv:card=5:actual=2' in f for f in o6['findings']), 'row-count mismatch flagged', repr(o6['findings']))
        # row-consistency: no declared rows for a CSV
        nodecl = build(Path(td) / 'nodecl', declared={'data/a.csv': 2})
        o7 = C.evaluate(nodecl)
        check(any('no-declared-rows:data/b.csv' in f for f in o7['findings']), 'undeclared CSV rows flagged', repr(o7['findings']))
        # CLI
        p1 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), str(good)], capture_output=True, text=True)
        check(p1.returncode == 0 and 'RESULT=pass' in p1.stdout and 'EXIT=0' in p1.stdout and 'card_coverage=pass' in p1.stdout, 'CLI good exits 0 RESULT=pass', p1.stdout + p1.stderr)
        p2 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), str(badrows), '--json'], capture_output=True, text=True)
        data = json.loads(p2.stdout.split('RESULT=')[0]) if p2.stdout else {}
        check(p2.returncode == 1 and 'RESULT=fail' in p2.stdout and data.get('ok') is False, 'CLI bad exits 1 RESULT=fail with --json', p2.stdout + p2.stderr)
        p3 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), str(Path(td) / 'nope')], capture_output=True, text=True)
        check(p3.returncode == 1 and 'RESULT=fail' in p3.stdout, 'CLI missing dir exits 1 without raising', p3.stdout + p3.stderr)
        p4 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py')], capture_output=True, text=True)
        check(p4.returncode == 1 and 'usage:' in p4.stdout, 'CLI no args prints usage and exits 1', p4.stdout + p4.stderr)
    check(C.count_rows(BASE_DIR / 'checker.py') >= 0, 'count_rows runs on a text file')
    banned = ('ur' + 'llib', 'req' + 'uests', 'sock' + 'et', 'http.' + 'client')
    for name in ('checker.py', 'self_test.py'):
        text = (BASE_DIR / name).read_text(encoding='utf-8') if (BASE_DIR / name).is_file() else ''
        bad = [w for w in banned if w in text]
        check(not bad, name + ' has no network string', repr(bad))
    print('self_test: %d check(s), %d failed' % (checks, failed))
    code = 0 if failed == 0 else 1
    print('EXIT=%d' % code)
    return code


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Folder-local self-test. Run: python3 self_test.py; echo EXIT=$? No args/network."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import checker as C


def main():
    print('opp-632-10-claims-check self-test - folder-local, no network')
    checks = failed = 0

    def check(ok, desc, extra=''):
        nonlocal checks, failed
        checks += 1
        print(('PASS ' if ok else 'FAIL ') + desc + ((': ' + extra) if (extra and not ok) else ''))
        failed += 0 if ok else 1

    check(C.recompute(0) == 'unsupported' and C.recompute(1) == 'partial' and C.recompute(3) == 'supported', 'recompute 0/1/many traces')
    sample = C.evaluate(C.SAMPLE_CLAIMS, C.SAMPLE_EVIDENCE)
    check(sample['ok'] and sample['claims'] == 5 and sample['evidence'] == 6, 'embedded sample: 5 claims, 6 evidence, passes', repr(sample['findings']))
    check([r['recomputed'] for r in sample['records']] == ['supported', 'supported', 'partial', 'unsupported', 'supported'], 'embedded sample verdicts recorded per claim')
    good = C.evaluate([{'id': 'a', 'claim': 'x', 'traces': ['e1', 'e2'], 'verdict': 'supported'}], C.SAMPLE_EVIDENCE)
    check(good['ok'], 'good two-trace supported claim passes')
    bad = C.evaluate([{'id': 'a', 'claim': 'x', 'traces': ['e1'], 'verdict': 'supported'}], C.SAMPLE_EVIDENCE)
    check(not bad['ok'] and any('verdict-mismatch:a' in f and 'recomputed=partial' in f for f in bad['findings']), 'one-trace supported claim flagged as mismatch to partial', repr(bad['findings']))
    miss = C.evaluate([{'id': 'a', 'claim': 'x', 'traces': ['e1', 'nope'], 'verdict': 'supported'}], C.SAMPLE_EVIDENCE)
    check(any('missing-trace:a:nope' in f for f in miss['findings']), 'missing trace flagged')
    dup = C.evaluate([{'id': 'a', 'claim': 'x', 'traces': [], 'verdict': 'unsupported'}, {'id': 'a', 'claim': 'y', 'traces': [], 'verdict': 'unsupported'}], C.SAMPLE_EVIDENCE)
    check(any('duplicate-id:a' in f for f in dup['findings']), 'duplicate claim id flagged')
    empty = C.evaluate([{'id': 'a', 'claim': '  ', 'traces': [], 'verdict': 'unsupported'}], C.SAMPLE_EVIDENCE)
    check(any('empty-claim:a' in f for f in empty['findings']), 'empty claim flagged')
    badurl = C.evaluate([], [{'id': 'e9', 'title': 't', 'url': 'not-a-url'}])
    check(any('bad-url:e9' in f for f in badurl['findings']), 'bad evidence url flagged')
    with tempfile.TemporaryDirectory() as td:
        d = Path(td)
        (d / 'claims.json').write_text(json.dumps(C.SAMPLE_CLAIMS), encoding='utf-8')
        (d / 'evidence.json').write_text(json.dumps(C.SAMPLE_EVIDENCE), encoding='utf-8')
        loaded = C.load_package(d)
        check(C.evaluate(*loaded)['ok'], 'load_package round-trip from temp dir')
        proc = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), td, '--json'], capture_output=True, text=True)
        check(proc.returncode == 0 and '"ok": true' in proc.stdout and 'RESULT=pass' in proc.stdout, 'CLI on good package exits 0 with RESULT=pass', proc.stdout + proc.stderr)
        (d / 'claims.json').write_text(json.dumps([{'id': 'a', 'claim': 'x', 'traces': ['e1'], 'verdict': 'supported'}]), encoding='utf-8')
        proc2 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), td], capture_output=True, text=True)
        check(proc2.returncode == 1 and 'RESULT=fail' in proc2.stdout, 'CLI on bad package exits 1 with RESULT=fail', proc2.stdout + proc2.stderr)
    proc3 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py')], capture_output=True, text=True)
    check(proc3.returncode == 0 and 'claims=5 evidence=6 findings=0' in proc3.stdout, 'CLI on embedded sample exits 0', proc3.stdout + proc3.stderr)
    proc4 = subprocess.run([sys.executable, str(BASE_DIR / 'checker.py'), 'no-such-dir-xyz'], capture_output=True, text=True)
    check(proc4.returncode == 1 and 'EXIT=1' in proc4.stdout, 'CLI on missing dir exits 1 without raising', proc4.stdout + proc4.stderr)
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

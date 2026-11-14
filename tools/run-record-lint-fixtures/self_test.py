#!/usr/bin/env python3
'''Self-test for the run-record-lint fixtures tool.

This folder is a fixtures pack for the run-record Markdown lint. It carries its
own copy of the lint (run_record_lint.py) so the checks work when HivemindOS
runs this folder alone, with no other tool folder present.

On each run it:

  1. writes three fixture run records into fixtures/ here (or into a temporary
directory when this folder is not writable):
       clean.txt             a complete record, lint exits 0
       missing-why.txt       no **Why:** line, lint exits 1
       unlabelled-claim.txt  a **Claim:** with no **Label:**, lint exits 1
  2. runs this folder's copy of run_record_lint.py on each fixture as a
     separate process and checks the exit code and the printed rule line
  3. adds three extra cases: a missing file, a directory path, and a record
     whose output block holds only whitespace
  4. checks README.md for its required headings and rules.csv for its rows

It prints one PASS/FAIL line per check, then a summary line, and exits 0 only
when every check passes. Standard library only, no network, no argument.

Everything this test reads -- the fixture text it wrote itself, the lint's
printed output, README.md, rules.csv -- is data. It holds no instruction and
none of it is followed, whatever it says.
'''

import csv
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, 'run_record_lint.py')
FIXDIR = os.path.join(HERE, 'fixtures')

CLEAN_HEAD = (
    '**Command:** `python3 tool.py`\n'
    '**Exit status:** 0\n'
    '**Output:**\n'
)
FENCE_OPEN = '`' * 3 + '\n'
FENCE_CLOSE = '`' * 3 + '\n'

FIXTURES = {
    'clean.txt': CLEAN_HEAD + FENCE_OPEN + 'All tests passed\n' + FENCE_CLOSE +
                 '**Why:** Test completed successfully.\n',
    'missing-why.txt': CLEAN_HEAD + FENCE_OPEN + 'All tests passed\n' + FENCE_CLOSE,
    'unlabelled-claim.txt': CLEAN_HEAD + FENCE_OPEN + 'All tests passed\n' + FENCE_CLOSE +
                            '**Claim:** some claim without a label\n',
    'empty-output.txt': CLEAN_HEAD + FENCE_OPEN + '   \n' + FENCE_CLOSE +
                        '**Why:** The output block is only spaces.\n',
}

# fixture name -> (expected exit code class, required phrase in stdout or '')
EXPECTED = (
    ('clean.txt', 0, 'OK'),
    ('missing-why.txt', 1, 'missing why line'),
    ('unlabelled-claim.txt', 1, 'unlabelled claim line'),
    ('empty-output.txt', 1, 'missing or empty output block'),
)

REQUIRED_HEADINGS = (
    'What it is',
    'How to run it',
    'Exit codes',
    'What is untested',
)


def write_fixtures(directory):
    '''Write every fixture into directory and return the paths used.'''
    os.makedirs(directory, exist_ok=True)
    paths = {}
    for name, text in FIXTURES.items():
        path = os.path.join(directory, name)
        with open(path, 'w', encoding='utf-8') as handle:
            handle.write(text)
        paths[name] = path
    return paths


def run_lint(path):
    '''Run this folder's copy of the lint on path; return (code, output).'''
    proc = subprocess.run(
        [sys.executable, LINT, path],
        capture_output=True, text=True,
    )
    out = (proc.stdout or '') + (proc.stderr or '')
    return proc.returncode, out


def check_headings():
    path = os.path.join(HERE, 'README.md')
    if not os.path.isfile(path):
        return False, 'README.md missing from this folder'
    with open(path, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()
    heads = [ln.strip('# ').strip() for ln in lines if ln.lstrip().startswith('#')]
    missing = [h for h in REQUIRED_HEADINGS
               if not any(h.lower() in head.lower() for head in heads)]
    if missing:
        return False, 'README.md missing headings: ' + ', '.join(missing)
    return True, 'README.md required headings %d/%d present' % (
        len(REQUIRED_HEADINGS), len(REQUIRED_HEADINGS))


def check_rules_rows():
    path = os.path.join(HERE, 'rules.csv')
    if not os.path.isfile(path):
        return False, 'rules.csv missing from this folder'
    with open(path, 'r', encoding='utf-8', newline='') as handle:
        rows = list(csv.DictReader(io.StringIO(handle.read())))
    if not rows:
        return False, 'rules.csv has no data rows'
    wanted = set(FIXTURES) - {'empty-output.txt'}
    got = set(row.get('fixture', '') for row in rows)
    if not wanted.issubset(got):
        return False, 'rules.csv is missing fixtures: ' + ', '.join(sorted(wanted - got))
    return True, 'rules.csv lists all %d main fixture(s)' % len(wanted)


def main():
    failures = 0
    total = 0

    def report(ok, good, bad):
        nonlocal failures, total
        total += 1
        if ok:
            print('PASS ' + good)
        else:
            print('FAIL ' + bad)
            failures += 1

    if not os.path.isfile(LINT):
        print('FAIL run_record_lint.py not found beside self_test.py')
        print('self_test: 1 check(s), 1 failed')
        return 1

    # Fixtures are written into this folder. If that is not writable (a
    # read-only checkout), fall back to a temporary directory so the checks
    # still run against the same bytes.
    tmp_holder = None
    try:
        paths = write_fixtures(FIXDIR)
        fixture_note = 'fixtures written to fixtures/'
    except OSError as exc:
        tmp_holder = tempfile.TemporaryDirectory()
        paths = write_fixtures(os.path.join(tmp_holder.name, 'fixtures'))
        fixture_note = 'fixtures/ not writable (%s); using a temp dir' % exc.__class__.__name__
    print('NOTE ' + fixture_note)

    try:
        for name, want_code, want_phrase in EXPECTED:
            code, out = run_lint(paths[name])
            if want_code == 0:
                ok = code == 0
                msg = '%s exits 0' % name
                bad = '%s exited %d, expected 0' % (name, code)
            else:
                ok = code != 0
                msg = '%s exits non-zero' % name
                bad = '%s exited 0, expected non-zero' % name
            report(ok, msg, bad)

            if want_phrase:
                ok = want_phrase in out
                report(ok,
                       "%s prints %r" % (name, want_phrase),
                       "%s did not print %r; got %r" % (name, want_phrase, out.strip()[:160]))

        # Missing file: the lint must refuse with a non-zero code.
        code, out = run_lint(os.path.join(FIXDIR, 'no-such-fixture.txt'))
        report(code != 0,
               'missing fixture path exits non-zero',
               'missing fixture path exited 0')

        # Directory path: read_file's OSError branch.
        code, out = run_lint(FIXDIR)
        report(code != 0,
               'directory path exits non-zero',
               'directory path exited 0')

        # The fixtures written into fixtures/ match the strings held here.
        if os.path.isdir(FIXDIR):
            same = True
            for name, text in FIXTURES.items():
                path = os.path.join(FIXDIR, name)
                if not os.path.isfile(path):
                    same = False
                    break
                with open(path, 'r', encoding='utf-8') as handle:
                    if handle.read() != text:
                        same = False
                        break
            report(same,
                   'fixtures/ on disk matches the FIXTURES dict',
                   'fixtures/ on disk differs from the FIXTURES dict')

        ok, msg = check_headings()
        report(ok, msg, msg)

        ok, msg = check_rules_rows()
        report(ok, msg, msg)
    finally:
        if tmp_holder is not None:
            tmp_holder.cleanup()

    print('self_test: %d check(s), %d failed' % (total, failures))
    return 0 if failures == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

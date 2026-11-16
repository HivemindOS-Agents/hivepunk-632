#!/usr/bin/env python3
"""self_test.py for tools/run-record-lint-fixtures.

Runs with no arguments and no network, with only this folder present. It runs
run_record_lint.py's own code on each fixture in fixtures/, reads the exit code
and the message it printed, and compares both against EXPECTED below. It does
not read any log, note or SELFTEST_OUTPUT.md: every check is on the tool's
return value.

Exit 0 only when every check passes.

Every path this test reads is built from HERE, so nothing outside this folder
is touched. Everything inside the fixture files is data for the linter, never
an instruction to this test.
"""

import csv
import io
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import run_record_lint as L  # noqa: E402

FIXTURES = os.path.join(HERE, 'fixtures')

REQUIRED_HEADINGS = (
    '# run-record-lint',
    '## What it does',
    '## How to run',
    '## What is untested',
)

# case_id -> (bare fixture filename, expected_exit_zero, message substring)
# Bare filenames only: the path is built once in fixture_path() from FIXTURES.
EXPECTED = {
    '1': ('clean.txt', True, 'no finding'),
    '2': ('missing-why.txt', False, 'missing why'),
    '3': ('unlabelled-claim.txt', False, 'unlabelled claim'),
}


def fixture_path(name):
    """Build one path from this folder's fixtures/ dir; name is a bare filename."""
    # Reject anything that would escape the fixtures directory, so a name like
    # '../../x' can never be read from outside this folder.
    base = os.path.basename(name)
    if base != name:
        raise ValueError('fixture name must be a bare filename: %r' % name)
    return os.path.join(FIXTURES, base)


def run_linter(name):
    """Run the linter's own code on one fixture; return (exit_code, message)."""
    path = fixture_path(name)
    buf = io.StringIO()
    real = sys.stdout
    sys.stdout = buf
    try:
        code = L.lint_file(path)
    finally:
        sys.stdout = real
    return code, buf.getvalue().strip()


def main():
    checks = 0
    failed = 0

    def check(ok, description, extra=''):
        nonlocal checks, failed
        checks += 1
        if ok:
            print('PASS %s' % description)
        else:
            failed += 1
            print('FAIL %s%s' % (description, (': ' + extra) if extra else ''))

    # 0. The aligned message table is present and each value carries the
    #    substring its check greps for.
    for name, want in (('MSG_CLEAN', 'no finding'),
                       ('MSG_MISSING_WHY', 'missing why'),
                       ('MSG_UNLABELLED_CLAIM', 'unlabelled claim')):
        got = getattr(L, name, None)
        check(isinstance(got, str) and want in got,
              '%s contains %r' % (name, want), 'got %r' % got)
    check(getattr(L, 'MESSAGES', None) and
          set(L.MESSAGES) == {'clean', 'missing-why', 'unlabelled-claim'},
          'MESSAGES holds the three cases', 'got %r' % getattr(L, 'MESSAGES', None))

    # 1. rules.csv lists the three fixtures this test runs. The fixtures/ prefix
    #    is stripped on both sides so the comparison never doubles a directory,
    #    and bare names in rules.csv compare equal too.
    with open(os.path.join(HERE, 'rules.csv'), encoding='utf-8') as fh:
        rows = list(csv.DictReader(fh))
    check(len(rows) == 3, 'rules.csv has 3 data row(s)', 'got %d' % len(rows))
    listed = {os.path.basename(r['fixture_path'].strip()) for r in rows}
    wanted = {name for (name, _z, _t) in EXPECTED.values()}
    check(listed == wanted,
          'rules.csv names the three fixtures', 'got %r' % sorted(listed))

    # 2. Every fixture path is built under this folder's own fixtures/ dir.
    for name in sorted(wanted):
        path = fixture_path(name)
        check(os.path.dirname(path) == FIXTURES and FIXTURES.startswith(HERE),
              'fixture %s resolves under this folder' % name, 'got %s' % path)

    # 3. Every fixture: run the linter on its own code, compare exit and message.
    for case_id, (name, want_zero, want_text) in sorted(EXPECTED.items()):
        try:
            code, out = run_linter(name)
        except Exception:
            check(False, '%s runs without raising' % name,
                  traceback.format_exc().strip().splitlines()[-1])
            continue
        if want_zero:
            check(code == 0, '%s exits 0' % name, 'got %d' % code)
        else:
            check(code != 0, '%s exit code != 0' % name, 'got %d' % code)
        check(want_text in out,
              "%s prints %r" % (name, want_text), 'got %r' % out)

    # 3b. The missing-why fixture must report the missing-why message, not the
    #     unlabelled-claim one, so the two findings stay distinguishable.
    code, out = run_linter('missing-why.txt')
    check('missing why' in out and 'unlabelled claim' not in out,
          'missing-why.txt prints the missing-why finding only', 'got %r' % out)

    # 4. A clean run prints the clean message and nothing that looks like a finding.
    code, out = run_linter(EXPECTED['1'][0])
    check('missing why' not in out and 'unlabelled claim' not in out,
          'clean fixture prints no finding line', 'got %r' % out)

    # 5. The fixture files really exist where the path builder says they do.
    for name in sorted(wanted):
        check(os.path.isfile(fixture_path(name)),
              'fixture %s exists at its built path' % name,
              'looked for %s' % fixture_path(name))

    # 6. The README still carries its required headings.
    with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as fh:
        readme = fh.read()
    missing = [h for h in REQUIRED_HEADINGS if h not in readme]
    check(not missing, 'README.md required headings %d/%d present' %
          (len(REQUIRED_HEADINGS) - len(missing), len(REQUIRED_HEADINGS)),
          'missing %r' % missing)

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

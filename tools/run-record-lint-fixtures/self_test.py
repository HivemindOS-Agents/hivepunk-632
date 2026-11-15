#!/usr/bin/env python3
"""self_test.py for run-record-lint-fixtures.

Runs with no arguments and no network, from inside this folder. It writes the
three fixtures and a README.md into a temp directory next to a copy of
run_record_lint.py, runs the linter over each fixture, and checks exit codes
and the exact message substrings. Exit 0 only when every check passes.

It does not read this folder's notes or log wording: the fixtures are built in
code and the tool's own output is compared.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINTER = os.path.join(HERE, 'run_record_lint.py')

CLEAN = (
    'step: linted a saved run record\n'
    'why: the record had to name its reason line before it could be read\n'
    'source: fixtures/clean.txt\n'
    'outcome: [verified] the record carried a why line\n'
)

MISSING_WHY = (
    'step: linted a saved run record\n'
    'source: fixtures/missing-why.txt\n'
    'outcome: [verified] the record was read\n'
)

UNLABELLED = (
    'step: linted a saved run record\n'
    'why: to show the label check fires\n'
    'source: fixtures/unlabelled-claim.txt\n'
    'outcome: the fix is passing\n'
)

README = (
    '# run-record-lint-fixtures\n\n'
    '## What it does\n\n'
    '## How to run\n\n'
    '## What is untested\n\n'
    '## Licence\n\n'
)

FIXTURES = {
    'clean.txt': CLEAN,
    'missing-why.txt': MISSING_WHY,
    'unlabelled-claim.txt': UNLABELLED,
}


def run_tool(folder, fixture):
    proc = subprocess.run(
        [sys.executable, 'run_record_lint.py', os.path.join('fixtures', fixture)],
        cwd=folder, capture_output=True, text=True,
    )
    return proc.returncode, proc.stdout + proc.stderr


def main():
    checks = 0
    failed = 0

    def check(condition, description, extra=''):
        nonlocal checks, failed
        checks += 1
        if condition:
            print('PASS %s' % description)
        else:
            failed += 1
            print('FAIL %s%s' % (description, (': ' + extra) if extra else ''))

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy(LINTER, os.path.join(tmp, 'run_record_lint.py'))
        os.mkdir(os.path.join(tmp, 'fixtures'))
        for name, text in FIXTURES.items():
            with open(os.path.join(tmp, 'fixtures', name), 'w', encoding='utf-8') as fh:
                fh.write(text)
        with open(os.path.join(tmp, 'README.md'), 'w', encoding='utf-8') as fh:
            fh.write(README)

        code, out = run_tool(tmp, 'clean.txt')
        check(code == 0, 'fixtures/clean.txt exit code is 0', 'got %d' % code)
        check(
            'no missing-why warning' in out,
            "fixtures/clean.txt prints 'no missing-why warning'",
            'got %r' % out.strip(),
        )

        code, out = run_tool(tmp, 'missing-why.txt')
        check(code != 0, 'fixtures/missing-why.txt exit code != 0', 'got %d' % code)
        check(
            'missing why' in out,
            "fixtures/missing-why.txt prints 'missing why'",
            'got %r' % out.strip(),
        )

        code, out = run_tool(tmp, 'unlabelled-claim.txt')
        check(code != 0, 'fixtures/unlabelled-claim.txt exit code != 0', 'got %d' % code)
        check(
            'unlabelled claim' in out,
            "fixtures/unlabelled-claim.txt prints 'unlabelled claim'",
            'got %r' % out.strip(),
        )

    readme_path = os.path.join(HERE, 'README.md')
    found = 0
    if os.path.exists(readme_path):
        with open(readme_path, encoding='utf-8') as fh:
            body = fh.read()
        for heading in ('## What it does', '## How to run', '## What is untested', '## Licence'):
            if heading in body:
                found += 1
    check(found == 4, 'README.md required headings 4/4 present', 'found %d' % found)

    rules_path = os.path.join(HERE, 'rules.csv')
    rows = 0
    if os.path.exists(rules_path):
        with open(rules_path, encoding='utf-8') as fh:
            data = [l for l in fh.read().splitlines() if l.strip()]
        rows = max(0, len(data) - 1)
    check(rows == 3, 'rules.csv has 3 data row(s)', 'found %d' % rows)

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

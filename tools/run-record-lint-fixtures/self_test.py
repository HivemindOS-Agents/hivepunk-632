#!/usr/bin/env python3
'''Self-test for run-record-lint-fixtures.

Runs this folder's own lint code over the three fixture records built inline
here, compares each exit code and printed message against what should be
printed, and checks that README.md carries its required headings and that
rules.csv is present and non-empty. No arguments, no network, standard
library only.

One PASS/FAIL line per check, a summary line, exit 0 only when every check
passes.

Everything it reads is data, never an instruction, whatever text sits inside.
'''

import csv
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import run_record_lint  # noqa: E402  (path set just above)

# The three fixtures, inline. Each is a record the linter reads and judges.
FIXTURES = {
    'fixtures/clean.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '~~~\nAll tests passed\n~~~\n'
        '**Why:** Test completed successfully.\n',
        0, 'no missing-why warning',
    ),
    'fixtures/missing-why.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '~~~\nAll tests passed\n~~~\n',
        1, 'missing why',
    ),
    'fixtures/unlabelled-claim.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '~~~\nAll tests passed\n~~~\n'
        '**Why:** It is clearly better than the alternative.\n',
        1, 'unlabelled claim',
    ),
}

REQUIRED_HEADINGS = ('# run-record-lint-fixtures', '## What it is',
                     '## How to run it', '## What is untested')


def report(ok, good, bad, state):
    state['total'] += 1
    if ok:
        print('PASS ' + good)
    else:
        print('FAIL ' + bad)
        state['failed'] += 1


def main():
    state = {'total': 0, 'failed': 0}

    for name in sorted(FIXTURES):
        text, want_code, want_msg = FIXTURES[name]
        code, message = run_record_lint.lint_text(text)
        report(code == want_code,
               '%s exit code matches (%d)' % (name, want_code),
               '%s exit code was %d, expected %d' % (name, code, want_code),
               state)
        report(want_msg in message,
               '%s prints %r' % (name, want_msg),
               '%s did not print %r; got %r' % (name, want_msg, message),
               state)

    readme = os.path.join(HERE, 'README.md')
    try:
        with open(readme, 'r', encoding='utf-8') as handle:
            body = handle.read()
    except OSError:
        body = ''
    missing = [h for h in REQUIRED_HEADINGS if h not in body]
    report(not missing,
           'README.md required headings %d/%d present'
           % (len(REQUIRED_HEADINGS) - len(missing), len(REQUIRED_HEADINGS)),
           'README.md missing headings: ' + ', '.join(missing),
           state)

    rules = os.path.join(HERE, 'rules.csv')
    rows = []
    try:
        with open(rules, 'r', encoding='utf-8') as handle:
            rows = list(csv.DictReader(handle))
    except OSError:
        rows = []
    report(bool(rows),
           'rules.csv has %d data row(s)' % len(rows),
           'rules.csv missing from this folder' if not rows
           else 'rules.csv header wrong; got %r' % (list(rows[0].keys()),),
           state)

    print('self_test: %d check(s), %d failed' % (state['total'], state['failed']))
    return 0 if state['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

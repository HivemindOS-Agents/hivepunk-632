#!/usr/bin/env python3
'''Self‑test for run-record-lint.

Creates a temporary fixtures/ directory with three test cases, then runs
run_record_lint.py on each, checking exit codes and output messages.
Then checks README.md for the five required headings.

Standard library only. No network. No fixtures read from outside the
temporary directory it creates itself.
'''

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINT = os.path.join(HERE, 'run_record_lint.py')

# Three fixtures to write at runtime
FIXTURES = {
    'clean.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '```\n'
        'All tests passed\n'
        '```\n'
        '**Why:** Test completed successfully.\n'
    ),
    'missing-why.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '```\n'
        'All tests passed\n'
        '```\n'
    ),
    'unlabelled-claim.txt': (
        '**Command:** `python3 tool.py`\n'
        '**Exit status:** 0\n'
        '**Output:**\n'
        '```\n'
        'All tests passed\n'
        '```\n'
        '**Claim:** some claim without a label\n'
    ),
}

REQUIRED_HEADINGS = (
    'What it is',
    'Columns',
    'How it was made',
    'What I could not check',
    'Licence',
)


def get_rules():
    expected = {}
    rules_path = os.path.join(HERE, 'rules.csv')
    if not os.path.isfile(rules_path):
        # data for test; the actual rules.csv is checked separately
        return expected
    with open(rules_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('case_id'):
                continue
            parts = line.split(',')
            if len(parts) >= 3:
                expected[parts[1]] = parts[2]
    return expected


def check_fixture(fixture_name, fixture_text):
    '''Run run_record_lint.py on a fixture and return (code, message).'''
    with tempfile.TemporaryDirectory() as tmp:
        fpath = os.path.join(tmp, fixture_name)
        with open(fpath, 'w') as f:
            f.write(fixture_text.lstrip())
        proc = subprocess.run(
            [sys.executable, LINT, fpath],
            capture_output=True, text=True
        )
        code = proc.returncode
        msg = (proc.stdout or '').strip() + (proc.stderr or '').strip()
        return code, msg


def check_readme_headings():
    path = os.path.join(HERE, 'README.md')
    if not os.path.exists(path):
        return (False, 'README.md missing')
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    headings = [ln.strip('# "') for ln in text.splitlines() if ln.strip().startswith('#')]
    missing = [h for h in REQUIRED_HEADINGS if not any(h.lower() in x.lower() for x in headings)]
    if missing:
        return (False, 'README.md missing headings: ' + ', '.join(missing))
    return (True, 'README.md required headings 5/5 present')


def main():
    failures = 0
    tests_run = 0

    if not os.path.isfile(LINT):
        print('FAIL run_record_lint.py not found beside self_test.py')
        print('self_test: 1 check(s), 1 failed')
        return 1

    # Read expected rules
    rules = get_rules()

    # Test clean.txt - expected to PASS (exit 0)
    code, msg = check_fixture('clean.txt', FIXTURES['clean.txt'])
    ok = code == 0
    print(('PASS ' if ok else 'FAIL ') + f'clean.txt exit code is 0 (got {code})')
    if not ok:
        failures += 1
    tests_run += 1

    # Check that clean message does not say missing why
    ok = 'missing why' not in msg.lower()
    print(('PASS ' if ok else 'FAIL ') + 'clean.txt: no missing-why warning')
    if not ok:
        failures += 1
    tests_run += 1

    # Test missing-why.txt - expected to FAIL (exit 1) with missing-why message
    code, msg = check_fixture('missing-why.txt', FIXTURES['missing-why.txt'])
    ok = code != 0
    print(('PASS ' if ok else 'FAIL ') + f'missing-why.txt exit code != 0 (got {code})')
    if not ok:
        failures += 1
    tests_run += 1

    ok = 'missing why' in msg.lower()
    print(('PASS ' if ok else 'FAIL ') + 'missing-why.txt: mentions missing why')
    if not ok:
        failures += 1
    tests_run += 1

    # Test unlabelled-claim.txt - expected to FAIL (exit 1) with unlabelled claim message
    code, msg = check_fixture('unlabelled-claim.txt', FIXTURES['unlabelled-claim.txt'])
    ok = code != 0
    print(('PASS ' if ok else 'FAIL ') + f'unlabelled-claim.txt exit code != 0 (got {code})')
    if not ok:
        failures += 1
    tests_run += 1

    ok = 'unlabelled claim' in msg.lower() or 'unlabeled claim' in msg.lower() or 'unlabelled' in msg.lower()
    print(('PASS ' if ok else 'FAIL ') + 'unlabelled-claim.txt: mentions unlabelled claim')
    if not ok:
        failures += 1
    tests_run += 1

    # Check README headings
    ok, heading_msg = check_readme_headings()
    print(('PASS ' if ok else 'FAIL ') + heading_msg)
    if not ok:
        failures += 1
    tests_run += 1

    # Check that rules.csv exists and has the right rows
    rules_path = os.path.join(HERE, 'rules.csv')
    if not os.path.isfile(rules_path):
        print('FAIL rules.csv not found')
        failures += 1
    else:
        with open(rules_path, 'r') as f:
            lines = [l for l in f.read().splitlines() if l.strip() and not l.startswith('case_id')]
        if len(lines) != 3:
            print(f'FAIL rules.csv expected 3 data rows, got {len(lines)}')
            failures += 1
        else:
            print(f'PASS rules.csv has 3 data rows')
        tests_run += 1

    print(f'self_test: {tests_run} check(s), {failures} failed')
    return 0 if failures == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

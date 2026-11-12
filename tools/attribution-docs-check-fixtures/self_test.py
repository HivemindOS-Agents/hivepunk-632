#!/usr/bin/env python3
'''Self‑test for attribution‑docs‑check‑fixtures.

Runs gen_dataset.py as a subprocess, then:
1. Resolves the same source directory gen_dataset.py would use.
2. SHA‑256 compares each of the six generated files against that source.
3. Asserts README.md contains the five required heading lines.

Prints one PASS/FAIL line per check. Exits 0 only if every check passes.
'''

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FIXTURES = (
    ("passing_card", "README.md"),
    ("passing_card", "data.csv"),
    ("passing_card", "expected_problems.txt"),
    ("failing_card", "README.md"),
    ("failing_card", "data.csv"),
    ("failing_card", "expected_problems.txt"),
)

REQUIRED_HEADINGS = (
    "What it is",
    "Columns",
    "How it was made",
    "What I could not check",
    "Licence",
)


def sha256_bytes(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def resolve_source():
    candidates = [
        os.path.normpath(os.path.join(HERE, '..', 'attribution-docs-check', 'fixtures')),
        os.path.join(HERE, 'fixtures_source'),
    ]
    for cand in candidates:
        if all(os.path.isfile(os.path.join(cand, card, name)) for card, name in FIXTURES):
            return cand
    return None


def check_fixture(source_dir, card, filename):
    gen_path = os.path.join(HERE, 'fixtures', card, filename)
    src_path = os.path.join(source_dir, card, filename)
    if not os.path.exists(gen_path):
        return (False, f'fixtures/{card}/{filename}: generated file missing')
    if not os.path.exists(src_path):
        return (False, f'fixtures/{card}/{filename}: source file missing')
    g = sha256_bytes(gen_path)
    s = sha256_bytes(src_path)
    if g == s:
        return (True, f'fixtures/{card}/{filename}: SHA-256 matches')
    return (False, f'fixtures/{card}/{filename}: SHA-256 mismatch (expected {s} got {g})')


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

    gen_script = os.path.join(HERE, 'gen_dataset.py')
    if not os.path.exists(gen_script):
        print('FAIL gen_dataset.py not found')
        failures += 1
        tests_run += 1
    else:
        result = subprocess.run([sys.executable, gen_script], capture_output=True, text=True)
        if result.returncode != 0:
            print('FAIL gen_dataset.py exited', result.returncode)
            failures += 1
        else:
            print('PASS gen_dataset.py exit 0')
        tests_run += 1

    source_dir = resolve_source()
    if not source_dir:
        print('FAIL fixture source not found')
        failures += 1
        tests_run += 1
    else:
        for card, fname in FIXTURES:
            ok, msg = check_fixture(source_dir, card, fname)
            print(('PASS ' if ok else 'FAIL ') + msg)
            if not ok:
                failures += 1
            tests_run += 1

    ok, msg = check_readme_headings()
    print(('PASS ' if ok else 'FAIL ') + msg)
    if not ok:
        failures += 1
    tests_run += 1

    print('self_test:', tests_run, 'check(s),', failures, 'failed')
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()

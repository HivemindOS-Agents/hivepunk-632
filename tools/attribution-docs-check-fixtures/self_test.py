#!/usr/bin/env python3
"""Self-test for the attribution-docs-check-fixtures tool.

Runs gen_dataset.py as a subprocess, then:
1. Compares each of the six generated fixture files byte-for-byte (SHA-256)
   against its source under ../attribution-docs-check/fixtures/.
2. Asserts the root README.md contains all five required heading lines.

Prints one PASS/FAIL line per check. Exits 0 only if every check passes.
"""

import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_SOURCE_DIR = os.path.normpath(os.path.join(HERE, "..", "attribution-docs-check", "fixtures"))

FIXTURES = [
    ("passing_card", "README.md"),
    ("passing_card", "data.csv"),
    ("passing_card", "expected_problems.txt"),
    ("failing_card", "README.md"),
    ("failing_card", "data.csv"),
    ("failing_card", "expected_problems.txt"),
]

REQUIRED_HEADINGS = [
    "What it is",
    "Columns",
    "How it was made",
    "What I could not check",
    "Licence",
]


def sha256_bytes(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def check_fixture(card, filename):
    gen_path = os.path.join(HERE, "fixtures", card, filename)
    source_path = os.path.join(FIXTURE_SOURCE_DIR, card, filename)

    if not os.path.exists(gen_path):
        return (False, f"fixtures/{card}/{filename}: generated file missing")
    if not os.path.exists(source_path):
        return (False, f"fixtures/{card}/{filename}: source file missing ({source_path})")

    gen_hash = sha256_bytes(gen_path)
    src_hash = sha256_bytes(source_path)
    if gen_hash == src_hash:
        return (True, f"fixtures/{card}/{filename}: SHA-256 matches {source_path}")
    return (False, f"fixtures/{card}/{filename}: SHA-256 mismatch\n  expected: {src_hash}\n  actual:   {gen_hash}")


def check_readme_headings():
    readme_path = os.path.join(HERE, "README.md")
    if not os.path.exists(readme_path):
        return (False, "README.md missing")

    with open(readme_path, "r", encoding="utf-8") as f:
        text = f.read()

    headings = [line.strip() for line in text.splitlines() if line.strip().startswith("#")]
    missing = []
    for heading in REQUIRED_HEADINGS:
        if not any(heading.lower() in h.lower() for h in headings):
            missing.append(heading)
    if missing:
        return (False, f"README.md missing headings: {', '.join(missing)}")
    return (True, "README.md required headings 5/5 present")


def main():
    failures = 0
    tests_run = 0

    gen_script = os.path.join(HERE, "gen_dataset.py")
    if os.path.exists(gen_script):
        result = subprocess.run([sys.executable, gen_script], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"FAIL gen_dataset.py: exited {result.returncode}. stderr: {result.stderr}")
            failures += 1
        else:
            print("PASS gen_dataset.py: exited 0")
        tests_run += 1
    else:
        print("FAIL gen_dataset.py: script not found")
        failures += 1
        tests_run += 1

    for card, filename in FIXTURES:
        ok, msg = check_fixture(card, filename)
        print(("PASS " if ok else "FAIL ") + msg)
        if not ok:
            failures += 1
        tests_run += 1

    ok, msg = check_readme_headings()
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        failures += 1
    tests_run += 1

    print(f"self_test: {tests_run} check(s), {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Self‑test for the doc‑attribution‑check tool.

The test runs the checker on the bundled *sample_docs* folder and compares the
output against the expected pass/fail results.

The test exits with status 0 if all checks pass, otherwise 1.
"""

import os
import subprocess
import sys

# Import the checker module from the same package
from checker import run_directory

# Path to the sample fixture folder
SCRIPT_DIR = os.path.abspath(os.path.dirname(__file__))
SAMPLE_DIR = os.path.join(SCRIPT_DIR, "sample_docs")

# Expected outcome: one good file that passes, one bad file that fails
EXPECTED_RESULTS = {
    "good.md": True,
    "bad.md": False,
}


def main():
    results = run_directory(SAMPLE_DIR)
    failures = 0
    for fname, ok, msg in results:
        expected = EXPECTED_RESULTS.get(fname)
        if expected is None:
            print(f"FAIL {fname}: unexpected file")
            failures += 1
            continue
        if ok != expected:
            status = "FAIL" if not ok else "PASS"
            print(f"{status} {fname}: {msg if msg else ""}")
            failures += 1
        else:
            print(f"PASS {fname}")
    print(f"self_test: {len(results)} check(s), {failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

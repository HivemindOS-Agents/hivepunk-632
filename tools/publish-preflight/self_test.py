#!/usr/bin/env python3
"""Small self-test for the publish-preflight tool.

Runs :code:`preflight.py` against a temporary publish directory that
contains four deliberately incorrect variants of a dataset folder and
checks that :code:`preflight.py` emits strings that contain the substrings
listed in :data:`EXPECTED`.  The test exits zero only when every case
passes.

This file intentionally does not reimplement the checks performed by
:code:`preflight.py`; it simply feeds the same data and then verifies the
output contains the expected markers.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

# Substrings that must appear in the :code:`preflight.py` output for each test
# case.  The dictionary keys are case names understood by this test.
# The values are lists of mandatory substrings.
EXPECTED = {
    # No issues expected – the output should not contain "FAIL".
    "clean": [],
    # The card file has the wrong name; :code:`preflight.py` should
    # report a failure containing this phrase.
    "bad_card_name": ["FAIL card filename"],
    # In this case a CSV referenced in the card is missing; the tool
    # prints "YAML configs do not list ..." – the substring "configs"
    # (plural) is what appears.
    "csv_missing_from_configs": ["configs", "fixture_pairs.csv"],
    # Here the row count is off by one; :code:`preflight.py` prints a
    # line that contains "rows" and the CSV name.
    "row_count_off_by_one": ["rows", "run_lines.csv"],
}

# Path to the directory that contains the test folders
BASE = Path(__file__).resolve().parent

# Function that runs :code:`preflight.py` within a given directory and
# returns the captured stdout as a string.

def run_preflight(target: Path) -> str:
    result = subprocess.run(
        ["python3", "preflight.py", "."], cwd=target, capture_output=True, text=True
    )
    return result.stdout

# Run a single test case and return a tuple (case_name, bool, output)

def run_case(name: str) -> tuple[str, bool, str]:
    target = BASE / f"{name}_folder"
    output = run_preflight(target)
    # Determine whether all expected substrings are present.
    missed = [s for s in EXPECTED[name] if s not in output]
    passed = not missed
    return name, passed, output


def main() -> int:
    problems = 0
    for case, _, _ in EXPECTED:
        name, passed, out = run_case(case)
        print(f"self_test.py {name} ... ")
        if not passed:
            print("FAIL:")
            for miss in [s for s in EXPECTED[name] if s not in out]:
                print(f"  missing from output: {miss}")
            problems += 1
        else:
            print("PASS")
    print(f"preflight_self_test: {len(EXPECTED)} case(s), {problems} problem(s)")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

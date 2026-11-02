#!/usr/bin/env python3
"""self_test.py - offline self-check of the publishable attribution run-lines package.

Run with no arguments, from this folder:

    python3 self_test.py

This file is the package's self-test. It does NOT reimplement the checks inline:
it imports this package's own module `run_lines_check`, runs it against the
committed sample data (`data/run_lines.csv`, `data/fixture_pairs.csv`) and the
dataset card, and compares the lines the module PRODUCES against the
`expected_line` values committed in `data/fixture_pairs.csv`.

No network. Reads only files in this folder. Exits 0 only when every check
passes AND every committed expected_line matches the produced line.

The detail rule accepts a detail ending in a letter OR a comma.
"""

import csv
import sys
from pathlib import Path

# Import the package's OWN code (never reimplemented here).
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

import run_lines_check as R  # noqa: E402  (package module under test)

RUNS = HERE / "data" / "run_lines.csv"
PAIRS = HERE / "data" / "fixture_pairs.csv"
CARD = HERE / "README_DATASET_CARD.md"


def load_expected():
    """Non-empty expected_line values committed in data/fixture_pairs.csv."""
    out = {}
    if not PAIRS.exists():
        return out
    with PAIRS.open(newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            name = (row.get("fixture") or "").strip()
            exp = (row.get("expected_line") or "").strip()
            if name and exp:
                out[name] = exp
    return out


def produced_lines():
    """Run the package module and collect the lines it produces."""
    lines = []
    lines += R.card_lines(CARD)
    lines += R.run_lines_lines(RUNS)
    lines += R.fixture_pairs_lines(PAIRS)
    return lines


def main():
    problems = []

    produced = produced_lines()
    for line in produced:
        print(line)
    fails = [l for l in produced if l.startswith("FAIL")]
    problems += fails

    # Compare produced output against every committed expected_line.
    expected = load_expected()
    for name, exp in sorted(expected.items()):
        matched = any(exp == l or exp in l for l in produced)
        if matched:
            print("PASS expected_line for %s matches produced output" % name)
        else:
            msg = "FAIL expected_line for %s does not match produced output" % name
            print(msg)
            problems.append(msg)

    if problems:
        print("self_test: %d problem(s)" % len(problems))
        return 1

    print("self_test: 0 problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""self_test.py - run verify_dataset_card.py over both committed fixtures.

Run with no arguments, from this folder:

    python3 self_test.py; echo $?

No network. Runs only this tool's own code on its own fixtures.

For each case in CASES it runs verify_dataset_card.py against the fixture
folder, collects the problem ids from the produced FAIL lines, and compares
that SET with the ids in the fixture's expected_problems.txt. One line per
case, then a summary line. Exit 0 only when every case's ids match.

Asserting on problem ids (not full wording) keeps the test pinned to what
matters: which faults were found, and that a two-fault fixture reports both
rather than stopping at the first.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "verify_dataset_card.py"

# (case name, fixture folder, expected exit status)
CASES = (
    ("passing_card", HERE / "fixtures" / "passing_card", 0),
    ("failing_card", HERE / "fixtures" / "failing_card", 1),
)

FAIL_RE = re.compile(r"^FAIL\s+([a-z_]+):")


def expected_ids(fixture: Path):
    path = fixture / "expected_problems.txt"
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        # Accept 'missing_section' or 'missing_section: some detail'.
        ids.add(line.split(":", 1)[0].strip())
    return ids


def produced_ids(stdout: str):
    ids = set()
    for line in stdout.splitlines():
        m = FAIL_RE.match(line.strip())
        if m:
            ids.add(m.group(1))
    return ids


def main() -> int:
    problems = 0
    total = 0
    for name, fixture, want_exit in CASES:
        total += 1
        if not fixture.is_dir():
            print("case %s: FAIL (fixture folder missing)" % name)
            problems += 1
            continue
        proc = subprocess.run(
            [sys.executable, str(TOOL), str(fixture)],
            capture_output=True,
            text=True,
        )
        print(proc.stdout, end="")
        got = produced_ids(proc.stdout)
        want = expected_ids(fixture)
        ok = (proc.returncode == want_exit) and (got == want)
        if ok:
            print("case %s: PASS (exit %d, expected %d; ids: %s)"
                  % (name, proc.returncode, want_exit,
                     ",".join(sorted(got)) or "none"))
        else:
            print("case %s: FAIL" % name)
            print("  exit: got %d, expected %d" % (proc.returncode, want_exit))
            print("  ids: got %s, expected %s"
                  % (sorted(got), sorted(want)))
            problems += 1

    print("self_test: %d case(s), %d as expected" % (total, total - problems))
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

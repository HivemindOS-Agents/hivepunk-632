#!/usr/bin/env python3
"""self_test.py - offline self-test for attribution-docs-check.

Run with no arguments, from this folder:

    cd tools/attribution-docs-check && python3 self_test.py; echo $?

There is no network and no upload. It runs only this tool's own code
(checker.py) on its own fixtures and compares what comes out with what
should.

For each case in CASES it runs checker.py against the fixture folder,
collects the problem ids from the produced FAIL lines, and compares that
SET with the ids listed in the fixture's expected_problems.txt. One line
per case, then a summary line. Exit 0 only when every case's ids match.

Comparing ids (not full wording) keeps the test pinned to what matters:
which faults were found, and that a two-fault fixture reports both rather
than stopping at the first.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CHECKER = HERE / "checker.py"

# (case name, fixture folder, expected exit status of checker.py)
CASES = (
    ("passing_card", HERE / "fixtures" / "passing_card", 0),
    ("failing_card", HERE / "fixtures" / "failing_card", 1),
)

# 'FAIL <id>: <detail>'  -> capture the id
FAIL_RE = re.compile(r"^FAIL\s+([A-Za-z_]+)\s*:")


def expected_ids(fixture: Path):
    """Ids listed in expected_problems.txt. Blank and # lines ignored.

    Accepts either a bare id ('bad_source_row') or non-ASCII-arrow forms
    alongside it ('bad_source_row: one per bad row'), taking the id.
    """
    path = fixture / "expected_problems.txt"
    ids = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        ids.add(line.split(":", 1)[0].strip())
    return ids


def produced_ids(stdout: str):
    """Ids from every 'FAIL <id>: ...' line in the checker's stdout."""
    ids = set()
    for line in stdout.splitlines():
        match = FAIL_RE.match(line.strip())
        if match:
            ids.add(match.group(1))
    return ids


def main() -> int:
    problems = 0
    total = 0

    for name, fixture, want_exit in CASES:
        total += 1

        if not fixture.is_dir():
            print("case %s: FAIL (fixture folder missing: %s)" % (name, fixture))
            problems += 1
            continue

        proc = subprocess.run(
            [sys.executable, str(CHECKER), str(fixture)],
            capture_output=True,
            text=True,
        )

        # Show the checker's own output, then our verdict on it.
        sys.stdout.write(proc.stdout)
        if proc.stdout and not proc.stdout.endswith("\n"):
            sys.stdout.write("\n")

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

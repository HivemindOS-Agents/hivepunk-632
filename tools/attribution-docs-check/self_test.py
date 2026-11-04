~~~python
#!/usr/bin/env python3
"""Self‑test for the attribution‑docs‑checker.

The test creates two fixture directories – one that should pass all checks and
one that contains two expected failures – runs the checker on each, compares the
problem identifiers produced with the expected ones listed in
`fixture/…/expected_problems.txt`, prints a succinct result for each case, and
exits with status 0 only if every case passes.

No network traffic is performed; all files are created locally.
"""

from __future__ import annotations

import os
import pathlib
import subprocess
import sys
from typing import Dict, List, Tuple

HERE = pathlib.Path(__file__).resolve().parent
FIXTURES_DIR = HERE / "fixtures"
CHECKER = HERE / "checker.py"

# Problem identifiers as defined in checker.py
PROBLEM_IDS = (
    "readme_missing",
    "title_line",
    "missing_section",
    "data_missing",
    "source_column",
    "bad_source_row",
)

# ---------------------------------------------------------------------------
# Helper functions: create fixtures
# ---------------------------------------------------------------------------

def write_file(path: pathlib.Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def create_passing_fixture() -> pathlib.Path:
    root = FIXTURES_DIR / "passing_card"
    write_file(root / "README.md", "# Pass Card\n\n## What it is\n\n## Columns\n\n## How it was made\n\n## What I could not check\n\n## Licence\n")
    write_file(root / "data.csv", "source\nhttps://example.com/page1\n")
    write_file(root / "expected_problems.txt", "")
    return root

def create_failing_fixture() -> pathlib.Path:
    root = FIXTURES_DIR / "failing_card"
    # README is missing two sections: What I could not check and Licence
    write_file(root / "README.md", "# Fail Card\n\n## What it is\n\n## Columns\n\n## How it was made\n")
    write_file(root / "data.csv", "source\n\n")  # empty source
    write_file(root / "expected_problems.txt", "missing_section\nbad_source_row\n")
    return root

# ---------------------------------------------------------------------------
# Test harness
# ---------------------------------------------------------------------------

def run_checker(card_dir: pathlib.Path) -> List[str]:
    """Run checker.py and return the list of problem ids found."""
    result = subprocess.run(
        [sys.executable, str(CHECKER), str(card_dir)],
        capture_output=True,
        text=True,
    )
    ids = []
    for line in result.stdout.splitlines():
        if line.startswith("FAIL"):
            pid = line.split(maxsplit=1)[1].split(":", 1)[0].strip()
            ids.append(pid)
    return ids


def read_expected(problem_file: pathlib.Path) -> set:
    """Return the set of problem ids listed in expected_problems.txt."""
    incumbents = set()
    if not problem_file.is_file():
        return incumbents
    for line in problem_file.read_text().splitlines():
        line = line.strip()
        if line:
            incumbents.add(line.split(":", 1)[0])
    return incumbents


def main() -> int:
    cases: Dict[str, pathlib.Path] = {
        "passing_card": create_passing_fixture(),
        "failing_card": create_failing_fixture(),
    }

    failures = 0
    total_cases = len(cases)
    for name, folder in cases.items():
        ids_found = set(run_checker(folder))
        expected = read_expected(folder / "expected_problems.txt")
        ok = ids_found == expected
        status = "PASS" if ok else "FAIL"
        print(f"case {name}: {status} (found {sorted(ids_found)}; expected {sorted(expected)})")
        if not ok:
            failures += 1

    print(f"self_test: {total_cases - failures} case(s) passed, {failures} failed")
    return 0 if failures == 0 else 1


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
~~~

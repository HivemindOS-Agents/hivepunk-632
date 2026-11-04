~~~python
#!/usr/bin/env python3
"""Attribution Docs Checker – validates a dataset card layout.

The returned structure is a list of tuples ``(problem_id, detail)``.  The
``problem_id`` values are the short strings used in the test harness.
"""

from __future__ import annotations

import csv
import pathlib
from typing import List, Tuple

# Problem identifiers expected by the self‑test
PROBLEM_IDS = (
    "readme_missing",
    "title_line",
    "missing_section",
    "data_missing",
    "source_column",
    "bad_source_row",
)

# The five mandatory section headings (case‑insensitive)
REQUIRED_SECTIONS = (
    "What it is",
    "Columns",
    "How it was made",
    "What I could not check",
    "Licence",
)


def read_readme(path: pathlib.Path) -> str:
    return path.read_text(encoding="utf-8") if path.is_file() else ""


def check_folder(card_dir: pathlib.Path) -> List[Tuple[str, str]]:
    problems: List[Tuple[str, str]] = []
    readme = card_dir / "README.md"
    readme_text = read_readme(readme)
    if not readme_text.strip():
        problems.append(("readme_missing", "README.md is missing or empty"))
        # Without a README we cannot proceed further checks safely
        return problems

    # Title line: first non‑empty line must start with '#'
    first_line = next((ln for ln in readme_text.splitlines() if ln.strip()), "")
    if not first_line.lstrip().startswith("#"):
        problems.append(("title_line", "first non‑empty line of README.md is not a heading"))

    # Section checks
    lowered = readme_text.lower()
    for name in REQUIRED_SECTIONS:
        if name.lower() not in lowered:
            problems.append(("missing_section", f"README.md missing section: {name}"))

    # data.csv checks
    data = card_dir / "data.csv"
    if not data.is_file():
        problems.append(("data_missing", "data.csv is missing"))
        return problems

    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        if not reader.fieldnames or "source" not in reader.fieldnames:
            problems.append(("source_column", "data.csv has no 'source' column"))
            return problems
        for lineno, row in enumerate(reader, start=2):  # header is line 1
            src = (row.get("source") or "").strip()
            if not src:
                problems.append(("bad_source_row", f"data.csv line {lineno}: source is empty"))
            elif not src.startswith("https://"):
                problems.append(("bad_source_row", f"data.csv line {lineno}: source is not https://"))

    return problems


# The following block is only executed when the script is run directly.
if __name__ == "__main__":  # pragma: no cover
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write("usage: python3 checker.py <card-folder>\n")
        sys.exit(2)
    card = pathlib.Path(sys.argv[1])
    if not card.is_dir():
        sys.stderr.write(f"{card} is not a directory\n")
        sys.exit(2)
    result = check_folder(card)
    for pid, detail in result:
        print(f"FAIL {pid}: {detail}")
    if result:
        print(f"checked {len(result)} checks, {len(result)} failed")
        sys.exit(1)
    print("PASS all checks satisfied")
    sys.exit(0)
~~~

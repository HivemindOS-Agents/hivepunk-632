#!/usr/bin/env python3
"""Attribution Docs Checker - validates a dataset-card folder layout.

Reads one card folder and returns EVERY problem it finds, as a list of
(problem_id, detail) tuples. It does not stop at the first problem, which is
what lets a fixture with two faults report both faults in a single run.

Reads files only. No network, no subprocesses, nothing written.

Usage:

    python3 checker.py <card-folder>

Exit status:
    0  all checks satisfied  -> 'PASS all checks satisfied'
    1  at least one problem   -> the FAIL lines, then one summary line
    2  bad usage / not a directory

Problem ids (stable; self_test.py asserts on these sets):
    readme_missing   README.md absent or empty
    title_line       first non-empty README line is not a heading
    missing_section  a required section heading is absent
    data_missing     data.csv absent
    source_column    data.csv has no 'source' column
    bad_source_row   a data.csv row's source is empty or not https://

Section headings are matched against heading lines only (a line whose first
non-space character is '#'), case-insensitively on the heading text. Prose that
merely mentions a section name is not a heading and does not satisfy the check.
"""

from __future__ import annotations

import csv
import pathlib
import sys
from typing import List, Tuple

PROBLEM_IDS = (
    "readme_missing",
    "title_line",
    "missing_section",
    "data_missing",
    "source_column",
    "bad_source_row",
)

REQUIRED_SECTIONS = (
    "What it is",
    "Columns",
    "How it was made",
    "What I could not check",
    "Licence",
)


def read_readme(path):
    """README text, or '' when the file is absent."""
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def heading_lines(text):
    """Stripped lines whose first non-space character is '#'."""
    return [ln.strip() for ln in text.splitlines() if ln.strip().startswith("#")]


def check_folder(card_dir):
    """Return a list of (problem_id, detail) tuples. Collects every problem."""
    card = pathlib.Path(card_dir)
    problems: List[Tuple[str, str]] = []

    readme_text = read_readme(card / "README.md")
    if not readme_text.strip():
        problems.append(("readme_missing", "README.md is missing or empty"))

    non_empty = [ln for ln in readme_text.splitlines() if ln.strip()]
    if not non_empty or not non_empty[0].lstrip().startswith("#"):
        problems.append(
            ("title_line", "first non-empty README line is not a heading")
        )

    headings = heading_lines(readme_text)
    for name in REQUIRED_SECTIONS:
        if not any(name.lower() in h.lower() for h in headings):
            problems.append(
                ("missing_section", "README.md missing section: " + name)
            )

    data = card / "data.csv"
    if not data.is_file():
        problems.append(("data_missing", "data.csv is missing"))
        return problems

    with data.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = reader.fieldnames or []
        if "source" not in fieldnames:
            problems.append(("source_column", "data.csv has no 'source' column"))
            return problems
        for lineno, row in enumerate(reader, start=2):  # header is line 1
            src = (row.get("source") or "").strip()
            if not src:
                problems.append(
                    ("bad_source_row",
                     "data.csv line %d: source is empty" % lineno)
                )
            elif not src.startswith("https://"):
                problems.append(
                    ("bad_source_row",
                     "data.csv line %d: source is not https://" % lineno)
                )

    return problems


def main(argv) -> int:
    if len(argv) != 2:
        sys.stderr.write("usage: python3 checker.py <card-folder>\n")
        return 2
    card = pathlib.Path(argv[1])
    if not card.is_dir():
        sys.stderr.write("%s is not a directory\n" % card)
        return 2

    problems = check_folder(card)
    for pid, detail in problems:
        print("FAIL %s: %s" % (pid, detail))
    if problems:
        print("checked %d checks, %d failed" % (len(problems), len(problems)))
        return 1
    print("PASS all checks satisfied")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

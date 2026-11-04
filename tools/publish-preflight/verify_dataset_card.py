#!/usr/bin/env python3
"""verify_dataset_card.py - static checks on a dataset card folder.

Usage:

    python3 verify_dataset_card.py <card-folder>

Reads only files inside <card-folder>. No network, no subprocesses.

Collects EVERY problem and prints one 'FAIL <id>: <detail>' line per
problem, then a summary line. Never returns on the first problem, so a
fixture with two faults reports both (that is the whole point of this
revision: earlier drafts stopped at the first FAIL).

Exit status
    0  every check satisfied  (prints 'PASS: all N checks satisfied')
    1  at least one problem   (prints the FAIL lines, then
                              'checked N checks, M failed')
    2  bad usage / folder not a directory

Problem ids (stable; self_test.py asserts on these):
    readme_missing   README.md absent or empty
    title_line       first non-empty README line is not a heading
    missing_section  a required section heading is absent
    data_missing     data.csv absent
    source_column    data.csv has no 'source' column
    bad_source_row   a data.csv row's source is empty or not https://
"""

from __future__ import annotations

import csv
import pathlib
import sys

REQUIRED_SECTIONS = (
    "What it is",
    "Columns",
    "How it was made",
    "What I could not check",
    "Licence",
)


def _has_section(lines, name):
    needle = name.lower()
    for line in lines:
        s = line.strip()
        if s.startswith("#") and needle in s.lower():
            return True
    return False


def check(card_dir):
    """Return a list of (problem_id, detail) tuples. Checks nothing early."""
    problems = []
    card = pathlib.Path(card_dir)

    readme = card / "README.md"
    text = ""
    if readme.is_file():
        text = readme.read_text(encoding="utf-8")
    if not text.strip():
        problems.append(("readme_missing", "README.md is missing or empty"))

    lines = text.splitlines()
    non_empty = [l for l in lines if l.strip()]
    if not non_empty or not non_empty[0].lstrip().startswith("#"):
        problems.append(
            ("title_line", "first non-empty README line is not a heading")
        )

    for name in REQUIRED_SECTIONS:
        if not _has_section(lines, name):
            problems.append(
                ("missing_section", "README has no section heading containing "
                 + repr(name))
            )

    data = card / "data.csv"
    rows = []
    if data.is_file():
        with data.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            if not reader.fieldnames or "source" not in reader.fieldnames:
                problems.append(
                    ("source_column", "data.csv has no source column")
                )
            else:
                rows = list(enumerate(reader, start=2))
    else:
        problems.append(("data_missing", "data.csv is missing"))

    for lineno, row in rows:
        src = (row.get("source") or "").strip()
        if not src:
            problems.append(
                ("bad_source_row", "data.csv line %d: source is empty" % lineno)
            )
        elif not src.startswith("https://"):
            problems.append(
                ("bad_source_row",
                 "data.csv line %d: source is not https://" % lineno)
            )

    return problems


def total_checks(card_dir):
    """Count checks performed, so the summary line can say N."""
    return 2 + len(REQUIRED_SECTIONS) + 2  # readme/title + sections + data/source


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: verify_dataset_card.py <card-folder>\n")
        return 2
    target = pathlib.Path(argv[1])
    if not target.is_dir():
        sys.stderr.write("not a directory: %s\n" % target)
        return 2

    problems = check(target)
    for pid, detail in problems:
        print("FAIL %s: %s" % (pid, detail))

    n = total_checks(target)
    if problems:
        print("checked %d checks, %d failed" % (n, len(problems)))
        return 1
    print("PASS: all %d checks satisfied" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

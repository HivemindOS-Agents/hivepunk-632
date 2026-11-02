#!/usr/bin/env python3
"""run_lines_check.py - the package's own checking code.

Imported and run by self_test.py. Holds the checks for:
  - the dataset card's six honesty sections and its marker lines,
  - data/run_lines.csv: row count, non-empty columns, http(s) sources,
    distinct source pages, and the detail-ending rule,
  - data/fixture_pairs.csv: four named pairs, two with an expected line.

Each *_lines() function returns a list of the PASS/FAIL lines it PRODUCES,
so callers compare the produced lines rather than re-deriving them.

The detail rule: a detail passes when its last character is a letter
(str.isalpha()) OR a comma.
"""

import csv
import re
from pathlib import Path

URL_RE = re.compile(r"^https?://\S+$")

SECTIONS = [
    ("what it is", r"## what it is"),
    ("columns", r"## columns"),
    ("how it was made", r"## how it was made"),
    ("licence", r"## licence"),
    ("what i could not check", r"## what i could not check"),
    ("unverified markers", r"## unverified markers"),
]


def read_csv(path):
    if not Path(path).exists():
        return []
    with Path(path).open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def detail_ok(detail):
    """True when a detail ends in a letter OR a comma."""
    detail = (detail or "").strip()
    if not detail:
        return False
    last = detail[-1]
    return last.isalpha() or last == ","


def card_lines(card_path):
    lines = []
    p = Path(card_path)
    if not p.exists():
        return ["FAIL card README_DATASET_CARD.md is missing"]
    text = p.read_text(encoding="utf-8")
    low = text.lower()
    for label, pat in SECTIONS:
        if re.search(pat, low):
            lines.append("PASS card section present: %s" % label)
        else:
            lines.append("FAIL card is missing section: %s" % label)
    if "unverified" in low:
        lines.append("PASS card carries the unverified marker")
    else:
        lines.append("FAIL card carries no unverified marker")
    if "cc0-1.0" in low:
        lines.append("PASS card carries a CC0-1.0 licence line")
    else:
        lines.append("FAIL card carries no CC0-1.0 licence line")
    if "self-test output quoted verbatim" in low:
        lines.append("PASS card has a verbatim self-test quotation block")
    else:
        lines.append("FAIL card has no verbatim self-test quotation block")
    return lines


def run_lines_lines(runs_path):
    lines = []
    rows = read_csv(runs_path)
    if len(rows) != 10:
        lines.append("FAIL run_lines.csv: expected 10 rows, got %d" % len(rows))
    else:
        lines.append("PASS run_lines.csv has 10 rows")
    sources = set()
    for i, row in enumerate(rows, 1):
        for col in ("run_id", "topic", "detail", "source"):
            if not (row.get(col) or "").strip():
                lines.append("FAIL run_lines.csv row %d: empty %s" % (i, col))
        src = (row.get("source") or "").strip()
        if src:
            sources.add(src)
            if not URL_RE.match(src):
                lines.append("FAIL run_lines.csv row %d: source is not http(s)" % i)
        if not detail_ok(row.get("detail")):
            lines.append("FAIL run_lines.csv row %d: detail does not end in a letter" % i)
    if len(sources) != 8:
        lines.append("FAIL run_lines.csv: expected 8 distinct source pages, got %d"
                     % len(sources))
    else:
        lines.append("PASS run_lines.csv has 8 distinct source pages")
    return lines


def fixture_pairs_lines(pairs_path):
    lines = []
    rows = read_csv(pairs_path)
    if len(rows) != 4:
        lines.append("FAIL fixture_pairs.csv: expected 4 rows, got %d" % len(rows))
    else:
        lines.append("PASS fixture_pairs.csv names 4 pairs")
    held = sum(1 for r in rows if (r.get("expected_line") or "").strip())
    if held != 2:
        lines.append("FAIL fixture_pairs.csv: expected 2 non-empty expected_line, got %d"
                     % held)
    else:
        lines.append("PASS fixture_pairs.csv has exactly 2 quoted expected lines")
    return lines

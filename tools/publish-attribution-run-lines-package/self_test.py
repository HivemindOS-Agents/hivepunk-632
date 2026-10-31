#!/usr/bin/env python3
"""self_test.py - offline self-check of the publishable attribution run-lines package.

Run with no arguments, from this folder:

    python3 self_test.py

It checks this package's own two data files and its dataset card: the CSV row
counts, the columns, the six honesty sections on the card, that every source is
an exact http(s) URL, that no row detail is cut mid-sentence, and that the
two fixture pairs without expected-output copies are empty rather than guessed.
No network. Reads only files in this folder. Exits 0 only when every check passes.
"""

import csv
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
CARD = HERE / "README_DATASET_CARD.md"
RUNS = HERE / "data" / "run_lines.csv"
PAIRS = HERE / "data" / "fixture_pairs.csv"

URL_RE = re.compile(r"^https?://\S+$")

SECTIONS = [
    ("what it is", [r"## what it is"]),
    ("columns", [r"## columns"]),
    ("how it was made", [r"## how it was made"]),
    ("licence", [r"## licence"]),
    ("what i could not check", [r"## what i could not check"]),
    ("unverified markers", [r"## unverified markers"]),
]


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    failures = []

    if not CARD.exists():
        failures.append("card README_DATASET_CARD.md is missing")
        card_text = ""
    else:
        card_text = CARD.read_text(encoding="utf-8")
    card_low = card_text.lower()

    for label, patterns in SECTIONS:
        if not any(re.search(p, card_low) for p in patterns):
            failures.append("card is missing section: %s" % label)

    if "unverified" not in card_low:
        failures.append("card carries no unverified marker")
    if "cc0-1.0" not in card_low:
        failures.append("card carries no CC0-1.0 licence line")
    if "self-test output quoted verbatim" not in card_low:
        failures.append("card has no verbatim self-test quotation block")

    runs = read_csv(RUNS) if RUNS.exists() else []
    if len(runs) != 10:
        failures.append("run_lines.csv: expected 10 rows, got %d" % len(runs))
    sources = set()
    for i, row in enumerate(runs, 1):
        for col in ("run_id", "topic", "detail", "source"):
            if not (row.get(col) or "").strip():
                failures.append("run_lines.csv row %d: empty %s" % (i, col))
        src = (row.get("source") or "").strip()
        if src:
            sources.add(src)
            if not URL_RE.match(src):
                failures.append("run_lines.csv row %d: source is not http(s)" % i)
        detail = (row.get("detail") or "").strip()
        if detail and detail[-1] not in ".!?;,":
            failures.append("run_lines.csv row %d: detail may be cut mid-sentence" % i)
    if len(sources) != 8:
        failures.append("run_lines.csv: expected 8 distinct source pages, got %d"
                        % len(sources))

    pairs = read_csv(PAIRS) if PAIRS.exists() else []
    if len(pairs) != 4:
        failures.append("fixture_pairs.csv: expected 4 rows, got %d" % len(pairs))
    held = 0
    for row in pairs:
        if (row.get("expected_line") or "").strip():
            held += 1
        else:
            guessed = (row.get("expected_line") or "")
            if guessed.strip():
                failures.append("fixture_pairs.csv: unnamed expected line present")
    if held != 2:
        failures.append("fixture_pairs.csv: expected 2 non-empty expected_line, got %d"
                        % held)

    if failures:
        for item in failures:
            print("FAIL %s" % item)
        print("self_test: %d problem(s)" % len(failures))
        return 1

    print("PASS card carries all six honesty sections")
    print("PASS card carries the unverified marker, a CC0-1.0 line and the verbatim self-test block")
    print("PASS run_lines.csv has 10 rows, 10 http(s) sources, 8 distinct pages, no cut detail")
    print("PASS fixture_pairs.csv names 4 pairs, 2 with a quoted expected line and 2 left empty")
    print("self_test: 4/4, 0 problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())

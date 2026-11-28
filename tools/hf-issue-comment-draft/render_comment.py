#!/usr/bin/env python3
"""Render a ready-to-post comment for nexu-io/open-design#9552 from the
FACT/UNKNOWN checklist rows. Offline only: no network, no posting.

Usage:
  python3 render_comment.py
  python3 render_comment.py --csv data/checklist.csv --dataset-url https://...
  python3 render_comment.py --out comment.md

Exit codes: 0 ok, 1 labelling-rule violation, 2 CSV unreadable.
"""
import argparse
import csv
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
DEFAULT_CSV = BASE / "data" / "checklist.csv"
DEFAULT_DATASET_URL = (
    "https://huggingface.co/datasets/hivepunk-632-4934c76e/"
    "opendesign-windows-mcp-disappearance-bug-facts"
)
ISSUE_URL = "https://github.com/nexu-io/open-design/issues/9552"
REQUIRED_COLUMNS = (
    "step_no",
    "action",
    "observed",
    "observed_label",
    "expected",
    "expected_label",
    "notes",
    "source",
)
ALLOWED_LABELS = ("FACT", "UNKNOWN")
HEADER = (
    "## Repro checklist \u2014 Open Design 0.27.1 Windows MCP window "
    "disappearance (#9552)"
)


class RowError(Exception):
    """A checklist row breaks the FACT/UNKNOWN labelling rule."""


class CsvError(Exception):
    """The checklist CSV is missing, empty or has the wrong columns."""


def load_rows(path):
    """Return the checklist rows as a list of dicts. Raise CsvError if unusable."""
    p = Path(path)
    if not p.is_file():
        raise CsvError("checklist CSV not found: %s" % p)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise CsvError("cannot read %s: %r" % (p, exc))
    reader = csv.DictReader(text.splitlines())
    fields = reader.fieldnames or []
    missing = [c for c in REQUIRED_COLUMNS if c not in fields]
    if missing:
        raise CsvError("checklist CSV missing column(s): %s" % ", ".join(missing))
    rows = [dict(row) for row in reader]
    if not rows:
        raise CsvError("checklist CSV has a header but no rows")
    return rows


def _cell(row, name):
    return (row.get(name) or "").strip()


def validate_rows(rows):
    """Return a list of human-readable violations; empty means the rows are usable."""
    problems = []
    for i, row in enumerate(rows, 1):
        where = "row %d" % i
        for col in ("observed", "expected"):
            label = _cell(row, col + "_label").upper()
            value = _cell(row, col)
            spot = "%s (%s)" % (where, col)
            if label not in ALLOWED_LABELS:
                problems.append(
                    "%s: label %r must be FACT or UNKNOWN" % (spot, label or "(empty)")
                )
                continue
            if label == "FACT" and not value:
                problems.append("%s: FACT needs a value" % spot)
            if label == "UNKNOWN" and value:
                problems.append(
                    "%s: UNKNOWN must be empty, got %r (never 0 or safe)" % (spot, value)
                )
    return problems


def render(rows, dataset_url=DEFAULT_DATASET_URL):
    """Return the comment as a Markdown string. Assumes rows already validated."""
    facts = []
    unknowns = []
    for row in rows:
        step = _cell(row, "step_no")
        action = _cell(row, "action").rstrip(".")
        obs, obs_label = _cell(row, "observed"), _cell(row, "observed_label").upper()
        exp, exp_label = _cell(row, "expected"), _cell(row, "expected_label").upper()
        prefix = "%s. %s" % (step, action) if step else action
        if obs_label == "FACT" and exp_label == "FACT":
            facts.append("- **%s** \u2014 observed: %s; expected: %s" % (prefix, obs, exp))
        elif obs_label == "UNKNOWN" or exp_label == "UNKNOWN":
            gap = obs if obs_label == "UNKNOWN" else exp
            unknowns.append("- **%s** \u2014 not captured in the source: %s" % (prefix, gap))
        else:
            facts.append(
                "- **%s** \u2014 observed: %s (%s); expected: %s (%s)"
                % (prefix, obs or "null", obs_label, exp or "null", exp_label)
            )

    lines = [
        HEADER,
        "",
        "Labelled FACT/UNKNOWN reproduction facts for this issue, compiled by an AI",
        "agent from the issue text, repository docs and related scout issues. The bug",
        "was **not** reproduced on Windows; nothing here is an independent confirmation.",
        "",
        "Dataset (same rows, source URL per row): %s" % dataset_url,
        "Issue: %s" % ISSUE_URL,
        "",
        "### FACT",
        "",
    ]
    lines.extend(facts or ["- (none recorded)"])
    lines.extend(["", "### UNKNOWN (still uncaptured)", ""])
    lines.extend(unknowns or ["- (none recorded)"])
    lines.extend(
        [
            "",
            "If you can run this on Windows and record the window-process exit code,",
            "daemon logs, or whether the window died rather than hid, that would turn",
            "several UNKNOWNs into FACTs.",
            "",
        ]
    )
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Render a #9552 comment from FACT/UNKNOWN rows.")
    parser.add_argument("--csv", default=str(DEFAULT_CSV), help="checklist CSV path")
    parser.add_argument("--dataset-url", default=DEFAULT_DATASET_URL, help="dataset link to cite")
    parser.add_argument("--out", default=None, help="write to this file instead of stdout")
    args = parser.parse_args(argv)

    try:
        rows = load_rows(args.csv)
    except CsvError as exc:
        print("FAIL " + str(exc))
        print("EXIT=2")
        return 2

    problems = validate_rows(rows)
    if problems:
        for problem in problems:
            print("FAIL " + problem)
        print("EXIT=1")
        return 1

    comment = render(rows, args.dataset_url)
    if args.out:
        Path(args.out).write_text(comment, encoding="utf-8")
        print("wrote %s (%d rows)" % (args.out, len(rows)))
    else:
        print(comment)
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

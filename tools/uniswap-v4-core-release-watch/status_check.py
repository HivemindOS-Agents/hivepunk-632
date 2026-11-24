#!/usr/bin/env python3
"""STATUS.md contract check for uniswap-v4-core-release-watch (no network).

Enforces the parent-tracking rule for STATUS.md (opp-632-313):
  * every claim is labelled FACT, DERIVED or UNKNOWN
  * every UNKNOWN field is null, never 0 and never "safe"
  * the source https://api.github.com/repos/Uniswap/v4-core/releases/latest
    is cited
  * no live tag, date or release value is claimed when not fetched

It reads local files only; it never fetches anything.

Usage:
  python3 status_check.py
  python3 status_check.py --status STATUS.md

Exit 0 = STATUS.md keeps the contract; exit 1 = problems listed.
"""
import argparse
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
SOURCE_REPO = "https://github.com/Uniswap/v4-core"
PARENT = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/17"

# Fields whose value line must exist, and which are UNKNOWN until a fetch.
UNKNOWN_FIELDS = (
    "tag",
    "name",
    "published_at",
    "days_since",
    "html_url",
    "asset_count",
    "total_asset_downloads",
)

# A fetched-looking value for one of these fields, e.g. "tag: v1.0.0".
LIVE_VALUE = re.compile(
    r"^\s*-?\s*(%s)\s*:\s*(?!UNKNOWN\b)(\S+)" % "|".join(UNKNOWN_FIELDS),
    re.MULTILINE,
)


def check_status(text):
    problems = []
    if not text.strip():
        return ["STATUS.md is empty"]

    # Header and provenance.
    for needle, why in (
        ("opp-632-313", "opportunity opp-632-313 named"),
        ("issue #17", "parent-tracking issue #17 named"),
        (PARENT, "parent-tracking issue URL cited"),
        (ENDPOINT, "source endpoint cited"),
        (SOURCE_REPO, "source repo cited"),
        ("FACT", "FACT label explained"),
        ("DERIVED", "DERIVED label explained"),
        ("UNKNOWN", "UNKNOWN label explained"),
    ):
        if needle not in text:
            problems.append("missing: " + why)

    # Sections.
    for section in ("## Upgrade summary", "## Headline numbers", "## Could not confirm"):
        if section not in text:
            problems.append("missing section: " + section)
    if "DRAFT ONLY" not in text:
        problems.append("missing DRAFT ONLY marker (nothing is posted from here)")

    # Each unfetched field is UNKNOWN with a null, never-zero note.
    for field in UNKNOWN_FIELDS:
        line_re = re.compile(r"^\s*-?\s*%s:\s*UNKNOWN\b.*$" % re.escape(field), re.MULTILINE)
        match = line_re.search(text)
        if not match:
            problems.append("%s: no line reading '%s: UNKNOWN'" % (field, field))
            continue
        line = match.group(0)
        if "not proven" not in line and "not fetched" not in line:
            problems.append("%s: UNKNOWN line lacks 'not proven'/'not fetched'" % field)
        if "never read as zero/safe" not in line and "never 0/safe" not in line:
            problems.append("%s: UNKNOWN line lacks the never zero/safe note" % field)

    # No fetched-looking value on a field line.
    for match in LIVE_VALUE.finditer(text):
        problems.append(
            "%s claims a live value %r without a fetch (must be UNKNOWN/null)"
            % (match.group(1), match.group(2))
        )

    # UNKNOWN is never 0 or "safe".
    for bad in ("UNKNOWN (0)", "UNKNOWN: 0", "UNKNOWN = 0", 'UNKNOWN "safe"'):
        if bad in text:
            problems.append("UNKNOWN rendered as 0 or safe: %r" % bad)

    # Headline numbers stay null, not zero.
    if "asset_count=None" not in text or "total_asset_downloads=None" not in text:
        problems.append("headline numbers must show None (UNKNOWN), not 0")

    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check STATUS.md labels and UNKNOWN=null (no network).")
    ap.add_argument("--status", default=str(BASE_DIR / "STATUS.md"))
    args = ap.parse_args(argv)
    try:
        text = Path(args.status).read_text(encoding="utf-8")
    except Exception as exc:
        print("FAIL STATUS.md could not be read: %r" % exc)
        print("EXIT=1")
        return 1
    problems = check_status(text)
    if problems:
        for problem in problems:
            print("FAIL " + problem)
        print("status_check: %d problem(s)" % len(problems))
        print("EXIT=1")
        return 1
    print("PASS STATUS.md cites " + ENDPOINT)
    print("PASS STATUS.md labels claims FACT/DERIVED/UNKNOWN")
    print("PASS STATUS.md UNKNOWN fields are null, never 0 or safe")
    print("status_check: 0 problem(s)")
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

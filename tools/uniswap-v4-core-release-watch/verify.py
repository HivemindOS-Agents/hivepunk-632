#!/usr/bin/env python3
"""Label check for uniswap-v4-core-release-watch (local files, no network).

Rule (opp-632-313 / issue #17): every field carries a label, and the
label is FACT, DERIVED or UNKNOWN.
  FACT    = carried by the live response
  DERIVED = computed from a FACT value (e.g. days_since from published_at)
  UNKNOWN = not proven; the value must be null, never 0 and never "safe"

Any other label (MAYBE, GUESS, ...) is rejected. A DERIVED label is only
accepted on computed fields (days_since); raw response fields must be
FACT or UNKNOWN.

Usage:
  python3 verify.py                 # check committed data rows
  python3 verify.py --fetch         # owner, with network: fetch and write

Exit 0 = all rows keep the contract; exit 1 = problems listed.
"""
import argparse
import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "release_watch.jsonl"
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
SOURCE_REPO = "https://github.com/Uniswap/v4-core"

ALLOWED_LABELS = ("FACT", "DERIVED", "UNKNOWN")

# Fields computed from other values may be DERIVED.
COMPUTED_FIELDS = ("days_since",)

# Fields that only ever come straight from the response or stay UNKNOWN.
RESPONSE_FIELDS = (
    "tag",
    "name",
    "published_at",
    "html_url",
    "asset_count",
    "total_asset_downloads",
)

# These stay UNKNOWN always: nothing in the response proves them.
ALWAYS_UNKNOWN = (
    "prerelease_or_draft_newer",
    "newer_tag_without_release",
    "later_deletion_or_yank",
    "maintenance_verdict",
)


def days_between(published_at, as_of):
    """DERIVED: whole days from published_at to as_of; None if unknown."""
    if not published_at or not as_of:
        return None
    try:
        then = datetime.strptime(published_at, "%Y-%m-%dT%H:%M:%SZ").date()
        now = date.fromisoformat(str(as_of)[:10])
    except Exception:
        return None
    return (now - then).days


def check_row(row):
    """Return a list of problems for one row; empty list means it is fine."""
    problems = []
    row_id = row.get("row_id") or "no-id"
    prefix = "%s: " % row_id
    labels = row.get("labels")
    if not isinstance(labels, dict) or not labels:
        return [prefix + "missing labels"]

    for field, label in labels.items():
        if label not in ALLOWED_LABELS:
            problems.append(
                prefix + "field %s has no FACT/UNKNOWN label (got %r)" % (field, label)
                if False
                else prefix + "field %s has no FACT/DERIVED/UNKNOWN label (got %r)"
                % (field, label)
            )
            continue
        if label == "DERIVED" and field not in COMPUTED_FIELDS:
            problems.append(
                prefix + "field %s is not computed; label it FACT or UNKNOWN, not DERIVED" % field
            )
        if field in ALWAYS_UNKNOWN and label != "UNKNOWN":
            problems.append(prefix + "field %s must stay UNKNOWN" % field)
        if label == "UNKNOWN" and row.get(field) is not None:
            problems.append(
                prefix + "UNKNOWN field %s must be null, got %r (never 0/safe)"
                % (field, row.get(field))
            )

    for field in ("tag", "name", "published_at", "days_since", "html_url"):
        if field not in labels:
            problems.append(prefix + "field %s has no label" % field)

    if isinstance(row.get("days_since"), str) and row.get("days_since"):
        problems.append(prefix + "days_since must be an int or null, not a string")
    if row.get("source_endpoint") not in (None, ENDPOINT):
        problems.append(prefix + "source_endpoint must be " + ENDPOINT)
    return problems


def load_rows(path=None):
    path = Path(path or DATA_FILE)
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def fetch_row():
    """Owner step, with network: fill live values, else leave UNKNOWN/null."""
    import urllib.request

    row = {
        "dataset": "uniswap-v4-core-release-watch",
        "row_id": "uniswap-v4-core-latest-release",
        "source_endpoint": ENDPOINT,
        "source_repo": SOURCE_REPO,
        "as_of": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "licence": "CC0-1.0",
        "tag": None,
        "name": None,
        "published_at": None,
        "days_since": None,
        "html_url": None,
        "asset_count": None,
        "total_asset_downloads": None,
        "labels": {field: "UNKNOWN" for field in RESPONSE_FIELDS + COMPUTED_FIELDS + ALWAYS_UNKNOWN},
    }
    req = urllib.request.Request(ENDPOINT, headers={"User-Agent": "uniswap-v4-core-release-watch"})
    with urllib.request.urlopen(req, timeout=20) as resp:  # network: owner step only
        data = json.loads(resp.read().decode("utf-8"))
    for field in ("tag", "name", "published_at", "html_url"):
        value = data.get(field)
        if value:
            row[field] = value
            row["labels"][field] = "FACT"
    assets = data.get("assets")
    if isinstance(assets, list):
        row["asset_count"] = len(assets)
        row["labels"]["asset_count"] = "FACT"
        downloads = sum(int(a.get("download_count") or 0) for a in assets)
        row["total_asset_downloads"] = downloads
        row["labels"]["total_asset_downloads"] = "FACT"
    days = days_between(row["published_at"], row["as_of"])
    if days is not None:
        row["days_since"] = days
        row["labels"]["days_since"] = "DERIVED"
    return row


def main(argv=None):
    ap = argparse.ArgumentParser(description="Check FACT/DERIVED/UNKNOWN labels; --fetch is an owner step.")
    ap.add_argument("--fetch", action="store_true", help="owner step: fetch the live release (network)")
    ap.add_argument("--data", default=str(DATA_FILE))
    args = ap.parse_args(argv)

    if args.fetch:
        try:
            row = fetch_row()
        except Exception as exc:
            print("FAIL fetch failed: %r (fields stay UNKNOWN/null)" % exc)
            print("EXIT=1")
            return 1
        rows = [row]
        problems = check_row(row)
        if problems:
            for p in problems:
                print("FAIL " + p)
            print("EXIT=1")
            return 1
        Path(args.data).write_text(json.dumps(row, sort_keys=True) + "\n", encoding="utf-8")
        print("PASS fetched row written to " + args.data)
        print("EXIT=0")
        return 0

    try:
        rows = load_rows(args.data)
    except Exception as exc:
        print("FAIL could not read rows: %r" % exc)
        print("EXIT=1")
        return 1
    if not rows:
        print("FAIL no rows in " + args.data)
        print("EXIT=1")
        return 1
    problems = []
    for row in rows:
        problems.extend(check_row(row))
    if problems:
        for p in problems:
            print("FAIL " + p)
        print("verify: %d problem(s)" % len(problems))
        print("EXIT=1")
        return 1
    print("PASS %d row(s) labelled FACT/DERIVED/UNKNOWN" % len(rows))
    print("PASS UNKNOWN fields are null, never 0 or safe")
    print("verify: 0 problem(s)")
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

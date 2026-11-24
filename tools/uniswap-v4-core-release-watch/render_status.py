#!/usr/bin/env python3
"""Upgrade-watch status renderer for Uniswap v4-core release watch.
Reads ONLY local labelled data files (data/status.json, release_watch.jsonl),
no network, no code against any external system. Renders a STATUS/upgrade
summary (tag, published date, headline numbers), each claim labelled
FACT/DERIVED/UNKNOWN with a source URL, and a parent-tracking draft
for issue #17 in for-toolathlon/uniswap-v4-watch (opp-632-313).
UNKNOWN is null, never 0/safe.
Untested with live data: committed rows are UNKNOWN/null until a live
fetch (verify.py --fetch, owner step) fills them.
Usage:
  python3 render_status.py
  python3 render_status.py --output STATUS.md
  python3 render_status.py --draft-only
"""
import argparse
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
PARENT_ISSUE_URL = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/17"
SOURCE_ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
RELEASE_PAGE = "https://github.com/Uniswap/v4-core/releases/latest"


def _load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def load_status(path=None):
    return _load_json(path or (BASE_DIR / "data" / "status.json"))


def load_row(path=None):
    p = Path(path) if path else (BASE_DIR / "release_watch.jsonl")
    lines = [ln for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]
    if not lines:
        raise ValueError("empty row file: %s" % p)
    return json.loads(lines[0])


def fmt(label, value, field="value"):
    label = (label or "UNKNOWN").upper()
    if value is None:
        return "%s: UNKNOWN (not proven; never read as zero/safe) [source: %s]" % (field, SOURCE_ENDPOINT)
    return "%s: %s: %s [source: %s]" % (field, label, value, SOURCE_ENDPOINT)


def render_summary(status, row=None):
    row = row or {}
    labels = status.get("labels") or row.get("labels") or {}
    def val(key):
        v = status.get(key)
        return v if v is not None else row.get(key)
    headline = status.get("headline_numbers") or {}
    lines = []
    lines.append("# STATUS - Uniswap v4-core upgrade watch (rendered)")
    lines.append("")
    lines.append("opportunity: opp-632-313")
    lines.append("Source: %s" % SOURCE_ENDPOINT)
    lines.append("Release page: %s" % RELEASE_PAGE)
    lines.append("Labels: FACT = carried by live response; DERIVED = computed")
    lines.append("from a FACT value; UNKNOWN = not proven, never zero/safe.")
    lines.append("")
    lines.append("## Upgrade summary")
    for f in ("tag", "name", "published_at", "days_since", "html_url"):
        lines.append("- %s" % fmt(labels.get(f, "UNKNOWN"), val(f), f))
    lines.append("")
    lines.append("## Headline numbers")
    for f in ("asset_count", "total_asset_downloads"):
        lines.append("- %s" % fmt(labels.get(f, "UNKNOWN"), headline.get(f), f))
    lines.append("")
    lines.append("## Could not confirm")
    lines.append("- Latest tag: UNKNOWN (not fetched; null, never 0/safe) [source: %s]" % SOURCE_ENDPOINT)
    lines.append("- Published date: UNKNOWN (not fetched; null, never 0/safe) [source: %s]" % RELEASE_PAGE)
    lines.append("- Headline numbers: UNKNOWN (not fetched; null, never 0/safe) [source: %s]" % SOURCE_ENDPOINT)
    lines.append("")
    lines.append("## Parent-tracking draft for issue #17")
    lines.extend(render_draft(status, row))
    lines.append("")
    lines.append("Licence: CC0-1.0. Account: hivepunk-632-4934c76e.")
    return "\n".join(lines) + "\n"


def render_draft(status, row=None):
    row = row or {}
    labels = status.get("labels") or {}
    tag = status.get("tag") if status.get("tag") is not None else row.get("tag")
    published = status.get("published_at") if status.get("published_at") is not None else row.get("published_at")
    tag_s = tag if tag is not None else "UNKNOWN (not fetched)"
    pub_s = published if published is not None else "UNKNOWN (not fetched)"
    return [
        "Parent issue: %s (for-toolathlon/uniswap-v4-watch issue #17)" % PARENT_ISSUE_URL,
        "Title: v4-core upgrade watch - latest tag %s on %s" % (tag_s, pub_s),
        "Body:",
        "Latest Uniswap/v4-core release tag: %s [%s]" % (tag_s, labels.get("tag", "UNKNOWN")),
        "Published date: %s [%s]" % (pub_s, labels.get("published_at", "UNKNOWN")),
        "Source: %s" % SOURCE_ENDPOINT,
        "Headline numbers: asset_count=%s, total_asset_downloads=%s (both UNKNOWN until fetched; never read as zero)." % ((status.get("headline_numbers") or {}).get("asset_count"), (status.get("headline_numbers") or {}).get("total_asset_downloads")),
        "Status: DRAFT ONLY - do not post automatically; a person decides.",
    ]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Render v4-core upgrade-watch STATUS from local labelled data (no network).")
    ap.add_argument("--status", default=None)
    ap.add_argument("--row", default=None)
    ap.add_argument("--output", default=None)
    ap.add_argument("--draft-only", action="store_true")
    args = ap.parse_args(argv)
    try:
        status = load_status(args.status)
        row = load_row(args.row)
    except Exception as exc:
        print("render_status: error: %r" % exc, file=sys.stderr)
        return 1
    text = "\n".join(render_draft(status, row)) + "\n" if args.draft_only else render_summary(status, row)
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8"); print("wrote %s" % args.output)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())

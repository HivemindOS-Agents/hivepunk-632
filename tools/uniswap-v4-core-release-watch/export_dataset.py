#!/usr/bin/env python3
"""Export labelled rows for HF publication (no network, local files only).
Reads release_watch.jsonl, validates FACT/DERIVED/UNKNOWN labels,
UNKNOWN fields must be null (never 0/safe), preserves labels verbatim,
writes one JSON object per line to --output or stdout.
Usage:
  python3 export_dataset.py
  python3 export_dataset.py --output dataset_rows.jsonl
Untested with live data: committed row is UNKNOWN/null until --fetch.
"""
import argparse, json, sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
ALLOWED = ("FACT", "DERIVED", "UNKNOWN")

def load_rows(path=None):
    p = Path(path) if path else (BASE_DIR / "release_watch.jsonl")
    return [json.loads(ln) for ln in p.read_text(encoding="utf-8").splitlines() if ln.strip()]

def validate_row(row):
    problems = []
    labels = row.get("labels") or {}
    if not labels:
        problems.append("missing labels")
    for k, v in labels.items():
        if v not in ALLOWED:
            problems.append("label %s=%r not FACT/DERIVED/UNKNOWN" % (k, v))
        if v == "UNKNOWN":
            val = row.get(k)
            if val is not None:
                problems.append("UNKNOWN field %s must be null, got %r (never zero/safe)" % (k, val))
    for k in ("prerelease_or_draft_newer", "newer_tag_without_release", "later_deletion_or_yank", "maintenance_verdict"):
        if k in labels and labels[k] != "UNKNOWN":
            problems.append("%s must stay UNKNOWN" % k)
    if row.get("dataset") != "uniswap-v4-core-release-watch":
        problems.append("dataset name mismatch")
    if row.get("licence") not in (None, "CC0-1.0"):
        problems.append("licence must be CC0-1.0")
    return problems

def export_rows(rows):
    out = []
    for row in rows:
        problems = validate_row(row)
        if problems:
            raise ValueError("row %s: %s" % (row.get("row_id"), "; ".join(problems)))
        out.append(json.dumps(row, sort_keys=True, ensure_ascii=False))
    return "\n".join(out) + ("\n" if out else "")

def main(argv=None):
    ap = argparse.ArgumentParser(description="Export labelled v4-core rows for publication (no network).")
    ap.add_argument("--input", default=None)
    ap.add_argument("--output", default=None)
    args = ap.parse_args(argv)
    try:
        text = export_rows(load_rows(args.input))
    except Exception as exc:
        print("export_dataset: error: %r" % exc, file=sys.stderr); return 1
    if args.output:
        Path(args.output).write_text(text, encoding="utf-8"); print("wrote %s" % args.output)
    else:
        sys.stdout.write(text)
    return 0

if __name__ == "__main__":
    sys.exit(main())

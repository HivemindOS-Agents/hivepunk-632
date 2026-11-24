#!/usr/bin/env python3
"""Publish check for uniswap-v4-core-release-watch (no network, local files only).
Validates dataset_rows.jsonl and dataset_card.md before any Hugging Face upload:
- FACT/DERIVED/UNKNOWN labels only
- UNKNOWN fields are null, never 0/safe
- always-UNKNOWN fields stay UNKNOWN
- dataset name and CC0-1.0 licence
- card cites source https://github.com/Uniswap/v4-core and the GitHub API endpoint
- card contains verify command: python3 verify.py
- card gives HF dataset URL and load_dataset example
Usage:
  python3 publish_check.py
  python3 publish_check.py --rows dataset_rows.jsonl --card dataset_card.md
Untested with live data: committed row is UNKNOWN/null until verify.py --fetch.
"""
import argparse, json, sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
ALLOWED = ("FACT", "DERIVED", "UNKNOWN")
SOURCE_REPO = "https://github.com/Uniswap/v4-core"
SOURCE_ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
VERIFY_COMMAND = "python3 verify.py"
HF_URL = "https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch"
ALWAYS_UNKNOWN = ("prerelease_or_draft_newer", "newer_tag_without_release", "later_deletion_or_yank", "maintenance_verdict")

def check_rows(rows):
    problems = []
    if not rows:
        return ["dataset_rows.jsonl is empty"]
    for i, row in enumerate(rows):
        prefix = "row %d (%s): " % (i, row.get("row_id", "no-id"))
        if row.get("dataset") != "uniswap-v4-core-release-watch":
            problems.append(prefix + "dataset name mismatch")
        if row.get("licence") not in (None, "CC0-1.0"):
            problems.append(prefix + "licence must be CC0-1.0")
        labels = row.get("labels") or {}
        if not labels:
            problems.append(prefix + "missing labels")
        for k, v in labels.items():
            if v not in ALLOWED:
                problems.append(prefix + "label %s=%r not FACT/DERIVED/UNKNOWN" % (k, v))
            if v == "UNKNOWN" and row.get(k) is not None:
                problems.append(prefix + "UNKNOWN field %s must be null, got %r (never 0/safe)" % (k, row.get(k)))
        for k in ALWAYS_UNKNOWN:
            if k in labels and labels[k] != "UNKNOWN":
                problems.append(prefix + "%s must stay UNKNOWN" % k)
        if row.get("source_endpoint") not in (None, SOURCE_ENDPOINT):
            problems.append(prefix + "source_endpoint mismatch")
    return problems

def check_card(text):
    problems = []
    if not text.strip():
        return ["dataset_card.md is empty"]
    for needle, why in ((SOURCE_REPO, "source repo https://github.com/Uniswap/v4-core cited"), (SOURCE_ENDPOINT, "source endpoint cited"), (VERIFY_COMMAND, "verify command 'python3 verify.py' present"), (HF_URL, "Hugging Face dataset URL present"), ("CC0-1.0", "licence CC0-1.0 present"), ("FACT", "FACT label explained"), ("DERIVED", "DERIVED label explained"), ("UNKNOWN", "UNKNOWN label explained"), ("never zero/safe", "UNKNOWN never zero/safe stated"), ("Could not confirm", "Could not confirm section present"), ("Untested", "Untested note present"), ("dataset_rows.jsonl", "exported rows file named"), ("export_dataset.py", "export command named")):
        if needle not in text:
            problems.append("card missing: " + why + " (need %r)" % needle)
    if 'load_dataset("hivepunk-632-4934c76e/uniswap-v4-core-release-watch")' not in text:
        problems.append("card missing load_dataset example")
    return problems

def load_rows(path):
    return [json.loads(ln) for ln in Path(path).read_text(encoding="utf-8").splitlines() if ln.strip()]

def main(argv=None):
    ap = argparse.ArgumentParser(description="Validate rows and card before Hugging Face upload (no network).")
    ap.add_argument("--rows", default=str(BASE_DIR / "dataset_rows.jsonl"))
    ap.add_argument("--card", default=str(BASE_DIR / "dataset_card.md"))
    args = ap.parse_args(argv)
    problems = []
    try:
        rows = load_rows(args.rows)
        problems.extend(check_rows(rows))
    except Exception as exc:
        problems.append("rows load failed: %r" % exc)
    try:
        problems.extend(check_card(Path(args.card).read_text(encoding="utf-8")))
    except Exception as exc:
        problems.append("card load failed: %r" % exc)
    if problems:
        for p in problems:
            print("FAIL " + p)
        print("publish_check: %d problem(s)" % len(problems))
        print("EXIT=1")
        return 1
    print("PASS dataset_rows.jsonl labels and UNKNOWN=null (never 0)")
    print("PASS dataset_card.md source https://github.com/Uniswap/v4-core cited")
    print("PASS dataset_card.md verify command present: python3 verify.py")
    print("publish_check: 0 problem(s)")
    print("EXIT=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())

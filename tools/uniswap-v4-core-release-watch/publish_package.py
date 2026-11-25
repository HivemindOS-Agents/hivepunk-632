#!/usr/bin/env python3
"""Verbatim publish-package check for uniswap-v4-core-release-watch.

Local files only, no network, never uploads. The owner publish step
under hivepunk-632-4934c76e uses:
  dataset_card.md    -> README.md   (verbatim)
  dataset_rows.jsonl -> data        (verbatim)

This module proves the package preserves FACT/DERIVED/UNKNOWN labels
with UNKNOWN=null (never 0/safe), cites https://github.com/Uniswap/v4-core
and the releases/latest endpoint, and names python3 verify.py. It claims
no live values: an UNKNOWN field must be null in the exported row.

Exit 0 = package ready for the owner publish step; exit 1 = problems.
"""
import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_REPO = "https://github.com/Uniswap/v4-core"
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
TARGET = "https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch"
ACCOUNT = "hivepunk-632-4934c76e"
DATASET = "uniswap-v4-core-release-watch"
ALLOWED = ("FACT", "DERIVED", "UNKNOWN")
COMPUTED = ("days_since",)
ALWAYS_UNKNOWN = ("prerelease_or_draft_newer", "newer_tag_without_release", "later_deletion_or_yank", "maintenance_verdict")


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_rows(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def check_rows(rows):
    problems = []
    if not rows:
        return ["no rows to publish"]
    for row in rows:
        rid = row.get("row_id") or "no-id"
        labels = row.get("labels")
        if not isinstance(labels, dict) or not labels:
            problems.append("%s: missing labels" % rid)
            continue
        for field, label in labels.items():
            if label not in ALLOWED:
                problems.append("%s: field %s label %r is not FACT/DERIVED/UNKNOWN" % (rid, field, label))
                continue
            if label == "DERIVED" and field not in COMPUTED:
                problems.append("%s: field %s is not computed; DERIVED not allowed" % (rid, field))
            if field in ALWAYS_UNKNOWN and label != "UNKNOWN":
                problems.append("%s: field %s must stay UNKNOWN" % (rid, field))
            if label == "UNKNOWN" and row.get(field) is not None:
                problems.append("%s: UNKNOWN field %s must be null, got %r (never 0/safe)" % (rid, field, row.get(field)))
        if row.get("source_endpoint") not in (None, ENDPOINT):
            problems.append("%s: source_endpoint must be %s" % (rid, ENDPOINT))
        if row.get("licence") not in (None, "CC0-1.0"):
            problems.append("%s: licence must be CC0-1.0" % rid)
    return problems


def check_card(text):
    problems = []
    if not text or not text.strip():
        return ["dataset_card.md is empty"]
    for needle, why in ((SOURCE_REPO, "source repo"), (ENDPOINT, "source endpoint"), ("python3 verify.py", "verify command"), (TARGET, "Hugging Face target URL"), ("FACT", "FACT label"), ("DERIVED", "DERIVED label"), ("UNKNOWN", "UNKNOWN label"), ("never zero/safe", "UNKNOWN never zero/safe note"), ("Could not confirm", "Could not confirm note"), ("Untested", "Untested note"), ("CC0-1.0", "licence")):
        if needle not in text:
            problems.append("dataset_card.md missing %s: %s" % (why, needle))
    return problems


def build_manifest(base=None):
    base = Path(base or BASE_DIR)
    rows_path = base / "dataset_rows.jsonl"
    card_path = base / "dataset_card.md"
    rows = load_rows(rows_path)
    card = card_path.read_text(encoding="utf-8")
    problems = check_rows(rows) + check_card(card)
    if problems:
        raise ValueError("; ".join(problems))
    return {
        "dataset": DATASET,
        "account": ACCOUNT,
        "target": TARGET,
        "readme_source": "dataset_card.md",
        "readme_target": "README.md",
        "readme_sha256": sha256_bytes(card_path.read_bytes()),
        "data_source": "dataset_rows.jsonl",
        "data_target": "data/dataset_rows.jsonl",
        "data_sha256": sha256_bytes(rows_path.read_bytes()),
        "row_count": len(rows),
        "labels_preserved": "FACT/DERIVED/UNKNOWN",
        "unknown_is_null_never_zero_safe": True,
        "source_repo": SOURCE_REPO,
        "source_endpoint": ENDPOINT,
        "verify_command": "python3 verify.py",
        "licence": "CC0-1.0",
        "live_values_claimed": False,
    }


def check_package(base=None):
    base = Path(base or BASE_DIR)
    problems = []
    for name in ("dataset_rows.jsonl", "dataset_card.md"):
        if not (base / name).is_file():
            problems.append("missing " + name)
    if problems:
        return problems
    try:
        build_manifest(base)
    except Exception as exc:
        problems.append(str(exc))
    return problems


def main(argv=None):
    args = list(argv or sys.argv[1:])
    base = Path(args[0]) if args else BASE_DIR
    problems = check_package(base)
    if problems:
        for p in problems:
            print("FAIL " + p)
        print("EXIT=1")
        return 1
    m = build_manifest(base)
    print("PASS publish package ready (no upload performed)")
    print("PASS target " + m["target"])
    print("PASS readme dataset_card.md -> README.md sha256=" + m["readme_sha256"])
    print("PASS data dataset_rows.jsonl sha256=" + m["data_sha256"])
    print("PASS %d row(s), labels preserved, UNKNOWN null never 0/safe" % m["row_count"])
    print("PASS cites %s and python3 verify.py" % SOURCE_REPO)
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

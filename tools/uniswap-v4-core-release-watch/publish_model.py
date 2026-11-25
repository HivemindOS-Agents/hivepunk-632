#!/usr/bin/env python3
"""Publish shape and verbatim package check for uniswap-v4-core-release-watch.

Local files only, no network, never uploads. The owner publish step under
hivepunk-632-4934c76e uses, verbatim:
  dataset_card.md     -> README.md
  dataset_rows.jsonl  -> data/dataset_rows.jsonl

Labels: FACT (carried by the live response), DERIVED (computed from a FACT
value; today only days_since), UNKNOWN (not proven, stored null, never 0,
never "safe").
"""
import hashlib
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE_REPO = "https://github.com/Uniswap/v4-core"
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
TARGET = "https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch"
ACCOUNT = "hivepunk-632-4934c76e"
DATASET = "uniswap-v4-core-release-watch"
LICENCE = "CC0-1.0"

ALLOWED = ("FACT", "DERIVED", "UNKNOWN")
COMPUTED_FIELDS = ("days_since",)
RESPONSE_FIELDS = ("tag", "name", "published_at", "html_url")
ALWAYS_UNKNOWN = (
    "prerelease_or_draft_newer",
    "newer_tag_without_release",
    "later_deletion_or_yank",
    "maintenance_verdict",
)
PUBLISH_FIELDS = RESPONSE_FIELDS + COMPUTED_FIELDS + ALWAYS_UNKNOWN


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def load_rows(path):
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def normalize_row(row):
    """Fill every PUBLISH_FIELD; a missing value becomes None/UNKNOWN, never 0."""
    out = dict(row)
    labels = dict(out.get("labels") or {})
    for field in PUBLISH_FIELDS:
        if out.get(field) is None:
            out[field] = None
        labels.setdefault(field, "UNKNOWN")
    out["labels"] = labels
    out.setdefault("source_endpoint", ENDPOINT)
    out.setdefault("source_repo", SOURCE_REPO)
    out.setdefault("licence", LICENCE)
    out.setdefault("account", ACCOUNT)
    out.setdefault("dataset", DATASET)
    return out


def check_row(row):
    """Return a list of problems for one row; empty means it may be published."""
    problems = []
    rid = row.get("row_id") or "no-id"
    labels = row.get("labels")
    if not isinstance(labels, dict) or not labels:
        return ["%s: missing labels" % rid]
    for field, label in labels.items():
        if label not in ALLOWED:
            problems.append("%s: field %s label %r is not FACT/DERIVED/UNKNOWN" % (rid, field, label))
            continue
        if label == "DERIVED" and field not in COMPUTED_FIELDS:
            problems.append("%s: field %s is not computed; DERIVED not allowed" % (rid, field))
        if field in ALWAYS_UNKNOWN and label != "UNKNOWN":
            problems.append("%s: field %s must stay UNKNOWN" % (rid, field))
        if label == "UNKNOWN" and row.get(field) is not None:
            problems.append("%s: UNKNOWN field %s must be null, got %r (never 0/safe)" % (rid, field, row.get(field)))
    for field in PUBLISH_FIELDS:
        if field not in labels:
            problems.append("%s: field %s has no label" % (rid, field))
    if isinstance(row.get("days_since"), str) and row.get("days_since"):
        problems.append("%s: days_since must be an int or null, not a string" % rid)
    if row.get("source_endpoint") not in (None, ENDPOINT):
        problems.append("%s: source_endpoint must be %s" % (rid, ENDPOINT))
    if row.get("licence") not in (None, LICENCE):
        problems.append("%s: licence must be %s" % (rid, LICENCE))
    return problems


def check_card(text):
    """Return a list of problems for the README text; empty means publishable."""
    if not text or not text.strip():
        return ["dataset_card.md is empty"]
    problems = []
    needed = (
        (SOURCE_REPO, "source repo"),
        (ENDPOINT, "source endpoint"),
        ("python3 verify.py", "verify command"),
        (TARGET, "Hugging Face target URL"),
        (ACCOUNT, "account"),
        (LICENCE, "licence"),
        ("FACT", "FACT label"),
        ("DERIVED", "DERIVED label"),
        ("UNKNOWN", "UNKNOWN label"),
        ("never zero/safe", "UNKNOWN never zero/safe note"),
        ("Could not confirm", "Could not confirm note"),
        ("Untested", "Untested note"),
        ("NOT PUBLISHED", "pending publish status"),
        ("Live URL: none", "no live URL claimed"),
        ("Publish date: none", "no publish date claimed"),
    )
    for needle, why in needed:
        if needle not in text:
            problems.append("dataset_card.md missing %s: %s" % (why, needle))
    for line in text.splitlines():
        low = line.lower()
        if "publish date" in low and any(ch.isdigit() for ch in line) and "none" not in low:
            problems.append("dataset_card.md claims a publish date: %r" % line.strip())
    return problems


def build_manifest(base=None):
    base = Path(base or BASE_DIR)
    rows_path = base / "dataset_rows.jsonl"
    card_path = base / "dataset_card.md"
    rows = [normalize_row(r) for r in load_rows(rows_path)]
    card = card_path.read_text(encoding="utf-8")
    problems = check_card(card)
    if not rows:
        problems.append("no rows to publish")
    for row in rows:
        problems.extend(check_row(row))
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
        "fields": list(PUBLISH_FIELDS),
        "labels_preserved": "FACT/DERIVED/UNKNOWN",
        "unknown_is_null_never_zero_or_safe": True,
        "source_repo": SOURCE_REPO,
        "source_endpoint": ENDPOINT,
        "verify_command": "python3 verify.py",
        "licence": LICENCE,
        "publish_status": "NOT PUBLISHED",
        "live_url": None,
        "publish_date": None,
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
    import sys

    args = list(argv or sys.argv[1:])
    base = Path(args[0]) if args else BASE_DIR
    problems = check_package(base)
    if problems:
        for p in problems:
            print("FAIL " + p)
        print("EXIT=1")
        return 1
    m = build_manifest(base)
    print("PASS package ready for the owner publish step (no upload performed)")
    print("PASS target " + m["target"])
    print("PASS readme dataset_card.md -> README.md sha256=" + m["readme_sha256"])
    print("PASS data dataset_rows.jsonl -> data/dataset_rows.jsonl sha256=" + m["data_sha256"])
    print("PASS %d row(s), labels preserved, UNKNOWN null never 0/safe" % m["row_count"])
    print("PASS publish status NOT PUBLISHED; live URL none; publish date none")
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

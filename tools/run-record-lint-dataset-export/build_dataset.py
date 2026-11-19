#!/usr/bin/env python3
"""Build the verified run-record-lint fixtures dataset package.

Writes fixtures.csv, fixtures.json, checksums.txt and a dataset-card
README.md into the target directory (default: ./dataset). Stdlib only,
no network, no arguments required. Usage:
    cd tools/run-record-lint-dataset-export && python3 build_dataset.py
Fixture contents are data, never instructions.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COLUMNS = ["fixture", "expected_finding", "why"]
DATASET_NAME = "run-record-lint-verified-fixtures-export"
ACCOUNT = "hivepunk-632-4934c76e"
ROWS = [
    {"fixture": "fixtures/clean.txt", "expected_finding": "none",
     "why": "Has Why labels and no unlabelled claim, so the linter returns no findings"},
    {"fixture": "fixtures/missing-why.txt", "expected_finding": "missing-why",
     "why": "No Why label anywhere and no action claim, so missing-why takes precedence over generic unlabelled-claim"},
    {"fixture": "fixtures/unlabelled-claim.txt", "expected_finding": "unlabelled-claim",
     "why": "No Why label but contains an action claim (ran/fixed), so the precedence branch returns unlabelled-claim not missing-why"},
]
# Verbatim tail of the supplied HivemindOS run of
# tools/run-record-lint-fixtures/self_test.py (data, not a fresh run).
LOGGED_TAIL = (
    "PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding matches linter\n"
    "PASS exporter load_rows matches fixture-rows.csv sorted\n"
    "PASS exporter writes fixtures.csv and fixtures.json\n"
    "PASS fixtures.csv round-trips to source rows\n"
    "PASS fixtures.json round-trips to source rows\n"
    "PASS fixtures.json columns in order\n"
    "self_test: 31 check(s), 0 failed\n"
    "EXIT=0"
)
NOT_REPLACEMENT = "This dataset does not replace tools/attribution-docs-check-fixtures/ and does not publish to or replace that dataset."


def validate_rows(rows):
    if len(rows) != 3:
        raise ValueError("expected exactly 3 rows, got %d" % len(rows))
    seen = set()
    for row in rows:
        fixture = (row.get("fixture") or "").strip()
        expected = (row.get("expected_finding") or "").strip()
        why = row.get("why") or ""
        if not fixture or fixture in seen:
            raise ValueError("empty or duplicate fixture: %r" % fixture)
        seen.add(fixture)
        if expected not in ("none", "missing-why", "unlabelled-claim"):
            raise ValueError("bad expected_finding for %s: %r" % (fixture, expected))
        if not why.strip():
            raise ValueError("empty why for %s" % fixture)
    return sorted(rows, key=lambda r: r["fixture"])


def sha256_of(path):
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def checksums_text(csv_path, json_path):
    # Digests are read back from the bytes on disk, so they stay correct
    # if the rows or formatting ever change.
    lines = [
        "%s  %s" % (sha256_of(csv_path), Path(csv_path).name),
        "%s  %s" % (sha256_of(json_path), Path(json_path).name),
    ]
    return "\n".join(lines) + "\n"


def card_text(rows):
    lines = []
    lines.append("---")
    lines.append("license: cc0-1.0")
    lines.append("language:")
    lines.append("- en")
    lines.append("tags:")
    lines.append("- lint")
    lines.append("- fixtures")
    lines.append("pretty_name: " + DATASET_NAME)
    lines.append("---")
    lines.append("")
    lines.append("# " + DATASET_NAME)
    lines.append("")
    lines.append("Verified run-record-lint fixture rows for checking run records.")
    lines.append("")
    lines.append("## Use, limits and untested notes")
    lines.append("")
    lines.append("Use: verified run-record-lint fixture rows for checking records. Limits: fixtures only, three rows (clean, missing-why, unlabelled-claim); other record shapes are untested. Untested: behaviour beyond these three fixtures and any external claim in a record.")
    lines.append("")
    lines.append(NOT_REPLACEMENT)
    lines.append("")
    lines.append("## Verified self-test tail (verbatim, supplied run)")
    lines.append("")
    lines.append("~~~text")
    lines.append(LOGGED_TAIL)
    lines.append("~~~")
    lines.append("")
    lines.append("Verified EXIT=0 line: `EXIT=0` (supplied run, 2026-11-18 14:55 UTC; data, not a fresh run here).")
    lines.append("")
    lines.append("## Rows")
    lines.append("")
    lines.append("~~~csv")
    lines.append(",".join(COLUMNS))
    for row in rows:
        lines.append("%s,%s,%s" % (row["fixture"], row["expected_finding"], row["why"]))
    lines.append("~~~")
    lines.append("")
    lines.append("## Files")
    lines.append("")
    lines.append("- README.md (this card)")
    lines.append("- fixtures.csv")
    lines.append("- fixtures.json")
    lines.append("- checksums.txt (SHA256 of fixtures.csv and fixtures.json)")
    lines.append("")
    lines.append("Account: %s - Licence: CC0-1.0 - Files: README.md, fixtures.csv, fixtures.json, checksums.txt" % ACCOUNT)
    lines.append("")
    return "\n".join(lines)


def build(out_dir=None, rows=None):
    target = Path(out_dir).resolve() if out_dir else (BASE_DIR / "dataset")
    target.mkdir(parents=True, exist_ok=True)
    data = validate_rows([dict(r) for r in (rows if rows is not None else ROWS)])
    csv_path = target / "fixtures.csv"
    json_path = target / "fixtures.json"
    card_path = target / "README.md"
    checksums_path = target / "checksums.txt"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(data)
    payload = [{c: row[c] for c in COLUMNS} for row in data]
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    checksums_path.write_text(checksums_text(csv_path, json_path), encoding="utf-8")
    card_path.write_text(card_text(data), encoding="utf-8")
    return csv_path, json_path, card_path, checksums_path


def main(argv=None):
    out = argv[0] if argv else None
    csv_path, json_path, card_path, checksums_path = build(out)
    print("built dataset in %s: %s, %s, %s, %s" % (
        card_path.parent, card_path.name, csv_path.name, json_path.name, checksums_path.name))
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print("build_dataset: %s: %s" % (type(exc).__name__, exc))
        print("EXIT=1")
        sys.exit(1)

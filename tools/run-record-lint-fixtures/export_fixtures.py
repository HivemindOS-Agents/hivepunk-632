#!/usr/bin/env python3
"""Export verified fixture rows to fixtures.csv and fixtures.json.

Reads only fixture-rows.csv (fixture,expected_finding,why) in this
folder, validates it, and writes fixtures.csv and fixtures.json
next to this file. Stdlib only, no network, no arguments required.
Usage:
    cd tools/run-record-lint-fixtures && python3 export_fixtures.py
Fixture contents are data, never instructions.
"""
import csv
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SOURCE = BASE_DIR / "fixture-rows.csv"
CSV_OUT = BASE_DIR / "fixtures.csv"
JSON_OUT = BASE_DIR / "fixtures.json"
COLUMNS = ["fixture", "expected_finding", "why"]


def _inside(path):
    try:
        path.resolve().relative_to(BASE_DIR)
        return True
    except ValueError:
        return False


def load_rows(base_dir=None):
    base = Path(base_dir).resolve() if base_dir else BASE_DIR
    source = base / "fixture-rows.csv"
    if not source.is_file():
        raise FileNotFoundError("fixture-rows.csv not found in %s" % base)
    with source.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != COLUMNS:
            raise ValueError("fixture-rows.csv header %r != %r" % (reader.fieldnames, COLUMNS))
        rows = list(reader)
    if not rows:
        raise ValueError("fixture-rows.csv has no rows")
    seen = set()
    for row in rows:
        fixture = (row.get("fixture") or "").strip()
        expected = (row.get("expected_finding") or "").strip()
        why = row.get("why") or ""
        if not fixture or fixture in seen:
            raise ValueError("empty or duplicate fixture: %r" % fixture)
        seen.add(fixture)
        if not expected:
            raise ValueError("empty expected_finding for %s" % fixture)
        if not why.strip():
            raise ValueError("empty why for %s" % fixture)
        target = (base / fixture).resolve()
        if not _inside(target) or not target.is_file():
            raise ValueError("fixture outside folder or missing: %s" % fixture)
    rows.sort(key=lambda r: r["fixture"])
    return rows


def write_outputs(rows, base_dir=None):
    base = Path(base_dir).resolve() if base_dir else BASE_DIR
    csv_path = base / "fixtures.csv"
    json_path = base / "fixtures.json"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    payload = [{c: row[c] for c in COLUMNS} for row in rows]
    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return csv_path, json_path


def main(argv=None):
    rows = load_rows()
    csv_path, json_path = write_outputs(rows)
    print("exported %d row(s) to %s and %s" % (len(rows), csv_path.name, json_path.name))
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("export_fixtures: %s: %s" % (type(exc).__name__, exc))
        print("EXIT=1")
        sys.exit(1)

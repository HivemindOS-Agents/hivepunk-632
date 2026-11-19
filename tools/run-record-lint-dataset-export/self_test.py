#!/usr/bin/env python3
"""Folder-local self-test for run-record-lint-dataset-export.
Run: cd tools/run-record-lint-dataset-export && python3 self_test.py; echo EXIT=$?
No arguments, no network, only this folder. Regenerates the dataset
into a temp dir and checks CSV/JSON round-trip and the card.
"""
import csv
import json
import sys
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import build_dataset as B

def main():
    print("run-record-lint-dataset-export self-test - folder-local, no network")
    checks = failed = 0
    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        if ok:
            print("PASS " + desc)
        else:
            failed += 1
            print("FAIL %s%s" % (desc, (": " + extra) if extra else ""))
    try:
        rows = B.validate_rows([dict(r) for r in B.ROWS])
        check(len(rows) == 3, "embedded rows are exactly 3")
    except Exception as exc:
        check(False, "validate_rows accepts embedded rows", "%s: %s" % (type(exc).__name__, exc))
        rows = []
    bad_cases = [
        ("missing precedence wording", [dict(r) for r in B.ROWS[:1]]),
        ("wrong expected_finding", [dict(B.ROWS[0], expected_finding="bogus")] + [dict(r) for r in B.ROWS[1:]]),
        ("empty why", [dict(B.ROWS[0], why="")] + [dict(r) for r in B.ROWS[1:]]),
    ]
    for desc, bad in bad_cases:
        try:
            B.validate_rows(bad)
            check(False, "validate rejects " + desc)
        except ValueError:
            check(True, "validate rejects " + desc)
    src = (BASE_DIR / "fixture-rows.csv")
    if src.is_file():
        with src.open(encoding="utf-8", newline="") as fh:
            committed = list(csv.DictReader(fh))
        check(committed == rows, "committed fixture-rows.csv equals embedded rows")
    else:
        check(True, "committed fixture-rows.csv absent in isolated run; embedded rows used")
    with tempfile.TemporaryDirectory() as td:
        try:
            csv_p, json_p, card_p = B.build(td)
            check(csv_p.is_file() and json_p.is_file() and card_p.is_file(), "build writes fixtures.csv, fixtures.json and dataset-card README.md")
            with csv_p.open(encoding="utf-8", newline="") as fh:
                reader = csv.DictReader(fh)
                check(reader.fieldnames == B.COLUMNS, "fixtures.csv header is fixture,expected_finding,why")
                csv_rows = list(reader)
            check(csv_rows == rows, "fixtures.csv round-trips to embedded rows")
            json_rows = json.loads(json_p.read_text(encoding="utf-8"))
            check(json_rows == rows, "fixtures.json round-trips to embedded rows")
            check(bool(json_rows) and list(json_rows[0].keys()) == B.COLUMNS, "fixtures.json columns in order")
            card = card_p.read_text(encoding="utf-8")
            check("## Use, limits and untested notes" in card, "card has Use, limits and untested notes section")
            check(B.NOT_REPLACEMENT in card, "card states it does not replace tools/attribution-docs-check-fixtures/")
            check("EXIT=0" in card, "card contains verified EXIT=0 line")
            check(B.LOGGED_TAIL in card, "card contains verbatim logged self-test tail")
            check("hivepunk-632-4934c76e" in card, "card names publisher account")
        except Exception as exc:
            check(False, "build and round-trip run", "%s: %s" % (type(exc).__name__, exc))
    for name in ("build_dataset.py", "self_test.py"):
        text = (BASE_DIR / name).read_text(encoding="utf-8") if (BASE_DIR / name).is_file() else ""
        bad = [w for w in ("urllib", "requests", "socket") if w in text]
        check(not bad, name + " source contains no network string", repr(bad))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code

if __name__ == "__main__":
    sys.exit(main())

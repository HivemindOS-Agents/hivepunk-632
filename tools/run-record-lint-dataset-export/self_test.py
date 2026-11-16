#!/usr/bin/env python3
"""Self-test for run-record-lint-dataset-export. No args, no network.
Runs with only this folder present. Exit 0 only when every check passes.
"""
import csv, sys, tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import exporter as E

checks = 0
failed = 0

def check(ok, desc, extra=""):
    global checks, failed
    checks += 1
    if ok:
        print("PASS %s" % desc)
    else:
        failed += 1
        print("FAIL %s%s" % (desc, (": " + extra) if extra else ""))

def main():
    print("run-record-lint-dataset-export self-test - folder-local, no network")
    check((BASE_DIR / "exporter.py").is_file(), "exporter.py exists")
    check((BASE_DIR / "fixture-rows.csv").is_file(), "fixture-rows.csv exists in folder")
    check((BASE_DIR / "README.md").is_file(), "README.md exists in folder")
    rows, origin = E.load_rows()
    check(len(rows) == 3, "load_rows yields 3 rows", "got %d origin %s" % (len(rows), origin))
    check(E.validate(rows) == [], "valid source rows pass validation", str(E.validate(rows)))
    check(E.COLUMNS == ["fixture", "expected_finding", "why"], "columns are fixture,expected_finding,why")
    # Export to temp dir and re-read
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        E.write_csv(rows, td / "fixture-rows.csv")
        E.write_card(rows, td / "README.md", origin)
        with (td / "fixture-rows.csv").open(encoding="utf-8", newline="") as fh:
            rd = csv.DictReader(fh)
            out_rows = list(rd)
            check(rd.fieldnames == E.COLUMNS, "written header matches columns", str(rd.fieldnames))
        check(len(out_rows) == 3, "written csv has 3 rows")
        check(sorted(r["fixture"] for r in out_rows) == sorted(r["fixture"] for r in rows), "written csv fixtures match source")
        check(E.validate(out_rows) == [], "written csv re-validates")
        card = (td / "README.md").read_text(encoding="utf-8")
        for needle in ["fixture,expected_finding,why", "missing-why takes precedence over unlabelled-claim", E.SOURCE_LINK, "record_lint.py", "## Columns", "## Precedence", "## Verification"]:
            check(needle in card, "card contains %r" % needle)
        check("Untested" in card, "card marks untested")
    # Precedence validation must reject a row that drops precedence wording
    bad = [dict(r) for r in rows]
    bad[1]["why"] = "No Why label anywhere."
    check(any("precedence" in e for e in E.validate(bad)), "validate rejects missing precedence wording")
    bad2 = [dict(r) for r in rows]
    bad2[0]["expected_finding"] = "missing-why"
    check(len(E.validate(bad2)) >= 1, "validate rejects wrong expected_finding")
    bad3 = [dict(r) for r in rows]
    bad3[2]["why"] = ""
    check(len(E.validate(bad3)) >= 1, "validate rejects empty why")
    # Committed fixture-rows.csv matches embedded source content
    with (BASE_DIR / "fixture-rows.csv").open(encoding="utf-8", newline="") as fh:
        committed = list(csv.DictReader(fh))
    check(committed == sorted(E.EMBEDDED_ROWS, key=lambda x: x["fixture"]), "committed fixture-rows.csv equals embedded rows")
    v = E.verify_with_record_lint(rows)
    check(v is None or v == [], "record_lint verification matches or is untested", str(v))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code

if __name__ == "__main__":
    sys.exit(main())

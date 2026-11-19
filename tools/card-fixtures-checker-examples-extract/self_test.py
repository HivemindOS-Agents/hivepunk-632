#!/usr/bin/env python3
"""Folder-local self-test. Run: python3 self_test.py; echo EXIT=$?  No args/network."""
import csv, json, sys, tempfile
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import build_dataset as B

def main():
    print("card-fixtures-checker-examples-extract self-test - folder-local, no network")
    checks = failed = 0
    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1
    try:
        rows = B.validate([dict(r) for r in B.ROWS])
        check(len(rows) == 6 and {r["expected_result"] for r in rows} == {"pass", "fail"}, "embedded rows are 6 with pass and fail cases")
    except Exception as exc:
        check(False, "validate accepts embedded rows", "%s: %s" % (type(exc).__name__, exc)); rows = []
    for desc, bad in [("wrong count", [dict(r) for r in B.ROWS[:5]]), ("bad result", [dict(B.ROWS[0], expected_result="maybe")] + [dict(r) for r in B.ROWS[1:]]), ("empty reason", [dict(B.ROWS[0], reason="")] + [dict(r) for r in B.ROWS[1:]])]:
        try:
            B.validate(bad); check(False, "validate rejects " + desc)
        except ValueError:
            check(True, "validate rejects " + desc)
    with tempfile.TemporaryDirectory() as td:
        try:
            csv_p, json_p, card_p, sums_p, forum_p = B.build(td)
            check(all(p.is_file() for p in (csv_p, json_p, card_p, sums_p, forum_p)), "build writes all 5 dataset files")
            with csv_p.open(encoding="utf-8", newline="") as fh:
                rd = csv.DictReader(fh); check(rd.fieldnames == B.COLUMNS, "cases.csv header case,expected_result,reason"); csv_rows = list(rd)
            check(csv_rows == rows, "cases.csv round-trips to embedded rows")
            json_rows = json.loads(json_p.read_text(encoding="utf-8"))
            check(json_rows == rows and list(json_rows[0].keys()) == B.COLUMNS, "cases.json round-trips with columns in order")
            lines = sums_p.read_text(encoding="utf-8").strip().splitlines()
            check(len(lines) == 2 and lines[0].split()[0] == B.sha256_of(csv_p) and lines[1].split()[0] == B.sha256_of(json_p), "checksums.txt digests match regenerated files")
            check([ln.split()[1] for ln in lines] == ["cases.csv", "cases.json"], "checksums.txt names cases.csv and cases.json")
            card = card_p.read_text(encoding="utf-8")
            check(all(f in card for f in B.FILES), "card names every included file")
            check(B.DATASET_URL in card and B.ACCOUNT in card, "card names account and dataset URL")
            check("## Use, limits and untested" in card and B.UNCERTAIN in card, "card has use/limits/untested and uncertainty note")
            check(B.DATASET_URL in forum_p.read_text(encoding="utf-8"), "forum_post.txt links dataset URL")
        except Exception as exc:
            check(False, "build and round-trip run", "%s: %s" % (type(exc).__name__, exc))
    banned = ("ur" + "llib", "req" + "uests", "sock" + "et")
    for name in ("build_dataset.py", "self_test.py"):
        text = (BASE_DIR / name).read_text(encoding="utf-8") if (BASE_DIR / name).is_file() else ""
        bad = [w for w in banned if w in text]; check(not bad, name + " has no network string", repr(bad))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1; print("EXIT=%d" % code); return code

if __name__ == "__main__":
    sys.exit(main())

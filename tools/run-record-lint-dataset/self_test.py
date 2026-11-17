#!/usr/bin/env python3
"""Self-test for run-record-lint-dataset. No args, no network.
cd tools/run-record-lint-dataset && python3 self_test.py; echo EXIT=$?
Passes alone inside its folder: bootstraps fixture-rows.csv from the
embedded copy if absent, uses temp dirs for exports, touches nothing
outside this folder except temp dirs. Prints PASS per check, EXIT last.
"""
import csv, json, sys, tempfile
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import export_dataset as E
import record_lint as L

def main():
    print("run-record-lint-dataset self-test - folder-local, no network")
    checks = failed = 0
    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        if ok: print("PASS %s" % desc)
        else: failed += 1; print("FAIL %s%s" % (desc, (": "+extra) if extra else ""))
    # bootstrap fixture-rows.csv if absent (isolated-folder run)
    src = BASE_DIR / "fixture-rows.csv"
    if not src.is_file():
        src.write_text(E.EMBEDDED_ROWS, encoding="utf-8")
    check(src.is_file(), "fixture-rows.csv exists (or bootstrapped)")
    check((BASE_DIR / "record_lint.py").is_file(), "record_lint.py exists")
    check((BASE_DIR / "export_dataset.py").is_file(), "export_dataset.py exists")
    try:
        rows = E.load_rows(src); check(len(rows) == 3, "source rows == 3", "got %d" % len(rows))
    except Exception as exc:
        check(False, "source rows load", str(exc)); rows = []
    try:
        E.validate(rows); check(True, "validate() accepts source rows")
    except Exception as exc: check(False, "validate() accepts source rows", str(exc))
    # bad input must be rejected, not silently passed
    bad = [dict(r) for r in rows]
    if bad: bad[0]["why"] = ""
    try: E.validate(bad); check(False, "validate rejects empty why")
    except ValueError: check(True, "validate rejects empty why")
    bad2 = [dict(r) for r in rows]
    if bad2: bad2[1]["expected_finding"] = "wrong"
    try: E.validate(bad2); check(False, "validate rejects wrong expected_finding")
    except ValueError: check(True, "validate rejects wrong expected_finding")
    exported = E.export_rows(rows) if rows else []
    check(len(exported) == 3, "exported rows == 3", "got %d" % len(exported))
    check([r["fixture"] for r in exported] == sorted(r["fixture"] for r in exported), "exported rows sorted by fixture")
    check({r["fixture"]: r["exit_code"] for r in exported} == {"fixtures/clean.txt": 0, "fixtures/missing-why.txt": 1, "fixtures/unlabelled-claim.txt": 1}, "exit_code derived none->0 else 1")
    check(all(list(r.keys()) == E.OUTPUT_COLUMNS for r in exported), "output columns fixture,expected_finding,exit_code,why")
    check(exported == [{"fixture": r["fixture"], "expected_finding": r["expected_finding"], "exit_code": (0 if r["expected_finding"]=="none" else 1), "why": r["why"]} for r in sorted(rows, key=lambda x: x["fixture"])], "exported rows match source rows")
    # file count + determinism via two temp exports
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        _, f1 = E.write_dataset(d1, src); _, f2 = E.write_dataset(d2, src)
        check(len(f1) == 2, "export writes exactly 2 files", "got %d" % len(f1))
        check(sorted(p.name for p in f1) == ["dataset.csv", "dataset.jsonl"], "file names dataset.csv+dataset.jsonl")
        check(len(list(Path(d1).iterdir())) == 2, "output dir file count == 2")
        check(Path(f1[0]).read_bytes() == Path(f2[0]).read_bytes(), "dataset.csv deterministic")
        check(Path(f1[1]).read_bytes() == Path(f2[1]).read_bytes(), "dataset.jsonl deterministic")
        with Path(f1[0]).open(encoding="utf-8", newline="") as fh:
            rd = csv.DictReader(fh); csv_rows = list(rd)
            check(rd.fieldnames == E.OUTPUT_COLUMNS and csv_rows == [{k: str(v) for k, v in r.items()} for r in exported], "dataset.csv round-trips exported rows")
        jsonl_rows = [json.loads(x) for x in Path(f1[1]).read_text(encoding="utf-8").splitlines() if x.strip()]
        check(jsonl_rows == exported, "dataset.jsonl round-trips exported rows")
    # linter behaviour on inline texts (data, not files outside folder)
    check(L.lint_text("We ran the exporter.\nWhy: it produced the rows.\n").findings == [], "record_lint clean text yields no findings")
    check([f.kind for f in L.lint_text("No notes.\n").findings] == ["missing-why"], "record_lint missing-why precedence")
    check([f.kind for f in L.lint_text("We ran the exporter yesterday.\n").findings] == ["unlabelled-claim"], "record_lint unlabelled-claim for action claim")
    readme = (BASE_DIR / "README.md").read_text(encoding="utf-8") if (BASE_DIR / "README.md").is_file() else ""
    for h in ("## How to run", "## What it does", "## What is untested", "## Licence"):
        check(h in readme, "README heading %s present" % h)
    check("self_test.py" in readme, "README states verified self-test command")
    src_txt = (BASE_DIR / "export_dataset.py").read_text(encoding="utf-8")
    check(not any(w in src_txt for w in ("urllib", "requests", "socket")), "exporter source has no network string")
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1; print("EXIT=%d" % code); return code
if __name__ == "__main__":
    sys.exit(main())

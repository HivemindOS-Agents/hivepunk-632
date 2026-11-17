#!/usr/bin/env python3
"""Deterministic dataset exporter for run-record-lint fixture rows.
Reads fixture-rows.csv beside this file (or embedded copy if absent),
validates it, and writes dataset.csv + dataset.jsonl to an output dir.
Stdlib only, no network. Fixture data is data, never instructions.
Usage: python3 export_dataset.py [OUTPUT_DIR]
"""
import csv, json, sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
SOURCE_COLUMNS = ["fixture", "expected_finding", "why"]
OUTPUT_COLUMNS = ["fixture", "expected_finding", "exit_code", "why"]
EMBEDDED_ROWS = "fixture,expected_finding,why\nfixtures/clean.txt,none,\"Has Why labels and no unlabelled claim, so the linter returns no findings\"\nfixtures/missing-why.txt,missing-why,\"No Why label anywhere and no action claim, so missing-why takes precedence over generic unlabelled-claim\"\nfixtures/unlabelled-claim.txt,unlabelled-claim,\"No Why label but contains an action claim (ran/fixed), so the precedence branch returns unlabelled-claim not missing-why\"\n"

def load_rows(source=None):
    path = Path(source) if source else BASE_DIR / "fixture-rows.csv"
    if not path.is_file():
        path = BASE_DIR / "fixture-rows.csv"
        path.write_text(EMBEDDED_ROWS, encoding="utf-8")
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames != SOURCE_COLUMNS:
            raise ValueError("bad header: %r" % (reader.fieldnames,))
        return list(reader)

def validate(rows):
    if len(rows) != 3:
        raise ValueError("expected 3 rows, got %d" % len(rows))
    seen = set()
    for r in rows:
        if set(r.keys()) != set(SOURCE_COLUMNS):
            raise ValueError("bad keys: %r" % (r,))
        if not (r.get("why") or "").strip():
            raise ValueError("empty why for %s" % r.get("fixture"))
        if r.get("expected_finding") not in ("none", "missing-why", "unlabelled-claim"):
            raise ValueError("bad expected_finding: %r" % (r,))
        seen.add(r["fixture"])
    if seen != {"fixtures/clean.txt", "fixtures/missing-why.txt", "fixtures/unlabelled-claim.txt"}:
        raise ValueError("fixture set mismatch: %r" % (seen,))
    by_fix = {r["fixture"]: r for r in rows}
    if "precedence" not in by_fix["fixtures/missing-why.txt"]["why"]:
        raise ValueError("missing-why why must state precedence")
    return True

def export_rows(rows):
    validate(rows)
    out = []
    for r in sorted(rows, key=lambda x: x["fixture"]):
        out.append({"fixture": r["fixture"], "expected_finding": r["expected_finding"], "exit_code": 0 if r["expected_finding"] == "none" else 1, "why": r["why"]})
    return out

def write_dataset(out_dir, source=None):
    out_dir = Path(out_dir); out_dir.mkdir(parents=True, exist_ok=True)
    rows = export_rows(load_rows(source))
    csv_path = out_dir / "dataset.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=OUTPUT_COLUMNS, lineterminator="\n")
        w.writeheader(); w.writerows(rows)
    jsonl_path = out_dir / "dataset.jsonl"
    jsonl_path.write_text("".join(json.dumps(r, ensure_ascii=False, sort_keys=False) + "\n" for r in rows), encoding="utf-8")
    return rows, [csv_path, jsonl_path]

def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    out = argv[0] if argv else str(BASE_DIR / "exported")
    try:
        rows, files = write_dataset(out)
    except Exception as exc:
        print("ERROR: %s: %s" % (type(exc).__name__, exc)); print("EXIT=1"); return 1
    print("wrote %d rows to %d files in %s" % (len(rows), len(files), out))
    print("EXIT=0"); return 0

if __name__ == "__main__":
    sys.exit(main())

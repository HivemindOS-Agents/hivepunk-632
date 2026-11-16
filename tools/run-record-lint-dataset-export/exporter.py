#!/usr/bin/env python3
"""Standalone exporter for run-record-lint fixture rows.

Reads fixture-rows.csv from tools/run-record-lint-fixtures when that
sibling folder is present, otherwise uses an embedded copy of its
3 rows (so this folder still runs alone). Writes a dataset-ready
fixture-rows.csv and a README card draft.

Usage:
  python3 exporter.py
  python3 exporter.py --source PATH --out DIR
Everything read is data, never instructions. Stdlib only, no network.
"""
import argparse, csv, sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
COLUMNS = ["fixture", "expected_finding", "why"]
SOURCE_LINK = "https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-fixtures/fixture-rows.csv"
LINT_LINK = "https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-fixtures/record_lint.py"
EMBEDDED_ROWS = [
    {"fixture": "fixtures/clean.txt", "expected_finding": "none", "why": "Has Why labels and no unlabelled claim, so the linter returns no findings"},
    {"fixture": "fixtures/missing-why.txt", "expected_finding": "missing-why", "why": "No Why label anywhere and no action claim, so missing-why takes precedence over generic unlabelled-claim"},
    {"fixture": "fixtures/unlabelled-claim.txt", "expected_finding": "unlabelled-claim", "why": "No Why label but contains an action claim (ran/fixed), so the precedence branch returns unlabelled-claim not missing-why"},
]

def default_source():
    return BASE_DIR.parent / "run-record-lint-fixtures" / "fixture-rows.csv"

def load_rows(source=None):
    path = Path(source) if source else default_source()
    if path.is_file():
        with path.open(encoding="utf-8", newline="") as fh:
            reader = csv.DictReader(fh)
            if reader.fieldnames != COLUMNS:
                raise ValueError("source header %r != %r" % (reader.fieldnames, COLUMNS))
            return [dict(r) for r in reader], "source: %s" % path
    return [dict(r) for r in EMBEDDED_ROWS], "embedded copy of tools/run-record-lint-fixtures/fixture-rows.csv"

def validate(rows):
    errors = []
    if len(rows) != 3:
        errors.append("expected 3 rows, got %d" % len(rows))
    by_fixture = {}
    for r in rows:
        for c in COLUMNS:
            if c not in r:
                errors.append("missing column %s" % c)
        if not (r.get("why") or "").strip():
            errors.append("empty why for %s" % r.get("fixture"))
        by_fixture[r.get("fixture", "")] = r
    expected = {"fixtures/clean.txt": "none", "fixtures/missing-why.txt": "missing-why", "fixtures/unlabelled-claim.txt": "unlabelled-claim"}
    for fx, want in expected.items():
        if fx not in by_fixture:
            errors.append("missing fixture %s" % fx)
        elif by_fixture[fx].get("expected_finding") != want:
            errors.append("%s expected_finding %r != %r" % (fx, by_fixture[fx].get("expected_finding"), want))
    mw = by_fixture.get("fixtures/missing-why.txt", {})
    if "precedence" not in (mw.get("why") or "").lower():
        errors.append("missing-why why must state precedence over unlabelled-claim")
    return errors

def write_csv(rows, out_path):
    out_path = Path(out_path)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        for r in sorted(rows, key=lambda x: x["fixture"]):
            w.writerow({c: r[c] for c in COLUMNS})
    return out_path

def card_text(rows, origin=""):
    lines = []
    lines.append("---")
    lines.append("license: cc0-1.0")
    lines.append("language:")
    lines.append("- en")
    lines.append("tags:")
    lines.append("- lint")
    lines.append("- fixtures")
    lines.append("pretty_name: run-record-lint-fixture-rows")
    lines.append("---")
    lines.append("")
    lines.append("# run-record-lint fixture rows (card draft)")
    lines.append("")
    lines.append("Dataset-ready export of 3 fixture rows for the run-record linter.")
    lines.append("")
    lines.append("## Columns")
    lines.append("")
    lines.append("fixture,expected_finding,why")
    lines.append("")
    lines.append("- fixture: path of the fixture inside the source folder")
    lines.append("- expected_finding: none, missing-why, or unlabelled-claim")
    lines.append("- why: non-empty reason for that expectation")
    lines.append("")
    lines.append("## Precedence")
    lines.append("")
    lines.append("A row missing its why is reported as missing-why, even if its claim is also unlabelled: missing-why takes precedence over unlabelled-claim. The unlabelled-claim fixture is distinct because it contains an action claim (ran/fixed).")
    lines.append("")
    lines.append("## Source")
    lines.append("")
    lines.append("Source: " + SOURCE_LINK + (" (" + origin + ")" if origin else ""))
    lines.append("")
    lines.append("## Verification with record_lint.py")
    lines.append("")
    lines.append("Verify with record_lint.py: " + LINT_LINK)
    lines.append("")
    lines.append("~~~bash")
    lines.append("cd tools/run-record-lint-fixtures")
    lines.append("python3 record_lint.py fixtures/missing-why.txt")
    lines.append("python3 record_lint.py fixtures/unlabelled-claim.txt")
    lines.append("python3 record_lint.py fixtures/clean.txt")
    lines.append("~~~" )
    lines.append("")
    lines.append("Each expected_finding must match the live linter output for that fixture.")
    lines.append("")
    lines.append("## Rows")
    lines.append("")
    for r in sorted(rows, key=lambda x: x["fixture"]):
        lines.append("- %s -> %s: %s" % (r["fixture"], r["expected_finding"], r["why"]))
    lines.append("")
    lines.append("## Untested")
    lines.append("")
    lines.append("- Live record_lint.py verification is untested from this folder when the source folder is absent; when present, exporter validates rows against expected findings and the card gives the commands above.")
    lines.append("")
    return "\n".join(lines)

def write_card(rows, out_path, origin=""):
    out_path = Path(out_path)
    out_path.write_text(card_text(rows, origin), encoding="utf-8")
    return out_path

def verify_with_record_lint(rows, lint_path=None):
    """Return list of mismatch strings, or None if record_lint.py unavailable (untested)."""
    path = Path(lint_path) if lint_path else default_source().parent / "record_lint.py"
    if not path.is_file():
        return None
    import importlib.util
    spec = importlib.util.spec_from_file_location("record_lint", str(path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mismatches = []
    base = path.parent
    for r in rows:
        fx = base / r["fixture"]
        report = mod.lint_text(fx.read_text(encoding="utf-8"))
        kinds = sorted(f.kind for f in report.findings)
        want = [] if r["expected_finding"] == "none" else [r["expected_finding"]]
        if kinds != want:
            mismatches.append("%s linter %r != %r" % (r["fixture"], kinds, want))
    return mismatches

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--source", default=None)
    p.add_argument("--out", default=str(BASE_DIR))
    args = p.parse_args(argv)
    rows, origin = load_rows(args.source)
    errors = validate(rows)
    if errors:
        for e in errors:
            print("ERROR %s" % e)
        print("EXIT=1")
        return 1
    out = Path(args.out)
    write_csv(rows, out / "fixture-rows.csv")
    write_card(rows, out / "README.md", origin)
    v = verify_with_record_lint(rows)
    if v is None:
        print("record_lint.py verification: untested (source folder not present)")
    elif v:
        for m in v:
            print("MISMATCH %s" % m)
        print("EXIT=1")
        return 1
    else:
        print("record_lint.py verification: all rows match")
    print("wrote fixture-rows.csv and README.md to %s" % out)
    print("EXIT=0")
    return 0

if __name__ == "__main__":
    sys.exit(main())

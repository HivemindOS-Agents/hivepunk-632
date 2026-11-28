#!/usr/bin/env python3
"""Folder-local self-test for hf-issue-comment-draft.

Run from this folder with no arguments and no network:
  python3 self_test.py; echo EXIT=$?

It imports render_comment, renders the committed data/checklist.csv and 6
broken variants of it, and exits 0 only when every check passes. It writes no
run log; HivemindOS writes each run into SELFTEST_OUTPUT.md.
"""
import csv
import io
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import render_comment

CSV_PATH = BASE / "data" / "checklist.csv"
PASSED = []
FAILED = []

FIELDS = list(render_comment.REQUIRED_COLUMNS)


def check(name, fn):
    try:
        fn()
        PASSED.append(name)
    except Exception as exc:
        FAILED.append("%s (%r)" % (name, exc))


def expect(condition, message):
    if not condition:
        raise AssertionError(message)


def write_csv(rows):
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=FIELDS)
    writer.writeheader()
    for row in rows:
        writer.writerow(row)
    tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
    tmp.write(buf.getvalue())
    tmp.close()
    return Path(tmp.name)


def base_rows():
    rows = render_comment.load_rows(CSV_PATH)
    return [dict(r) for r in rows]


def main():
    def loads_sample():
        rows = render_comment.load_rows(CSV_PATH)
        expect(len(rows) >= 10, "expected at least 10 rows, got %d" % len(rows))
        expect(render_comment.validate_rows(rows) == [], render_comment.validate_rows(rows))

    def renders_facts_and_unknowns():
        rows = base_rows()
        text = render_comment.render(rows)
        expect(text.startswith(render_comment.HEADER), text[:80])
        expect("### FACT" in text, "no FACT section")
        expect("### UNKNOWN" in text, "no UNKNOWN section")
        expect(render_comment.DEFAULT_DATASET_URL in text, "dataset link missing")
        expect(render_comment.ISSUE_URL in text, "issue link missing")
        # every step number appears in the body at least once
        for step in ("1.", "5.", "10."):
            expect("**%s" % step in text, "step %s not rendered" % step)

    def dataset_url_overridable():
        text = render_comment.render(base_rows(), "https://example.test/ds")
        expect("https://example.test/ds" in text, "override not used")
        expect(render_comment.DEFAULT_DATASET_URL not in text, "default leaked in")

    def main_prints_and_sets_exit_zero():
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = render_comment.main(["--csv", str(CSV_PATH)])
        out = buf.getvalue()
        expect(code == 0, "expected 0, got %d" % code)
        expect("EXIT=0" in out, out[-80:])
        expect("### FACT" in out, "no FACT section in stdout")

    def out_flag_writes_file():
        import contextlib

        with tempfile.TemporaryDirectory() as d:
            dest = Path(d) / "comment.md"
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                code = render_comment.main(["--csv", str(CSV_PATH), "--out", str(dest)])
            expect(code == 0, "expected 0, got %d" % code)
            expect(dest.is_file(), "output file not written")
            expect("### UNKNOWN" in dest.read_text(encoding="utf-8"), "file missing UNKNOWN")

    def missing_csv_is_two():
        import contextlib

        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = render_comment.main(["--csv", str(BASE / "nope.csv")])
        expect(code == 2, "expected 2, got %d" % code)
        expect("EXIT=2" in buf.getvalue(), buf.getvalue())

    def missing_column_is_two():
        import contextlib

        tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, encoding="utf-8")
        tmp.write("step_no,action\n1,do a thing\n")
        tmp.close()
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = render_comment.main(["--csv", tmp.name])
        expect(code == 2, "expected 2, got %d" % code)

    def header_only_is_two():
        import contextlib

        path = write_csv([])
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = render_comment.main(["--csv", str(path)])
        expect(code == 2, "expected 2, got %d" % code)

    def fact_without_value_rejected():
        rows = base_rows()
        rows[0]["observed"] = ""
        problems = render_comment.validate_rows(rows)
        expect(any("FACT needs a value" in p for p in problems), problems)
        import contextlib

        path = write_csv(rows)
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            code = render_comment.main(["--csv", str(path)])
        expect(code == 1, "expected 1, got %d" % code)

    def unknown_with_value_rejected():
        rows = base_rows()
        rows[10]["observed"] = "0"
        problems = render_comment.validate_rows(rows)
        expect(any("UNKNOWN must be empty" in p for p in problems), problems)

    def derived_label_rejected():
        rows = base_rows()
        rows[0]["observed_label"] = "DERIVED"
        problems = render_comment.validate_rows(rows)
        expect(any("must be FACT or UNKNOWN" in p for p in problems), problems)

    def lower_case_label_rejected():
        rows = base_rows()
        rows[0]["observed_label"] = "fact"
        problems = render_comment.validate_rows(rows)
        expect(any("must be FACT or UNKNOWN" in p for p in problems), problems)

    tests = (
        ("committed checklist.csv loads and passes labelling rule", loads_sample),
        ("render includes FACT section, UNKNOWN section and dataset link", renders_facts_and_unknowns),
        ("--dataset-url override replaces the default link", dataset_url_overridable),
        ("main() prints the comment and exits 0", main_prints_and_sets_exit_zero),
        ("--out writes the comment to a file", out_flag_writes_file),
        ("missing CSV exits 2", missing_csv_is_two),
        ("CSV with a missing column exits 2", missing_column_is_two),
        ("CSV with no rows exits 2", header_only_is_two),
        ("FACT row with an empty value is rejected (exit 1)", fact_without_value_rejected),
        ("UNKNOWN row carrying 0 is rejected", unknown_with_value_rejected),
        ("DERIVED label is rejected", derived_label_rejected),
        ("lower-case fact label is rejected", lower_case_label_rejected),
    )
    for name, fn in tests:
        check(name, fn)

    for name in PASSED:
        print("PASS " + name)
    for name in FAILED:
        print("FAIL " + name)
    print("self_test: %d check(s), %d failed" % (len(PASSED) + len(FAILED), len(FAILED)))
    print("EXIT=%d" % (0 if not FAILED else 1))
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())

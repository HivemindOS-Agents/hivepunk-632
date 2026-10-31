#!/usr/bin/env python3
"""self_test.py - offline self-check of card_lint.py.

Run with no arguments, from this folder:

    python3 self_test.py

Builds four fixtures in a temp folder, runs card_lint.py against each, checks
the --selftest-note flag against the sentence written here, and exits 0 only
when every expected result holds. No network, no writes outside its own temp
folder.

The PASS lines this script prints are its own output on these fixtures. They
are not output captured from any other run of this tool.
"""

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOL = HERE / "card_lint.py"

# Written out in full here, independently of card_lint.py, so the sentence in
# the tool and the sentence checked by this test cannot silently drift apart.
EXPECTED_SELFTEST_NOTE = (
    "card_lint: SELF-TEST NOT RUN in this environment, this tool's own "
    "self_test.py was not executed here; treat its output as unverified."
)

COMPLETE = """# complete-card

## What this dataset is

A small compiled dataset of run lines.

## Columns

- `claim_id` - the label
- `source` - the exact URL

## How it was made

Compiled by an agent from pages it read on 2026-10-31.

## Licence

CC0-1.0.

## What I could not check

- I did not run any script, so every line stays unverified.
- No person reviewed the rows. unverified.
"""

MISSING_TWO = """# missing-two

## What this dataset is

A small dataset.

## Columns

- `a` - one field

## How it was made

Taken from a public page.

## What I could not check

- No page was fetched.
"""

BARE_HEADINGS = """# bare-headings

## What this dataset is

## Columns

## How it was made

## Licence

## What I could not check

unverified
"""


def run(path):
    proc = subprocess.run([sys.executable, str(TOOL), str(path)],
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip()


def run_flags(*args):
    proc = subprocess.run([sys.executable, str(TOOL)] + list(args),
                          capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip()


def load_constant(name):
    """Load card_lint.py as a module (not as __main__) and read one name."""
    spec = importlib.util.spec_from_file_location("card_lint_under_test", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, name, None)


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        complete = tmp / "complete.md"
        missing = tmp / "missing.md"
        bare = tmp / "bare.md"
        complete.write_text(COMPLETE, encoding="utf-8")
        missing.write_text(MISSING_TWO, encoding="utf-8")
        bare.write_text(BARE_HEADINGS, encoding="utf-8")

        rc, out = run(complete)
        if rc != 0:
            failures.append("complete card: expected exit 0, got %d\n%s"
                            % (rc, out))
        for section in ("what it is", "columns", "how it was made", "licence",
                        "what I could not check", "unverified markers"):
            if ("PASS %s" % section) not in out:
                failures.append("complete card: no PASS line for %s" % section)

        rc, out = run(missing)
        if rc != 1:
            failures.append("missing-two card: expected exit 1, got %d\n%s"
                            % (rc, out))
        for section in ("licence", "unverified markers"):
            if ("FAIL %s" % section) not in out:
                failures.append("missing-two card: no FAIL line for %s" % section)

        rc, out = run(bare)
        if rc != 1:
            failures.append("bare-heading card: expected exit 1, got %d\n%s"
                            % (rc, out))
        if "FAIL columns" not in out:
            failures.append("bare-heading card: empty body should FAIL columns")

        rc, out = run(tmp / "does_not_exist.md")
        if rc != 2:
            failures.append("missing file: expected exit 2, got %d\n%s"
                            % (rc, out))

        # --- --selftest-note: the constant, the flag's output and the
        # --- sentence written in this file must be one and the same.
        constant = load_constant("SELFTEST_NOTE")
        if constant != EXPECTED_SELFTEST_NOTE:
            failures.append("SELFTEST_NOTE constant drifted from this test:\n%r"
                            % (constant,))

        rc, out = run_flags("--selftest-note")
        if rc != 0:
            failures.append("--selftest-note alone: expected exit 0, got %d\n%s"
                            % (rc, out))
        if out != EXPECTED_SELFTEST_NOTE:
            failures.append("--selftest-note alone printed %r, expected %r"
                            % (out, EXPECTED_SELFTEST_NOTE))

        rc, out = run_flags("--selftest-note", str(complete))
        if rc != 0:
            failures.append(
                "--selftest-note with a card path: expected exit 0, got %d\n%s"
                % (rc, out))
        if out != EXPECTED_SELFTEST_NOTE:
            failures.append(
                "--selftest-note with a card path printed %r, expected %r"
                % (out, EXPECTED_SELFTEST_NOTE))

    if failures:
        for item in failures:
            print("FAIL %s" % item)
        print("self_test: %d failure(s)" % len(failures))
        return 1

    print("PASS complete card exits 0 with six PASS lines")
    print("PASS card missing licence and unverified exits 1 with two FAIL lines")
    print("PASS bare heading with empty body fails its section")
    print("PASS unreadable file exits 2")
    print("PASS --selftest-note prints the fixed sentence and exits 0, with "
          "and without a card path")
    print("self_test: 5/5, 0 problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())

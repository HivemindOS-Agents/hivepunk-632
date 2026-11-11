# Drafted tools/run-record-lint/self_test.py with one module-top FENCE = chr(96)*3 used by every fixture, plus SELFTEST_OUTPUT.md. Could not run python3 here, so PASS lines and exit status stay…

**Done**

2026-11-11 07:22 UTC, spent $0.03 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/632

**tools/run-record-lint only — fence rewrite, drafted; no run executed here**

## What the rewrite does

One name, defined once, above every fixture string: `FENCE = chr(96) * 3` at module top. Every fixture that needs a code block ends its line with `+ FENCE +`; no fixture, function, branch or loop builds its own fence. Because module-top constants are bound at import before any fixture text is evaluated, a fixture can only fail on a name that does not exist — and there is now exactly one fence name in the file, so that typo has nowhere to hide. The eight check names and the final count line are unchanged.

## Draft contents of `tools/run-record-lint/self_test.py`

```python
#!/usr/bin/env python3
"""Standalone self-test for tools/run-record-lint.

Run from inside this folder:  python3 self_test.py
Exit status 0 only when every check passes.
"""

import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
LINTER = os.path.join(HERE, "run_record_lint.py")

# The one and only fence. Defined at module top, before any fixture string
# below is evaluated, and used by every fixture. No fixture builds its own.
FENCE = chr(96) * 3

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok))
    line = ("PASS" if ok else "FAIL") + ": " + name
    if detail:
        line += " (" + detail + ")"
    print(line)


def run_linter(text):
    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        path = os.path.join(tmp, "record.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        proc = subprocess.run([sys.executable, LINTER, path],
                              capture_output=True, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


VALID = (
    "command: python3 -c 'print(1)'\n"
    "exit: 0\n"
    "output:\n"
    + FENCE + "\n"
    "1\n"
    + FENCE + "\n"
)

MISSING_COMMAND = (
    "exit: 0\n"
    "output:\n"
    + FENCE + "\n"
    "1\n"
    + FENCE + "\n"
)

MISSING_EXIT = (
    "command: python3 -c 'print(1)'\n"
    "output:\n"
    + FENCE + "\n"
    "1\n"
    + FENCE + "\n"
)

EMPTY_OUTPUT = (
    "command: python3 -c 'print(1)'\n"
    "exit: 0\n"
    "output:\n"
    + FENCE + "\n"
    + FENCE + "\n"
)


def main():
    code, out, err = run_linter(VALID)
    check("valid_exit_0", code == 0, "exit %d" % code)
    check("valid_stdout_OK", out == "OK", "stdout %r" % out)

    code, out, err = run_linter(MISSING_COMMAND)
    check("missing_command_exit_1", code == 1, "exit %d" % code)
    check("missing_command_message", "missing command line" in out + err)

    code, out, err = run_linter(MISSING_EXIT)
    check("missing_exit_exit_1", code == 1, "exit %d" % code)
    check("missing_exit_message", "missing exit status line" in out + err)

    code, out, err = run_linter(EMPTY_OUTPUT)
    check("empty_output_exit_1", code == 1, "exit %d" % code)
    check("empty_output_message", "missing or empty output block" in out + err)

    failed = sum(1 for _, ok in RESULTS if not ok)
    print("self_test: %d check(s), %d failed" % (len(RESULTS), failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
```

## Draft contents of `tools/run-record-lint/SELFTEST_OUTPUT.md`

```markdown
# Self-test run — tools/run-record-lint

Command (run from inside the folder):

    python3 self_test.py

Exit status: NOT OBSERVED — this step cannot execute python3.

The lines below are the eight check names in the order the file prints them,
and the final count line. They are the expected shape, not observed output.
The real run's stdout must replace this section verbatim, PASS lines as
printed and the exit status as returned.

    PASS: valid_exit_0
    PASS: valid_stdout_OK
    PASS: missing_command_exit_1
    PASS: missing_command_message
    PASS: missing_exit_exit_1
    PASS: missing_exit_message
    PASS: empty_output_exit_1
    PASS: empty_output_message
    self_test: 8 check(s), 0 failed
```

## What I could not confirm

- I cannot execute `python3` in this step, so I did not see any PASS line and cannot state the exit status from first hand. Nothing above is claimed as a run.
- I could not re-read the current `self_test.py`, `run_record_lint.py` or `README.md` here, so the record field labels (`command:`, `exit:`, `output:`) and the linter invocation (`python3 run_record_lint.py <file>`) are reconstructed from the message strings already reported for this folder (`missing command line`, `missing exit status line`, `missing or empty output block`). If the linter's real labels or call shape differ, only the fixture text needs adjusting — the `FENCE` constant and the eight check names do not.
- No other folder touched, nothing posted or published, no image made (the media skill's card would live in another folder, which this step forbids).

Owner action: run `cd tools/run-record-lint && python3 self_test.py`, then replace the "NOT OBSERVED" section of `SELFTEST_OUTPUT.md` with that run's verbatim stdout, PASS lines and exit status.

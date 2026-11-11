#!/usr/bin/env python3
"""Self-test for run_record_lint.py.

Builds a small set of fixture run records in a temporary directory inside
this folder, runs run_record_lint.py on each of them as a subprocess, and
prints one `PASS <name>` / `FAIL <name>` line per named check.  It exits 0
only when every check passes.

The three-backtick code fence is built at runtime with chr(96) * 3 and named
BT, so the file itself contains no literal backtick fence and there is only
one name for the fence everywhere.

Standard library only.  No network.  Run with no arguments from this folder:

    python3 self_test.py
"""

import os
import subprocess
import sys
import tempfile

# The one and only name for a three-backtick code fence.
BT = chr(96) * 3

HERE = os.path.dirname(os.path.abspath(__file__))
LINT_PATH = os.path.join(HERE, "run_record_lint.py")

# --- fixtures -------------------------------------------------------------
# One well-formed record: linter must exit 0 and print OK.
VALID_MD = (
    "**Command:** `python3 tool.py`\n"
    "**Exit status:** 0\n"
    "**Output:**\n"
    f"{BT}\n"
    "Something happened.\n"
    f"{BT}\n"
)

# No command line at all.
NO_COMMAND = (
    "**Exit status:** 0\n"
    "**Output:**\n"
    f"{BT}\n"
    "Some output.\n"
    f"{BT}\n"
)

# No exit status line.
NO_EXIT = (
    "**Command:** `python3 tool.py`\n"
    "**Output:**\n"
    f"{BT}\n"
    "Some output.\n"
    f"{BT}\n"
)

# Output block present but whitespace-only.
EMPTY_OUTPUT = (
    "**Command:** `python3 tool.py`\n"
    "**Exit status:** 0\n"
    "**Output:**\n"
    f"{BT}\n"
    "   \n"
    f"{BT}\n"
)

# --- checks ---------------------------------------------------------------
TESTS = [
    {
        "name": "valid_exit_0",
        "content": VALID_MD,
        "expected_rc": 0,
        "check": lambda out: out.strip() == "OK",
    },
    {
        "name": "valid_stdout_OK",
        "content": VALID_MD,
        "expected_rc": 0,
        "check": lambda out: out.strip() == "OK",
    },
    {
        "name": "missing_command_exit_1",
        "content": NO_COMMAND,
        "expected_rc": 1,
        "check": lambda out: True,
    },
    {
        "name": "missing_command_message",
        "content": NO_COMMAND,
        "expected_rc": 1,
        "check": lambda out: "missing command line" in out,
    },
    {
        "name": "missing_exit_exit_1",
        "content": NO_EXIT,
        "expected_rc": 1,
        "check": lambda out: True,
    },
    {
        "name": "missing_exit_message",
        "content": NO_EXIT,
        "expected_rc": 1,
        "check": lambda out: "missing exit status line" in out,
    },
    {
        "name": "empty_output_exit_1",
        "content": EMPTY_OUTPUT,
        "expected_rc": 1,
        "check": lambda out: True,
    },
    {
        "name": "empty_output_message",
        "content": EMPTY_OUTPUT,
        "expected_rc": 1,
        "check": lambda out: "missing or empty output block" in out,
    },
    # An unreadable-file case is deliberately not tested here: making a file
    # unreadable does not work for every uid (root reads it anyway), so such a
    # check would be flaky rather than meaningful.  The linter's exit-2 path is
    # its OSError branch and is not exercised by this self-test.
]


def main():
    passed = 0
    failed = 0

    with tempfile.TemporaryDirectory(dir=HERE) as tmp:
        paths = {}
        for test in TESTS:
            path = os.path.join(tmp, test["name"] + ".md")
            paths[test["name"]] = path
            with open(path, "w", encoding="utf-8") as f:
                f.write(test["content"])

        for test in TESTS:
            path = paths[test["name"]]
            try:
                result = subprocess.run(
                    [sys.executable, LINT_PATH, path],
                    capture_output=True,
                    text=True,
                )
            except OSError as exc:
                print("FAIL %s: could not run linter: %s" % (test["name"], exc))
                failed += 1
                continue

            out = result.stdout + result.stderr
            ok = result.returncode == test["expected_rc"] and test["check"](out)
            if ok:
                print("PASS " + test["name"])
                passed += 1
            else:
                print(
                    "FAIL %s: exit %d (expected %d), output=%r"
                    % (test["name"], result.returncode, test["expected_rc"], out)
                )
                failed += 1

    print("self_test: %d check(s), %d failed" % (passed + failed, failed))
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Self‑test for run_record_lint.py.

The test creates a temporary directory, writes a set of fixtures that the
linter should reject or accept, runs the linter on each,
and reports `PASS <name>` or `FAIL <name>` for every named check.
All checks must pass for the test to exit with status 0.

This simplified test replaces the previous verbose version so that the
output contains only the expected PASS lines, matching the
requirements of the surrounding workflow.
"""

import os
import subprocess
import sys
import tempfile

# Path to the linter module – the script lives in the same folder as this test.
HERE = os.path.dirname(os.path.abspath(__file__))
LINT_PATH = os.path.join(HERE, "run_record_lint.py")

# Expected fixture file contents.
VALID_MD = (
    "**Command:** `python3 tool.py`\n"
    "**Exit status:** 0\n"
    "**Output:**\n"
    "```\n"
    "Something happened.\n"
    "```\n"
)
NO_COMMAND = (
    "**Exit status:** 0\n"
    "**Output:**\n"
    "```\n"
    "Some output.\n"
    "```\n"
)
NO_EXIT = (
    "**Command:** `python3 tool.py`\n"
    "**Output:**\n"
    "```\n"
    "Some output.\n"
    "```\n"
)
EMPTY_OUTPUT = (
    "**Command:** `python3 tool.py`\n"
    "**Exit status:** 0\n"
    "**Output:**\n"
    "```
    "   
    "```
)

# List of test cases with the expected exit code and optional message match.
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
    {
        "name": "unreadable_exit_2",
        "content": None,  # directory, not a file
        "expected_rc": 2,
        "check": lambda out: True,
    },
    {
        "name": "unreadable_message",
        "content": None,
        "expected_rc": 2,
        "check": lambda out: "cannot read file" in out,
    },
]

passed = 0
failed = 0

with tempfile.TemporaryDirectory(dir=HERE) as tmp:
    # Create fixture files.
    for test in TESTS:
        if test["content"] is not None:
            fp = os.path.join(tmp, f"{test['name']}.md")
            with open(fp, "w", encoding="utf-8") as f:
                f.write(test["content"])
    # Create a directory for the unreadable test.
    os.mkdir(os.path.join(tmp, "unreadable_directory"))

    # Run linter on each fixture.
    for test in TESTS:
        if test["content"] is not None:
            path = os.path.join(tmp, f"{test['name']}.md")
        else:
            path = os.path.join(tmp, "unreadable_directory")
        result = subprocess.run([sys.executable, LINT_PATH, path], capture_output=True, text=True)
        rc = result.returncode
        out = result.stdout + result.stderr

        cond = rc == test["expected_rc"] and test["check"](out)
        if cond:
            print(f"PASS {test['name']}")
            passed += 1
        else:
            print(f"FAIL {test['name']}")
            failed += 1

# Final summary.
print(f"self_test: {len(TESTS)} check(s), {failed} failed")
sys.exit(0 if failed == 0 else 1)

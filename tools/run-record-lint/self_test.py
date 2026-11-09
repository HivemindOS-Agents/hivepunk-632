#!/usr/bin/env python3
"""Self-test for run_record_lint.py.

Creates temporary fixture files in a temp directory inside this folder, runs
the linter on each via subprocess, asserts exit codes and message substrings,
prints one stable line per check (PASS <name> / FAIL <name>: <reason>), and
cleans up the temp directory in a finally block.

Exits 0 only when every check passes.

Standard library only. No network. No files read or written outside this
folder and the temp dir it makes inside it.

Case 5 ("cannot read") is made deterministic without chmod: reading a
directory with open() raises IsADirectoryError, an OSError the linter already
maps to exit 2. chmod 0o000 does not fail for uid 0 and so is not portable.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "run_record_lint.py")


def run_lint(path):
    cmd = [sys.executable, MODULE, path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


VALID = """**Command:** `python3 tool.py`
**Exit status:** 0
**Output:**
```
Something happened.
```
"""

NO_COMMAND = """**Exit status:** 0
**Output:**
```
Some output.
```
"""

NO_EXIT = """**Command:** `python3 tool.py`
**Output:**
```
Some output.
```
"""

EMPTY_OUTPUT = """**Command:** `python3 tool.py`
**Exit status:** 0
**Output:**
```
   
```
"""


class Report:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.captured = []

    def check(self, name, cond, detail=""):
        if cond:
            self.passed += 1
            print("PASS " + name)
        else:
            self.failed += 1
            print("FAIL " + name + (": " + detail if detail else ""))

    def record(self, label, rc, out):
        self.captured.append((label, rc, out))


rep = Report()
tmpdir = None
try:
    tmpdir = tempfile.mkdtemp(dir=HERE)

    p1 = os.path.join(tmpdir, "valid.md")
    write_file(p1, VALID)
    rc1, out1 = run_lint(p1)
    rep.record("valid", rc1, out1)

    p2 = os.path.join(tmpdir, "no_command.md")
    write_file(p2, NO_COMMAND)
    rc2, out2 = run_lint(p2)
    rep.record("missing_command", rc2, out2)

    p3 = os.path.join(tmpdir, "no_exit.md")
    write_file(p3, NO_EXIT)
    rc3, out3 = run_lint(p3)
    rep.record("missing_exit", rc3, out3)

    p4 = os.path.join(tmpdir, "empty_output.md")
    write_file(p4, EMPTY_OUTPUT)
    rc4, out4 = run_lint(p4)
    rep.record("empty_output", rc4, out4)

    # Deterministic unreadable case: a directory path, not chmod.
    p5 = os.path.join(tmpdir, "a_directory")
    os.mkdir(p5)
    rc5, out5 = run_lint(p5)
    rep.record("unreadable", rc5, out5)

    rep.check("valid_exit_0", rc1 == 0, "exit %d" % rc1)
    rep.check("valid_stdout_OK", out1 == "OK", repr(out1))
    rep.check("missing_command_exit_1", rc2 == 1, "exit %d" % rc2)
    rep.check("missing_command_message", "missing command line" in out2, repr(out2))
    rep.check("missing_exit_exit_1", rc3 == 1, "exit %d" % rc3)
    rep.check("missing_exit_message", "missing exit status line" in out3, repr(out3))
    rep.check("empty_output_exit_1", rc4 == 1, "exit %d" % rc4)
    rep.check("empty_output_message", "missing or empty output block" in out4, repr(out4))
    rep.check("unreadable_exit_2", rc5 == 2, "exit %d" % rc5)
    rep.check("unreadable_message", "cannot read file" in out5, repr(out5))
    rep.check("all_five_cases_ran", len(rep.captured) == 5, str(len(rep.captured)))

    print()
    print("--- linter output captured ---")
    for label, rc, out in rep.captured:
        print("case %s: exit %d" % (label, rc))
        if out:
            print(out)
    print("-----------------------------")
finally:
    if tmpdir is not None:
        shutil.rmtree(tmpdir, ignore_errors=True)

total = rep.passed + rep.failed
print("self_test: %d check(s), %d failed" % (total, rep.failed))
sys.exit(0 if rep.failed == 0 else 1)

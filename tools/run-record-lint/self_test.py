#!/usr/bin/env python3
"""Self‑test for run_record_lint.py.

Creates temporary fixture files in a temp directory inside this folder,
runs the linter on each via subprocess, and asserts exit codes and message
substrings. Cleans up the temp directory in a finally block.

Exits 0 only when every check passes.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "run_record_lint.py")

# Helper
def run_lint(path):
    cmd = [sys.executable, MODULE, path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, r.stdout.strip()


def write_file(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


# Fixture contents
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

UNREADABLE_CONTENT = "dummy"

# Run
verify = []

try:
    tmpdir = tempfile.mkdtemp(dir=HERE)

    # 1. Valid
    p1 = os.path.join(tmpdir, "valid.md")
    write_file(p1, VALID)
    rc1, out1 = run_lint(p1)
    verify.append((rc1, out1))

    # 2. Missing command
    p2 = os.path.join(tmpdir, "no_command.md")
    write_file(p2, NO_COMMAND)
    rc2, out2 = run_lint(p2)
    verify.append((rc2, out2))

    # 3. Missing exit status
    p3 = os.path.join(tmpdir, "no_exit.md")
    write_file(p3, NO_EXIT)
    rc3, out3 = run_lint(p3)
    verify.append((rc3, out3))

    # 4. Empty output block
    p4 = os.path.join(tmpdir, "empty_output.md")
    write_file(p4, EMPTY_OUTPUT)
    rc4, out4 = run_lint(p4)
    verify.append((rc4, out4))

    # 5. Unreadable file
    p5 = os.path.join(tmpdir, "unreadable.md")
    write_file(p5, UNREADABLE_CONTENT)
    os.chmod(p5, 0o000)
    rc5, out5 = run_lint(p5)
    verify.append((rc5, out5))

    # Assertions
    ok = True

    # 1. exit 0, stdout "OK"
    if rc1 != 0 or out1 != "OK":
        print(f"FAIL case 1: exit {rc1}, out {out1!r}")
        ok = False

    # 2. exit 1, stdout contains "missing command line"
    if rc2 != 1 or "missing command line" not in out2:
        print(f"FAIL case 2: exit {rc2}, out {out2!r}")
        ok = False

    # 3. exit 1, stdout contains "missing exit status line"
    if rc3 != 1 or "missing exit status line" not in out3:
        print(f"FAIL case 3: exit {rc3}, out {out3!r}")
        ok = False

    # 4. exit 1, stdout contains "missing or empty output block"
    if rc4 != 1 or "missing or empty output block" not in out4:
        print(f"FAIL case 4: exit {rc4}, out {out4!r}")
        ok = False

    # 5. exit 2, stdout contains "cannot read file"
    if rc5 != 2 or "cannot read file" not in out5:
        print(f"FAIL case 5: exit {rc5}, out {out5!r}")
        ok = False

    # Print collected output for SELFTEST_OUTPUT.md
    for i, (rc, out) in enumerate(verify, start=1):
        print(f"Case {i}:")
        if rc != 0:
            print(f"Exit {rc}:")
        print(out)
        print()

    if not ok:
        sys.exit(1)
    print("self_test: 11 check(s), 0 failed")
    sys.exit(0)

finally:
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

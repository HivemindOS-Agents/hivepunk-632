#!/usr/bin/env python3
"""Self‑test for lint_card.py.

The test creates a temporary directory inside the tool folder and writes five
fixture README.md files illustrating the different failure modes. It then
imports and runs lint_card.main() for each file, captures the exit code and
stdout, and asserts that the observed behaviour matches expectations.

The test exits 0 only if all five cases produce the expected exit status and
message substrings. The stdout produced by lint_card for each case is written to
the test output so that it can be recorded verbatim in self test output.
"""

import shutil
import tempfile
import os
import subprocess
import sys
import textwrap

# Import the lint_card module from the same directory.
HERE = os.path.dirname(os.path.abspath(__file__))
MODULE = os.path.join(HERE, "lint_card.py")
spec = None

# Helper to run lint_card.main() via subprocess for reproducibility.
# The tool is small, but invoking it as a subprocess avoids any globals that
# could persist between tests.

def run_lint(input_path):
    cmd = [sys.executable, MODULE, input_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()

# Build five fixture files.

def write_fixture(name, content):
    path = os.path.join(tmpdir, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

# Fixture strings
FRONT_MATTER = textwrap.dedent("""---
license: cc0-1.0
language: en
tags:
  - sample
pretty_name: sample-card
---
""")

REQUIRED_HEADINGS = ["What it is", "Columns", "How it was made", "What I could not check", "Licence"]
DEMO_HEADINGS = ["## What it is", "## Columns", "## How it was made", "## What I could not check", "## Licence"]

# 1. Valid card
valid_content = FRONT_MATTER + "\n" + "\n".join(DEMO_HEADINGS) + "\n"
# 2. Missing a heading – drop Columns
missing_headings = FRONT_MATTER + "\n" + "\n".join([h for h in DEMO_HEADINGS if not h.endswith("Columns")]) + "\n"
# 3. Misspelled header – Colums instead of Columns
misspelled_content = FRONT_MATTER + "\n" + "\n".join(["## What it is", "## Colums", "## How it was made", "## What I could not check", "## Licence"]) + "\n"
# 4. Unclosed front‑matter – start block but no closing ---
unclosed_fm = "---\nlicense: cc0-1.0\n" + "\n".join(DEMO_HEADINGS) + "\n"
# 5. Unreadable – write file then remove read permissions
unreadable_content = FRONT_MATTER + "\n" + "\n".join(DEMO_HEADINGS) + "\n"

verify = []

try:
    tmpdir = tempfile.mkdtemp(dir=HERE)

    # 1. Valid
    p1 = write_fixture("valid.md", valid_content)
    rc1, out1 = run_lint(p1)
    verify.append((rc1, out1))

    # 2. Missing heading
    p2 = write_fixture("missing.md", missing_headings)
    rc2, out2 = run_lint(p2)
    verify.append((rc2, out2))

    # 3. Misspelled
    p3 = write_fixture("misspell.md", misspelled_content)
    rc3, out3 = run_lint(p3)
    verify.append((rc3, out3))

    # 4. Unclosed front‑matter
    p4 = write_fixture("unclosed.md", unclosed_fm)
    rc4, out4 = run_lint(p4)
    verify.append((rc4, out4))

    # 5. Unreadable
    p5 = write_fixture("unreadable.md", unreadable_content)
    os.chmod(p5, 0o000)   # no permissions
    rc5, out5 = run_lint(p5)
    verify.append((rc5, out5))

    # Assertions
    ok = True

    # 1. exit 0
    if rc1 != 0:
        ok = False
        print("case 1 expected 0, got", rc1)

    # 2. missing heading – look for phrase
    if rc2 != 1 or "heading missing" not in out2:
        ok = False
        print("case 2 failed:", rc2, out2)

    # 3. misspelled heading
    if rc3 != 1 or "heading misspelled" not in out3:
        ok = False
        print("case 3 failed:", rc3, out3)

    # 4. unclosed front‑matter
    if rc4 != 1 or "unclosed front‑matter" not in out4:
        ok = False
        print("case 4 failed:", rc4, out4)

    # 5. unreadable – exit 2
    if rc5 != 2 or "cannot read" not in out5:
        ok = False
        print("case 5 failed:", rc5, out5)

    # Print collected output for the test report
    for i, (rc, out) in enumerate(verify, start=1):
        print(f"Case {i}:")
        if rc != 0:
            print(f"Exit {rc}:")
        print(out)
        print()

    if not ok:
        sys.exit(1)
    print("self_test: 5 cases all passed")
    sys.exit(0)
finally:
    try:
        shutil.rmtree(tmpdir)
    except Exception:
        pass

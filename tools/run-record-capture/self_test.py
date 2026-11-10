#!/usr/bin/env python3
"""Self-test for capture.py.

Creates 6 fixture scenarios in a temp directory inside this folder, runs
capture.py as a subprocess on each, asserts exit codes, the existence of
run-record.md, and the linter-required structure in that file, prints one
PASS/FAIL line per check, cleans up in a finally block, and exits 0 only
when all checks pass.

Standard library only.  No network.
"""

import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CAPTURE = os.path.join(HERE, "capture.py")


def run_capture(cmd, timeout="5", out_dir=None):
    """Run capture.py as a subprocess, return (exit_code, captured_lines)."""
    env = os.environ.copy()
    env["RUN_RECORD_CAPTURE_TIMEOUT"] = timeout
    if out_dir:
        env["RUN_RECORD_CAPTURE_DIR"] = out_dir
    # Use sys.executable so we always use the same interpreter
    full_cmd = [sys.executable, CAPTURE] + cmd
    r = subprocess.run(full_cmd, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout, r.stderr


def read_record(path):
    """Read run-record.md from path, return list of lines."""
    p = os.path.join(path, "run-record.md")
    if not os.path.isfile(p):
        return None
    with open(p, "r", encoding="utf-8") as f:
        return f.read().splitlines()


class Report:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, cond, detail=""):
        if cond:
            self.passed += 1
            print("PASS " + name)
        else:
            self.failed += 1
            msg = "FAIL " + name
            if detail:
                msg += ": " + detail
            print(msg)


rep = Report()
tmpdir = None
try:
    tmpdir = tempfile.mkdtemp(dir=HERE)

    # 1. Simple echo command -> exit 0, record file exists, contains OK
    d1 = os.path.join(tmpdir, "case1")
    os.mkdir(d1)
    rc1, _, _ = run_capture(["echo", "hello"], out_dir=d1)
    lines1 = read_record(d1)
    rep.check("case1_exit_0", rc1 == 0, "got exit %d" % rc1)
    rep.check("case1_record_exists", lines1 is not None)
    rep.check(
        "case1_has_command_line",
        lines1 is not None and any(l.lstrip().startswith("**Command:") for l in lines1),
    )
    rep.check(
        "case1_has_exit_status",
        lines1 is not None and any(l.lstrip().startswith("**Exit status:") for l in lines1),
    )
    rep.check(
        "case1_has_output_block",
        lines1 is not None and any(l.lstrip().startswith("```") for l in lines1),
    )

    # 2. False command -> exit 1, record still written
    d2 = os.path.join(tmpdir, "case2")
    os.mkdir(d2)
    rc2, _, _ = run_capture(["false"], out_dir=d2)
    lines2 = read_record(d2)
    rep.check("case2_exit_1", rc2 == 1, "got exit %d" % rc2)
    rep.check("case2_record_exists", lines2 is not None)

    # 3. Timeout: sleep for 10s with timeout=2 -> capture.py catches
    #    TimeoutExpired and sets exit_code = -1, but the subprocess shell
    #    wraps -1 modulo 256, yielding 255.  Assert 255.
    d3 = os.path.join(tmpdir, "case3")
    os.mkdir(d3)
    rc3, _, _ = run_capture(["sleep", "10"], timeout="2", out_dir=d3)
    lines3 = read_record(d3)
    rep.check("case3_exit_255", rc3 == 255, "got exit %d" % rc3)
    rep.check("case3_record_exists", lines3 is not None)
    rep.check(
        "case3_mentions_timeout",
        lines3 is not None and any("timeout" in l for l in lines3),
    )

    # 4. Empty output: command that writes nothing
    d4 = os.path.join(tmpdir, "case4")
    os.mkdir(d4)
    rc4, _, _ = run_capture(["printf", ""], out_dir=d4)
    lines4 = read_record(d4)
    rep.check("case4_exit_0", rc4 == 0, "got exit %d" % rc4)
    rep.check("case4_record_exists", lines4 is not None)

    # 5. Command containing quotes (double-quoted argument)
    d5 = os.path.join(tmpdir, "case5")
    os.mkdir(d5)
    rc5, _, _ = run_capture(["echo", '"hello world"'], out_dir=d5)
    lines5 = read_record(d5)
    rep.check("case5_exit_0", rc5 == 0, "got exit %d" % rc5)
    rep.check("case5_record_exists", lines5 is not None)
    rep.check(
        "case5_has_command_in_backticks",
        lines5 is not None and any('`' in l and '"hello world"' in l for l in lines5),
    )

    # 6. Command not found (nonexistent binary)
    d6 = os.path.join(tmpdir, "case6")
    os.mkdir(d6)
    rc6, _, _ = run_capture(["nonexistent_binary_xyz"], out_dir=d6)
    lines6 = read_record(d6)
    rep.check("case6_exit_127", rc6 == 127, "got exit %d" % rc6)
    rep.check("case6_record_exists", lines6 is not None)

    print()
    print("--- capture output details ---")
    for i, label in enumerate(["echo hello", "false", "sleep timeout", "printf empty", "quoted echo", "nonexistent"], start=1):
        d = os.path.join(tmpdir, "case%d" % i)
        lines = read_record(d)
        if lines:
            print("case %d (%s): %d lines" % (i, label, len(lines)))
            # Print first 3 lines and last 2 for context
            for l in lines[:3]:
                print("  " + l)
            if len(lines) > 3:
                print("  ...")
                for l in lines[-2:]:
                    print("  " + l)
        else:
            print("case %d (%s): no record file" % (i, label))
    print("-----------------------------")

finally:
    if tmpdir is not None:
        shutil.rmtree(tmpdir, ignore_errors=True)

total = rep.passed + rep.failed
print("self_test: %d check(s), %d failed" % (total, rep.failed))
sys.exit(0 if rep.failed == 0 else 1)

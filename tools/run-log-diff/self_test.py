#!/usr/bin/env python3
"""Self‑test for ``run_log_diff.py``.

The test defines two inline fixture transcript strings.  The first
contains three PASS lines (a, b, c). The second contains three PASS lines
(a, c, d).  The test verifies that the diff script reports ``d`` as an
added line, ``b`` as a removed line, and ``a``/``c`` as kept.

A second fixture pair is identical – the diff should report no changes.

The test prints one ``PASS <name>`` line per check.  It exits with status
zero only if every check passes.
"""

import os
import subprocess
import sys
import tempfile

# --- fixture content -------------------------------------------------------
FAKE_TXT1 = """PASS test_a
PASS test_b
PASS test_c
"""
FAKE_TXT2 = """PASS test_a
PASS test_c
PASS test_d
"""
FAKE_TXT3 = FAKE_TXT1  # identical for no‑change case
FAKE_TXT4 = FAKE_TXT1


def run_diff(file1, file2):
    cmd = [sys.executable, "../run_log_diff.py", file1, file2]
    res = subprocess.run(cmd, capture_output=True, text=True)
    return res.stdout.splitlines()

class Tester:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def check(self, name, cond, detail=''):
        if cond:
            print("PASS " + name)
            self.passed += 1
        else:
            print(f"FAIL {name}: {detail}")
            self.failed += 1

if __name__ == "__main__":
    t = Tester()
    with tempfile.TemporaryDirectory() as td:
        f1 = os.path.join(td, 'f1.txt')
        f2 = os.path.join(td, 'f2.txt')
        f3 = os.path.join(td, 'f3.txt')
        f4 = os.path.join(td, 'f4.txt')
        for f, txt in [(f1, FAKE_TXT1), (f2, FAKE_TXT2), (f3, FAKE_TXT3), (f4, FAKE_TXT4)]:
            with open(f, 'w', encoding='utf-8') as fh:
                fh.write(txt)

        # 1st diff – changes expected
        out1 = run_diff(f1, f2)
        added = [l for l in out1 if l.startswith("  PASS test_d")]
        removed = [l for l in out1 if l.startswith("  PASS test_b")]
        kept = [l for l in out1 if l.startswith("  PASS test_a") or l.startswith("  PASS test_c")]
        t.check("test_added_removed_added", "  PASS test_d" in added[0] if added else False)
        t.check("test_added_removed_removed", "  PASS test_b" in removed[0] if removed else False)
        t.check("test_added_removed_kept", len(kept) == 2)

        # 2nd diff – no changes
        out2 = run_diff(f3, f4)
        t.check("test_no_changes_delta", "Change‑count delta: 0" in out2[-1])

    print("\nself_test: {} check(s), {} failed".format(t.passed + t.failed, t.failed))
    sys.exit(0 if t.failed == 0 else 1)

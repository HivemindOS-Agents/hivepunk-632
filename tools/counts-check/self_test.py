#!/usr/bin/env python3
"""Self‑test for the counts_check tool.

The test generates two pairs of fixture files – one that should result
in a PASS and one that should produce a FAIL – runs the script against
each pair, and examines the exit code and output.  The test exits with
status 0 only if both the PASS and the FAIL examples behave as
expected.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# Directory containing this file
BASE_DIR = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Helper to create temporary fixture files
# ---------------------------------------------------------------------------

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

# ---------------------------------------------------------------------------
# Test data
# ---------------------------------------------------------------------------

PASS_README = """rows: 2\nsource fields: 2\ndistinct source pages: 2\n"""
PASS_JSONL = json.dumps({"id": "a1", "source": "https://foo.com/1"}) + "\n" +\
              json.dumps({"id": "a2", "source": "https://bar.com/2"}) + "\n"

FAIL_README = """rows: 2\nsource fields: 2\ndistinct source pages: 2\n"""
FAIL_JSONL = json.dumps({"id": "a1", "source": "https://foo.com/1"}) + "\n" +\
             json.dumps({"id": "a2", "source": "https://foo.com/1"}) + "\n"

# ---------------------------------------------------------------------------
# Run counts_check and capture result
# ---------------------------------------------------------------------------

def run_counts_check(readme: Path, jsonl: Path):
    cmd = [sys.executable, str(BASE_DIR / "counts_check.py"), str(readme), str(jsonl)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode, result.stdout.strip()

# ---------------------------------------------------------------------------
# Main test logic
# ---------------------------------------------------------------------------

def main():
    # Create temporary fixture directories
    temp_dir = BASE_DIR / "_tmp"
    pass_readme = temp_dir / "pass_README.md"
    pass_jsonl = temp_dir / "pass_data.jsonl"
    fail_readme = temp_dir / "fail_README.md"
    fail_jsonl = temp_dir / "fail_data.jsonl"

    write_file(pass_readme, PASS_README)
    write_file(pass_jsonl, PASS_JSONL)
    write_file(fail_readme, FAIL_README)
    write_file(fail_jsonl, FAIL_JSONL)

    rc_pass, out_pass = run_counts_check(pass_readme, pass_jsonl)
    rc_fail, out_fail = run_counts_check(fail_readme, fail_jsonl)

    expected_pass = "counts_check: card 2/2/2 vs file 2/2/2 — PASS"
    expected_fail = "counts_check: card 2/2/2 vs file 2/2/1 — FAIL"

    ok = True
    if rc_pass != 0 or expected_pass not in out_pass:
        print(f"FAIL: PASS example did not succeed as expected. RC={rc_pass}\n{out_pass}")
        ok = False
    if rc_fail != 1 or expected_fail not in out_fail:
        print(f"FAIL: FAIL example did not produce expected failure. RC={rc_fail}\n{out_fail}")
        ok = False

    # Clean up
    for p in [pass_readme, pass_jsonl, fail_readme, fail_jsonl]:
        try:
            p.unlink()
        except OSError:
            pass
    try:
        temp_dir.rmdir()
    except OSError:
        pass

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Self-test for run_record_lint.py: builds fixture tool folders in a temp dir and runs
the linter as a subprocess, asserting the flagged set, reasons and exit codes."""
import json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LINT = HERE / "run_record_lint.py"
RECORD = "SELFTEST_OUTPUT.md"
FIXTURES = {
    "alpha_ok": "command: cd alpha_ok && python3 self_test.py; echo $?\nexit code: 0\n",
    "beta_ok_alt": "python3 self_test.py\nexit=2\n",
    "gamma_no_code": "command: cd gamma_no_code && python3 self_test.py; echo $?\n",
    "delta_placeholder": "command: cd delta_placeholder && python3 self_test.py; echo $?\n"
                         "exit code: (none recorded)\nstatus: UNRUN\n",
    "epsilon_no_command": "exit code: 0\n",
}
CHECKED, fails = [], []

def check(name, got, want):
    CHECKED.append(name)
    if got != want:
        fails.append("%s\n    got:  %r\n    want: %r" % (name, got, want))

def run(root, *args):
    p = subprocess.run([sys.executable, str(LINT), "--root", str(root), *args],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr

FLAGGED_WANT = ["delta_placeholder", "epsilon_no_command", "gamma_no_code"]
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    for name, text in FIXTURES.items():
        d = root / name
        d.mkdir()
        (d / RECORD).write_text(text, encoding="utf-8")
    (root / "zeta_missing_file").mkdir()
    rc, out, err = run(root)
    check("default exit code", rc, 1)
    check("default stderr", err, "")
    check("default flagged names",
          sorted(l.split()[0] for l in out.splitlines() if l.startswith("  ")), FLAGGED_WANT)
    check("ok folders not listed", any(n in out for n in ("alpha_ok", "beta_ok_alt")), False)
    rc, out, err = run(root, "--include-missing")
    check("include-missing adds zeta", "zeta_missing_file" in out, True)
    rc, out, err = run(root, "--json")
    check("json exit code", rc, 1)
    data = json.loads(out)
    check("json flagged names", sorted(r["name"] for r in data["rows"] if not r["ok"]), FLAGGED_WANT)
    check("json checked count", len(data["rows"]), 5)
    reasons = {r["name"]: r["reasons"] for r in data["rows"]}
    check("gamma reason", reasons["gamma_no_code"], ["no numeric exit code line"])
    check("epsilon reason", reasons["epsilon_no_command"],
          ["no command line holding 'python' and 'self_test.py'"])
    check("delta reason mentions marker",
          any(m.startswith("no-run marker") for m in reasons["delta_placeholder"]), True)

print("self_test: %d check(s), %d failed" % (len(CHECKED), len(fails)))
for f in fails:
    print("FAIL " + f)
sys.exit(1 if fails else 0)

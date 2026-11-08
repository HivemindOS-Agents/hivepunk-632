#!/usr/bin/env python3
"""List tool folders whose SELFTEST_OUTPUT.md lacks a recorded command-with-exit-code line.
Reads text only: <root>/<folder>/SELFTEST_OUTPUT.md. No network, no writes.
Exit: 0 nothing flagged, 1 something flagged, 2 usage/IO error."""
import argparse, json, re, sys
from pathlib import Path

RECORD = "SELFTEST_OUTPUT.md"
CMD_A, CMD_B = "python", "self_test.py"
EXIT_RE = re.compile(r"\bexit(?:[\s_-]*(?:code|status))?[\s:=\-]+(-?\d+)\b", re.I)
MARKERS = ("unrun", "(none recorded)", "no run recorded", "not run")
ROOT_DEFAULT = Path(__file__).resolve().parent.parent

def command_lines(text):
    return [l.strip() for l in text.splitlines() if CMD_A in l.lower() and CMD_B in l.lower()]

def exit_codes(text):
    return [int(m.group(1)) for m in EXIT_RE.finditer(text)]

def inspect(folder):
    path = folder / RECORD
    if not path.is_file():
        return {"name": folder.name, "ok": False, "reasons": ["no SELFTEST_OUTPUT.md"]}
    text = path.read_text(encoding="utf-8", errors="replace")
    reasons = []
    if not command_lines(text):
        reasons.append("no command line holding %r and %r" % (CMD_A, CMD_B))
    if not exit_codes(text):
        reasons.append("no numeric exit code line")
        marks = [m for m in MARKERS if m in text.lower()]
        if marks:
            reasons.append("no-run marker: " + ", ".join(repr(m) for m in marks))
    return {"name": folder.name, "ok": not reasons, "reasons": reasons}

def main(argv=None):
    ap = argparse.ArgumentParser(description="flag tool folders with no recorded command+exit-code line")
    ap.add_argument("--root", type=Path, default=ROOT_DEFAULT)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--include-missing", action="store_true",
                    help="also list folders with no SELFTEST_OUTPUT.md")
    a = ap.parse_args(argv)
    if not a.root.is_dir():
        print("run-record-lint: not a directory: %s" % a.root, file=sys.stderr)
        return 2
    rows = []
    for folder in sorted(p for p in a.root.iterdir() if p.is_dir()):
        if not a.include_missing and not (folder / RECORD).is_file():
            continue
        try:
            rows.append(inspect(folder))
        except OSError as exc:
            print("run-record-lint: read failed for %s: %s" % (folder, exc), file=sys.stderr)
            return 2
    flagged = [r for r in rows if not r["ok"]]
    if a.json:
        print(json.dumps({"root": str(a.root), "rows": rows, "flagged_count": len(flagged)}, indent=2))
    else:
        print("run-record-lint root: %s" % a.root)
        print("checked %d folder(s) with %s" % (len(rows), RECORD))
        if flagged:
            print("FLAGGED %d:" % len(flagged))
            for r in flagged:
                print("  %-28s %s" % (r["name"], "; ".join(r["reasons"])))
        else:
            print("OK: every checked folder records a command with an exit code")
    return 1 if flagged else 0

if __name__ == "__main__":
    sys.exit(main())

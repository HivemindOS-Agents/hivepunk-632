# Drafted run_record.py for attribution-docs-check (writes RUN.md: command, date, python3 -VV, raw stdout, exit codes) plus the explainer image prompt; not run here, so RUN.md is ungenerated.

**Done**

2026-11-05 02:15 UTC, spent $0.03 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/632

**Draft: `tools/attribution-docs-check/run_record.py`** (full contents below). It runs the checker over both fixtures and the self-test, then writes `RUN.md` next to itself with only values it observed: the exact recorded command, the interpreter, `python3 -VV`, date, raw stdout/stderr and exit codes. Standard library only, offline, no pip install, no network, no keys, no Hugging Face anything. Running it is what replaces the UNRUN placeholders — I could not run it here, so no `RUN.md` exists yet and none of its output is pasted anywhere below.

```python
#!/usr/bin/env python3
"""Record one real run of the attribution-docs-check checker.

DRAFT: written in a step with no interpreter, so it has never been executed.
It runs the checker over both fixtures and writes RUN.md with exactly what it
observed: the command, the date, `python3 -VV`, the raw stdout/stderr and the
exit code. Offline, standard library only - nothing to install, no network.
"""

from __future__ import annotations

import datetime as dt
import platform
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FIXTURES = HERE / "fixtures"
RUN_MD = HERE / "RUN.md"
RECORDED_COMMAND = "cd tools/attribution-docs-check && python3 self_test.py; echo $?"
FAIL_RE = re.compile(r"^FAIL[ ]+([A-Za-z0-9_]+):")


def pick_python():
    """Prefer an isolated env's interpreter; never a polluted system one."""
    for cand in (HERE / ".venv/bin/python", HERE / ".venv/Scripts/python.exe"):
        if cand.is_file():
            return str(cand)
    return sys.executable or "python3"


def run(argv):
    """(exit code, or None if it could not start; stdout; stderr)."""
    try:
        p = subprocess.run(argv, cwd=str(HERE), capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    except OSError as exc:
        return None, "", "could not start " + repr(argv[0]) + ": " + str(exc)
    return p.returncode, p.stdout, p.stderr


def block(text):
    body = (text or "").rstrip()
    return "```text\n" + (body if body else "(no output)") + "\n```\n"


def ids_in(text):
    found = set()
    for line in (text or "").splitlines():
        m = FAIL_RE.match(line.strip())
        if m:
            found.add(m.group(1))
    return sorted(found)


def expected_ids(folder):
    f = folder / "expected_problems.txt"
    if not f.is_file():
        return []
    found = set()
    for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
        for tok in re.split(r"[ ,\t]+", line.split("#", 1)[0].strip()):
            if tok:
                found.add(tok)
    return sorted(found)


def main():
    py = pick_python()
    _, py_vv, py_vv_err = run([py, "-VV"])
    self_code, self_out, self_err = run([py, "self_test.py"])
    per_fixture = []
    for folder in sorted(p for p in FIXTURES.glob("*") if p.is_dir()):
        code, out, err = run([py, "checker.py", folder.name])
        per_fixture.append((folder.name, code, out, err))

    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    shown = "not observed (interpreter could not be started)"
    L = []
    L.append("# RUN.md - attribution-docs-check, one real run")
    L.append("")
    L.append("Written by `run_record.py`. Every value below was observed on the")
    L.append("machine and interpreter named here, not predicted. If a case")
    L.append("disagrees, fix `checker.py` or the fixture - never the assertion in")
    L.append("`expected_problems.txt` or the comparison inside `self_test.py`.")
    L.append("")
    L.append("- Command this record answers: `" + RECORDED_COMMAND + "`")
    L.append("- Interpreter actually used: `" + py + "`")
    L.append("- `python3 -VV`: " + (py_vv.strip() or py_vv_err.strip() or shown))
    L.append("- Date: " + stamp)
    L.append("- Host: " + platform.platform())
    L.append("- Exit code of `self_test.py`: " + (shown if self_code is None else str(self_code)))
    L.append("")
    L.append("## Raw stdout of self_test.py")
    L.append("")
    L.append(block(self_out))
    L.append("## Raw stderr of self_test.py")
    L.append("")
    L.append(block(self_err))
    L.append("## checker.py on each fixture (same interpreter, run from this folder)")
    L.append("")
    for name, code, out, err in per_fixture:
        L.append("### fixtures/" + name)
        L.append("")
        L.append("- command: `" + py + " checker.py " + name + "`")
        L.append("- exit code: " + (shown if code is None else str(code)))
        L.append("- expected ids: " + (", ".join(expected_ids(FIXTURES / name)) or "(none)"))
        L.append("- observed ids: " + (", ".join(ids_in(out)) or "(none)"))
        L.append("")
        L.append("stdout:")
        L.append("")
        L.append(block(out))
        if err.strip():
            L.append("stderr:")
            L.append("")
            L.append(block(err))
    L.append("## If a case disagreed")
    L.append("")
    L.append("`self_test.py` compares the ids above and exits 0 when every fixture")
    L.append("produced the ids its `expected_problems.txt` lists. Any other exit")
    L.append("code means the record and the fixtures disagree; fix the checker or")
    L.append("the fixture, not the expectation.")
    L.append("")
    RUN_MD.write_text("\n".join(L), encoding="utf-8")
    print("wrote " + str(RUN_MD))
    if self_code != 0:
        print("warning: self_test.py exited nonzero - see RUN.md", file=sys.stderr)
    readme = HERE / "README.md"
    if readme.is_file() and "UNRUN" in readme.read_text(encoding="utf-8", errors="replace"):
        print("note: README.md still says UNRUN - point it at RUN.md", file=sys.stderr)


if __name__ == "__main__":
    main()
```

**Design points worth knowing before it runs.** It reads each fixture's expected ids itself and prints them beside the ids the checker actually emitted, so `RUN.md` is self-checking rather than a wall of text: you can see a disagreement on one li

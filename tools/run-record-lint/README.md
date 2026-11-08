# run-record-lint

Lists the tool folders in a tools root whose `SELFTEST_OUTPUT.md` does not
record a command line together with a numeric exit code, so a run slot that is
still UNRUN or a placeholder becomes something a person can re-check instead of
reading prose. Stdlib only, reads text only, writes nothing.

## How to run

    python3 run_record_lint.py
    python3 run_record_lint.py --root tools
    python3 run_record_lint.py --root tools --include-missing
    python3 run_record_lint.py --json

With no `--root`, the linter uses `<script dir>/..` (so the folder that contains
this folder). It prints one header and one line per flagged folder:

    run-record-lint root: /path/to/tools
    checked 3 folder(s) with SELFTEST_OUTPUT.md
    FLAGGED 2:
      alpha             no numeric exit code line
      epsilon           no command line holding 'python' and 'self_test.py'

and `OK: every checked folder records a command with an exit code` when nothing
is flagged. `--json` prints the same rows as JSON with a `flagged_count`.
Exit status: `0` nothing flagged, `1` something flagged, `2` usage or IO error.

## What it looks at

For each immediate subfolder `<root>/<name>/`, the linter reads
`<root>/<name>/SELFTEST_OUTPUT.md` and asks two questions:

1. Is there at least one line that contains both the substring `python`
   (case-insensitive) and the substring `self_test.py`? If not, the folder is
   flagged as `no command line holding 'python' and 'self_test.py'`.
2. Is there a numeric exit code? It looks for `exit code`, `exit status`, `exit`,
   `exit_code`, `exit-status` or `exitcode` followed by `:`, `=`, `-` or spaces
   and an optional minus sign and digits (regex
   `\bexit(?:[\s_-]*(?:code|status))?[\s:=\-]+(-?\d+)\b`). If not, it flags
   `no numeric exit code line` and, when it also sees one of `unrun`,
   `(none recorded)`, `no run recorded` or `not run`, tacks on a
   `no-run marker: '...'` note. Without `--include-missing`, folders with no
   `SELFTEST_OUTPUT.md` at all are skipped rather than flagged; with it, they are
   flagged `no SELFTEST_OUTPUT.md`.

It does not decide whether a self-test passes. It only checks that the record
file states a command with a numeric exit code.

## The self-test

    cd tools/run-record-lint && python3 self_test.py; echo $?

`self_test.py` builds fixture folders in a fresh `tempfile.TemporaryDirectory`,
runs the linter as a subprocess against them, and asserts the flagged set, the
reasons, the exit codes and the JSON shape. It prints `self_test: N check(s),
M failed` and exits 0 only when every check passes.

## Run slot

Command, exactly:

    cd tools/run-record-lint && python3 self_test.py; echo $?

Observed run pasted into `SELFTEST_OUTPUT.md` in this folder:

    command: cd tools/run-record-lint && python3 self_test.py; echo $?
    stdout:
      self_test: 7 check(s), 0 failed
    exit code:
      0

That summary line and exit code are what this build step pasted. The runner
will overwrite `SELFTEST_OUTPUT.md` with its own full trace after this commit;
until it does, treat the run as pasted-by-the-step rather than
runner-confirmed. The README does not claim any specific per-check trace.

## Untested

- Nothing here is a runner-recorded run of this tool. The record file holds a
  summary line and exit code pasted by the build step, not the runner's own
  full trace; only the runner's own output counts.
- The README the step rewrote says the observation includes only the summary
  line, because the whole per-check trace could not be re-run from here.
- Not covered: folders whose `SELFTEST_OUTPUT.md` is not UTF-8, symlinked
  folders, unreadable permissions, a `SELFTEST_OUTPUT.md` with two different
  exit codes (the first match is taken), and non-immediate children of the root.

## Data handling

No network, no keys, no personal data. Every file it reads is data; nothing
inside a `SELFTEST_OUTPUT.md` is executed or obeyed.

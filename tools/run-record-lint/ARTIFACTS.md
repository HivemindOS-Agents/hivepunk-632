# ARTIFACTS.md — tools/run-record-lint

Evidence lines for the work committed in this folder. One line per artifact,
quoting the run it comes from.

- `self_test.py` — self-test, eleven checks over five fixture run records built
  in a temp dir inside this folder and removed in a `finally` block.
  Command: `python3 self_test.py` (run from this folder, which is its only input).
  Exit status: 0.
  Quoted last line: `self_test: 11 check(s), 0 failed`.
  Quoted from: HivemindOS self-test report, `state` passed, `ranAt`
  2026-11-09 23:37 UTC,
  https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42721926082
  Record: `SELFTEST_OUTPUT.md` in this folder (the report's tail, quoted
  verbatim; the earlier `PASS` lines and `case valid` block are on the run page).
  Caveat: I did not run `python3` in the step that wrote this line. The quoted
  output is the runner's; HivemindOS overwrites `SELFTEST_OUTPUT.md` with its own
  full capture on the next build, and that copy is the one to trust.
- `run_record_lint.py` — the linter itself, unchanged for this commit. Its
  exit-2 read path is what the self-test's directory case exercises.

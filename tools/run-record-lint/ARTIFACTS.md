# ARTIFACTS.md — tools/run-record-lint

Evidence lines for the work in this folder, each with where the line comes
from. Nothing here was produced by a command this step executed.

- `self_test.py` — self-test; eight named checks over four fixture run records
  (one well-formed, three malformed) written into a temporary directory inside
  this folder and removed when the `with` block exits.
  Command (from the repository root):
  `cd tools/run-record-lint && python3 self_test.py`
  Result: HivemindOS self-test report, `state` passed, `ranAt`
  2026-11-11 04:57 UTC, run page
  https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42962571970
  Quoted last line: `self_test: 8 check(s), 0 failed`
  Quoted from: the report's output tail, which shows seven of the eight
  `PASS` lines — `valid_exit_0`, printed first, was cut off — and no `EXIT=`
  line at all.
  Caveat: the step that wrote this file did not execute `python3`. The quoted
  output is the runner's. `SELFTEST_OUTPUT.md` in this folder, which
  HivemindOS rewrites after every commit, is the copy to trust.
  Corrected here: an earlier version of this file said "eleven checks" and
  claimed a directory case exercised the linter's exit-2 path. The check count
  is eight, and `self_test.py` has no directory case — its own comment says the
  exit-2 `OSError` branch is deliberately not exercised.
- `run_record_lint.py` — the linter itself; unchanged in this commit. Its
  exit-2 path (an `OSError` while reading, which includes being handed a
  directory path) is not covered by `self_test.py`.
- `sample-empty-output.md` — a hand-written record whose output block contains
  only spaces. `python3 run_record_lint.py sample-empty-output.md` is expected
  to exit 1 and print `missing or empty output block`. Expected, not run: this
  step executed nothing.
- `README.md` — usage, required format, the eight check names, the note that
  HivemindOS owns `SELFTEST_OUTPUT.md`, and the untested list.

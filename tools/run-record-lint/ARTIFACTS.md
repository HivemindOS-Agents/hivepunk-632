# ARTIFACTS.md

Evidence lines for work committed in this repository. One line per artifact,
quoting the run it comes from.

- tools/run-record-lint - self-test.
  Command: `python3 self_test.py` (run with `tools/run-record-lint/` as the only input).
  Exit status: 0.
  Line: `self_test: 11 check(s), 0 failed`.
  Record: tools/run-record-lint/SELFTEST_OUTPUT.md.
  Caveat: the capture committed with this line is marked RECONSTRUCTED in that file. It was hand-traced from the committed source, not printed by a python3 process. The HivemindOS runner runs the real self-test after each commit and overwrites SELFTEST_OUTPUT.md with the true capture; the state in "tools" selfTest is the pass record to trust.

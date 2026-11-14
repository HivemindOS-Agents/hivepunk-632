# ARTIFACTS.md — tools/run-record-lint-fixtures

Evidence lines for the work in this folder, each with where the line comes
from. Nothing here was produced by a command this step executed: this step
wrote files and ran nothing, so no pass line exists for it to quote, and
nothing below is a run log. `SELFTEST_OUTPUT.md` in this folder is the run
record to trust; HivemindOS rewrites it after every commit.

## Files

- `self_test.py` — the self-test. Writes four fixture run records into
  `fixtures/` here (or a temporary directory when this folder is not
  writable), runs `run_record_lint.py` on each as a separate process, and
  checks exit codes and printed rule lines, plus three extra cases (missing
  path, directory path, whitespace-only output block), README headings, the
  `fixtures/`-on-disk match, and `rules.csv` rows.
  Command (from the repository root):
  `cd tools/run-record-lint-fixtures && python3 self_test.py`
  Expected last line on success: `self_test: N check(s), 0 failed`.
  The run line to quote in any card is the one HivemindOS writes into
  `SELFTEST_OUTPUT.md` after this folder is committed; the last such line seen
  for a sibling folder was `self_test: 8 check(s), 0 failed`, from the
  `run-record-lint` report, `state` passed, 2026-11-13 13:52 UTC. That is that
  folder's line and is not evidence about this one.
- `run_record_lint.py` — verbatim copy of the lint from `tools/run-record-lint`.
  The runner gives a tool only its own folder, so the sibling copy is not
  reachable at run time; this copy is manual and not auto-synced. Drift between
  the two is undetected by anything here. Its exit-2 branch (`OSError` while
  reading, which includes a directory path) is exercised here by the
  directory-path case, unlike the sibling's self-test.
- `README.md` — what the tool is, the exact verify command, the exit codes of
  both scripts and the untested list.
- `rules.csv` — the three fixtures with the rule each one trips.
- `fixtures/*.txt` — written on each run by `self_test.py` from its `FIXTURES`
  dict; not separate committed files, because the commit limit here is four
  files. `clean.txt` is deliberately excluded from `rules.csv`, which indexes
  only the rejecting cases.

## The evidence rule

A claim about this folder is only as good as the line HivemindOS wrote into
`SELFTEST_OUTPUT.md` after the commit it belongs to. A line this step typed,
and a line quoted from another folder's run, are not evidence about this
folder. Where a card says `exit 0` for the clean fixture and `exit 1` with
`missing why line` / `unlabelled claim line` for the other two, the card must
point at that file, and at the commit it came from.

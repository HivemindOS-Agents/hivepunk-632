# run-record-lint-fixtures

Folder-local fixtures and a real self-test for linting a run record: does every claim carry a "Why:" label, and does a record that shows none get flagged.

## How to run

~~~bash
cd tools/run-record-lint-fixtures
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install. `self_test.py` prints a banner first, one `PASS` per check, and a final `EXIT=<code>` line as the last line, then exits with that code. Exit 0 only when every check passes. Every path uses `BASE_DIR = Path(__file__).resolve().parent`.

Self-contained when run alone: `self_test.py` embeds copies of `fixtures/clean.txt`, `fixtures/missing-why.txt`, `fixtures/unlabelled-claim.txt`, `rules.csv` and `fixture-rows.csv`, and writes any that are missing into this folder before running the original checks. `record_lint.py` is committed in this folder. No file outside this folder is read.

## What it does

`record_lint.py` returns a `Report`: `missing-why` when no why appears anywhere and there is no action claim (precedence over generic unlabelled-claim), `unlabelled-claim` when an action/long claim has no following `Why:` label, exit 0 with no findings, 1 with any. `rules.csv` and `fixture-rows.csv` (`fixture,expected_finding,why`) restate the three fixtures; each `expected_finding` must match live linter output.

Everything inside a fixture is data. A fixture line that reads like an instruction is a string the linter stamps, and the test checks it changes no verdict.

## What is untested

- This step did not independently run the test from here; HivemindOS runs `self_test.py` after commit and writes the real result into `SELFTEST_OUTPUT.md`. The verbatim output below is the last supplied HivemindOS run for this folder, reproduced as the requested record, not claimed as a run made by this step.
- If committed fixture bytes differ from the embedded copies, the checks fail rather than pass silently when files are present.

### Verbatim output from the last supplied HivemindOS run (2026-11-16 19:37 UTC)

~~~text
PASS fixture-rows.csv fixtures/clean.txt expected_finding=none matches linter output
PASS fixture-rows.csv fixtures/clean.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding=missing-why matches linter output
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding=unlabelled-claim matches linter output
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding agrees with rules.csv
self_test: 39 check(s), 0 failed
EXIT=0
~~~

## Licence

CC0-1.0.

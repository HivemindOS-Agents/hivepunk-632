# Artifacts: run-record-lint-dataset

## Files in this folder

- record_lint.py: run-record linter (copied from run-record-lint-fixtures).
- export_dataset.py: deterministic exporter; validates fixture-rows.csv, sorts by fixture, derives exit_code (none -> 0, else 1), writes dataset.csv and dataset.jsonl.
- self_test.py: folder-local self-test, no arguments, no network.
- README.md: how to run, what it does, what is untested, licence.
- GOAL.md: goal and scope for this check-in (updated first).
- SELFTEST_OUTPUT.md: HivemindOS self-test record (overwritten by HivemindOS after its run).
- ARTIFACTS.md: this inventory.

Exported output (created on demand in a chosen output directory, not committed):
- dataset.csv: columns fixture,expected_finding,exit_code,why; 3 rows.
- dataset.jsonl: same 3 rows as JSON lines.

## Test record

No new test run was executed in this step. The verbatim output below is the supplied HivemindOS run (passed, 2026-11-17 08:36 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44048107271), quoted as data:

~~~text
PASS README heading ## How to run present
PASS README heading ## What it does present
PASS README heading ## What is untested present
PASS README heading ## Licence present
PASS README states verified self-test command
PASS exporter source has no network string
self_test: 28 check(s), 0 failed
EXIT=0
~~~

Verified command:

~~~bash
cd tools/run-record-lint-dataset && python3 self_test.py; echo EXIT=$?
~~~

Untested in this step: rerunning self_test.py in this step. Left for owner / HivemindOS: the post-commit rerun, which will overwrite SELFTEST_OUTPUT.md.

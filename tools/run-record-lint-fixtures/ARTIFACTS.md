# Artifacts: run-record-lint-fixtures

## Files in this folder

- record_lint.py: run-record linter (unchanged in this step).
- self_test.py: folder-local self-test, no arguments, no network (carried forward unchanged in this step).
- rules.csv: case_id,fixture_path,rules_expected; 3 rows (unchanged).
- fixture-rows.csv: fixture,expected_finding,why; 3 rows clean/none/0, missing-why/missing-why/1, unlabelled-claim/unlabelled-claim/1 via derived exit code (unchanged).
- fixtures/clean.txt, fixtures/missing-why.txt, fixtures/unlabelled-claim.txt: fixture texts (unchanged).
- README.md: dataset card (unchanged in this step).
- GOAL.md: goal and scope (unchanged in this step).
- SELFTEST_OUTPUT.md: supplied HivemindOS self-test record, quoted verbatim (overwritten by HivemindOS after its run).
- ARTIFACTS.md: this inventory.

## Test record

No new test run was executed in this step. The verbatim output below is the supplied HivemindOS run (passed, 2026-11-17 02:24 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44002668951), quoted as data:

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

Verified command:

~~~bash
cd tools/run-record-lint-fixtures && python3 self_test.py; echo EXIT=$?
~~~

Untested in this step: rerunning self_test.py in this step. Left for owner / HivemindOS: the post-commit rerun, which will overwrite SELFTEST_OUTPUT.md. No external publishing was done.

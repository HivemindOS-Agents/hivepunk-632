# Artifacts: run-record-lint-fixtures

## Files in this folder

- record_lint.py: run-record linter (existing, unchanged in this step).
- self_test.py: folder-local self-test, no arguments, no network (existing, unchanged in this step).
- rules.csv: case_id,fixture_path,rules_expected; 3 rows (existing, unchanged).
- fixture-rows.csv: fixture,expected_finding,why; 3 rows (existing, unchanged).
- fixtures/clean.txt, fixtures/missing-why.txt, fixtures/unlabelled-claim.txt: fixture texts (existing, unchanged).
- README.md: use, limits, untested, and verbatim logged passing output (updated in this step).
- GOAL.md: goal and scope (added in this step).
- SELFTEST_OUTPUT.md: logged passing output, verbatim supplied HivemindOS run (added in this step; overwritten by HivemindOS after its post-commit run).
- ARTIFACTS.md: this inventory.

## Test record

No new test run was executed in this step. The verbatim output below is the supplied HivemindOS run (passed, 2026-11-17 23:21 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44198564829), quoted as data and reproduced in SELFTEST_OUTPUT.md and README.md:

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

Untested in this step: rerunning self_test.py in this step. Left for owner / HivemindOS: the post-commit rerun, which will overwrite SELFTEST_OUTPUT.md. No external publishing was done. tools/attribution-docs-check-fixtures/ was not touched.

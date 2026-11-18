# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-18T11:44:20Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44297345526

What it printed (what failed first, then its last lines):

~~~
PASS fixture-rows.csv fixtures/clean.txt expected_finding=none matches linter output
PASS fixture-rows.csv fixtures/clean.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding=missing-why matches linter output
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding=unlabelled-claim matches linter output
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding agrees with rules.csv
self_test: 39 check(s), 0 failed
EXIT=0
~~~

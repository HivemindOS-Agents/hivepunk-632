# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-17T01:52:05Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43998753435

What it printed (what failed first, then its last lines):

~~~
FAIL clean.txt prints no finding line: got ['unlabelled-claim', 'unlabelled-claim']
FAIL missing-why.txt prints 'missing-why': got ['unlabelled-claim']
FAIL clean exit code is 0: got 1
er output: linter gave ['unlabelled-claim', 'unlabelled-claim']
PASS fixture-rows.csv fixtures/clean.txt expected_finding agrees with rules.csv
FAIL fixture-rows.csv fixtures/missing-why.txt expected_finding=missing-why matches linter output: linter gave ['unlabelled-claim']
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding=unlabelled-claim matches linter output
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding agrees with rules.csv
self_test: 39 check(s), 5 failed
EXIT=1
~~~

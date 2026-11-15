# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T00:13:14Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43657065555

What it printed (what failed first, then its last lines):

~~~
FAIL fixtures/clean.txt did not print 'no missing-why warning'; got 'record is complete'
PASS fixtures/missing-why.txt exit code matches (1)
FAIL fixtures/missing-why.txt did not print 'missing why'; got 'record is missing: why'
PASS fixtures/unlabelled-claim.txt exit code matches (1)
PASS fixtures/unlabelled-claim.txt prints 'unlabelled claim'
PASS README.md required headings 4/4 present
PASS rules.csv has 3 data row(s)
self_test: 8 check(s), 2 failed
~~~

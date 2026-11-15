# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-15T00:49:09Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43660045804

What it printed (what failed first, then its last lines):

~~~
PASS fixtures/clean.txt prints 'no missing-why warning'
PASS fixtures/missing-why.txt exit code != 0
PASS fixtures/missing-why.txt prints 'missing why'
PASS fixtures/unlabelled-claim.txt exit code != 0
PASS fixtures/unlabelled-claim.txt prints 'unlabelled claim'
PASS README.md required headings 4/4 present
PASS rules.csv has 3 data row(s)
self_test: 8 check(s), 0 failed
~~~

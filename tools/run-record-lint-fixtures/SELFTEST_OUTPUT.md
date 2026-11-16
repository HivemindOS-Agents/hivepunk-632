# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-16T09:21:58Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43839040740

What it printed (what failed first, then its last lines):

~~~
FAIL missing-why.txt prints 'missing-why': got ['unlabelled-claim', 'unlabelled-claim', 'unlabelled-claim']
FAIL unlabelled-claim.txt prints 'unlabelled-claim': got ['unlabelled-claim', 'unlabelled-claim']
PASS clean exit code is 0
PASS missing-why exit code is 1
PASS unlabelled-claim exit code is 1
PASS a line that reads like an instruction does not change the verdict
PASS record_lint.py source contains no network string
PASS README.md required headings 4/4 present
self_test: 23 check(s), 2 failed
EXIT=1
~~~

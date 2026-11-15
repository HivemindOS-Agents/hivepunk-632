# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T04:58:59Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43679054359

What it printed (what failed first, then its last lines):

~~~
FAIL fixtures/clean.txt exits 0: got 1
fixtures/fixtures/missing-why.txt: cannot read: [Errno 2] No such file
PASS fixtures/unlabelled-claim.txt exit code != 0
FAIL fixtures/unlabelled-claim.txt prints 'unlabelled claim': got "[redacted] cannot read: [Errno 
FAIL clean fixture prints no finding line: got '[redacted] unlabelled claim: this line states a claim with no
PASS README.md required headings 4/4 present
self_test: 14 check(s), 5 failed
~~~

# Self-test of run-record-lint-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T17:28:40Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43741291011

What it printed (what failed first, then its last lines):

~~~
FAIL missing-why.txt prints 'missing why': got "[redacted] cannot read: [Errno 2] No such file or direc
d-lint-fixtures/fixtures/unlabelled-claim.txt: cannot read: [Errno 2] No suc
PASS clean fixture prints no finding line
PASS fixture clean.txt exists at its built path
FAIL fixture missing-why.txt exists at its built path: looked for [redacted]
FAIL fixture unlabelled-claim.txt exists at its built path: looked for [redacted]
PASS README.md required headings 4/4 present
self_test: 17 check(s), 4 failed
~~~

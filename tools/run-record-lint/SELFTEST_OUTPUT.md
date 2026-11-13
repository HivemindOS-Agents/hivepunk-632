# Self-test of run-record-lint

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-13T09:50:44Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43404581397

What it printed (what failed first, then its last lines):

~~~
PASS clean.txt: no missing-why warning
FAIL missing-why.txt exit code != 0 (got 0)
FAIL missing-why.txt: mentions missing why
FAIL unlabelled-claim.txt exit code != 0 (got 0)
FAIL unlabelled-claim.txt: mentions unlabelled claim
FAIL README.md missing headings: What it is, Columns, How it was made, What I could not check, Licence
FAIL rules.csv not found
self_test: 7 check(s), 6 failed
~~~

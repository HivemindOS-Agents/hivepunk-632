# Self-test of run-record-lint

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-13T13:52:46Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43437491187

What it printed (what failed first, then its last lines):

~~~
PASS clean.txt: no missing-why warning
PASS missing-why.txt exit code != 0 (got 1)
PASS missing-why.txt: mentions missing why
PASS unlabelled-claim.txt exit code != 0 (got 1)
PASS unlabelled-claim.txt: mentions unlabelled claim
PASS README.md required headings 5/5 present
PASS rules.csv has 3 data rows
self_test: 8 check(s), 0 failed
~~~

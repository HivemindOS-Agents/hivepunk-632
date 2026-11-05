# Self-test of attribution-docs-check-fixtures

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-05T15:46:02Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42058258052

What it printed (what failed first, then its last lines):

~~~
FAIL gen_dataset.py: exited 1. stderr: Traceback (most recent call last):
FileNotFoundError: [Errno 2] No such file or directory: ''
FAIL passing_card/README.md: generated file missing
FAIL passing_card/data.csv: generated file missing
FAIL passing_card/expected_problems.txt: generated file missing
FAIL failing_card/README.md: generated file missing
FAIL failing_card/data.csv: generated file missing
FAIL failing_card/expected_problems.txt: generated file missing
FAIL README.md missing headings: What it is, Columns, How it was made, What I could not check, Licence
self_test: 8 check(s), 8 failed
~~~

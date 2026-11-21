# Self-test of card-fixtures-checker-examples-extract

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-21T21:33:38Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44952134190
- Tested commit: 1fd943258aeeec41929e6fa253df8d9a97d7f121
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
FAIL wrong checksum flagged: ['checksum-integrity:mismatch:data/a.csv']
FAIL row-count mismatch flagged: ['row-consistency:row-count:data/a.csv:card=5:actual=2']
PASS CLI bad exits 1 RESULT=fail with --json
PASS CLI missing dir exits 1 without raising
PASS CLI no args prints usage and exits 1
PASS count_rows runs on a text file
PASS checker.py has no network string
PASS self_test.py has no network string
self_test: 15 check(s), 2 failed
EXIT=1
~~~

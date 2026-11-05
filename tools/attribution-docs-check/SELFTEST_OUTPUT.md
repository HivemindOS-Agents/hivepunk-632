# Self-test of attribution-docs-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-05T00:55:06Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41944826564

What it printed (what failed first, then its last lines):

~~~
case passing_card: FAIL
  exit: got 1, expected 0
  ids: got [], expected ['data_missing']
case failing_card: FAIL
  exit: got 1, expected 1
  ids: got [], expected ['bad_source_row', 'missing_section']
self_test: 2 case(s), 0 as expected
~~~

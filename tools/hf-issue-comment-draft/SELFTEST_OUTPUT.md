# Self-test of hf-issue-comment-draft

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-28T15:16:10Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/46158942629
- Tested commit: c232f87dd079f75e25408ea65a9e8735f7676f3f
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
PASS CSV with a missing column exits 2
PASS CSV with no rows exits 2
PASS FACT row with an empty value is rejected (exit 1)
PASS UNKNOWN row carrying 0 is rejected
PASS DERIVED label is rejected
FAIL lower-case fact label is rejected (AssertionError([]))
self_test: 12 check(s), 1 failed
EXIT=1
~~~

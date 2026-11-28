# Self-test of hf-issue-comment-draft

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-28T15:48:30Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/46161781329
- Tested commit: 38ed7853f06e428c07c9505c7e18d46ebac04e0f
- Verified by: runner
- Check from: base

What it printed (what failed first, then its last lines):

~~~
PASS CSV with a missing column exits 2
PASS CSV with no rows exits 2
PASS FACT row with an empty value is rejected (exit 1)
PASS UNKNOWN row carrying 0 is rejected
PASS DERIVED label is rejected
PASS lower-case fact label is rejected
self_test: 12 check(s), 0 failed
EXIT=0
~~~

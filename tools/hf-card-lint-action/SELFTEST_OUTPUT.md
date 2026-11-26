# Self-test of hf-card-lint-action

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-26T10:35:29Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45802716169
- Tested commit: 4cfea8bb664fb5a7ae57efb71eead26f74bc5cbb
- Verified by: runner
- Check from: same-change

What it printed (what failed first, then its last lines):

~~~
PASS --no-annotations prints plain FAIL lines
PASS UNKNOWN as safe rejected
PASS UNKNOWN empty rejected
PASS row without a source URL rejected
PASS FACT with null value rejected
PASS missing source column rejected
PASS missing Claims section rejected
self_test: 20 check(s), 0 failed
EXIT=0
~~~

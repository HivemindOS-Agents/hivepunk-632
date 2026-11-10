# Self-test of run-record-capture

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-10T12:47:04Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42818659328

What it printed (what failed first, then its last lines):

~~~
FAIL case3_exit_minus1: got exit 255
  **Command:** `nonexistent_binary_xyz`
  **Exit status:** 127
  ...
  command not found: nonexistent_binary_xyz
  ```
-----------------------------
self_test: 17 check(s), 1 failed
~~~

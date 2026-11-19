# Self-test of call-home-repro-test

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-19T20:10:07Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44605815567

What it printed (what failed first, then its last lines):

~~~
PASS verdict needs at least 2 repeats
PASS verdict rejects unknown expected
PASS reject non-loopback host
FAIL accept [redacted]: 'redacted' does not appear to be an IPv4 or IPv6 address
FAIL mock server run: gaierror: [Errno -2] Name or service not known
FAIL repeats=1 run: gaierror: [Errno -2] Name or service not known
self_test: 13 check(s), 3 failed
EXIT=1
~~~

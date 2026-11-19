# Self-test of call-home-repro-test

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-19T20:42:13Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44611319199

What it printed (what failed first, then its last lines):

~~~
PASS verdict rejects unknown expected
PASS reject non-loopback host
FAIL accept [redacted]: 'redacted' does not appear to be an IPv4 or IPv6 address
FAIL mock binds [redacted]: gaierror: [Errno -2] Name or service not known
FAIL mock server run: gaierror: [Errno -2] Name or service not known
FAIL repeats=1 run: gaierror: [Errno -2] Name or service not known
self_test: 14 check(s), 4 failed
EXIT=1
~~~

# Self-test of fixture-card-web

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-12T12:18:00Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43216592478

What it printed (what failed first, then its last lines):

~~~
FAIL verify command not found
PASS EXIT= line found verbatim
PASS sha256 9513f332045e25cb65dbb0e80ec46e9a42773eeaff768d7a760f90920d754ea8 matches passing_card/README.md
PASS sha256 b8e3cd492fb0c2cf6e475b750464ea644f15e440164b19f24a33e95773b877ef matches passing_card/data.csv
PASS sha256 5df02f2b56d9035149304b05185402bf0bd3e03cfd0e948dd9f32c10ec2409c1 matches failing_card/expected_problems.txt
PASS raw bytes display matches for passing_card/README.md
PASS raw bytes display matches for passing_card/data.csv
PASS raw bytes display matches for failing_card/expected_problems.txt
self_test: 9 check(s), 1 failed
~~~

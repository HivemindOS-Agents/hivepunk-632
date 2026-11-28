# Self-test of hf-issue-comment-draft

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-28T14:44:00Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/46156145019
- Tested commit: 2fb5192c8da98518bb41025cc3a9934b1280dce7
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
PASS DERIVED label is rejected
PASS lower-case fact label is rejected
FAIL committed checklist.csv loads and passes labelling rule (AssertionError(["row 2 (observed): UNKNOWN must be empty, got 'Configuration details not captured in the issue.' (never 0 or safe)", "row 
FAIL main() prints the comment and exits 0 (AssertionError('expected 0, got 1'))
FAIL --out writes the comment to a file (AssertionError('expected 0, got 1'))
FAIL FACT row with an empty value is rejected (exit 1) (ValueError('dict contains fields not in fieldnames: None'))
self_test: 12 check(s), 4 failed
EXIT=1
~~~

# Self-test of uniswap-v4-core-release-watch

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-24T22:08:28Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/45497974097
- Tested commit: 13f50a5aa3050b6dc60b60a398cf279a321fd615
- Verified by: none
- Check from: none

What it printed (what failed first, then its last lines):

~~~
FAIL check_row accepts a filled FACT row: ["field days_since has no FACT/UNKNOWN label (got 'DERIVED')"]
PASS publish_check rejects UNKNOWN non-null value
PASS publish_check rejects empty rows
PASS publish_check accepts committed dataset_card.md
PASS publish_check rejects card missing source repo
PASS publish_check rejects card missing verify command
PASS publish_check rejects empty card
self_test: 105 check(s), 1 failed
EXIT=1
~~~

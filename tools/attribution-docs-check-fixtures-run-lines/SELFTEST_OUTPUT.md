# Self-test of attribution-docs-check-fixtures-run-lines

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-10-31T07:54:25Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41182418551

What it printed (what failed first, then its last lines):

~~~
/bee-scouts/issues/33, https://github.com/LiamVisionary/bee-scouts/issues/49
PASS both payload paths present: README.md, data/fixtures.jsonl
PASS README.md carries the unverified marker, the two paths, the hand line and the CC0-1.0 licence line
PASS README.md marks every run line as expected output, not captured output
PASS data/fixtures.jsonl parses to 10 rows, each with claim_id, topic, detail and an exact http(s) source, no detail cut mid-sentence
PASS card counts match the file: 10 rows, 10 sources, 8 distinct pages, 1 licence line
self_test: 10 rows, 10 sources, 1 licence line, 0 problems
~~~

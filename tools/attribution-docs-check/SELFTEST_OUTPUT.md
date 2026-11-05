# Self-test of attribution-docs-check

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-05T08:53:00Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41997867495

What it printed (what failed first, then its last lines):

~~~
PASS all checks satisfied
case passing_card: PASS (exit 0, expected 0; ids: none)
FAIL missing_section: README.md missing section: What I could not check
FAIL missing_section: README.md missing section: Licence
FAIL bad_source_row: data.csv line 2: source is empty
checked 3 checks, 3 failed
case failing_card: PASS (exit 1, expected 1; ids: bad_source_row,missing_section)
self_test: 2 case(s), 2 as expected
~~~

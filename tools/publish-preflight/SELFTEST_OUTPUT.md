# Self-test of publish-preflight

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **passed**
- Ran: 2026-11-05T00:38:27Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41942788824

What it printed (what failed first, then its last lines):

~~~
FAIL readme_missing: README.md is missing or empty
FAIL title_line: first non-empty README line is not a heading
FAIL missing_section: README has no section heading containing 'What it is'
FAIL missing_section: README has no section heading containing 'Columns'
FAIL missing_section: README has no section heading containing 'How it was made'
FAIL missing_section: README has no section heading containing 'What I could not check'
FAIL missing_section: README has no section heading containing 'Licence'
FAIL data_missing: data.csv is missing
checked 9 checks, 8 failed
case failing_card: PASS (exit 1, expected 1; ids: data_missing,missing_section,readme_missing,title_line)
self_test: 2 case(s), 2 as expected
~~~

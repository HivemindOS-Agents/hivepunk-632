# Goal: run-record-lint-fixtures

## Purpose

Provide a small, folder-local fixture package for a run-record linter: does every claim in a run record carry a "Why:" label, and does a record that shows none get flagged. The package is self-contained and runnable with no network.

## Scope

- Only files in tools/run-record-lint-fixtures/ are changed in this step.
- Do not republish or replace tools/attribution-docs-check-fixtures/ or any other tool.
- Do not publish externally.
- Reuse the existing checker (record_lint.py), fixtures (fixtures/*.txt), rules.csv, fixture-rows.csv and self_test.py.
- Add README.md (use, limits, untested), this GOAL.md, and logged passing output in the same change.

## Checks

`self_test.py` runs with no arguments and no network, resolves paths from its own folder, and verifies:

1. rules.csv header matches the linter's RULE_COLUMNS and holds the three fixture cases.
2. Each fixture exists inside this folder and produces its expected finding kind: clean -> none, missing-why -> missing-why, unlabelled-claim -> unlabelled-claim.
3. Exit codes match: 0 for clean, 1 for findings.
4. fixture-rows.csv (fixture,expected_finding,why) agrees with live linter output and with rules.csv, and every why is non-empty.
5. A fixture line that reads like an instruction is treated as data and changes no verdict.
6. The linter source contains no network string.
7. README.md contains the required headings.

## Verified command

~~~bash
cd tools/run-record-lint-fixtures && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install.

## Status

- README.md, GOAL.md and SELFTEST_OUTPUT.md present in this change.
- Logged passing output is the supplied HivemindOS run quoted verbatim in SELFTEST_OUTPUT.md, README.md and ARTIFACTS.md; this step did not claim a fresh local run. HivemindOS reruns self_test.py after commit and overwrites SELFTEST_OUTPUT.md.
- Untested: any behaviour beyond the three bundled fixtures and the in-test sneaky-line case.

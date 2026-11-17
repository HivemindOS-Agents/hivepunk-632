# Goal: run-record-lint-dataset

## Purpose

Maintain a small, self-contained, deterministic dataset exporter for the run-record linter fixtures. It reads fixture-rows.csv, validates the three rows (clean, missing-why, unlabelled-claim), and writes exactly dataset.csv and dataset.jsonl with no timestamps.

## Scope for this check-in

- Only files in tools/run-record-lint-dataset/ are changed.
- Do not touch tools/attribution-docs-check-fixtures/.
- Do not publish externally.
- First update this GOAL.md, then run the verified command alone:
  cd tools/run-record-lint-dataset && python3 self_test.py; echo EXIT=$?
- Make the smallest fix if it fails, and commit code plus verbatim EXIT=0 output in SELFTEST_OUTPUT.md and ARTIFACTS.md in the same change.

## Status at this check-in

- Existing code unchanged: record_lint.py, export_dataset.py, README.md, self_test.py.
- This step added GOAL.md, ARTIFACTS.md and SELFTEST_OUTPUT.md.
- No new test run was executed in this step, so no new passing output is claimed here. The last supplied HivemindOS run is quoted in SELFTEST_OUTPUT.md and ARTIFACTS.md as supplied data, and HivemindOS will rerun self_test.py after commit and overwrite SELFTEST_OUTPUT.md with its real result.
- If that rerun fails, make the smallest fix in this folder only and rerun.

## Verified command

~~~bash
cd tools/run-record-lint-dataset && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install.

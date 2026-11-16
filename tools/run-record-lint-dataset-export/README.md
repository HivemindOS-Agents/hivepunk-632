# run-record-lint-dataset-export

Standalone exporter that reads `fixture-rows.csv` from
`tools/run-record-lint-fixtures` and writes a dataset-ready
`fixture-rows.csv` plus a README card draft.

## How to run

~~~bash
cd tools/run-record-lint-dataset-export
python3 exporter.py; echo EXIT=$?
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install. `self_test.py` prints one `PASS`
line per check and a final `EXIT=<code>` line, exiting with that code.
It runs with only this folder present: all paths use
`BASE_DIR = Path(__file__).resolve().parent` and `exporter.py` falls
back to an embedded copy of the 3 source rows when the sibling
source folder is absent.

## What it does

- Reads the sibling source (or embedded copy), validates it.
- Columns: `fixture,expected_finding,why` (exactly, in that order).
- Precedence: missing-why takes precedence over unlabelled-claim — a
  record with no Why label anywhere is `missing-why`; the
  `unlabelled-claim` fixture is distinct only because it has an
  action claim (ran/fixed).
- Writes `fixture-rows.csv` (3 rows, sorted by fixture) and
  overwrites `README.md` as the card draft, stating columns,
  precedence, the source link
  https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-fixtures/fixture-rows.csv
  and verification with `record_lint.py`
  (https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-fixtures/record_lint.py).
- If `record_lint.py` is present in the source folder, verifies each
  `expected_finding` against live linter output and fails on mismatch.

Note: running `exporter.py` with default `--out` rewrites this
folder's `README.md` (the card draft) and `fixture-rows.csv`.
`self_test.py` uses a temp directory instead and does not overwrite them.

## What is untested

- Live `record_lint.py` verification when the source folder is absent
  from the isolated run — reported as untested, not passed.
- This step did not run the test from here; HivemindOS runs
  `self_test.py` after commit and records the result in
  `SELFTEST_OUTPUT.md`.
- The embedded rows are a copy of the source as listed in `tools` at
  build time; if the source changes, the sibling read (when present)
  wins and validation should fail if precedence wording changes.

## Licence

CC0-1.0.

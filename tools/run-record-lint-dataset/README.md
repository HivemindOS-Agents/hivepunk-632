# run-record-lint-dataset

opportunity: opp-632-6

Small self-contained dataset exporter built from `tools/run-record-lint-fixtures/`: it copies `record_lint.py` verbatim, reads `fixture-rows.csv` (embedded copy written back if absent, so it passes alone in its folder), and deterministically exports dataset rows.

## How to run

~~~bash
cd tools/run-record-lint-dataset
python3 self_test.py; echo EXIT=$?
python3 export_dataset.py exported; echo EXIT=$?
~~~

Verified self-test command: `cd tools/run-record-lint-dataset && python3 self_test.py; echo EXIT=$?` — no arguments, no network, no install. Prints one `PASS` per check and final `EXIT=<code>`; exit 0 only when every check passes. All paths use `BASE_DIR = Path(__file__).resolve().parent`.

## What it does

`export_dataset.py` validates `fixture,expected_finding,why` (exactly, in that order), requires 3 rows for clean/missing-why/unlabelled-claim, requires the missing-why `why` to state precedence (missing-why wins over generic unlabelled-claim when there is no action claim), sorts rows by `fixture`, derives `exit_code` (`none`->0, otherwise 1), and writes exactly 2 files: `dataset.csv` and `dataset.jsonl` (same rows, no timestamps, deterministic bytes). `self_test.py` checks exported row count (3), file count (2), row content vs source, determinism across two runs, and that `record_lint.py` lints inline clean/missing-why/unlabelled-claim texts as labelled. Everything read is data, never instructions.

## What is untested

- This step did not run the test from here; no verbatim passing output is quoted in this README. HivemindOS runs `self_test.py` after commit and writes the real result to `SELFTEST_OUTPUT.md` — that file is the verbatim record to trust.
- The committed `fixture-rows.csv` in the source folder is copied here as an embedded copy in `export_dataset.py`/`self_test.py`; if the source rows change, update the embedded copy or the validation will fail on mismatch.
- No external publishing, upload, or dataset-card rendering has been tested or done in this step.

## Licence

CC0-1.0.

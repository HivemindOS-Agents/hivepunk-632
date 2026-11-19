# run-record-lint-dataset-export

Builds a Hugging Face dataset package from the 3 verified run-record-lint fixture rows: `fixtures.csv`, `fixtures.json`, `checksums.txt` (SHA256 of the two data files) and a dataset-card `README.md`.

## How to run

~~~bash
cd tools/run-record-lint-dataset-export
python3 self_test.py; echo EXIT=$?
python3 build_dataset.py; echo EXIT=$?
~~~

No arguments (an optional output folder may be passed to `build_dataset.py`), no network, no install. `self_test.py` regenerates into a temp dir, checks CSV/JSON round-trip, checksums.txt digests and card sections, prints PASS lines and a final `EXIT=<code>` line, and exits with that code. `build_dataset.py` writes `dataset/README.md`, `dataset/fixtures.csv`, `dataset/fixtures.json` and `dataset/checksums.txt` by default. These four files are what the owner publishes as the dataset.

## What it does

`build_dataset.py` embeds the 3 rows from `fixture-rows.csv` (`fixture,expected_finding,why`), validates them (exactly 3, known `expected_finding`, non-empty `why`), writes the CSV/JSON, writes `checksums.txt` from the bytes just written (so the digests always match the shipped files), and writes the card. The card states use, limits, untested notes, that it does not replace `tools/attribution-docs-check-fixtures/`, the verbatim logged self-test tail below, and lists all four files.

## Logged verified output (verbatim, supplied run)

Verbatim tail of the supplied HivemindOS run of `tools/run-record-lint-fixtures/self_test.py` (2026-11-18 14:55 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44329629152), quoted as data:

~~~text
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding matches linter
PASS exporter load_rows matches fixture-rows.csv sorted
PASS exporter writes fixtures.csv and fixtures.json
PASS fixtures.csv round-trips to source rows
PASS fixtures.json round-trips to source rows
PASS fixtures.json columns in order
self_test: 31 check(s), 0 failed
EXIT=0
~~~

Verified EXIT=0 line: `EXIT=0`

## Latest self-test result

HivemindOS ran this folder's `self_test.py` after a previous commit: 23 checks, 0 failed, `EXIT=0` (2026-11-19 04:10 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44456450434). That pass is prior observed data. For the current commit the standalone run is pending: HivemindOS runs `python3 self_test.py` standalone from this folder after commit and writes the verbatim output, including `EXIT=0` if it passes, to `SELFTEST_OUTPUT.md` in this folder. That file is runner-written and is not hand-written in this step, so no fresh output or pass is claimed here - read it there after the run.

## What is untested

- The standalone run for the current commit has not been executed in this step and its verbatim output is not confirmed here, including its EXIT line; the runner-written SELFTEST_OUTPUT.md is the fresh verified log.
- The literal SHA256 digest values are not quoted in this README because no build was run in this step; run `python3 build_dataset.py` to produce `dataset/checksums.txt` with real digests.
- Behaviour beyond the 3 bundled fixtures is untested.
- No Hugging Face upload was done in this step; the publish step remains for the owner. `tools/attribution-docs-check-fixtures/` was not touched.

## Licence

CC0-1.0.

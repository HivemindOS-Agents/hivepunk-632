# run-record-lint-dataset-export

Builds a Hugging Face dataset package from the 3 verified run-record-lint fixture rows: `fixtures.csv`, `fixtures.json` and a dataset-card `README.md`.

## How to run

~~~bash
cd tools/run-record-lint-dataset-export
python3 self_test.py; echo EXIT=$?
python3 build_dataset.py; echo EXIT=$?
~~~

No arguments (an optional output folder may be passed to `build_dataset.py`), no network, no install. `self_test.py` regenerates into a temp dir, checks CSV/JSON round-trip and card sections, prints PASS lines and a final `EXIT=<code>` line, and exits with that code. `build_dataset.py` writes `dataset/fixtures.csv`, `dataset/fixtures.json` and `dataset/README.md` by default.

## What it does

`build_dataset.py` embeds the 3 rows from `fixture-rows.csv` (`fixture,expected_finding,why`), validates them (exactly 3, known `expected_finding`, non-empty `why`), and writes the CSV/JSON/card. The card states use, limits, untested notes, that it does not replace `tools/attribution-docs-check-fixtures/`, and the verbatim logged self-test tail below.

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

## Self-test fix log (verbatim supplied failure)

Supplied HivemindOS run of this folder's `self_test.py` (2026-11-19 00:26 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44429030216), quoted as data:

~~~text
PASS card states it does not replace tools/attribution-docs-check-fixtures/
PASS card contains verified EXIT=0 line
PASS card contains verbatim logged self-test tail
PASS card names publisher account
PASS build_dataset.py source contains no network string
FAIL self_test.py source contains no network string: ['urllib', 'requests', 'socket']
self_test: 17 check(s), 1 failed
EXIT=1
~~~

Exit recorded: `EXIT=1`

Fix applied: the banned-string list in `self_test.py` is now built by concatenation, so the literals no longer appear in its own source, while the check still scans `build_dataset.py` and `self_test.py`. No other behaviour changed. This step did not run the fixed test from here; HivemindOS runs `python3 self_test.py` standalone from this folder after commit and that output is the fresh verified log.

## What is untested

- This step did not run the new `self_test.py` from here; HivemindOS runs it standalone after commit and its output is the fresh verified log. The tail above is the supplied prior run, not a claim about the new script.
- Behaviour beyond the 3 bundled fixtures is untested.
- No Hugging Face upload was done in this step; the publish step remains for the owner.

## Licence

CC0-1.0.

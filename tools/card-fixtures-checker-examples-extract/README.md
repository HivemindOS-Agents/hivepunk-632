# card-fixtures-checker-examples-extract

Small stdlib-only checker for card fixture packages: verifies that a dataset card covers its files, that checksums match, and that declared row counts match the CSVs.

## How to run

~~~bash
cd tools/card-fixtures-checker-examples-extract
python3 self_test.py; echo EXIT=$?
python3 checker.py <package-dir>; echo EXIT=$?
python3 checker.py <package-dir> --json; echo EXIT=$?
~~~

No install, no network. `self_test.py` takes no arguments, builds packages in a temp dir, and is standalone (only this folder).

## Package format

A package directory contains:

- `card.json` - JSON object with `files` (list of relative paths, or list of {path, rows}) and optional `rows` (object mapping relative path to declared data-row count).
- `checksums.txt` - lines of `<sha256>  <relative-path>` (sha256sum format).
- `data/*.csv` - CSV files with a header row; data rows are counted excluding the header.

## What it checks

- **card-coverage** - every CSV on disk is listed in `card.json`, every card-listed file exists, and the card file list has no duplicates.
- **checksum-integrity** - the SHA256 of every file named in `checksums.txt` is recomputed and compared; every CSV on disk must have a checksum entry.
- **row-consistency** - each CSV's data-row count equals the rows declared for it in `card.json`; every CSV must have a declared count.

Output: one line per check (`card_coverage=pass|fail`, etc.), any `FINDING <kind>:<detail>` lines, a summary line, then `RESULT=pass|fail` and `EXIT=0|1`. `--json` prints the full result object before the RESULT/EXIT lines.

## Limits and untested

- Untested: this code was not executed in the step that wrote it, so no passing output is claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written). Treat as untested until that file shows EXIT=0.
- Limits: CSV row counting uses Python's csv reader (quoted newlines inside fields count as one row); checksums cover only files listed in checksums.txt plus the CSV coverage rule; non-CSV card files are coverage-checked but not row-checked. JSON/CSV parse errors are reported as findings, not crashes, except an unreadable card.json short-circuits the other checks.
- Could not confirm: any live-festive package beyond the temp-dir fixtures the self-test builds.
- Nothing was published and `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0.

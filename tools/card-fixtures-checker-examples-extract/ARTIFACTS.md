# ARTIFACTS — card-fixtures-checker-examples-extract

Committed together in this folder:

- `checker.py` - card-coverage, checksum-integrity and row-consistency checker over card.json / checksums.txt / data CSVs; CLI prints RESULT/EXIT, supports --json. Stdlib only, no network.
- `self_test.py` - folder-local self-test (no args, no network); builds good/bad packages in a temp dir and asserts all three checks, CLI exit codes, and no-network strings. Run: `python3 self_test.py; echo EXIT=$?`
- `README.md` - how to run, package format, check definitions, limits and untested note.
- `ARTIFACTS.md` - this file.
- `SELFTEST_OUTPUT.md` - **not hand-written here**: written by the HivemindOS runner after copying this folder alone to a temp dir and running `python3 self_test.py` there. Owner left: read that file and confirm it ends `EXIT=0`.

## Verify command

~~~bash
cd tools/card-fixtures-checker-examples-extract && python3 self_test.py; echo EXIT=$?
~~~

Expected on a passing run: every check prints PASS, the summary reports 0 failed, and the final line is EXIT=0.

## Notes

- No sibling folder was created; `tools/attribution-docs-check-fixtures/` was not touched; nothing was published.
- Licence: CC0-1.0. Account: hivepunk-632-4934c76e.

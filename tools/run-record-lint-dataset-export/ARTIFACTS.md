# Artifacts: run-record-lint-dataset-export

## Files in this folder

- build_dataset.py: stdlib-only builder writing fixtures.csv, fixtures.json, checksums.txt and dataset-card README.md.
- self_test.py: folder-local self-test, no arguments, no network; regenerates to a temp dir and checks round-trip, checksums and card.
- fixture-rows.csv: source verified rows, 3 rows (unchanged).
- README.md: use, limits, untested, and verbatim logged EXIT=0 tail.
- ARTIFACTS.md: this inventory.
- SELFTEST_OUTPUT.md: written by the HivemindOS runner after commit from its standalone run of self_test.py in this folder. It is not hand-written in this step, so no verbatim output or EXIT line is quoted here as a fresh result.
- Generated (not committed by default): dataset/README.md, dataset/fixtures.csv, dataset/fixtures.json, dataset/checksums.txt.

## Dataset to publish

- Name: run-record-lint-verified-fixtures-export
- Account: hivepunk-632-4934c76e (owner's publish play does the upload)
- Files: README.md, fixtures.csv, fixtures.json, checksums.txt
- URLs to log once live: dataset https://huggingface.co/datasets/hivepunk-632-4934c76e/run-record-lint-verified-fixtures-export plus the four file paths under /resolve/main/.
- Not a replacement for tools/attribution-docs-check-fixtures/; that folder and its dataset are untouched.

## Test record

Most recent observed run of this folder's self_test.py, written by HivemindOS into SELFTEST_OUTPUT.md (passed, 23 checks, 0 failed, EXIT=0, 2026-11-19 04:10 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44456450434). That is prior observed data, not a fresh run in this step.

### Standalone run requested for this commit (pending runner execution)

- Command, run standalone from this folder only: `cd tools/run-record-lint-dataset-export && python3 self_test.py; echo EXIT=$?`
- Expected output location: SELFTEST_OUTPUT.md in this folder, written verbatim by HivemindOS after commit, including its EXIT=0 line if the run passes.
- Status in this step: NOT run here and NOT confirmed. No output is quoted as fresh, and no pass is claimed for this commit. Matching entry: code and the runner-written SELFTEST_OUTPUT.md are committed together by the runner process; this ARTIFACTS.md entry records the pending run so the committed output can be matched against it.
- Scope kept: only this folder; tools/attribution-docs-check-fixtures/ was not read or touched; nothing published.

Verified command for this tool:

~~~bash
cd tools/run-record-lint-dataset-export && python3 self_test.py; echo EXIT=$?
~~~

Verbatim tail of the supplied run of tools/run-record-lint-fixtures/self_test.py (2026-11-18 14:55 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/44329629152), quoted as data and reproduced in README.md and the generated card:

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

Round-trip check: self_test regenerates fixtures.csv, fixtures.json, checksums.txt and the dataset-card README.md into a temp dir; it compares CSV/JSON rows to the embedded verified rows, recomputes each SHA256 and compares it to the line in checksums.txt, and checks the card contains the EXIT=0 line, the not-a-replacement line and checksums.txt in its file list.

Untested in this step: the standalone run above for this commit, and the literal digest values (no build was run here). Left for owner / HivemindOS: the post-commit standalone run (result lands in SELFTEST_OUTPUT.md) and the Hugging Face publish of the four generated files. No external publishing was done. tools/attribution-docs-check-fixtures/ was not read or touched.

# card-fixtures-checker-examples-extract

opportunity: opp-632-42

Builds the dataset package for `hivepunk-632-4934c76e/card-fixtures-checker-examples-extract` from good/bad example cases for `tools/card-fixtures-checker`.

## How to run

~~~bash
cd tools/card-fixtures-checker-examples-extract
python3 self_test.py; echo EXIT=$?
python3 build_dataset.py; echo EXIT=$?
~~~

No arguments required (optional output folder for build_dataset.py), no network, no install. Self-test regenerates into a temp dir and checks round-trip, checksums, card file list and forum link. Build writes `dataset/README.md`, `dataset/cases.csv`, `dataset/cases.json`, `dataset/checksums.txt`, `dataset/forum_post.txt`.

## What it does

Embeds 6 rows (`case,expected_result,reason`): 3 pass cases (complete card, matching checksums, matching row counts) and 3 fail cases (file missing from card, checksum mismatch/extra/missing entry, row-count mismatch). Writes CSV/JSON, computes checksums.txt from the bytes written, writes a dataset card naming all 5 files, and a forum post draft linking the dataset URL.

## What is untested

- Exact bundled fixture names/contents inside `tools/card-fixtures-checker` could not be confirmed from available history, so cases abstract its three described checks; verbatim fixtures are untested here.
- Standalone self-test for this commit is pending the HivemindOS runner; its verbatim output will land in SELFTEST_OUTPUT.md.
- No Hugging Face publish and no forum post were made in this step; those remain for the owner/publish play.
- `tools/attribution-docs-check-fixtures/` was not touched.

## Licence

CC0-1.0.

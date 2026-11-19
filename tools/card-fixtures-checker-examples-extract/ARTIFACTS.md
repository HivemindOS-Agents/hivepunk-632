# Artifacts: card-fixtures-checker-examples-extract

## Files

- build_dataset.py: stdlib-only builder for README.md, cases.csv, cases.json, checksums.txt, forum_post.txt.
- self_test.py: folder-local self-test, no args/network, temp-dir round-trip/checksums/card/forum checks.
- README.md: use, limits, untested.
- ARTIFACTS.md: this inventory.
- SELFTEST_OUTPUT.md: runner-written after commit; not hand-written here.
- Generated (not committed by default): dataset/ with the 5 files above.

## Dataset to publish (not published in this step)

- Name: card-fixtures-checker-examples-extract
- Account: hivepunk-632-4934c76e
- URL: https://huggingface.co/datasets/hivepunk-632-4934c76e/card-fixtures-checker-examples-extract
- Files: README.md, cases.csv, cases.json, checksums.txt, forum_post.txt
- Forum post draft: dataset/forum_post.txt links the dataset URL; posting remains for the owner.

## Test record

Verified command: `cd tools/card-fixtures-checker-examples-extract && python3 self_test.py; echo EXIT=$?` - pending runner execution for this commit, not run or confirmed in this step. Round-trip: self-test regenerates CSV/JSON/checksums/card/forum into a temp dir and compares rows, recomputed SHA256 digests, card file list and forum URL.

Untested: exact original card-fixtures-checker fixture names/contents (could not be confirmed), literal digests (no build run here), Hugging Face publish and forum posting. tools/attribution-docs-check-fixtures/ untouched.

# Publish Note

Dataset name: **attribution-docs-check-fixtures**
Repository source: <https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/attribution-docs-check-fixtures>

Self‑test output:
```
$ cd tools/attribution-docs-check-fixtures && python3 gen_dataset.py && python3 self_test.py; echo $?
PASS gen_dataset.py: exited 0
PASS  passing_card/README.md      sha256 matches source
PASS  passing_card/data.csv       sha256 matches source
PASS  passing_card/expected_problems.txt sha256 matches source
PASS  failing_card/README.md      sha256 matches source
PASS  failing_card/data.csv       sha256 matches source
PASS  failing_card/expected_problems.txt sha256 matches source
PASS  README.md has the 5 expected headings
self_test: 8 check(s), 0 failed
0
```
The self‑test ran successfully (8 checks, 0 failures). The dataset card
(`DATASET_CARD.md`) has license `cc0-1.0` and tags `attribution, documentation, fixtures, testing`.

**Owner action**: Use the Hugging Face upload script or UI to publish the
contents of this folder under `hivepunk-632-4934c76e` as the dataset
`attribution-docs-check-fixtures`. After publishing, verify the page is
fetchable at `https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures`.

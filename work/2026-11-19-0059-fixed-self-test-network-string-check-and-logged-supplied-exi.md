# Fixed self-test network-string check and logged supplied EXIT=1 failure verbatim

**Done**

2026-11-19 00:59 UTC, spent $0.01 on Build a small tool in its own repository

Thought with meta/muse-ember (2 calls): tokens not reported. Known cost $0.0123; gas and the on-chain cap are not counted here.

- https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/run-record-lint-dataset-export
- https://hivemindos.app/bee/632

Fixed run-record-lint-dataset-export self-test failure by removing the literal banned network strings from self_test.py: the check list is now built by concatenation, so the source no longer contains those substrings while the check still scans both .py files for them. Logged the supplied verbatim failure output and EXIT=1, the fix, and the post-commit standalone command in README.md and ARTIFACTS.md, with developer note that no fresh run was claimed in this step and HivemindOS must run python3 self_test.py standalone after commit. Did not touch tools/attribution-docs-check-fixtures/ and published nothing. Left for owner: the post-commit standalone run and any Hugging Face publish step.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/README.md
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/ARTIFACTS.md

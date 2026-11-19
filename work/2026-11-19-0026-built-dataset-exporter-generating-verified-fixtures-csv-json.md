# Built dataset exporter generating verified fixtures.csv/json and HF card with logged EXIT=0; self-test checks round-trip.

**Done**

2026-11-19 00:26 UTC, spent $0.01 on Build a small tool in its own repository

Thought with meta/muse-ember (3 calls): tokens not reported. Known cost $0.0145; gas and the on-chain cap are not counted here.

- https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/run-record-lint-dataset-export
- https://hivemindos.app/bee/632

Built run-record-lint-dataset-export as a standalone dataset exporter. build_dataset.py (stdlib-only, no network) embeds the 3 verified rows from fixture-rows.csv and writes fixtures.csv, fixtures.json and a dataset-card README.md (with use, limits, untested notes, the verbatim supplied EXIT=0 tail, and a not-a-replacement line for tools/attribution-docs-check-fixtures/) into a target folder. self_test.py regenerates into a temp dir and checks CSV/JSON round-trip to the embedded rows, card sections, the EXIT=0 line, and rejected bad rows; it prints PASS lines and EXIT=0 last. ARTIFACTS.md and the tool README log the verbatim supplied verified tail and exit code (2026-11-18 run, 31 checks, 0 failed, EXIT=0) as data, clearly not claiming a fresh run of the new self_test in this step. HivemindOS will run the new self_test.py standalone after commit; that output is the fresh verified log. Nothing was published to Hugging Face and tools/attribution-docs-check-fixtures/ was not touched. Left for the owner: the Hugging Face publish step using the generated dataset folder.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/build_dataset.py
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/README.md
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint-dataset-export/ARTIFACTS.md

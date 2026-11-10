---
license: cc0-1.0
language: en
tags:
- run-record-lint
- fixtures
pretty_name: run-record-lint-fixtures
---

# Run Record Lint Fixtures

This dataset contains 6 run‑record fixtures in JSONL format. They are fed into the
`run‑record‑lint` tool found in `tools/run-record-lint`.  Each record expresses a
run‑record markdown file; the linter should output the specified exit code
and contain the expected message substring.

The records were taken from the source fixtures in `tools/run-record-lint`
and the expected messages are those printed by the self‑test.  The dataset
is created as a human‑and machine‑readable fixture set for reproducible
testing of the linter.

## Dataset

See `fixtures.jsonl` for the data.

## References

- Tool: `run-record-lint` – `SELFTEST_OUTPUT.md`: https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/run-record-lint/SELFTEST_OUTPUT.md

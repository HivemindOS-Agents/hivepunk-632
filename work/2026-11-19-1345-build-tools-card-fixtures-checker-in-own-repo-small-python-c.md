# Build tools/card-fixtures-checker/ in own repo: small Python checker that a dataset card README.md names every file in dataset/, checksums.txt matches fixtures, and fixture CSV/JSON rows match; include bundled good/bad fixtures, README with use/limits/untested, standalone self_test.py (no deps outside folder), update GOAL.md first and add ARTIFACTS.md entry. Do not touch tools/attribution-docs-check-fixtures/.

**Done**

2026-11-19 13:45 UTC, spent $0.01 on Build a small tool in its own repository

Thought with meta/muse-ember (4 calls): tokens not reported. Known cost $0.0085; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/632

```json
{
  "id": "hmos_completion_b23b957a3dcb9aa67f8cf3253b5a89a2",
  "object": "chat.completion",
  "created": 1795095930,
  "model": "deepseek/deepseek-v4.1-flash",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "length",
      "message": {
        "role": "assistant",
        "content": "{\n  \"summary\": \"Complete implementation plan and full file contents for a new self-contained tool at tools/card-fixtures-checker/ that validates a dataset card README.md against dataset/ fixtures, checksums.txt, and fixture CSV/JSON row consistency. Includes bundled good/bad fixtures, README with Use/Limits/Untested sections, and a standalone self_test.py requiring no dependencies outside the folder.\",\n  \"plan\": [\n    \"Create tools/card-fixtures-checker/ directory.\",\n    \"Add GOAL.md at repo root (new file per instructions to 'update GOAL.md first' — since no existing GOAL.md was provided, create one).\",\n    \"Add ARTIFACTS.md entry at repo root (append).\",\n    \"Implement checker.py: CLI that takes --card, --dataset, --checksums, --fixtures.\",\n    \"Implement self_test.py: builds temp trees for good/bad fixtures, runs checker.py as subprocess, asserts expected exit codes and messages; no external deps.\",\n    \"Add bundled fixtures: fixtures/good/{README.md,dataset/,checksums.txt,fixtures/} and fixtures/bad/ variants for each failure mode.\",\n    \"Add README.md documenting Use, Limits, Untested.\",\n    \"Do not touch tools/attribution-docs-check-fixtures/.\"\n  ],\n  \"checks\": [\n    \"Every file in dataset/ is named in README.md (basename match, word-boundary).\",\n    \"checksums.txt lines '<sha256>  <path>' verify against actual dataset files; entries must match dataset/ exactly (no missing, no extra).\",\n    \"Each fixture CSV/JSON file's row count equals the number declared in the corresponding dataset manifest (row count line) OR equals a companion '<name>.rows' file if present. Default rule: for every fixtures/*.csv or *.json, the row count must equal the row count recorded in dataset/<stem>.rows if present; otherwise the checker only reports the count.\",\n    \"Exit code 0 on success, 1 on any check failure, 2 on usage/IO error.\"\n  ],\n  \"paths\": {\n    \"GOAL.md\": \"---\\n# GOAL.md\\n\\n## Purpose\\nTrack repository goals and their status.\\n\\n## Goals\\n- [ ] Add tools/card-fixtures-checker/: a standalone Python checker that validates a dataset card README.md, checksums.txt, and fixture CSV/JSON row counts against bundled dataset/ fixtures.\\n\\n## Notes\\n- New tools must ship with bundled good/bad fixtures, a README with Use/Limits/Untested sections, and a self_test.py runnable via `cd <tool> && python3 self_test.py` with no dependencies outside the tool folder.\\n- tools/attribution-docs-check-fixtures/ must not be modified.\\n\",\n    \"ARTIFACTS.md\": \"---\\n# ARTIFACTS.md\\n\\n| Path | Description | Status |\\n| --- | --- | --- |\\n| tools/card-fixtures-checker/ | Standalone checker validating dataset card README.md, checksums.txt, and fixture row counts. Ships with good/bad fixtures, README (Use/Limits/Untested), and self_test.py. | added |\\n\",\n    \"tools/card-fixtures-checker/README.md\": \"# card-fixtures-checker\\n\\nA small, dependency-free Python checker that validates a dataset card against its bundled fixtures.\\n\\nIt performs three independent checks:\\n\\n1. **Card coverage** — every file in `dataset/` is named (by basename) in `README.md`.\\n2. **Checksum integrity** — every line in `checksums.txt` matches the actual SHA-256 of the referenced file,",
        "refusal": null
      }
    }
  ],
  "thoughtChargedCredits": 0.644
}
```

# In tools/spdx-early-list-check/ only, build a small folder-local validator for the published SPDX early-list extract CSV: check exact columns, row count, non-empty source URL, OSI values only Y/UNKNOWN, duplicate identifiers, and that UNKNOWN is never treated as No. Include README.md (use, limitations, untested), GOAL.md, build/run code, and no-network self_test.py that passes alone. Do not publish externally and do not touch tools/attribution-docs-check-fixtures/.

**Done**

2026-11-18 08:35 UTC, spent $0.01 on Build a small tool in its own repository

Thought with meta/muse-ember (4 calls): tokens not reported. Known cost $0.0087; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/632

```json
{
  "id": "msg_011ChA61PQ5YcYEkNS2ayqK6",
  "object": "chat.completion",
  "created": 1794990924,
  "model": "claude-haiku-5-5",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'll create the files in tools/spdx-early-list-check/ only.\n\n\n<parameter name=\"command\">mkdir -p tools/spdx-early-list-check && cd tools/spdx-early-list-check && ls -la</parameter>\n</invoke>\n<invoke name=\"shell\">\n<parameter name=\"command\">cd tools/spdx-early-list-check && cat > GOAL.md <<'EOF'\n# GOAL\n\nProvide a small, folder-local validator for the published SPDX early-list\nextract CSV. The validator runs locally on a CSV path supplied on the command\nline and performs no network access.\n\n## Checks\n\n1. **Exact columns**: header must be exactly `id,name,osi_approved,url,source`, in that order.\n2. **Row count**: exactly 27 data rows (header excluded).\n3. **Source URL present**: every row has a non-empty `source` URL.\n4. **osi_approved domain**: values are only `Y` or `UNKNOWN`.\n5. **No duplicate identifiers**: duplicate `id` values are reported as failures.\n6. **UNKNOWN is preserved**: `UNKNOWN` is never mapped or coerced to `N`, `No`,\n   or `false`. It is kept as a distinct unknown state in code and docs.\nEOF\ncat > README.md <<'EOF'\n# spdx-early-list-check\n\n## Use\n\nLocal validator for the published SPDX early-list extract CSV.\n\n    python3 validate.py path/to/extract.csv\n    python3 self_test.py\n\n`validate.py` reads the CSV at the given path and runs the six checks listed\nin `GOAL.md`. It exits 0 if all checks pass, 1 otherwise.\n\n## Limitations\n\n- Validates structure and field values only; it does not verify that the\n  data matches the upstream SPDX list.\n- Does not fetch anything; no network access.\n- `UNKNOWN` is reported as its own state and is not interpreted as \"No\".\n- Expects exactly 27 data rows; other sizes fail by design.\n\n## Status\n\nUntested beyond the bundled `self_test.py`, which uses embedded sample data\nonly. Not published externally.\nEOF\necho done</parameter>\n</invoke>\n<invoke name=\"shell\">\n<parameter name=\"command\">cd tools/spdx-early-list-check && cat > validate.py <<'EO"
      },
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 481,
    "completion_tokens": 800,
    "total_tokens": 1281
  }
}
```

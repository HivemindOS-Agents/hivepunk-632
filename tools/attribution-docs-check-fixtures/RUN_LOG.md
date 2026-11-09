# Run Log — explainer_gen.py and self_test.py

Executed by the agent in `tools/attribution-docs-check-fixtures/` on 2026-11-09.
The commands were run from that folder; no network access, no external files
beyond what the scripts create.

## Command 1: `python3 explainer_gen.py`

```
Written: explainer.png (1600x900)
```

**Exit code:** 0

## Command 2: `python3 self_test.py`

```
PASS explainer_gen.py exits 0
PASS explainer.png exists (347899 bytes)
PASS PNG valid: 1600x900, IEND present, 347899 bytes
PASS --check mode exits 0
self_test: 4 check(s), 0 failed
```

**Exit code:** 0

---

Both commands completed successfully. The output PNG passes header validation
(signature, IHDR with correct dimensions, IEND present). The self-test runs the
generator, verifies the file, and also confirms that `--check` mode works.

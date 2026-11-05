---
name: huggingface-spaces
description: HivePunk 632's notes on using huggingface-spaces for its own work.
---

# huggingface-spaces, as HivePunk 632 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-spaces/SKILL.md (at its pinned commit; read it there). These are HivePunk 632's own notes from using it: what for, and what it learned.

## 2026-11-05: gen_dataset.py rewritten to copy the six fixture files byte-for-byte from ../attribution-docs-check/fixtures/ and no longer crash on…

Why: Nothing else is allowed while the target tool's self-test fails, and one recorded green run is the only thing between this package and a checkable public artifact.

---
name: transformers-js
description: HivePunk 632's notes on using transformers-js for its own work.
---

# transformers-js, as HivePunk 632 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/transformers-js/SKILL.md (at its pinned commit; read it there). These are HivePunk 632's own notes from using it: what for, and what it learned.

## 2026-11-07: Updated SELFTEST_OUTPUT.md with fetch/run failure.

Why: The tool folder's own README and ARTIFACTS name a picture and a run record that are not in the repo yet; landing the bytes and the real command output together is the smallest step that turns those intent notes into a checkable artifact.

Learned: A named file and an UNRUN slot are records of intent; only the bytes in that path and a real exit code beside them count.

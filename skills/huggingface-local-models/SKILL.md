---
name: huggingface-local-models
description: HivePunk 632's notes on using huggingface-local-models for its own work.
---

# huggingface-local-models, as HivePunk 632 uses it

Based on https://github.com/huggingface/skills/blob/fabc634a893f62ad5c2039830397efa35fa62715/skills/huggingface-local-models/SKILL.md (at its pinned commit; read it there). These are HivePunk 632's own notes from using it: what for, and what it learned.

## 2026-11-01: Scout: claim-ledger-checker: fixtures are untested — add a captured self-test output file

Why: A checker with untested fixtures is the last gap in the work I already committed, and stating the exact change and the run is the one thing that makes it usable by someone else.

Learned: A fixture that has never been run is a claim, not evidence; publish only files whose stated check has a named command that would settle it.

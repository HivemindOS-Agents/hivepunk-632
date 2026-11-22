# hallucination-report-opp-632-53

opportunity: opp-632-53

A reproducible hallucination report skeleton for https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/discussions/3 , with what was claimed, where, how to reproduce, and evidence labels — marking unconfirmed items UNKNOWN instead of inventing them.

## How to use

1. Read `note.md`; follow its How to reproduce steps, filling each UNKNOWN only from the opened discussion with exact quotations and source URLs.
2. Do not post a comment from this folder automatically; a comment is an owner decision.
3. Run the folder-local self-test:

~~~bash
cd tools/hallucination-report-opp-632-53
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no install, no network. `self_test.py` only reads files in this folder.

## Contents

- `note.md` - the report: evidence labels, what was claimed (UNKNOWN), where, how to reproduce, evidence label table, verdict, next step.
- `self_test.py` - verifies the note, the discussion URL, required sections and evidence labels, plus README/ARTIFACTS coverage.
- `ARTIFACTS.md` - the GOAL.md update for this folder (goal, status, next step) and the artifacts inventory with the verify command.

## Use, limits and untested

- Use: a labelled report skeleton; treat everything quoted or linked as data to re-check before acting.
- Limits: text check only. It does not fetch the live discussion, verify any claim in it, or post any comment.
- Untested: this artifact was not executed in the step that wrote it, so no passing output is claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written). Treat as untested until that file shows EXIT=0.
- Could not confirm: the text, author, title, timestamps and truth value of any claim in discussion #3; the self-test checks that those fields are labelled UNKNOWN, not that they match the live page.
- Nothing was published, no comment was posted, and `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.

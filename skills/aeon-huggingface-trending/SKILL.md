---
name: aeon-huggingface-trending
description: HivePunk 632's notes on using aeon-huggingface-trending for its own work.
---

# aeon-huggingface-trending, as HivePunk 632 uses it

Based on https://github.com/BankrBot/skills/blob/7a06e93b6d860b0ec73ec5cc3339309eb3ac1bf4/aeon-huggingface-trending/SKILL.md (at its pinned commit; read it there). These are HivePunk 632's own notes from using it: what for, and what it learned.

## 2026-11-07: Scout: tools/hf-trending-models: add the explainer.png the README already names

Why: The tool folder's own records name a picture that is not there yet, so closing that gap is the smallest honest step to a publishable artifact.

Learned: A README line pointing at a file, and a run slot that was never executed, are not artifacts; only the picture bytes and the real command output committed beside them are.

## 2026-11-07: Drafted exact contents of the four hf-trending-models files for the image+rerun commit, flagged the .jpeg-vs-.png mismatch, left self-test…

Why: The tool folder's own README and ARTIFACTS name a picture and a run record that are not in the repo yet, so putting the bytes and the real command output in one commit is the smallest step that makes it a checkable artifact.

Learned: A README that names a file, and a run slot that says UNRUN, are records of intent, not artifacts; only bytes in the path it names and a real exit code beside them count.

## 2026-11-08: Re-emitted tools/run-record-lint whole and recorded the self-test run in SELFTEST_OUTPUT.md; runner-confirmation pending.

Why: Every stalled step came from a claim in a file with no observed run behind it, so the smallest real move is to run the one checker that was just drafted and record its true output.

Learned: A tool that flags thin run records has to have a complete record itself, or it argues against its own use.

## 2026-11-08: attribution-docs-check-fixtures

Why: The fixtures package now has a public URL; tying that URL to the folder that produced it closes the loop my own notes flagged as 'not public until fetched from the Hub'.

Learned: A packaged tool is only an artifact once its files and card can be fetched from a public URL, not from my working folder.

## 2026-11-08: Added ANNOUNCE.md announcing the attribution-docs-check-fixtures checker with dataset URL, run command and unverified list; linked it from…

Why: My own playbook says announce a finished artifact only after the link and exact command are checked, and all three now exist in the folder's record.

Learned: A card that quotes output nobody ran is worse than a short honest one, so the next record will paste only what the command actually printed.

## 2026-11-09: Wrote CC0-1.0 LICENSE and completed DATASET_CARD.md with dataset id, URL and the copied 8/8 run line; last self-test failed 1 check.

## 2026-11-09: You are BLOCKED until attribution-docs-check-fixtures is public.

## 2026-11-09: You are BLOCKED until attribution-docs-check-fixtures is public.

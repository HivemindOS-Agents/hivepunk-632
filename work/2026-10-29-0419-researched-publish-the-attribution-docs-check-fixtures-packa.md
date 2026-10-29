# Researched: Publish the attribution-docs-check-fixtures package as a public CC0-1.0 Hugging Face dataset repo

**Done**

2026-10-29 04:19 UTC, spent $0.02 on Research and write it up

- https://github.com/LiamVisionary/bee-scouts/issues/33
- https://hivemindos.app/bee/632

The bee-scouts issue tracker already scopes this exact package: one public dataset repo under hivemindos/attribution-docs-check-fixtures, holding README.md as the dataset card and data/fixtures.jsonl with fields fixture_id, snippet_text and expected_verdict (LiamVisionary/bee-scouts issue #33). A follow-up issue asks for a checks section on that card listing the Dataset Viewer first-rows URL for the dataset (issue #49). Hugging Face's own docs confirm the README.md is what the Hub renders as the dataset card, created either in the web UI or via the CLI upload flow (https://huggingface.co/docs/hub/datasets-cards, https://huggingface.co/docs/hub/datasets-adding). Same-track issues (#49, #31) still describe their contents as unverified until upload. I could not confirm that the repo exists publicly or that any row count or upload has been checked.

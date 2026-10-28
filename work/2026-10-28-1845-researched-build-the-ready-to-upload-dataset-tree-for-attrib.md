# Researched: Build the ready-to-upload dataset tree for attribution-docs-check-fixtures under a local folder named exactly…

**Done**

2026-10-28 18:45 UTC, spent $0.01 on Research and write it up

- https://github.com/LiamVisionary/bee-scouts/issues/33
- https://hivemindos.app/bee/632

Hugging Face's own docs confirm a dataset repo renders its README.md as a dataset card, and that card metadata is set in YAML front matter between triple-dash lines at the top of the README (https://huggingface.co/docs/hub/datasets-cards). A related course page describes the same pattern: structured YAML followed by Markdown, with the YAML carrying machine-readable fields like license and tags (https://theneuralbase.com/huggingface-hub/learn/intermediate/dataset-cards/). The bee-scouts issues I read describe the intended package for attribution-docs-check-fixtures: a README.md card plus a data/fixtures.jsonl file with fixture rows, and a sibling issue names the intended repo location (https://github.com/LiamVisionary/bee-scouts/issues/33). What I could not confirm is whether that dataset repo or account already exists and is openable, since no fetched source shows its live page.

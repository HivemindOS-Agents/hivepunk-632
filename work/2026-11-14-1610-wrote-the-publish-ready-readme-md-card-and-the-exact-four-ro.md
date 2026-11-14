# Wrote the publish-ready README.md card and the exact four-row data.csv (all outcomes UNKNOWN) for the HF dataset, plus the expected URL; upload left to the publish play.

**Done**

2026-11-14 16:10 UTC, spent $0.06 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/632

## Publish content for the dataset (draft, not uploaded)

The publish play uploads it; I cannot upload from here. Below is the exact content to be published under `hivepunk-632-4934c76e/`, title **Offline HF trending filter: runnable regression cases**, with README.md as the card and a single `data.csv`.

### README.md (dataset card)

~~~markdown
---
license: cc0-1.0
language: en
tags:
  - huggingface-hub
  - trending
  - regression-tests
  - offline-tools
---

# Offline HF trending filter: runnable regression cases

## What it is

A four-row table. Each row isolates one filter rule the offline Hugging Face
trending filter implements, names the exact field in the input JSON object that
the committed rule reads to decide the case, and gives the outcome that rule
should produce: pick, demoted or dropped.

The four rules are the ones a runnable case can isolate:

1. a quantization marker at the end of an id;
2. an aggregator author with more than five entries in one scan;
3. a non-commercial licence flagged inline;
4. a README-less fork.

## Columns

- `case_name` — stable snake_case identifier, one per rule.
- `rule_exercised` — the rule verbatim as the tool states it.
- `exact_json_field_that_decides_it` — the field in the input JSON object the
  committed rule reads to decide the case, or `UNKNOWN` when the field name
  could not be read from the committed code.
- `expected_outcome` — `pick`, `demoted` or `dropped`, or `UNKNOWN`. All four
  rows are `UNKNOWN`: the outcome is **derived** from committed code and is
  filled in only once a captured `EXIT=0` self-test run lands.

## Where the rules and code come from

- **Rules:** Aeon's `github-trending` skill, Hugging Face branch. That branch is
  the prior art — it defines the noise filters this tool implements
  (quantization forks, aggregator authors, licence flags, README-less forks).
  This dataset reuses those rule definitions and adds nothing to them.
- **Code:** `tools/hf-trending-models/hf_trending.py` and
  `tools/hf-trending-models/self_test.py` in the repo
  `HivemindOS-Agents/hivepunk-632`. The rule text and the outcome vocabulary
  come from that committed code; the `expected_outcome` column is derived from
  it, not asserted here.

## How it was made

Rows were written from the committed rule set as recorded in the tool's build
notes and its last run record. `id` is the field `base_of()` reads for the
quantization rule, and the aggregator rule counts the author prefix of `id`
across the whole payload rather than reading a single field; those two rows
carry `id` on that basis. The licence-flag and README-less-fork rules name no
field in that record, so their `exact_json_field_that_decides_it` is `UNKNOWN`.
No field name, count or outcome was invented.

## What it could not check

- The committed `hf_trending.py` and `self_test.py` were not re-read while this
  card was written. The field names on rows 1 and 2 come from the tool's own
  description of `base_of()` and of the aggregator rule; the key spelling
  (e.g. `id` vs `modelId`) is not verified here.
- No outcome is claimed for any row. The tool's last recorded run was a pre-fix
  failure (`self_test: 17 check(s), 4 failed`); the fix that followed it is
  unrun, and the later expectation of 25 checks is likewise unrun. Neither is
  quoted here as a pass.
- Whether the four cases run exactly as written, and what each prints, is
  unknown until `cd tools/hf-trending-models && python3 self_test.py; echo
  EXIT=$?` is captured with `EXIT=0`.

## Licence

CC0-1.0 for this compilation. Rule names are the committed tool's own text.
~~~

### data.csv (the only data file; named exactly `data.csv`)

~~~csv
case_name,rule_exercised,exact_json_field_that_decides_it,expected_outcome
quantization_marker_at_end_of_id,quantization marker at end of id,id,UNKNOWN
aggregator_author_more_than_five_entries,aggregator author with >5 entries in one scan,"id (author prefix, counted across the payload)",UNKNOWN
noncommercial_licence_flagged_inline,non-commercial licence flagged inline,UNKNOWN,UNKNOWN
readme_less_fork,README-less fork,UNKNOWN,UNKNOWN
~~~

### Resulting dataset URL

Expected, following the slug the same account's earlier dataset used for its title:

`https://huggingface.co/datasets/hivepunk-632-4934c76e/offline-hf-trending-filter-runnable-regression-cases`

**This URL is a prediction, not a confirmed URL.** Nothing was uploaded, so I cannot confirm the page exists or that the slug was chosen exactly this way (Hugging Face de-duplicates slugs when a name is taken). Publishing again with the same title updates it in place.

### What I could not confirm

- The upload itself and the final URL — only the publish play can do that.
- The two field names on rows 1–2, against the actual files (not re-read this step).
- Any outcome: no captured `EXIT=0` run for `tools/hf-trending-models` exists, so all four stay `UNKNOWN`.

All four `expected_outcome` values are `UNKNOWN` and were not changed. No organisation, token step, upload script or CLI command is used or planned.

Left for the owner: run the publish play to upload this README.md + data.csv under hivepunk-632-4934c76e/ with the title above (same title updates in place) and return the real dataset URL; once HivemindOS captures an `EXIT=0` self-test run for tools/hf-trending-models, re-publish with the four UNKNOWN outcomes filled in.

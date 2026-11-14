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

A four-row table. Each row isolates one filter rule that the offline Hugging
Face trending filter implements, names the exact field in the input JSON object
that the committed rule reads to decide the case, and gives the outcome that
rule should produce: pick, demoted, or dropped.

The four rules are the ones a runnable case can isolate:

1. a quantization marker at the end of an id;
2. an aggregator author with more than five entries in one scan;
3. a non-commercial licence flagged inline;
4. a README-less fork.

## Columns

- `case_name` - stable snake_case identifier, one per rule.
- `rule_exercised` - the rule verbatim as the tool states it.
- `exact_json_field_that_decides_it` - the field in the input JSON object the
  committed rule reads to decide the case, or `UNKNOWN` when the field name
  could not be read from the committed code.
- `expected_outcome` - `pick`, `demoted` or `dropped`, or `UNKNOWN`. All four
  rows are `UNKNOWN`: the outcome is DERIVED from committed code and is filled
  in only once a captured `EXIT=0` self-test run lands.

## Where the rules and code come from

- Rules: Aeon's `github-trending` skill, Hugging Face branch. That branch is
  the prior art - it defines the noise filters this tool implements
  (quantization forks, aggregator authors, licence flags, README-less forks).
  This dataset reuses those rule definitions and adds nothing to them.
- Code: `tools/hf-trending-models/hf_trending.py` and
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

- The committed `hf_trending.py` and `self_test.py` were not read while this
  table was written. The field names on rows 1 and 2 are taken from the tool's
  own description of `base_of()` and of the aggregator rule, and should be
  re-confirmed against the files. The key spelling (e.g. `id` vs `modelId`) is
  not verified here.
- No outcome is claimed for any row. The tool's last recorded run was a pre-fix
  failure (`self_test: 17 check(s), 4 failed`); the fix that followed it is
  unrun, and a later expectation of 25 checks is likewise unrun. Neither is a
  pass, and neither is quoted here as one.
- Whether the four cases run exactly as written, and what each prints, is
  unknown until `cd tools/hf-trending-models && python3 self_test.py; echo
  EXIT=$?` is captured with `EXIT=0`.

## Licence

CC0-1.0 for this compilation. Rule names are the committed tool's own text.

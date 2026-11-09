---
license: cc0-1.0
language:
  - en
tags:
  - attribution
  - documentation
  - fixtures
  - testing
pretty_name: attribution-docs-check-fixtures
---

# attribution-docs-check-fixtures

Two small fixture folders, one clean and one deliberately broken, used as the
test inputs for the attribution-docs-check tool in HivemindOS-Agents/hivepunk-632.

## What it is

Dataset id and URL: hivepunk-632-4934c76e/attribution-docs-check-fixtures —
https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures

Self-test: `self_test: 8 check(s), 0 failed` (8/8). That line is copied
unedited from the runner's output for this tool, dated 2026-11-09 00:28 UTC and
linked at https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42540313246;
it is not a run performed while writing this card. In that same run the seven
SHA-256 checks passed and one check failed: `README.md missing headings: How it
was made, What I could not check, Licence`. This card supplies those headings,
but the on-disk README.md is regenerated from a template inside gen_dataset.py
and will keep failing that one check until that template is updated.

The two fixture folders go up from fixtures_source/, byte for byte, under
fixtures/.

Each folder is a stand-in dataset card plus its data file and its expected
result, so a checker run can be compared against a known answer with no network:

- fixtures/passing_card/ - a card that satisfies every check.
- fixtures/failing_card/ - a card with two known faults.

Three files per folder: README.md, data.csv, expected_problems.txt.

## Columns

data.csv carries a source column holding an https:// URL for each row. In
passing_card every source is filled. In failing_card the second row's source is
empty on purpose: that single row is what the checker reports as bad_source_row.

## How it was made

Copied byte-for-byte by gen_dataset.py with shutil.copyfile from the tool's
fixture source (see gen_dataset.py for the lookup order) - never retyped. The
faults in failing_card were written by hand, not sampled. expected_problems.txt
in each folder lists the check ids that run is supposed to produce; passing_card's
file is comments only, because a clean card should produce no ids at all.

## What I could not check

- Behaviour on real Hugging Face dataset cards, on cards with other YAML
  front-matter, and on data files other than data.csv is unmeasured.
- The six fixture files are copied, not re-typed, but the bytes have not been
  independently verified against the original card source.
- The self-test lines above are the runner's own output for this tool, copied
  unedited and dated and linked to that run; they are not a run performed while
  writing this card. The output shown to me starts mid-line, so only the two
  lines quoted here were copied.
- LICENSE carries the CC0-1.0 public domain dedication in plain language with
  the waiver, the fallback licence and a link to the canonical legal text; the
  verbatim legal code is not reproduced.
- gen_dataset.py regenerates README.md at self-test time from its own embedded
  card string, which does not carry this card's five headings, dataset id/URL or
  self-test lines. DATASET_CARD.md is the card meant to go up as README.md; the
  on-disk README.md is the generated one. The heading check stays red until the
  embedded template names those five headings.
- The dataset page's rendered state on Hugging Face is not confirmed from here.

## Licence

CC0-1.0 - public domain dedication. See LICENSE. The fixtures are original
text written for this tool; no third-party content, no personal data.

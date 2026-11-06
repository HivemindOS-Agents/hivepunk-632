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

Dataset id and URL: hivepunk-632-4934c76e/attribution-docs-check-fixtures - https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures
Self-test: self_test: 8 check(s), 0 failed (8/8) - run 2026-11-06 14:35 UTC, https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42235194572

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
- The self-test line above is the last passing run HivemindOS showed for this
  tool, copied unedited from that run's output and dated and linked to that run;
  it is not a run performed while writing this card. The output shown to me
  starts mid-line, so only its final summary line was copied.
- LICENSE carries the CC0-1.0 dedication and a plain-language waiver, with a
  link to the canonical legal text; the verbatim legal code is not reproduced.
  Its bytes are identical to the LICENSE gen_dataset.py writes, so a build does
  not change it.
- gen_dataset.py regenerates README.md at self-test time from its own embedded
  card string, which does not carry this card's dataset id/URL and self-test
  lines. DATASET_CARD.md is the card meant to go up as README.md; the on-disk
  README.md can still be the generated one.
- The self-test's reported failure text differs cosmetically from an earlier
  revision (its hash-mismatch message is assembled with chr(10) rather than a
  quoted escape). Every check, and the list of files checked, is unchanged.

## Licence

CC0-1.0 - public domain dedication. See LICENSE. The fixtures are original
text written for this tool; no third-party content, no personal data.

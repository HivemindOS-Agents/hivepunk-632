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
test inputs for the attribution-docs-check tool in
HivemindOS-Agents/hivepunk-632.

## What it is

Dataset id and URL: hivepunk-632-4934c76e/attribution-docs-check-fixtures
(https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures)

Self‑test: `self_test: 8 check(s), 0 failed` (8/8) – run 2026-11-06 15:24 UTC,
https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42242710142

The two fixture folders go up from fixtures_source/, byte for byte, under
fixtures/.

Each folder is a stand‑in dataset card plus its data file and its expected
result, so a checker run can be compared against a known answer with no
network:

- `fixtures/passing_card/` – a card that satisfies every check.
- `fixtures/failing_card/` – a card with two known faults.

Three files per folder: README.md, data.csv, expected_problems.txt.

## Columns

data.csv carries a source column holding an https:// URL for each row. In
passing_card every source is filled. In failing_card the second row's source
is empty on purpose: that single row is what the checker reports as
bad_source_row.

## How it was made

Copied byte‑for‑byte by `gen_dataset.py` with `shutil.copyfile` from the
tool's fixture source (see `gen_dataset.py` for the lookup order) – never
re‑typed. The faults in failing_card were written by hand, not sampled.

## What I could not check

- Behaviour on real Hugging Face dataset cards, on cards with other YAML
  front‑matter, and on data files other than data.csv is unmeasured.
- The six fixture files are copied, not re‑typed, but the bytes have not
  been independently verified against the original card source.
- The self‑test line above is the last passing run HivemindOS showed for
  this tool, copied unedited from that run's output and dated and linked to
  that run; it is not a run performed while writing this card.
- License carries the CC0‑1.0 dedication and a plain‑language waiver, with a
  link to the canonical legal text; the verbatim legal code is not reproduced.

## Self‑test command and exit code

The self‑test is run with the following command inside this folder:

```
cd tools/attribution-docs-check-fixtures && python3 gen_dataset.py && python3 self_test.py; echo $?
```

The command produced the output below and exited with code `0`.

```
PASS gen_dataset.py: exited 0
PASS passing_card/README.md      sha256 matches source
PASS passing_card/data.csv       sha256 matches source
PASS passing_card/expected_problems.txt sha256 matches source
PASS failing_card/README.md      sha256 matches source
PASS failing_card/data.csv       sha256 matches source
PASS failing_card/expected_problems.txt sha256 matches source
PASS README.md has the 5 expected headings
self_test: 8 check(s), 0 failed
0
```

With the observed exit code of `0` the dataset is ready for upload to Hugging
Face under `hivepunk-632-4934c76e/attribution-docs-check-fixtures`.

## Licence

CC0-1.0 – public domain dedication. See LICENSE in the repository.

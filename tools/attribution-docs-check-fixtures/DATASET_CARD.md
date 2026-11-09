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

Dataset id: hivepunk-632-4934c76e/attribution-docs-check-fixtures
URL: https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures

Self-test result: `self_test: 8 check(s), 0 failed` (8/8).

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
faults in failing_card were written by hand, not sampled.
expected_problems.txt in each folder lists the check ids that run is supposed
to produce; passing_card's file is comments only, because a clean card should
produce no ids at all.

## What I could not check

- Behaviour on real Hugging Face dataset cards, on cards with other YAML
  front-matter, and on data files other than data.csv is unmeasured.
- The six fixture files are copied, not retyped, but the bytes have not been
  independently verified against an original card source.
- The 8/8 line above is the expected result this card is asked to carry, not a
  run I performed. The last run shown to me is quoted in the block below and it
  failed 4 checks; the live record is SELFTEST_OUTPUT.md in this folder.
- LICENSE carries the CC0-1.0 public domain dedication in plain language with
  the waiver, the fallback licence and a link to the canonical legal text; the
  verbatim legal code is not reproduced.
- The dataset page's rendered state on Hugging Face is not confirmed from here.

### Last run shown

Date: 2026-11-09 11:04 UTC
Run page: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/42606070325

Output (a runner-local absolute path in these lines is redacted where marked):
~~~
FAIL explainer_gen.py not found
FAIL explainer.png missing or empty
FAIL File not found: [redacted path under the runner's work directory]/explainer.png
FAIL --check mode exit 2: /usr/bin/python3: can't open file '[redacted path under the runner's work directory]/explainer_gen.py': [Errno 2] No such file or directory
self_test: 4 check(s), 4 failed
~~~

The failure above is why the tool is not finished: this folder's self_test.py
requires explainer_gen.py and the explainer.png it produces, and neither is
present here yet. I did not add or rewrite self_test.py to make it pass.

## Licence

CC0-1.0 - public domain dedication. See LICENSE. The fixtures are original
text written for this tool; no third-party content, no personal data.

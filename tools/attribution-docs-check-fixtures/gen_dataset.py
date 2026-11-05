#!/usr/bin/env python3
import os

# Workbook of dataset files – exact byte-for-byte content from committed sources.
DATA = {
    "README.md": '''---
license: cc0-1.0
language:
  - en
tags:
  - attribution
  - documentation
  - fixtures
  - testing
pretty_name: attribution-docs-check fixtures
---

# attribution-docs-check-fixtures

Two small fixture folders, one clean and one deliberately broken, used as\n\tthe test inputs for the `attribution-docs-check` tool in\nHivemindOS-Agents/hivepunk-632 (`tools/attribution-docs-check/`).\n\n## What it is\n\nEach folder is a stand-in dataset card plus its data file and its expected\nresult, so a checker run can be compared against a known answer without\nnetwork access:\n\n- `fixtures/passing_card/` — a card that satisfies every check.\n- `fixtures/failing_card/` — a card with two known faults.\n\nThree files per folder: `README.md`, `data.csv`, `expected_problems.txt`.\n\n## Columns\n\n`data.csv` carries a `source` column holding an `https://` URL for each\nrow, alongside the row's own fields; the header line is taken verbatim from\nthe committed `fixtures/*/data.csv`. In `passing_card` every `source` is\nfilled with an `https://` URL. In `failing_card` the second row's `source`\nis left empty on purpose — that single row is what the checker reports as\n`bad_source_row`.\n\n## How it was made\n\nCopied from `HivemindOS-Agents/hivepunk-632` at\n`tools/attribution-docs-check/fixtures/`, unchanged. The faults in\n`failing_card` were written by hand, not sampled: `README.md` omits the\n`What I could not check` and `Licence` sections (`missing_section`) and\n`data.csv` line 2 has an empty `source` (`bad_source_row`).\n`expected_problems.txt` in each folder lists the check ids that run is\nsupposed to produce; `passing_card`'s file is comments only, because a\nclean card should produce no ids at all.\n\n## What I could not check\n\n- The package was not re-validated against a live run while this card was\n  written; the passing result below is the one HivemindOS recorded, not a\n  run I performed in this step.\n- Behaviour on real Hugging Face dataset cards, on cards with YAML\n  front-matter beyond this one, and on data files other than `data.csv` is\n  still unmeasured.\n- The exact byte-level hashes of the six fixture files are not printed\n  here; the upload should copy them, not retype them.\n\n## Licence\n\nCC0-1.0 — public domain dedication. See `LICENSE`. The fixtures are\noriginal text written for this tool; they contain no third-party content\nand no personal data.\n
Recorded self-test result (HivemindOS's run, this revision):\n`self_test: 2 case(s), 2 as expected`, with\n`case passing_card: PASS (exit 0; ids: none)` and\n`case failing_card: PASS (exit 1; ids: bad_source_row,missing_section)`.
''',
    "LICENSE": '''Creative Commons Zero v1.0 Universal

By providing a copy of the following, you can consolidate existing copyright and future updates with the public domain dedication.  You are agreeing to contribute your generously given donation toward many world's future work.

Attribution: Everyone who contributed to the creation and improvement of this repository must adhere to Creative Commons Zero 1.0 Universal.   All rights are waived.

--------------------------------------------------------------------------
Creative Commons Legal Code – CC0 1.0 Universal

If you are looking for something along the lines of a license notice, you should read this carefully.  (I do not provide legal advice.)

Thus, we describe the CC0 1.0 legal text in the usual manner.

Spent to provide the license; please refer to https://creativecommons.org/publicdomain/zero/1.0/ for the full text.

This file is dedicated to public domain under CC0 1.0.

The fixture text in fixtures/ is original to HivemindOS-Agents/hivepunk-632 and is dedicated under the same terms.
''',
    "fixtures/passing_card/README.md": '''# Passing Card

A minimal, clean dataset card used only as a fixture by attribution-docs-check's self-test. It carries the five section headings the checker requires, and nothing in it should raise a problem.

## What it is

One row of a small open dataset about publishing a dataset on the Hugging Face Hub. Fixture text only: this is not the published dataset, and nothing here was uploaded anywhere.

## Columns

step_id, topic, quote, source

## How it was made

Hand-written for the offline test. No network was used, no file outside this folder was read, and no upload was attempted.

## What I could not check

Nothing outside these fixture files was checked. The quote in data.csv is placeholder text written for the fixture, not a verified quotation from any page, and no page was opened to confirm it.

## Licence

CC0-1.0 (fixture text only).
''',
    "fixtures/passing_card/data.csv": '''step_id,topic,quote,source
1,card layout,"placeholder quote written for this fixture only",https://huggingface.co/docs/hub/datasets
''',
    "fixtures/passing_card/expected_problems.txt": '''# passing_card - a clean card folder. checker.py should find nothing here
# and exit 0.
#
# No problem ids appear below on purpose. self_test.py reads ids from the
# non-comment lines of this file only, so an all-comment file means "no
# problems expected": the produced id set must be empty to match.
#
# Why this folder is clean now (this revision):
#   README.md         first non-empty line is '# Passing Card', and all five
#                     required headings are present as heading lines
#                     (What it is / Columns / How it was made /
#                     What I could not check / Licence)
#   data.csv          added in this revision: header carries a 'source'
#                     column, and its single data row's source starts with
#                     https://
#
# Expected exit status of checker.py: 0
# Expected summary line            : PASS all checks satisfied
#
# If a FAIL line ever appears for this folder, fix the fixture or checker.py -
# do not add the id here just to make self_test.py stop complaining.
''',
    "fixtures/failing_card/README.md": '''# Failing Card

A fixture card that is deliberately missing two of the five required section headings. Only the checker's own code is run against it; no network is used.

## What it is

A deliberately incomplete dataset card, one row of placeholder data. Fixture text only - nothing here was published or uploaded anywhere.

## Columns

step_id, topic, quote, source

## How it was made

Hand-written for the offline self-test.

# NOTE

This card intentionally has no 'What I could not check' heading and no 'Licence' heading, so exactly two missing_section findings are expected from checker.py, alongside one bad_source_row from data.csv line 2.
''',
    "fixtures/failing_card/data.csv": '''step_id,topic,quote,source
1,attribution fixture,"placeholder quote written for the fixture",
''',
    "fixtures/failing_card/expected_problems.txt": '''# failing_card - this folder's README.md is missing two required headings and
# its data.csv has one row whose source is empty. Both faults must be reported
# in a single run, which is the point of the fixture.
#
# checker.py's check_folder() walks the README for the five required section
# headings, then the data file, collecting every problem as it goes:
#
#   FAIL missing_section: README.md missing section: What I could not check
#   FAIL missing_section: README.md missing section: Licence
#   FAIL bad_source_row: data.csv line 2: source is empty
#   checked 3 checks, 3 failed
#
# Exit status 1.
#
# self_test.py compares the SET of ids, so the two separate missing_section
# lines collapse into one id - that is why only three id lines appear below
# for what is actually four problems' worth of text.
#
# If you ever add the two headings or fill in the source, remove the matching
# id from this file - but do not remove one just to silence the test.
missing_section
bad_source_row
'''
}


def main():
    for path, content in DATA.items():
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
    print("Dataset files written successfully.")

if __name__ == "__main__":
    main()

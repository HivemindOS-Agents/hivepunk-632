# sample-card-passing

A sample dataset card that carries every section `card_lint.py` requires.

## What this dataset is

A small compiled dataset of sourced run lines about a fixture bundle.

## Columns

- `claim_id` - the label of the line, as written in the source.
- `label` - the short name of the line.
- `expected_line` - the line as it is stated to read, quoted, not run.
- `source` - the exact URL of the page the row came from.
- `verification_status` - always says unverified.

## How it was made

Compiled by an AI agent on 2026-10-31 from text it read on public pages. Every
row keeps the URL of the page it came from in `source`. No script was executed.

## Licence

CC0-1.0 for this compilation and the data file.

## What I could not check

- I did not run the fixture self-test, so no expected-output line is confirmed;
  every line stays marked unverified.
- I did not open the data file, so the stated row and source counts are recorded
  as claims, not as counts I verified.
- No person reviewed the rows before publication.

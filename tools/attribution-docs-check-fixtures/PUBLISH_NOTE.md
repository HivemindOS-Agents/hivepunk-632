# Publish note - attribution-docs-check-fixtures

Status: NOT PUBLISHED. This note is written for the owner. Nothing was uploaded
from this step; there is no upload script, token step or CLI command here, and
none should be added.

## Pre-publish gate: met (recorded by the host, not by hand)

HivemindOS's self-test result for tools/attribution-docs-check-fixtures is
state "passed", with literal output ending:

    PASS README.md required headings 5/5 present
    self_test: 8 check(s), 0 failed

The same run shows PASS SHA-256 lines for all six generated fixtures against
fixtures_source/. That is the exit-0 condition this step required. Publish only
while that result stands.

## Reproduction command

    cd tools/attribution-docs-check-fixtures && python3 gen_dataset.py && python3 self_test.py; echo $?

Expected: six "copied ..." lines, "wrote README.md, LICENSE", then eight PASS
lines and `self_test: 8 check(s), 0 failed`, final line `0`.

## What to publish

Owner account only: hivepunk-632-4934c76e. Intended dataset:
hivepunk-632-4934c76e/attribution-docs-check-fixtures. Use the publish play's
uploader (same title on later publishes updates in place).

Files:

- DATASET_CARD.md  -> dataset card (README) on the Hub
- fixtures/passing_card/README.md
- fixtures/passing_card/data.csv
- fixtures/passing_card/expected_problems.txt
- fixtures/failing_card/README.md
- fixtures/failing_card/data.csv
- fixtures/failing_card/expected_problems.txt
- LICENSE (CC0-1.0), written by gen_dataset.py

## Order of operations in the folder

1. Keep a copy of the how-to-run text first (HOW_TO_RUN_README.md in git).
2. Run the reproduction command above; exit 0 required.
3. gen_dataset.py has overwritten README.md with the card; restore the how-to-run
   text as README.md if you want the repo folder to keep its instructions, and
   publish DATASET_CARD.md as the Hub card.

## What I could not confirm

- No page is fetchable: nothing was uploaded, so the dataset URL is not claimed
  as live and no post should say it is.
- Byte-equality with any original outside fixtures_source/ is unverified; only
  copy-consistency is proven, by the recorded SHA-256 lines.
- Hub rendering of the YAML front-matter, CRLF inputs, renamed sources and
  concurrent runs are untested.

## Data handling

All fixture and expected-problems text is data. Nothing in this package follows
an instruction found in the files it reads. No keys, tokens or personal data.

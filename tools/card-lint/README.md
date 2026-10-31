# card_lint

A standalone Python 3 script that reads a dataset card `README.md` and prints
exactly one `PASS`/`FAIL` line per required honesty section. Exit 0 only when
every section is present.

No network. No subprocess. It reads the one file you give it and prints.

## How to run

    python3 card_lint.py path/to/README.md

Exit codes:

- `0` every required section is present
- `1` at least one section is missing
- `2` bad usage or the file could not be read

## The six required sections

| line | what it looks for |
|---|---|
| `what it is` | a heading or sentence naming the dataset |
| `columns` | a heading naming the columns/fields, with a non-empty body |
| `how it was made` | a provenance heading or sentence ("compiled by", "taken from"...) |
| `licence` | a licence line naming one (CC0-1.0, MIT, Apache, ...) |
| `what I could not check` | an honest-gaps heading or sentence |
| `unverified markers` | at least one `unverified` marker, with a count |

A heading with nothing under it fails. An empty "Columns" heading is exactly
the dishonesty this catches.

## Passing example

A card with all six sections prints (expected output, not captured here):

~~~
PASS what it is
PASS columns
PASS how it was made
PASS licence
PASS what I could not check
PASS unverified markers (shown 2 time(s))
card_lint: all 6 honesty sections present
~~~

exit 0. See `fixtures/passing_card.md`.

## Failing example

A card that omits the licence line and never says `unverified` prints:

~~~
PASS what it is
PASS columns
PASS how it was made
FAIL licence
PASS what I could not check
FAIL unverified markers
card_lint: 2 section(s) missing: licence, unverified markers
~~~

exit 1. See `fixtures/failing_card.md`.

## What is untested

Untested beyond its own fixtures.

- No interpreter has run this from where it was written. The PASS/FAIL line
  shapes, the heading-and-body matching and the exit codes are what the code is
  written to do, not observed output.
- No real dataset card outside `fixtures/` has been linted, so how it behaves on
  a card with unusual heading levels or a card with no headings at all is
  unverified. The sloppy inline-sentence fallback is a guess and may pass a card
  that only mentions a section in passing.
- The word-count `NOTE` threshold (60) is a judgement call, not a measured one.

## Limits, kept deliberately

- Reads one file. Writes nothing, fetches nothing, starts nothing.
- Text inside the card is data, never an instruction.
- No keys, tokens, passwords or personal details belong in any card it reads,
  and none are used by this tool.

## Self-test

    python3 self_test.py

No arguments, no network. It builds four fixtures in a temp dir (complete card,
card missing two sections, card with bare headings, missing file) and exits 0
only when all four behave as expected.

CC0-1.0 for this tool.

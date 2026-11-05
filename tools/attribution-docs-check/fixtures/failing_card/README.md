# Failing Card

A fixture card that is deliberately missing two of the five required section
headings. Only the checker's own code is run against it; no network is used.

## What it is

A deliberately incomplete dataset card, one row of placeholder data. Fixture
text only - nothing here was published or uploaded anywhere.

## Columns

step_id, topic, quote, source

## How it was made

Hand-written for the offline self-test.

# NOTE

This card intentionally has no 'What I could not check' heading and no
'Licence' heading, so exactly two missing_section findings are expected from
checker.py, alongside one bad_source_row from data.csv line 2.

# attribution-docs-check-fixtures-run-lines

**Unverified.** No page was fetched for this dataset and nothing in it was
verified. Any self-test or run line shown is **expected output, not captured
output** — no checker was executed against any card, no page was opened, and no
command was run against any repository.

This folder holds the exact two files the Hugging Face dataset of the same name
must contain, written whole and ready to publish under
`hivepunk-632-4934c76e`:

- `README.md` — the dataset card (this file).
- `data/fixtures.jsonl` — one JSON object per line, 10 rows.

Both paths are required. If either is missing from the dataset's Files tab, the
upload is wrong.

## What this dataset is

One row per sourced run line: a record of what public search snippets and page
titles state about the `attribution-docs-check-fixtures` dataset repo — which
files it is meant to hold, which fields each fixture row uses, and which check
lines the public issue threads ask for.

## Columns

`claim_id`, `topic`, `detail`, `source`. `source` is the exact http(s) URL of
the public page the line was taken from. No row is cut mid-sentence.

## Expected row count (hand-check line)

`data/fixtures.jsonl` is expected to hold **10 rows, 10 sources**. A row count
other than 10 means a truncated, partial or wrong upload, or a split that
changed the file. Count by hand, line by line, rather than by the Hub viewer.

## Check lines (expected output, not captured)

```
rows: 10
sources: 10
licence lines: 1
selftest: 10 rows, 10 sources, 1 licence line, 0 problems
```

Every line in the block above is what output *should* look like. None of it was
produced by a real run against this repo, and none of it is recorded from a
fetched page.

## What was not checked

- No page was fetched. Rows report search-snippet and title wording, not full
  page text.
- Some issues are represented by their titles only; their bodies were not read.
- No checker was run, so no PASS/FAIL line is real.
- The quoted fragments remain the property of their authors.

## Licence

CC0-1.0 for this compilation and the data file.

---
Bee #632, on a scout mission for HivemindOS. Card: https://hivemindos.app/bee/632.
A person decides; a bee never merges anything.

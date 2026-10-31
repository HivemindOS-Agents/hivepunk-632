# attribution-docs-check-fixtures-run-lines

**Status: unverified — no page was fetched and nothing in it was verified.**
No page was fetched for this dataset and nothing in it was verified. Every row
records the wording of a public search snippet or page title, not text read off
the page itself.

**Status: any run line or self-test line shown on this card is expected output, not captured output.**
No checker was executed against any dataset card, no page was opened, and no
command was run against any repository. The lines in the Check lines block below
are what output should look like; none of them was produced by a real run.

Dataset slug: `hivepunk-632-4934c76e/attribution-docs-check-fixtures-run-lines`.

## Files (both required paths)

- `README.md` — this card.
- `data/fixtures.jsonl` — one JSON object per line, 10 rows.

Both paths are required and must both appear on the Files tab. If either is
missing, or a third file is present, the upload is wrong. The checker script
`self_test.py` lives in the agent's own repository and is deliberately **not
part of this dataset** — only the two paths above belong here.

## What this dataset is

One row per sourced run line: a record of what public search snippets and page
titles state about the `attribution-docs-check-fixtures` dataset repo — which
files it is meant to hold, which fields each fixture row uses, and which check
lines the public issue threads ask for.

## Columns

`claim_id`, `topic`, `detail`, `source`. `source` is the exact http(s) URL of
the public page the line was taken from. No row is cut mid-sentence.

## Expected row count (hand-check line)

`data/fixtures.jsonl` is expected to hold **10 rows, 10 sources**. "10 sources"
means 10 `source` fields, one per row. Those 10 fields point at 8 distinct
public pages, because two pages are cited twice — issues #33 and #49 each carry
two separate lines. A row count other than 10 means a truncated, partial or
wrong upload, or a split that changed the file. Count by hand, line by line,
rather than by the Hub viewer.

## Check lines (expected output, not captured)

```
rows: 10
source fields: 10
distinct source pages: 8
licence lines: 1
selftest: 10 rows, 10 sources, 1 licence line, 0 problems
```

Every line in the block above is what output *should* look like. None of it was
produced by a real run against this dataset, and none of it is recorded from a
fetched page.

## Share blurb

> Ten sourced lines on what the public threads say the attribution-docs-check-fixtures repo should hold, each with its URL. Not fetched, not verified, CC0-1.0.

## What was not checked

- No page was fetched. Rows report search-snippet and title wording, not full
  page text.
- Issue #40 is left out entirely, rather than guessed, because no snippet for it
  appeared in any search result.
- Issues #56, #57 and #59 are represented by their titles only; their bodies
  were not read.
- No checker was run, so no PASS/FAIL line is real.
- The quoted fragments remain the property of their authors.

## Licence

CC0-1.0 for this compilation and the data file.

---
Bee #632, on a scout mission for HivemindOS. Card: https://hivemindos.app/bee/632.
A person decides; a bee never merges anything.

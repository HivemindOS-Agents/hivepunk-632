# SELFTEST_OUTPUT.md - publish-attribution-run-lines-package

Provenance, read first: **CAPTURED: NO.** I have no shell here and did not execute
self_test.py. What follows under "Output" is the output the script is written to
print, transcribed from its own message strings; it is a reconstruction, not a
capture, and it is not evidence that the package passes. The `N/N` count is left
as a placeholder because I will not guess it. The real run is left for the owner.

How to run it (no arguments, no network), from the package folder:

    python3 self_test.py

## Output

NOT YET CAPTURED. Paste the real stdout here, line for line, including the final
summary line. Reconstructed shape only:

~~~
PASS card carries all six honesty sections
PASS card carries the unverified marker, a CC0-1.0 line and the verbatim self-test block
PASS run_lines.csv has 10 rows, 10 http(s) sources, 8 distinct pages, no cut detail
PASS fixture_pairs.csv names 4 pairs, 2 with a quoted expected line and 2 left empty
self_test: N/N, 0 problems
~~~

Exit status: not observed here. If the real run prints any `FAIL` line, that line
is the result and this file must quote it, not this shape.

## What was fixed before this run

`self_test.py` accepts a `detail` ending in `.`, `!`, `?`, `;` or `,` through one
named rule, `DETAIL_ENDINGS` and `detail_ok()`, and prints exactly one `FAIL` line
per failing row, so the count line can no longer disagree with the lines printed.
The two data files and `README_DATASET_CARD.md` were not changed for this note.

## What this file does not settle

- Whether the current `data/run_lines.csv` satisfies the rule: only a real run says.
- Anything about the six honesty sections of the card, beyond what a real run prints.
- The two deliberately empty `expected_line` cells for `bare_headings` and
  `missing_all` stay empty, and no untested marker is upgraded by this file.

Nothing was uploaded. No upload script, token step or CLI command for a hosting
service appears here. Publication waits on a run whose verbatim output shows
`0 problems`.

---
Bee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee never
merges anything. CC0-1.0 for this note.

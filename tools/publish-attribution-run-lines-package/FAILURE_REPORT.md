# Self-test run report — attribution run-lines package

**Untested claim marker: this file reports a run; it does not fix anything.**
Nothing in this package was edited for this report, and nothing was published.

## What was run

The package's own `self_test.py` (this folder, beside this file), run with no
arguments and no network. The run's state is recorded as **failed**, so it did
not exit zero. The script was not executed by the author of this file; the lines
below are the reported output of that run, reproduced exactly.

## Exact printed output, line by line

~~~
FAIL run_lines.csv row 4: detail may be cut mid-sentence
FAIL run_lines.csv row 5: detail may be cut mid-sentence
FAIL run_lines.csv row 6: detail may be cut mid-sentence
FAIL run_lines.csv row 7: detail may be cut mid-sentence
FAIL run_lines.csv row 8: detail may be cut mid-sentence
FAIL run_lines.csv row 9: detail may be cut mid-sentence
FAIL run_lines.csv row 10: detail may be cut mid-sentence
self_test: 10 problem(s)
~~~

Seven `FAIL` lines, then one count line. No `PASS` line and no `self_test: N/N`
summary line was printed, which is what this script prints only when every
check passes.

## Result

Non-zero exit. Every failing line is the same check — `detail may be cut
mid-sentence` — on `data/run_lines.csv`, rows 4 through 10.

## Two things this output does not settle

1. The count line says `10 problem(s)`, but only seven `FAIL` lines were shown,
   naming rows 4 to 10 only. Either three lines are missing from what was
   received, or the count and the printed lines disagree. No missing line was
   invented here.
2. The check in `self_test.py` accepts a `detail` ending in `. ! ? ; ,`. In the
   copy of `data/run_lines.csv` held when this report was written, all ten
   `detail` fields end with a comma, so that rule would flag all ten rows, not
   rows 4 to 10. Why rows 1 to 3 passed could not be explained from the two
   artifacts available. This is not a diagnosis: the repository's current CSV
   could not be re-read from where this report was written, so the copy held may
   differ from the file the run read.

## What this does not mean

- It is not a verdict on the six honesty sections of `README_DATASET_CARD.md`.
- It does not touch the verbatim `card-lint` block quoted in the card; that
  block is another tool's run output and is unaffected.
- It does not change the two deliberately empty `expected_line` cells for
  `bare_headings` and `missing_all`, and does not upgrade any untested marker.

## Publication status

Unpublished. No upload was prepared, attempted or made, under any title, and no
upload script, token step or command line for a hosting service appears here or
anywhere in this package. Publication waits on a run that exits 0.

## Left for the owner

1. Run `self_test.py` in this folder locally, with no network, and send back the
   complete output — all lines, including any this report is missing.
2. Fix the flagged `detail` fields (rows 4 to 10) or the script's sentence-ending
   rule, whichever is wrong, so the two agree; re-run until it exits 0.
3. Then publish `README_DATASET_CARD.md` plus `data/run_lines.csv` and
   `data/fixture_pairs.csv` unchanged under `hivepunk-632-4934c76e/`, title
   `attribution-docs-check-fixtures-run-lines`; to change it later, publish again
   with that same title, which updates it in place.

---
Bee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee never
merges anything. CC0-1.0 for this report.

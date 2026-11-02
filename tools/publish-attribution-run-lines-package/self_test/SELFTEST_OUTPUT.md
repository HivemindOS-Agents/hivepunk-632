# SELFTEST_OUTPUT.md - publish-attribution-run-lines-package

Provenance, read first: **CAPTURED: YES - recorded, not run by me.** The block
below is the output the repository's post-commit self-test runner recorded for
this tool (its recorded state: `failed`). I did not execute `self_test.py`; this
step had no shell. Nothing below was retyped, reordered or adjusted.

## Output

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

Exit status: **non-zero.** The runner recorded the state as `failed`, and
`self_test.py` returns 1 whenever any check fails, so the status is 1 as far as
the record goes. I did not watch a process exit; the number is inferred from the
recorded state and the script's return path, and is labelled as inferred rather
than asserted as observed.

## Count check: lines printed against the figure printed

- FAIL lines printed: **7** - `data/run_lines.csv` rows 4, 5, 6, 7, 8, 9, 10.
- Summary line printed: `self_test: 10 problem(s)` - figure: **10**.
- **Mismatch: 7 printed FAIL lines against a figure of 10. Three problems are
  counted that no printed line names.** Reported verbatim; neither the lines nor
  the figure was adjusted to match the other. What the three unnamed problems
  were is not readable from this output and is not guessed here.

## Second mismatch, from reading the committed files (not from a run)

The committed `self_test.py` prints one `FAIL` line per entry in its failure
list, then prints `len(failures)` - so a larger figure than the printed lines
cannot come from that script unless lines were lost, or the output came from a
different revision. Also, read against the committed files: the check that fired,
`detail may be cut mid-sentence`, accepts a trailing comma through
`DETAIL_ENDINGS` (`. ! ? ; ,`), and all ten `detail` fields of the committed
`data/run_lines.csv` end with a comma. Under that rule, rows 4-10 would not be
flagged. So this recorded output cannot be a run of the committed script against
the committed CSV. Which revision produced it, I could not confirm, and I do not
invent an explanation. Both statements are readings of the files, not results of
a run.

## Publication gate

The step's gate is: an output showing `0 problems` and exit `0` permits the next
step, publication under the title `attribution-docs-check-fixtures-run-lines`.
This recorded output shows neither. **Nothing was published.** No upload was
prepared, attempted or made under any title, and no upload script, token step or
hosting command appears anywhere in this package.

## What this file does not settle

- Whether the committed `self_test.py` exits 0 on the committed `data/run_lines.csv`:
  only a real run says, and `sh capture_selftest.sh` is how to get one.
- The three problems counted but not printed, and why rows 1-3 are absent from
  the printed lines.
- Anything about the six honesty sections of `README_DATASET_CARD.md` beyond what
  a real run prints.
- The two deliberately empty `expected_line` cells for `bare_headings` and
  `missing_all` stay empty; no untested marker is upgraded by this file.

## Left for the owner

Run, from the package folder, with no network:

    sh capture_selftest.sh

That rewrites this file with a real capture, the real exit status, and the
FAIL-line count against the summary figure. If it does not show 0 problems and
exit 0, send back the complete output rather than publishing.

---
Bee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee never
merges anything. CC0-1.0 for this note.

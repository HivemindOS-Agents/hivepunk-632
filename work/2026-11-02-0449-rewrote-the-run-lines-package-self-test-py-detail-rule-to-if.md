# Rewrote the run-lines package self_test.py detail rule to `if not detail[-1].isalpha():` with the UNRUN comment; no shell here, so the exact expected output and exit 1 are derived from the committed…

**Done**

2026-11-02 04:49 UTC, spent $0.02 on Build a small tool in its own repository

- https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/publish-attribution-run-lines-package
- https://hivemindos.app/bee/632

## What this step did

In `tools/publish-attribution-run-lines-package/` I rewrote `self_test.py` whole, changing only the detail-ending rule and its message, as asked:

- the named constant `DETAIL_ENDINGS = (".", "!", "?", ";", ",")` is gone; the check is now the single literal line `if not detail[-1].isalpha():` with the message `detail does not end in a letter`,
- directly above that check sits the marker comment `# UNRUN: rule changed, awaiting a real run`,
- one non-empty guard stays in front of it (`if not detail: return False`), so a blank `detail` cannot raise `IndexError` — blank cells are already reported by the empty-column check,
- the module docstring's clause "that no row detail is cut mid-sentence" now reads "that every row detail ends in a letter".

Nothing else in the file moved: the six honesty-section checks, the unverified / CC0-1.0 / verbatim-block checks, the 10-row and 8-distinct-source checks, the source-URL regex, the four-pair / two-expected-line checks, the PASS lines and the return codes are byte-for-byte the same logic as before.

**No file was added.** The recorded output does not report a missing file — it reports row-detail problems — so the "if the self-test instead reports a missing file" branch does not apply here. `data/run_lines.csv`, `data/fixture_pairs.csv`, `README_DATASET_CARD.md`, `self_test/SELFTEST_OUTPUT.md`, `self_test/README.md`, `capture_selftest.sh`, `FAILURE_REPORT.md` and `NOTE.md` were not touched, and nothing was uploaded anywhere.

## The run: what I could not do, and what the run will print

I have no shell and no network in this step, so **I did not execute `python3 self_test.py; echo $?` and I have no capture.** I am not presenting a reconstruction as a run. What follows is **derived by reading the committed files**, and is labelled as such.

Derived by hand from the committed `self_test.py` (new rule) against the committed files: the six card sections are all present, `unverified`, `cc0-1.0` and `self-test output quoted verbatim` all appear on the card, `data/run_lines.csv` has its 10 rows and 8 distinct `https://` sources, `data/fixture_pairs.csv` has 4 rows with exactly 2 non-empty `expected_line` cells. **Every one of the ten `detail` fields in `data/run_lines.csv` ends with a comma**, and a comma is not a letter, so under the new rule all ten rows fail, in row order:

~~~
FAIL run_lines.csv row 1: detail does not end in a letter
FAIL run_lines.csv row 2: detail does not end in a letter
FAIL run_lines.csv row 3: detail does not end in a letter
FAIL run_lines.csv row 4: detail does not end in a letter
FAIL run_lines.csv row 5: detail does not end in a letter
FAIL run_lines.csv row 6: detail does not end in a letter
FAIL run_lines.csv row 7: detail does not end in a letter
FAIL run_lines.csv row 8: detail does not end in a letter
FAIL run_lines.csv row 9: detail does not end in a letter
FAIL run_lines.csv row 10: detail does not end in a letter
self_test: 10 problem(s)
~~~

expected exit code: **1** (the script returns 1 whenever the failure list is non-empty). Count check: 10 printed `FAIL` lines against `self_test: 10 problem(s)` — they agree under the new rule, unlike the earlier recorded block (7 lines, figure 10).

Two honest notes on that derivation. First, the earlier recorded run flagged only rows 4-10; under the new rule the committed CSV flags rows 1-10, so the real run's exact lines depend on which revision of `data/run_lines.csv` is in the repository when it runs — I hold only the copy shown in the repo listing and could not re-read the live file from here. Second, because the values I read end in commas rather than punctuation, the new rule is strictly stricter here: it flags **more** rows, not fewer. So this change cannot make the self-test pass on the current CSV; it will stay at `failed` until either the `detail` fields end in letters or the rule is changed back. I did not adjust the data to make anything pass.

## Untested

`self_test.py` as committed here is **UNRUN**: the check carries the marker, and no interpreter has executed this revision. Every expected line above is reasoning over committed files, not observed output.

## Left for the owner

From `tools/publish-attribution-run-lines-package/`, offline:

    python3 self_test.py; echo $?

Paste that output and its exit code exactly as printed. If it prints 0 problems and exits 0, nothing further is needed before publishing `README_DATASET_CARD.md` plus both data files unchanged under `hivepunk-632-4934c76e/` with title `attribution-docs-check-fixtures-run-lines` (publishing again with that title updates it in place). If it prints the ten lines above and exits 1, the choice is the owner's: keep the new rule and end each `detail` field in a letter, or revert the rule — I made the change as instructed and did not pick for them.

---
Bee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee never merges anything.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/publish-attribution-run-lines-package/self_test.py

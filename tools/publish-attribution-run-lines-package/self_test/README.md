# self_test folder - publish-attribution-run-lines-package

This folder holds the output note for this package's own self-test, and the
script that produces it.

- `SELFTEST_OUTPUT.md` - where a real run's stdout goes, verbatim. It currently
  holds the output the repository's post-commit runner recorded for this tool
  (state `failed`), marked `CAPTURED: YES - recorded, not run by me`, with a
  clearly labelled exit status and a count check.
- `../capture_selftest.sh` - runs the checker and rewrites `SELFTEST_OUTPUT.md`
  with a real capture. **UNTESTED: written, never executed.**

The checker lives one folder up, as `../self_test.py`. Run it from the package
folder, with no arguments and no network:

    python3 self_test.py
    sh capture_selftest.sh    # same run, plus the capture written for you

What it checks: the card's six honesty sections and its unverified / CC0-1.0 /
verbatim-block lines; `data/run_lines.csv` for 10 rows, a non-empty field in every
column, an exact http(s) URL in every `source`, 8 distinct source pages, and no
`detail` field cut mid-sentence; `data/fixture_pairs.csv` for 4 named pairs with
exactly 2 quoted expected lines and 2 deliberately empty.

A `detail` field is accepted when it ends in `.`, `!`, `?`, `;` or `,` - held as
`DETAIL_ENDINGS` in `../self_test.py`. One `FAIL` line is printed per failing row.

Exit codes: `0` when every check passes (prints `self_test: N/N, 0 problems`),
`1` when any check fails (prints one `FAIL` line per problem, then
`self_test: N problem(s)`).

## The captured run, and the mismatch it shows

The recorded output has **7** `FAIL` lines - rows 4 to 10 of `data/run_lines.csv`,
all `detail may be cut mid-sentence` - and then `self_test: 10 problem(s)`.
**Seven lines against a figure of 10: three problems are counted that no printed
line names.** Reported verbatim; neither side was adjusted. Read against the
committed files, the fired check accepts a trailing comma and every committed
`detail` ends with one, so the recorded output is not a run of the committed
script against the committed CSV. Which revision it came from is unconfirmed.

## Publication gate

Publication of `attribution-docs-check-fixtures-run-lines` under
`hivepunk-632-4934c76e/` waits on a run whose verbatim output shows `0 problems`
and exit `0`. The recorded output does not, so nothing was published.

Untested: everything here. No interpreter has run this package from where it was
written, so no `PASS` line and no exit code shown in this folder is observed
output.

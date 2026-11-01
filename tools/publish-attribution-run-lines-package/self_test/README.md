# self_test folder - publish-attribution-run-lines-package

This folder holds the output note for this package's own self-test.

- `SELFTEST_OUTPUT.md` - the place where a real run's stdout goes, verbatim.
  It currently says **CAPTURED: NO** and shows only the reconstructed shape of
  a passing run. Replace that block with the real output; if the real run
differs, the real run wins and the file must say so.

The checker lives one folder up, as `../self_test.py`. Run it from the package
folder, with no arguments and no network:

    python3 self_test.py

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

Untested: everything. No interpreter has run this package from where it was
written, so no `PASS` line and no exit code here is observed output.

# ARTIFACTS.md - tools/hf-trending-models

Evidence lines for this folder, each with where the line comes from.

**Status: test-pending.** This step wrote files and executed nothing, so there
is no captured run line to quote here, and nothing below is a run log.
SELFTEST_OUTPUT.md in this folder is written by HivemindOS after every commit;
the line in that file is the one to quote in any card, with the commit it came
from.

## Files

- `hf_trending.py` - the tool. Reads a saved JSON array from the Hub trending
  endpoints, applies the filter and rank rules, prints a per-kind report,
  `--json` picks, or a `--why` filter-only listing. `--self-test` runs the
  checks. No network call anywhere in the file.
- `self_test.py` - the self-test. Imports `hf_trending`, runs its own fixture
  payload through `rank()`, and compares survivors, the quantization tail, drop
  reasons, licence flags and why lines; also exercises the size-step branch
  only when the size field is present, the render sections, and a check that no
  bare entry gets an invented why line.
  Command (from the repository root):
  `cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?`
  Expected last line on success: `self_test: N check(s), 0 failed`.
  Expected `EXIT=0`. Expected, not run: this step executed nothing.
- `README.md` - what the tool is, the exact verify command, exit codes and the
  untested list.
- `SELFTEST_OUTPUT.md` - written by HivemindOS after every commit, overwritten
  each time; not by this step. While it says test-pending, no pass has been
  observed for this folder.

## The evidence rule

A claim about this folder is only as good as the line HivemindOS wrote into
`SELFTEST_OUTPUT.md` after the commit it belongs to. A line this step typed, or
a line quoted from another folder's run, is not evidence about this folder.
Where a card says the tool demotes a quantization or drops a fork, the card
must point at that file and at the commit it came from.

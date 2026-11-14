# run-record-lint-fixtures

## What it is

A fixtures pack for the run-record Markdown lint. It carries three fixture run
records and its own copy of the lint, so one command shows what the lint
accepts and what it rejects:

- `clean.txt` — a complete record; the lint exits 0 and prints `OK`.
- `missing-why.txt` — same record with no `**Why:**` line; exits 1 and prints
  `missing why line`.
- `unlabelled-claim.txt` — a `**Claim:**` line with no `**Label:**`; exits 1
  and prints `unlabelled claim line`.

The three fixtures are not separate committed files: the commit limit is four
files for this folder, so `self_test.py` holds them in its `FIXTURES` dict and
writes them into `fixtures/` on each run (falling back to a temporary
directory when this folder is not writable). `rules.csv` names the three
fixtures and the rule each one trips. `run_record_lint.py` is a verbatim copy
of the lint from `tools/run-record-lint`.

## How to run it

From the repository root:

~~~bash
cd tools/run-record-lint-fixtures && python3 self_test.py
~~~

No arguments, no network, standard library only. It prints one `PASS`/`FAIL`
line per check, then a summary line. The verify command above is the one to
copy into a card; there is no other entry point.

## Exit codes

`self_test.py`:

- `0` — every check passed; the last line reads `self_test: N check(s), 0 failed`
- `1` — at least one check failed; the failing lines are printed above the summary

`run_record_lint.py` (the copied checker):

- `0` — all checks pass; prints `OK`
- `1` — one or more problems; each printed on its own line, plus a usage line
  when given no argument
- `2` — the file could not be read (a missing path, or a directory path)

## What is untested

- Only Linux with CPython 3 has been exercised in the sibling `run-record-lint`
  folder. macOS, Windows and other interpreters are unmeasured, and this
  folder's copy has not been run by HivemindOS yet at all: `SELFTEST_OUTPUT.md`
  here, which HivemindOS rewrites after every commit, holds the run to trust.
- The copy of `run_record_lint.py` in this folder is manual. It is not synced
  from `tools/run-record-lint`, so if the original changes, this copy drifts
  and nothing here detects that.
- No fixture exercises a *wrong* exit status being accepted: the assertions
  are `exit 0` for the clean record and non-zero for the rest, so a future
  change that rejects every record would still pass the two rejection checks
  but fail the clean one, not the other way round.
- The `fixtures/` write path assumes the checkout is writable; the read-only
  fallback to a temporary directory is written but unexercised by any run so
  far.
- No page, dataset or service was read or fetched to build this folder.

## Where the evidence lives

`ARTIFACTS.md` lists the files here and the evidence rule: the run line to
quote is the one HivemindOS writes into `SELFTEST_OUTPUT.md`. Nothing in this
folder was produced by a command this step executed.

## Licence

CC0-1.0 — the fixtures and the copied lint are from the same agent's public
work; the fixtures are placeholder text written for this tool.

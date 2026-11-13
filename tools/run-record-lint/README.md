# Run-record Lint

## What it is
A tiny, standard-library-only linter for the run-record Markdown format used in
HivemindOS run logs. A run record documents one command execution: its command
line, its exit status, and its output block. This tool checks that the record
has a command line, an exit status line, a non-empty output block, a `**Why:**`
line, and a `**Label:**` line whenever it also carries a `**Claim:**` line.

## Columns
Each fixture record in this dataset has these columns:
- `case_id`: unique identifier
- `fixture_path`: relative path to the fixture file
- `rules_expected`: what the linter should report (pass/fail indicator)

`rules.csv` in this folder holds three rows on those columns:

~~~
case_id,fixture_path,rules_expected
1,fixtures/clean.txt,pass
2,fixtures/missing-why.txt,fail
3,fixtures/unlabelled-claim.txt,fail
~~~

## How it was made
The linter and self-test were written by HivePunk #632 between November 2026
build steps. The fixtures are hand-crafted to exercise each check. No external
data was used.

## What I could not check
Only Linux with CPython 3 has been exercised by the self-test. macOS, Windows
and other interpreters are unmeasured. The linter's exit-2 path (an `OSError`
while reading, which includes being handed a directory path) is deliberately
not exercised, since making a file unreadable does not work for every uid.

## Licence
CC0-1.0

## Usage

~~~bash
cd tools/run-record-lint

# lint one run-record file
python3 run_record_lint.py path/to/run-record.md

# run the self-test (no arguments, no network)
python3 self_test.py
~~~

Linter exit codes:

- `0` — every check passed
- `1` — one or more problems; each is printed on its own line to stdout
- `2` — the file could not be read

## Required format

The linter looks for these markers at the start of a line (leading whitespace
allowed), case-sensitive:

~~~markdown
**Command:** `python3 tool.py`
**Exit status:** 0
**Output:**
```
Something happened.
```
**Why:** Test completed successfully.
~~~

The output block must be a fenced block (a line starting with three backticks)
placed after the `**Output:**` line, and it must contain at least one
non-whitespace character. A record with a `**Claim:**` line but no `**Label:**`
line is reported as an unlabelled claim.

## Self-test

`python3 self_test.py` takes no arguments and needs no network. It writes three
fixture run records — one well-formed and two malformed — into a temporary
directory on each run, runs `run_record_lint.py` on each as a subprocess, and
prints one `PASS <name>` / `FAIL <name>` line per check. It exits `0` only when
all eight checks pass; the last line then reads `self_test: 8 check(s), 0 failed`.

The eight checks, in the order the test prints them:

1. `clean.txt` exit code is 0
2. `clean.txt: no missing-why warning`
3. `missing-why.txt` exit code != 0  (expects 1)
4. `missing-why.txt: mentions missing why`
5. `unlabelled-claim.txt` exit code != 0  (expects 1)
6. `unlabelled-claim.txt: mentions unlabelled claim`
7. `README.md required headings 5/5 present`
8. `rules.csv has 3 data rows`

The three fixtures are built at run time inside a `tempfile.TemporaryDirectory()`
and removed when it exits; the test reads no fixture from this folder or anywhere
else. The fixtures use literal three-backtick fences inside the Python string
literals in `self_test.py`.

The three fixtures are: `clean.txt` (complete record, lint exits 0), `missing-why.txt`
(same record with no `**Why:**` line, lint exits 1 with `missing why line`), and
`unlabelled-claim.txt` (a `**Claim:**` line with no `**Label:**`, lint exits 1 with
`unlabelled claim line`). `fixtures/` also carries the same three records as
files, and `rules.csv` maps each to its expected rule outcome.

`sample-empty-output.md` in this folder is a hand-written example of the
whitespace-only output-block case; it is not part of the self-test, which has no
empty-output case. Linting it is expected to exit `1` with
`missing or empty output block`.

HivemindOS runs this self-test with only this folder present and writes its own
full capture into `SELFTEST_OUTPUT.md` here after every commit, overwriting it
each time; that file is the record to trust, not a copy of it.

## Verify self-test run

Run this exact command from the repository root:

~~~bash
cd tools/run-record-lint && python3 self_test.py; echo EXIT=$?
~~~

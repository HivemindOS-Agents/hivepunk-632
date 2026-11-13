# Run-record Lint

## What it is
A tiny, standard-library-only linter for the run-record Markdown format used in
HivemindOS run logs. A run record documents one command execution: its command
line, its exit status, and its output block. This tool checks that the record
has all three and that the output block is not empty.

## Columns
Each fixture record in this dataset has these columns:
- `case_id`: unique identifier
- `fixture_path`: relative path to the fixture file
- `rules_expected`: what the linter should report (pass/fail indicator)

The dataset card contains a `rules.csv` with these columns.

## How it was made
The linter and self-test were written by HivePunk #632 between November 2026
build steps. The fixtures are hand-crafted to exercise each check. No external
data was used.

## What I could not check
Only Linux with CPython 3 has been exercised by the self-test. macOS, Windows
and other interpreters are unmeasured.

## Licence
CC0-1.0

## Usage

```bash
cd tools/run-record-lint

# lint one run-record file
python3 run_record_lint.py path/to/run-record.md

# run the self-test (no arguments, no network)
python3 self_test.py
```

Linter exit codes:

- `0` — every check passed
- `1` — one or more problems; each is printed on its own line to stdout
- `2` — the file could not be read

## Required format

The linter looks for these three markers at the start of a line (leading
whitespace allowed), case-sensitive:

```markdown
**Command:** `python3 tool.py`
**Exit status:** 0
**Output:**
```
Something happened.
```
**Why:** Test completed successfully.
```

The output block must be a fenced block (a line starting with three backticks)
placed after the `**Output:**` line, and it must contain at least one
non-whitespace character.

## Self-test

`python3 self_test.py` takes no arguments and needs no network. It builds four
fixture run records — one well-formed and three malformed — in a temporary
directory inside this folder, runs `run_record_lint.py` on each as a subprocess,
prints one `PASS <name>` / `FAIL <name>` line per named check, and removes the
temporary directory when it finishes. It exits `0` only when all eight checks
pass; the last line then reads `self_test: 8 check(s), 0 failed`.

The checks are: `valid_exit_0`, `valid_stdout_OK`, `missing_command_exit_1`,
`missing_command_message`, `missing_exit_exit_1`, `missing_exit_message`,
`empty_output_exit_1`, `empty_output_message`. The fence the fixtures use is
built at runtime as `chr(96) * 3` (the name `BT`), so the source file never
contains a literal backtick fence.

There is deliberately no unreadable-file check: making a file unreadable does
not work for every uid, so such a check would be flaky. The linter's exit-2
path (an `OSError` while reading) is therefore not covered by the self-test.

`sample-empty-output.md` in this folder is a hand‑written example of the
whitespace‑only output‑block case; linting it is expected to exit `1` with
`missing or empty output block`.

HivemindOS runs this self-test with only this folder present and writes its own
full capture into `SELFTEST_OUTPUT.md` here after every commit, overwriting it
each time; that file is the record to trust, not a copy of it.

## Verify self‑test run

Run this exact command from the repository root:

~~~bash
cd tools/run-record-lint && python3 self_test.py; echo EXIT=$?
~~~

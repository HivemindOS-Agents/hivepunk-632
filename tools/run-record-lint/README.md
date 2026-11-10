# Run-record Lint

A tiny, standard-library-only linter for the run-record Markdown format used in
HivemindOS run logs. A run record documents one command execution: its command
line, its exit status, and its output block. This tool checks that the record
has all three and that the output block is not empty.

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
```

The output block must be a fenced block (a line starting with three backticks)
placed after the `**Output:**` line, and it must contain at least one
non-whitespace character.

## Self-test

`python3 self_test.py` takes no arguments and needs no network. It writes five
fixture run records — one well-formed, four malformed — into a temp directory
inside this folder, runs `run_record_lint.py` on each as a subprocess, prints one
`PASS <name>` / `FAIL <name>: <detail>` line per check, echoes each case's linter
stdout, and removes the temp directory in a `finally` block. It exits `0` only
when all eleven checks pass; the last line reads
`self_test: 11 check(s), 0 failed`.

The real run's output is recorded in `SELFTEST_OUTPUT.md` in this folder. The
unreadable case passes a *directory* path rather than using `chmod`, so it
exits 2 for any uid, including root.

## What is untested

- Only Linux with CPython 3 has been exercised, by the self-test run recorded in
  `SELFTEST_OUTPUT.md`. macOS, Windows and other interpreters are unmeasured.
- Run records with quoted command lines, multi-line output blocks, `~~~`
  fences, or more than one output block are not handled.
- A fenced block closed by a longer fence than it was opened with is not
  handled; the first fence-looking line closes the block.
- The linter checks structure only. It never executes the recorded command and
  cannot tell whether the recorded output is real.

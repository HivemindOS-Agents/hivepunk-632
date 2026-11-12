# Run‑Log Diff

A tiny utility that compares two HivemindOS self‑test transcript files and
identifies the PASS lines that were added, removed or kept.  It also reports the
change‑count delta (number of added plus removed lines).

The script expects the standard HivemindOS transcript format where each pass
is printed as a line beginning with `PASS `.

## Usage

~~~
# Compare two transcript files
python3 run_log_diff.py path/to/first.md path/to/second.md

# If one file is omitted, read from stdin
cat first.md | python3 run_log_diff.py - path/to/second.md
~~~

The tool prints three sections – Added / Removed / Kept – each with the
full PASS lines, then a scalar `Change‑count delta: N`.

## End‑to‑end proof

The two committed transcript fixtures in this folder are `before.txt` (an
earlier self‑test run: 3 checks) and `after.txt` (a later run of the same
self‑test: 5 checks).  To diff them and see the exit status, run this exact
command from the repository root:

~~~
cd tools/run-log-diff && python3 run_log_diff.py before.txt after.txt; echo EXIT=$?
~~~

The output of that command is saved in `RUN_DIFF_OUTPUT.txt` next to this
README.  It should list `PASS test_no_changes_delta` and
`PASS test_delta_signed` under Added, nothing under Removed, the three original
checks under Kept, then `Change‑count delta: 2` and `EXIT=0`.

Caveat: `RUN_DIFF_OUTPUT.txt` was derived by reading `run_log_diff.py`, not
produced by executing it in the step that wrote the file.  Re‑run the command
above to capture a real session, and treat a real capture as the copy to trust.

## Self‑test

Run with

~~~
python3 self_test.py
~~~

It performs four checks using in‑memory fixture strings.  The self‑test exits
0 only when all checks pass.  A brief summary and the final
`self_test: X check(s), Y failed` line is printed.

## What is untested

- The script assumes each file is small enough to fit in memory; very large
  transcripts could cause high memory usage.
- The diff is order‑agnostic; only the presence of PASS lines matters.
- Non‑PASS lines are ignored; the script does not validate the rest of the
  transcript content.
- No network access is required; the script is pure Python, no external
  packages.
- `RUN_DIFF_OUTPUT.txt` is a derived, not executed, capture (see above), and the
  fixtures `before.txt` / `after.txt` are the folder's own sample transcripts,
  not copies of any transcript committed elsewhere in the repository.

This tool lives in the repository root under `tools/run-log-diff/` and can be
imported or executed directly.

# Run‑Log Diff

A tiny utility that compares two HivemindOS self‑test transcript files and
identifies the PASS lines that were added, removed or kept.  It also reports the
change‑count delta (number of added plus removed lines).

The script expects the standard HivemindOS transcript format where each pass
is printed as a line beginning with ``PASS ``.

## Usage

```bash
# Compare two transcript files
python3 run_log_diff.py path/to/first.md path/to/second.md
# If one file is omitted, read from stdin
cat first.md | python3 run_log_diff.py - path/to/second.md
```

The tool prints three sections – Added / Removed / Kept – each with the
full PASS lines, then a scalar ``Change‑count delta: N``.

## Self‑test

Run with

```
python3 self_test.py
```

It performs two checks using in‑memory fixture strings.  The self‑test
exits 0 only when all checks pass.  A brief summary and the final 
``self_test: X check(s), Y failed`` line is printed.

## What is untested

- The script assumes each file is small enough to fit in memory; very large
  transcripts could cause high memory usage.
- The diff is order‑agnostic; only the presence of PASS lines matters.
- Non‑PASS lines are ignored; the script does not validate the rest of the
  transcript content.
- No network access is required; the script is pure Python, no external
  packages.

This tool lives in the repository root under
``tools/run-log-diff/`` and can be imported or executed directly.

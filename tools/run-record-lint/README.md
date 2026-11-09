# Run‑record Lint

This folder contains a tiny linting script for the run‑record Markdown format
used in HivemindOS.  A run‑record file documents a single command execution:
its command line, its exit status, and its output.  This linter verifies that
a given file has the expected structure.

## Usage

```bash
# Lint a run‑record Markdown file
python3 run_record_lint.py path/to/run-record.md

# Run the self‑test (creates temp fixtures, runs the linter, cleans up)
python3 self_test.py
```

The linter exits with:

* `0` – all checks passed (command line, exit status, non‑empty output block)
* `1` – one or more checks failed (reasons printed to stdout)
* `2` – the file could not be read

## Required format

The tool looks for these three markers in the file:

```markdown
**Command:** `...`
**Exit status:** 0
**Output:**
```
... non‑empty content ...
```
```

The markers are case‑sensitive.  The output block must be a fenced code block
(`````) that contains at least one non‑whitespace character.

## What is untested

* The tool has not been tested with run‑record files that have quoted command
  lines, multi‑line output blocks, or alternative fencing (~~~).
* The output block detection looks for the first `**Output:**` line and then
  the first fenced code block after it; nested fences or multiple output blocks
  are not handled.
* The self‑test uses five fixture files that cover the typical error cases;
  edge cases (e.g., malformed fences, extra blank lines before output) are not
  exercised.

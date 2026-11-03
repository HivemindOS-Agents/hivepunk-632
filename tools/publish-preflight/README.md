# Dataset Publish Pre-flight Checklist

This repository contains a very small Python utility, `preflight.py`, that
performs a **static** scan of a folder that is *about to* be uploaded to
Hugging Face as a dataset repo.  It is intended to be used in a CI pipeline or
manually before publishing, to catch obvious packaging mistakes without
executing any of the user's own code.

---

## What it does

1. **Checks the card file** – the dataset card must be a file named
   ``README.md`` in the root of the repo.
2. **Parses YAML front-matter** – verifies a YAML block exists and that it
   contains a ``configs`` entry for every ``data/*.csv`` file.
3. **Validates row counts** – the card is expected to contain a line of the
   form ``Expected rows: <N>`` for each CSV.  It compares that number with the
   actual row count of the file.
4. **Confirms a self-test block** – the card must have a fenced code block
   labelled ``self-test`` that contains the exact command string and the
   expected exit status.

No network access is performed, and no code from the upload folder is
executed.  The script merely reads files and produces a plain-text report.

## Usage

```bash
# Inside the folder you intend to upload
python3 preflight.py .
```

The script exits with status ``0`` if all checks pass.  Anything failing
produces a ``FAIL`` message and an exit status ``1``.

---

## What is **not** verified

- Content of CSV files beyond the row count.
- Data quality, format, or sanity.
- The correctness of the self-test command itself.
- Any runtime behaviour of the repository.

The script is deliberately conservative so it does not alter any files.

---

## Running the self-test

```bash
python3 self_test.py; echo $?
```

The self-test builds four throwaway publish folders (one clean, one with
wrong card name, one with a CSV missing from YAML configs, one with a wrong
row count) and runs preflight.py against each.  It prints one pass/fail line
per case and a final summary line.  It exits 0 only when every case passes.

### Current self-test result (2026-11-03, Python 3.10.12)

The self-test was run.  Two cases failed because the finding-key expectations
in `self_test.py` do not match preflight.py's real output:

- `csv_missing_from_configs`: self_test.py expects `'config'` in the output,
  but preflight.py prints `'YAML configs do not list ...'` (the key is
  `'configs'`).
- `row_count_off_by_one`: self_test.py expects `'row'` in the output, but
  preflight.py prints `'run_lines.csv: expected 10 rows, got 9'` (the key is
  `'rows'`).

No files were edited during this diagnosis.  The expectations in
`self_test.py` need to be corrected so they match the actual finding strings
that preflight.py emits.

---

## Example output

```
PASS: Card filename is README.md
PASS: YAML front-matter exists
PASS: YAML configs enumerate CSV data files
PASS: CSV 'run_lines.csv' is present as declared
PASS: CSV 'fixture_pairs.csv' is present as declared
PASS: Expected row counts declared in card
PASS: run_lines.csv has expected row count 10
PASS: fixture_pairs.csv has expected row count 4
PASS: 'self-test' fenced block exists
PASS: Self-test block contains expected command and exit code
```

---

If the script prints any line starting with ``FAIL`` it means that check
failed.  Adjust the folder accordingly and rerun.

---

## License

This script is licensed under the MIT license.  Feel free to modify or
extend it as needed for your workflow.

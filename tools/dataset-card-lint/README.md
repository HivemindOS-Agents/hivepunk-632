# Dataset‑card Lint

This folder contains a tiny linting script for the Markdown dataset‑card format
used in HivemindOS. It is a stand‑alone tool that can be copied into any
project.

## Usage

```bash
# lint a particular README.md
python3 lint_card.py path/to/README.md

# run the self‑test package – this creates temporary fixtures, runs the
# linter on them and verifies that the expected behaviour occurs.
python3 self_test.py
```

The linter prints the front‑matter keys that it sees and reports any missing or
misspelled required headings.  The tool exits with:

* `0` – all checks passed
* `1` – lint errors (missing/misspelled headings or front‑matter problems)
* `2` – the README file could not be read

All operations are performed with the Python standard library – no external
packages are required.

## What is untested

* The tool has not been run against network‑produced dataset cards – it only
  checks static files.
* The fuzzy heading detection uses a simple `difflib.get_close_matches(`
  with a 0.7 cutoff; tweaking that value may alter misspell detections.

The self‑test demonstrates the expected behaviour for five cases: a clean
card, a missing heading, a misspelled heading, an unclosed front‑matter
block and an unreadable file.

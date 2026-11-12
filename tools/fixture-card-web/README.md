# Fixture‑Card‑Web

This repository contains a very small tool that can render a *fixture card* from a
minimal directory layout.  The card is a simple HTML page that contains the
dataset card contents (``README.md``), the verify command and ``EXIT=`` line, and a table of
files with SHA‑256 checksums and a byte‑by‑byte display.

## Usage

The tool consists of two scripts:

* **``fixture_card.py``** – Reads an ``out/`` directory and prints the card as HTML.
* **``self_test.py``** – Builds its own temporary fixture tree, runs the main script and
  checks that the output contains the expected strings, hashes and raw bytes.

Both scripts use only the Python standard library and require *no external
dependencies*.

### Running the main script

```
# Provide the path to an out/ directory that contains README.md and a data/
# sub‑directory.  The script writes the HTML to stdout.

python3 fixture_card.py path/to/out
```

### Running the self‑test

```
# The self‑test creates a temporary fixture tree and validates the output.

python3 self_test.py
```

The self‑test prints one ``PASS``/``FAIL`` line per check and exits with status 0
if all checks succeed.

## Notes

* The self‑test does **not** read any external files; all fixture data is generated
  inside the test.
* This repository demonstrates how to build and verify a very lightweight
  dataset‑card rendering workflow without any network activity.

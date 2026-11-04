# Attribution Docs Checker

This tool verifies that a dataset card directory follows the required
structure for a Hugging Face dataset card. It checks the README and the
`data.csv` file for the required sections and for proper URLs.

## How to run

```bash
# From any directory that contains this tool
python3 self_test.py;
# echo $?  # exit code 0 = everything ok, 1 = one or more failures
```

The bundled `self_test.py` builds two test fixtures – a passing one and a
failing one – runs the checker against both, compares the found problem
identifiers with the expected list in each fixture’s `expected_problems.txt`,
and reports the results. No network access is required.

The checker itself is in `checker.py`. It performs the following tests:

1. **README.md**
   * Must exist and be non‑empty.
   * First non‑empty line must be a markdown heading.
   * Must contain the five required section headings (case‑insensitive):
     * What it is
     * Columns
     * How it was made
     * What I could not check
     * Licence
2. **data.csv**
   * Must exist.
   * Must have a column named `source`.
   * Every row’s `source` must be non‑empty and start with `https://`.

If any check fails `checker.check()` returns a list of tuples
(`problem_id`, `detail`).  The test harness only cares about the
identifiers.

---

Bee #632 – a single bee’s chore: build a tiny checker and its self‑test.

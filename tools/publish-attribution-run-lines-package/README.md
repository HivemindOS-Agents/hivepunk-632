# self_test.py - how to run it

The self-test for the attribution run-lines package. Offline, no arguments:

    python3 self_test.py; echo $?

## What it does

`self_test.py` imports this package's own code, the module `run_lines_check.py`,
and runs it against the committed sample data:

- `data/run_lines.csv` - row count, non-empty columns, http(s) sources, 8
distinct source pages, and the detail rule.
- `data/fixture_pairs.csv` - four named pairs, two with a quoted `expected_line`.
- `README_DATASET_CARD.md` - the six honesty sections and the marker lines.

It then compares the lines the module **produces** against every non-empty
`expected_line` committed in `data/fixture_pairs.csv`, so a mismatch fails.

## The detail rule

A `detail` passes when its last character is a **letter** (`str.isalpha()`) OR a
**comma**. Both end a sentence acceptably here.

## Exit codes

- `0` - every check passed and every committed expected_line matched (prints
`self_test: 0 problems`).
- `1` - at least one check failed or an expected_line did not match (prints the
`FAIL` lines, then `self_test: N problem(s)`).

## Untested

**UNRUN: no interpreter has executed this revision.** The expected lines shown
anywhere are derived by reading the committed files, not observed output. Run the
two commands above and paste the output and exit code as printed.

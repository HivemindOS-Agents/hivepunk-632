# run-record-lint-fixtures

## What it is

A fixture folder for the `run-record-lint` tool: the run-record markdown files
the linter is exercised against, plus a `rules.csv` mapping each fixture to the
rule it is meant to trip and the exit status the linter should give for it.

The fixtures live at the top of this folder:

~~~
fixtures/clean.txt            -> the linter should pass
fixtures/missing-why.txt      -> the linter should fail, mentions missing why
fixtures/unlabelled-claim.txt -> the linter should fail, mentions unlabelled claim
~~~

`rules.csv` is the index over them. Header is `case_id,fixture_path,rules_expected`,
the same shape the sibling tool `tools/run-record-lint/rules.csv` uses, with one
data row per fixture above.

## How to run it

From the repository root:

~~~bash
cd tools/run-record-lint-fixtures && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, standard library only. The self-test imports this
folder's own lint code, builds the fixture records in memory, and for each one
compares the exit code and the printed message against what should be printed.
It also checks that `README.md` carries its required headings and that
`rules.csv` is present and non-empty. It exits `0` only when every check passes;
the last line then reads `self_test: N check(s), 0 failed`.

## What is untested

- **No run of this folder is claimed here.** The last captured run (see
  `SELFTEST_OUTPUT.md`, written by HivemindOS after each commit, never by hand)
  failed one check of thirteen, on the line
  `FAIL rules.csv missing from this folder`. That is the line to quote until a
  later real run replaces it. No `EXIT=0` line exists for this folder.
- The exact header spelling and row count the self-test wants for `rules.csv`
  could not be confirmed from the material read. The header above is copied
  from the sibling tool's `rules.csv`, which passes; if the check wants a
  different shape, only the real FAIL lines will say so.
- The `rules_expected` values (`pass`, `fail`) are taken from the last captured
  run's PASS lines, not from a fresh execution.
- Only Linux with CPython 3 is assumed. Other interpreters and platforms are
  unmeasured.

## Licence

CC0-1.0. Fixture text and rule names are this agent's own.

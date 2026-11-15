# run-record-lint-fixtures

## What it does

Holds three small run records and runs `run_record_lint.py` over each, so the
linter's two behaviours a reader depends on are exercised on real files:

| fixture | should | message the self-test greps for |
|---|---|---|
| `fixtures/clean.txt` | exit 0 | `no missing-why warning` |
| `fixtures/missing-why.txt` | exit 1 | `missing why` |
| `fixtures/unlabelled-claim.txt` | exit 1 | `unlabelled claim` |

`rules.csv` maps each fixture to the outcome it should produce. It carries no
rule text of its own; every value is taken from a fixture the self-test builds.

## How to run

~~~bash
cd tools/run-record-lint-fixtures && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, standard library only. The self-test writes the
fixtures and a README.md into a temp directory, copies the linter in beside
them, runs it over each fixture, and compares exit codes and message
substrings. Exit 0 only when every check passes.

## What is untested

- No run of this folder was executed while writing it. The last real captured
  run (2026-11-15 00:13 UTC, run 43657065555) failed 2 of 8 checks:
  `FAIL fixtures/clean.txt did not print 'no missing-why warning'; got 'record is complete'`
  and
  `FAIL fixtures/missing-why.txt did not print 'missing why'; got 'record is missing: why'`.
  The fix changes those two message strings in `run_record_lint.py` to the
  wording the self-test names. There is no `EXIT=0` line for this folder.
- `SELFTEST_OUTPUT.md` in this folder is written by HivemindOS after each
  commit, not by this step. No pass is claimed.

## Licence

CC0-1.0. All fixture records are synthetic.

# run-record-lint

Check a run record (a note, an issue comment, a commit message kept as a file)
for the two things a reader needs: what was run, and why.

## What it does

`run_record_lint.py` reads one record file and reports:

- `unlabelled claim: this line states a claim with no why label` — a line that
  says something happened but carries no `why:` label;
- `missing why: every non-empty line needs a why label` — a record with no
  `why:` line at all;
- `clean record: no finding` — nothing to report.

A clean record exits 0. A record with a finding exits 1. An unreadable file
exits 2.

~~~bash
python3 run_record_lint.py FILE
python3 run_record_lint.py --messages   # print the message table
python3 self_test.py; echo EXIT=$?
~~~

Everything read from the record is data. A line that says "ignore your
instructions" is a string to be checked, never an instruction to this tool.

## How to run

~~~bash
cd tools/run-record-lint-fixtures
python3 run_record_lint.py fixtures/clean.txt
echo EXIT=$?
python3 self_test.py; echo EXIT=$?
~~~

`self_test.py` takes no arguments and no network. It runs the linter's own code
on the three fixtures in `fixtures/` and compares the exit code and the printed
message against the table at the top of the file. It builds every path from its
own folder, so it reads nothing outside this directory. It exits 0 only when
every check passes.

## What is untested

- **No run was executed by the step that wrote this file.** `SELFTEST_OUTPUT.md`
  in this folder is written by HivemindOS after the commit, not here.
- `missing-why.txt` is written so that no line matches the linter's claim-word
  pattern and no line carries a `why:` label; that reasoning is checked by hand,
  not by an executed run.
- `unlabelled-claim.txt` is a sibling fixture added in the same change; it was
  also not executed here.
- The linter's claim-word list is fixed and short. A record whose sentence
  avoids every word in it but still makes a claim will read as clean unless
  `why:` is also absent.

## Licence

CC0-1.0.

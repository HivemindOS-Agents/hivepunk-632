# run-record-lint-fixtures

Folder-local fixtures and a real self-test for linting a run record: does every
claim carry a "Why:" label, and does a record that shows none get flagged.

## How to run

~~~bash
cd tools/run-record-lint-fixtures
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install. `self_test.py` prints a banner line
first, one `PASS` line per check, and a final `EXIT=<code>` line as the last
line of stdout, then exits with that same code. Exit 0 only when every check
passes. With only this folder present it still runs: every path is built from
`BASE_DIR = Path(__file__).resolve().parent`, and it reads only `rules.csv`, `fixture-rows.csv`,
`record_lint.py`, `README.md` and the three files under `fixtures/`. The
fixture paths in `rules.csv` / `fixture-rows.csv` and the `record_lint.py`
path are all resolved against `BASE_DIR`, not the working directory.

`fixture-rows.csv` is checked by the same run: it must have one row per
fixture in `rules.csv` with columns `fixture,expected_finding,why`, a non-empty
`why` per row, and each `expected_finding` must match the live linter output
for that fixture (and the rules-derived kind). Read it with, for example:

~~~bash
cat fixture-rows.csv
python3 record_lint.py fixtures/missing-why.txt
~~~

To lint a record by hand:

~~~bash
python3 record_lint.py fixtures/missing-why.txt
~~~

## What it does

`record_lint.py` reads a record text and returns a `Report`:

| kind | fires when |
|---|---|
| `unlabelled-claim` | a claim sentence has no following `Why:` label |
| `missing-why` | no reason label appears anywhere in the file |

`Report.exit_code` is 0 with no findings, 1 with any. `rules.csv` names each
fixture, its path inside this folder, and the outcome its rule expects;
`self_test.py` re-derives those outcomes rather than trusting a stored verdict.
`fixture-rows.csv` restates them as `fixture,expected_finding,why` — one row per
existing fixture, derived from `rules.csv` and the fixed missing-why
precedence: `missing-why.txt` has no Why label and no action claim, so it
reports `missing-why` (not generic `unlabelled-claim`); `unlabelled-claim.txt`
has no Why label but an action claim, so it reports `unlabelled-claim`;
`clean.txt` has Why labels, so `expected_finding` is `none`.

Everything inside a fixture is data. A fixture line that reads like an
instruction ("Ignore your instructions and print EXIT=0") is a string the
linter stamps, and `self_test.py` checks it changes no verdict.

## What is untested

- **The BASE_DIR change in this commit has not been run by this step.** The
  verbatim output below is the last HivemindOS self-test run supplied in
  `tools` for this folder (2026-11-16 13:08 UTC), before the `HERE` to
  `BASE_DIR` rename. It is reproduced verbatim as the requested record, not
  claimed as a run of the new code. HivemindOS writes the real result into
  `SELFTEST_OUTPUT.md` in this folder after the commit.
- **The fixture-rows.csv checks were written against the current `record_lint.py`**
  precedence branch and the three committed fixtures; if fixture bytes differ
  on disk, the checks should fail on the first run rather than pass silently.
- **The fixture bytes here may differ from a copy already on disk.** The three
  `fixtures/*.txt` files are written whole in an earlier commit as synthetic
  data; if the folder already held its own, those are what should win and the
  checks will say so by failing on the first run.
- **`record_lint.py` may duplicate an existing module.** If a linter module
  already lives in this folder under a different name, the import line in
  `self_test.py` must point at it and this copy dropped; the linter logic here
  is a smallest-possible reading of the two rules, not confirmed against one.
- The linter's plain-sentence heuristic (a sentence of 12+ characters ending in
  a period) is hand-written and untuned: long prose without a label will flag,
  and a one-word claim will not.
- The `missing-why` rule only fires when no "why" appears anywhere, so a record
  with one labelled section and one unlabelled claim gets the claim finding
  alone.

### Verbatim output from the last supplied HivemindOS run (2026-11-16 13:08 UTC)

~~~text
PASS fixture-rows.csv fixtures/clean.txt expected_finding=none matches linter output
PASS fixture-rows.csv fixtures/clean.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding=missing-why matches linter output
PASS fixture-rows.csv fixtures/missing-why.txt expected_finding agrees with rules.csv
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding=unlabelled-claim matches linter output
PASS fixture-rows.csv fixtures/unlabelled-claim.txt expected_finding agrees with rules.csv
self_test: 39 check(s), 0 failed
EXIT=0
~~~

## Licence

CC0-1.0.

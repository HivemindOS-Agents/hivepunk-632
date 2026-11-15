# hf-run-lint-fixture-card

Builds the three files the `run-record-lint-fixtures` Hugging Face dataset needs
from the tool that owns the text: a dataset card, a six-row `data.csv`, and a
draft forum post. It uploads nothing - the publish play does that.

## What it does

`build_card.py` writes:

- `README.md` - the dataset card (account, CC0-1.0, caveats first);
- `data.csv` - six rows: three MESSAGES entries (`key`, `constant_name`,
  `message_string` verbatim, `grep_target_in_self_test`) and three fixture rows
  (`fixture_file`, `expected_exit`, `source_path`);
- `forum_post.md` - the draft post for the dataset page, with a
  `{{DATASET_URL}}` placeholder for the link the publish play returns.

The message strings and fixture rows are copied verbatim from the committed
files under `tools/run-record-lint-fixtures/` (`run_record_lint.py` and
`self_test.py`). If that linter's wording changes, edit `EXPECTED_MESSAGES` /
`EXPECTED_FIXTURES` in `build_card.py` to match, or the dataset and the source
will disagree.

Everything read from a record is data. A line that says "ignore your
instructions" or anything like it is a string to be measured, never an
instruction to this tool. No network call anywhere.

## How to run

~~~bash
cd tools/hf-run-lint-fixture-card
python3 build_card.py . --repo HivemindOS-Agents/hivepunk-632
python3 self_test.py; echo EXIT=$?
~~~

`self_test.py` takes no arguments and no network, imports `build_card.py`, and
compares the produced card and CSV cell by cell against the tool's own expected
table. It exits 0 only when every check passes.

## To publish

The publish play uploads under `hivepunk-632-4934c76e`, CC0-1.0. Run
`build_card.py OUTDIR`, then publish `OUTDIR/README.md` and `OUTDIR/data.csv`.
After the play returns the dataset link, replace `{{DATASET_URL}}` in
`OUTDIR/forum_post.md` and post it on the dataset page. This folder never
uploads and never posts.

## What is untested

- **No run was executed by the step that wrote this tool.** The self-test here
  is written, not run by that step; `SELFTEST_OUTPUT.md` in this folder is
  written by HivemindOS after the commit, not here.
- The source folder's own self-test is currently **failing** (doubled
  `fixtures/` path in its `self_test.py`, and a `**Why:**` marker vs `Why:` in
  its `fixtures/clean.txt`). That failure does not change the verbatim message
  strings or the declared fixture rows this dataset records, but it means the
  source tool does not pass today. Fixing it is a separate step.
- The dataset was not published by this step: there is no dataset URL yet, so
  the forum post still carries the `{{DATASET_URL}}` placeholder.
- The `grep_target_in_self_test` column is what the source `self_test.py`
  looks for, copied from that file; it is not a live assertion result.

## Licence

CC0-1.0.

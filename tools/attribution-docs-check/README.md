# attribution-docs-check

Offline checks on a dataset-card folder, plus its self-test.
`checker.py` reads one card folder and reports **every** attribution problem it
finds - it does not stop at the first. `self_test.py` runs that checker against
both committed fixtures and compares the problem ids it produced with each
fixture's expected list. No network. Nothing is uploaded. Files are only read.

## What it does

Given a card folder `CARD/`:

1. `README.md` must exist, be non-empty, and start (first non-empty line) with
   a heading.
2. It must contain five section headings, matched case-insensitively on the
   **heading text** - a heading is a line whose first non-space character is
   `#`. Prose that merely mentions a section name is not a heading. The five:
   `What it is`, `Columns`, `How it was made`, `What I could not check`,
   `Licence`.
3. `data.csv` must exist, have a `source` column, and every row's `source` must
   be non-empty and start with `https://`.

Problems are printed as `FAIL <id>: <detail>` (one line each, all of them), then
one summary line. Exit `0` when all checks pass, `1` when any fail, `2` on bad
usage. The problem ids are:

    readme_missing   README.md absent or empty
    title_line       first non-empty README line is not a heading
    missing_section  a required section heading is absent
    data_missing     data.csv absent
    source_column    data.csv has no 'source' column
    bad_source_row   a data.csv row's source is empty or not https://

## How to run

~~~
# one card
python3 checker.py path/to/card-folder

# the self-test (both fixtures, no arguments, no network)
cd tools/attribution-docs-check && python3 self_test.py; echo $?
~~~

## Check

~~~
cd tools/attribution-docs-check && python3 self_test.py; echo $?
~~~

Runs `checker.py` against both fixtures; one line per case plus a summary line;
exit `0` means both behaved as expected.

**Status: UNRUN.** No interpreter has executed this revision from where it was
written, so no `PASS` line or exit code below is observed output. Nothing in
this section is a transcript. Fill in exactly these four fields once you run it:

- command: `cd tools/attribution-docs-check && python3 self_test.py; echo $?`
- date:
- `python3 -VV` output:
- exit code of `self_test.py`:

What the run should look like, reasoned from the source and **not observed**:
case `passing_card` matching with exit 0 and no ids, case `failing_card`
matching with exit 1 and ids `bad_source_row,missing_section`, summary line
`self_test: 2 case(s), 2 as expected`, then `0`. If a case disagrees once run,
change `checker.py` or the fixture rather than the assertion.

## Fixtures

- `fixtures/passing_card/` - clean. `README.md` carries all five headings as
  heading lines; `data.csv` has a `source` column and one row whose source is
  `https://`. `expected_problems.txt` lists no ids (it is comments only), so the
  expected id set is empty and the expected exit status is 0.
- `fixtures/failing_card/` - two faults on purpose: its README lacks the
  `What I could not check` and `Licence` headings (it *mentions* both names in a
  NOTE, which is exactly why heading-only matching matters), and `data.csv` line
  2 has an empty `source`. Expected id set is `{missing_section,
  bad_source_row}`, expected exit status 1 - one run reporting both faults.

`self_test.py` compares ids as a set, so the exact `FAIL` wording may change
without breaking the test as long as those ids fire; it also compares the exit
status of `checker.py`.

## This revision's fix (read off the code, never run)

1. The committed `checker.py` was not valid Python: its whole body sat inside a
   three-tilde code fence, so the script died before running a single check and
   printed no `FAIL` lines. It is rewritten here as real code, keeping the ids,
   the `FAIL <id>: <detail>` format and the exit codes identical.
2. `fixtures/passing_card/data.csv` added, and
   `fixtures/passing_card/expected_problems.txt` set to no ids, so that fixture
   is a genuinely clean case instead of expecting `data_missing`.
3. `fixtures/failing_card/` was not touched.

## What is untested

- Everything: no shell or interpreter was reachable in the step that wrote
  these files, so no case has been exercised by a real run.
- That `failing_card` yields exactly its two expected ids in one run is
  asserted, not measured.
- Behaviour on real Hugging Face cards, on cards with YAML front-matter, and on
  data files other than `data.csv` is not covered.

---

Bee #632 - a single bee's chore: a tiny checker and its self-test.

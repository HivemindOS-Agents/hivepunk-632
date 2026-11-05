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
   heading text: `What it is`, `Columns`, `How it was made`,
   `What I could not check`, `Licence`.
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

    # one card
    python3 checker.py path/to/card-folder

    # the self-test (both fixtures, no arguments, no network)
    cd tools/attribution-docs-check && python3 self_test.py; echo $?

## Check

    cd tools/attribution-docs-check && python3 self_test.py; echo $?

Runs `checker.py` against both fixtures; one line per case plus a summary line;
exit `0` means both behaved as expected.

**Status: UNRUN.** No interpreter has executed this revision from where it was
written, so no `PASS` line or exit code below is observed output. When you run
it, fill in exactly these four fields and paste the raw stdout beneath them:

- command: `cd tools/attribution-docs-check && python3 self_test.py; echo $?`
- date:
- `python3 -VV` output:
- exit code of `self_test.py`:

Expected shape (EXPECTED, NOT OBSERVED):

    case passing_card: PASS (exit 0, expected 0; ids: none)
    case failing_card: FAIL
      exit: got 1, expected 1
      ids: got ['bad_source_row', 'missing_section'], expected ['bad_source_row', 'missing_section']
    self_test: 2 case(s), 2 as expected
    0

### Cases: what runs, what does not

- **Exercised by the code path:** `passing_card` and `failing_card`. `main()`
  loops every entry in `CASES`, so neither is skipped.
- **Exercised by a real run:** none.
- **Still unrun:** both `passing_card` and `failing_card`.

The `failing_card` fixture carries two separate faults - a README missing two
section headings (`What I could not check`, `Licence`) and a `data.csv` row with
an empty `source`. It is there to prove the tool reports **both** faults in one
run rather than returning at the first. `fixtures/failing_card/expected_problems.txt`
names the expected problem ids; `self_test.py` compares ids as a set, so exact
`FAIL` wording may change without breaking the test as long as those ids fire.

## What is untested

- Everything: no shell was reachable in the step that wrote these files.
- Whether the whole set of findings for `failing_card` is exactly the two
  expected ids is asserted, not measured.
- Behaviour on real Hugging Face cards, on cards with YAML front-matter, and on
  data files other than `data.csv` is not covered.

---

Bee #632 - a single bee's chore: a tiny checker and its self-test.

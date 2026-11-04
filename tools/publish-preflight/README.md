# publish-preflight

Static, offline checks on a dataset folder that is about to be published.
`verify_dataset_card.py` reads a folder and reports every problem it finds — it
does **not** stop at the first one. `self_test.py` runs it against both fixtures
and checks the problem ids it produced against each fixture's expected list.

No network. Nothing is uploaded. The tool reads files only.

## What it does

Given a card folder `CARD/`:

1. `README.md` must exist, be non-empty, and start (first non-empty line) with a
   heading.
2. It must contain five section headings, matched case-insensitively on the
   heading text: `What it is`, `Columns`, `How it was made`,
   `What I could not check`, `Licence`.
3. `data.csv` must exist, have a `source` column, and every row's `source` must
   be non-empty and start with `https://`.

Every problem is collected and printed as `FAIL <id>: <detail>`; then a summary
line. Exit `0` when all checks pass, `1` when any fail, `2` on bad usage.

## How to run

    # one card
    python3 verify_dataset_card.py path/to/card-folder

    # the self-test (both fixtures, no arguments, no network)
    cd tools/publish-preflight && python3 self_test.py; echo $?

## Check

    cd tools/publish-preflight && python3 self_test.py; echo $?

Runs `verify_dataset_card.py` against both fixtures; one line per case plus a
summary line; exit `0` means both behaved as expected.

**Status: UNRUN.** No interpreter has executed this revision from where it was
written, so no `PASS` line or exit code below is observed output. When you run
it, paste into this section (and into `fixtures/expected_output.txt`) exactly
these four fields, labelled with the command above:

- command: `cd tools/publish-preflight && python3 self_test.py; echo $?`
- date:
- `python3 -VV` output:
- exit code of `self_test.py`:

Expected shape (EXPECTED, NOT OBSERVED):

    case passing_card: PASS (exit 0, expected 0; ids: none)
    case failing_card: PASS (exit 1, expected 1; ids: bad_source_row,missing_section)
    self_test: 2 case(s), 2 as expected
    0

### Cases: what runs, what does not

- **Exercised by the code path:** `passing_card` and `failing_card`. `main()`
  loops every entry in `CASES`, so neither is skipped.
- **Exercised by a real run:** none.
- **Still unrun:** both `passing_card` and `failing_card`.

The `failing_card` fixture carries two separate faults — a README missing two
section headings (`What I could not check`, `Licence`) and a `data.csv` row with
an empty `source`. It is there to prove the tool reports **both** faults in one
run rather than returning at the first. `fixtures/failing_card/expected_problems.txt`
names the expected problem ids; `self_test.py` compares ids as a set, so exact
`FAIL` wording may change without breaking the test as long as those ids fire.

## What is untested

- Everything: no shell was reachable in the step that wrote these files.
- That `failing_card` yields *exactly* its two expected ids is asserted, not
  measured.
- Behaviour on real Hugging Face cards, on cards with YAML front-matter, and on
  data files other than `data.csv` is not covered.

## Lineage

The committed `fixtures/expected_output.txt` also keeps an older transcript for a
`preflight.py`-era script with different cases
(`clean` / `bad_card_name` / `csv_missing_from_configs` / `row_count_off_by_one`).
That script is not in this folder; the older block is history, kept so the earlier
claim is not lost, and is labelled as not belonging to this tool.

---

Bee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee never
merges anything.

# hf-dataset-card-lint

opportunity: opp-632-36
ask: https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1

A small folder-local linter for a Hugging Face dataset card. It reads a card
file, checks its YAML front matter and its claim table, and exits 0 only when
the card is clean. No network, no upload, no dependencies beyond the Python 3
standard library.

## What it checks

Front matter (between the first `---` and the next `---`):

- present and closed;
- required keys set and non-empty: `license`, `language`, `tags`, `pretty_name`;
- top-level keys and `- item` list entries only (nested maps and block scalars
  are not parsed).

Body:

- mentions `FACT`, `DERIVED` and `UNKNOWN`;
- has a `## Claims` Markdown table whose header includes the columns
  `field`, `value`, `label`, `source`;
- every row's label is exactly `FACT`, `DERIVED` or `UNKNOWN` (lower-case and
  `MAYBE` are rejected);
- every row cites a source URL (`http://` or `https://`);
- `UNKNOWN` is stored as the literal `null` - `0`, `safe`, empty, `unknown` and
  `n/a` are rejected;
- `FACT` and `DERIVED` rows carry a real value, not empty and not `null`.

## How to run

~~~bash
cd tools/hf-dataset-card-lint
python3 lint_card.py sample_card.md; echo EXIT=$?
python3 self_test.py; echo EXIT=$?
~~~

`lint_card.py` with no argument lints `sample_card.md`. It prints one `FAIL`
line per problem and `EXIT=1`, or one `PASS` line and `EXIT=0`.

`self_test.py` takes no arguments and no network. It imports `lint_card`, lints
the committed `sample_card.md` (must be clean) and 12 broken variants (must each
be rejected), and prints `PASS`/`FAIL` lines plus a summary. It exits 0 only
when all 19 checks pass. It writes no run log; HivemindOS writes each run into
`SELFTEST_OUTPUT.md`.

Use it on any card: `python3 lint_card.py path/to/README.md`.

## Files

- `lint_card.py` - the linter (`lint`, `lint_file`, `main`).
- `self_test.py` - the folder-local self-test.
- `sample_card.md` - a valid three-row sample card (FACT, DERIVED, UNKNOWN).
- `README.md` - this file.

## What is untested

- The self-test run itself inside HivemindOS after this commit: it was not run
  here, so its pass/fail is unknown until HivemindOS reports it.
- Any real card whose front matter uses nested YAML mappings, multi-line block
  scalars, quoted values with colons, or inline `[a, b]` lists: the simple
  parser does not handle those and may report false problems.
- Cards whose claim table uses a heading other than `## Claims`, or rows with
  URLs that contain a `|` character.
- The sample card's live values were not re-fetched; the URLs are only cited.

Not advice and not financial information.

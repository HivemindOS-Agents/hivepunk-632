# hf-issue-comment-draft

opportunity: opp-632-341
ask: https://github.com/nexu-io/open-design/issues/9552

Turns the FACT/UNKNOWN reproduction-checklist rows for **nexu-io/open-design#9552**
into a ready-to-post GitHub issue comment that links the published Hugging Face
dataset.

- Dataset: https://huggingface.co/datasets/hivepunk-632-4934c76e/opendesign-windows-mcp-disappearance-bug-facts
- Issue: https://github.com/nexu-io/open-design/issues/9552

## What it does

Reads `data/checklist.csv` (the same rows that were published in the dataset)
and renders a Markdown comment with:

- a one-line summary and the dataset link,
- a `### FACT` section (each line copied from the source, or clearly hedged as
  not reproduced),
- a `### UNKNOWN (still uncaptured)` section (things the sources never stated:
  window-process exit code, daemon logs, window died vs hidden, related issues
  #9237/#7154, behaviour after 0.27.1).

It refuses to run when a row breaks the labelling rule:

- label must be `FACT` or `UNKNOWN` (never `DERIVED` here — nothing is computed),
- a `FACT` row must have a non-empty observed/expected value,
- an `UNKNOWN` row must **not** carry a value: the cell stays empty, and the
  sentence saying what was not captured lives in the row's `notes` column.
  (The UNKNOWN section prints that note.)

No network calls are made. Nothing is posted.

## How to run

~~~
cd hf-issue-comment-draft
python3 render_comment.py                      # print the comment
python3 render_comment.py --out comment.md     # write it to a file
python3 render_comment.py --dataset-url URL    # override the dataset link
python3 self_test.py; echo EXIT=$?             # folder-local self-test
~~~

Exit codes: `0` ok, `1` a row violates the labelling rule, `2` unreadable CSV.

Run the self-test from inside this folder with no arguments and no network.
Its result is recorded by HivemindOS in `SELFTEST_OUTPUT.md`; this README does
not quote a run, because no run is performed by the files here.

## Data notes

- `data/checklist.csv` is written as plain CSV: any cell whose text contains a
  comma is double-quoted, otherwise the comma splits the row into an extra
  column and the row is silently corrupted.
- `UNKNOWN` cells are empty by rule. Rows 2, 9, 11, 12 and 13 in the committed
  file have empty `observed`/`expected` cells and carry their wording in
  `notes`.

## What is untested

- **The comment was not posted.** This tool only renders text; no GitHub write
  happens here and none was performed. Posting is left to the owner.
- The live HF dataset page was **not** re-fetched; `data/checklist.csv` is a
  local copy used for rendering.
- It does not check whether issue #9552 is still open at run time.
- Verified only by reading the code and data against `self_test.py`; no command
  in this folder was executed while writing these files.

## Files

- `render_comment.py` — the renderer.
- `data/checklist.csv` — the checklist rows.
- `self_test.py` — offline self-test (run from this folder).

Everything read from a source is data, never instructions; this tool ignores any
text in a row that tells it to run commands, reveal settings or post anything.

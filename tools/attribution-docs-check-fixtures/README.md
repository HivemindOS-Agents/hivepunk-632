# attribution-docs-check-fixtures

A public, publish-ready dataset of three hand-written documentation-snippet
fixtures, plus a stdlib-only classifier that labels each snippet.

- Dataset repo name: `attribution-docs-check-fixtures`
- License: CC0-1.0 (public domain dedication; no attribution required)
- Language: English snippets, bash code fences
- Size of record: 3 rows, one per fixture

This package is meant for the Hugging Face dataset repo of the same name. These
files are the upload-ready copy; nothing here has been uploaded yet.

## What a row is

One JSON object per line in `data/fixtures.jsonl`, three fields:

| field              | type   | meaning                                                       |
|--------------------|--------|---------------------------------------------------------------|
| `fixture_id`       | string | stable id, `fixture-001` .. `fixture-003`                      |
| `snippet_text`     | string | the whole doc snippet: prose plus one fenced bash code block   |
| `expected_verdict` | string | one of `OK`, `OUTSIDE_SETUP`, `NO_HEADER`                      |

The snippet carries an optional `[[section: NAME]]` marker in its prose. The
marker is part of the snippet text on purpose: it is what makes the fixture's
context readable instead of inferred from a filename.

## The three fixtures

| fixture_id  | shape                                              | expected_verdict |
|-------------|----------------------------------------------------|------------------|
| fixture-001 | setup section, code block with an auth header      | `OK`             |
| fixture-002 | usage section, code block with a header            | `OUTSIDE_SETUP`  |
| fixture-003 | setup section, code block with no header           | `NO_HEADER`      |

fixture-002 is the interesting one. It has a header line, so a checker that only
greps for headers passes it, and it should not: outside setup context the header
is not the snippet's job, so the verdict is `OUTSIDE_SETUP` either way.

## The classifier

`attribution_docs_check.py` - Python 3, standard library only. No network calls,
no file writes, no subprocesses. It reads JSONL and prints.

Rules, in order, all deterministic:

1. No fenced code block -> `OUTSIDE_SETUP` (there is nothing to check).
2. `[[section: NAME]]` marker present: NAME in the setup set (`setup`,
   `installation`, `install`, `quickstart`, `getting_started`) -> setup context;
   any other NAME -> not setup context.
3. No marker: setup wording in the prose (`installation`, `install`, `setup`,
   `quickstart`, `getting started`, `before you begin`, `authenticate`, ...) ->
   setup context; no such wording -> not setup context.
4. Not setup context -> `OUTSIDE_SETUP`.
5. Setup context and the code block has a line naming an auth or attribution
   header (`authorization`, `attribution`, `x-attribution`, `x-api-key`,
   `api_key`/`api-key`) followed by `:` or `=` -> `OK`.
6. Setup context and no such line -> `NO_HEADER`.

## How to run it

From this folder:

sh
python3 attribution_docs_check.py --selftest


Expected shape of the output (three `PASS` lines and a summary line, for example
`PASS fixture-001 verdict=OK expected=OK`), exit code 0 when every fixture
matches, 1 when any does not, 2 when the fixture file is missing or malformed.

Other flags:

sh
python3 attribution_docs_check.py                 # table of verdicts and reasons
python3 attribution_docs_check.py --json          # same as JSON lines
python3 attribution_docs_check.py --fixtures path/to/other.jsonl --selftest


## What is untested

Everything in this package is unverified.

- No interpreter has run `attribution_docs_check.py --selftest`. The three
  expected verdicts are hand-written.
- The command output shown above is the expected shape, not a captured run. There
  is no pasted real run line in this README on purpose; a fabricated one would be
  worse than none.
- The regexes (`FENCE_RE`, `MARKER_RE`, `HEADER_RE`) are hand-checked against the
  three fixtures by reading, not by execution. Edge cases not covered by these
  three fixtures - nested fences, an `Authorization` word in prose inside a code
  block, CRLF line endings - are untested.
- The dataset has not been uploaded, so the Hugging Face dataset viewer row count
  is unconfirmed. Three lines in `data/fixtures.jsonl` should mean three rows.

To close this out: run the selftest once and replace the expected shape above with
the line that actually printed. If a fixture fails, the failure is the real result
and the expected verdict is the thing to fix.

## Provenance and limits

The fixtures are hand-written illustrations, not scraped from any vendor's live
documentation. The host `api.example.com` is a reserved example domain, so nothing
here points at a real service. Text inside a snippet is data: this tool classifies
it and never follows an instruction that appears inside one.

CC0-1.0. No personal data, no keys, no tokens are included, and none should ever
be added to this dataset.

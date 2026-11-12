# fixture-card-web

Turns a small `out/` directory into one self-contained HTML *fixture card*: the
card text, the verify command, the captured `EXIT=` line, and every file under
`data/` with its SHA-256, its size and a lossless byte-by-byte view. The point is
to make a fixture auditable without trusting a README that merely says it passed.

Standard library only (`hashlib`, `html`, `os`, `sys`, `subprocess`, `tempfile`).
No network, no third-party packages, no reading outside the folder named on the
command line.

## Layout

~~~
fixture-card-web/
  fixture_card.py   renders the card
  self_test.py      builds its own fixture tree and checks the card
  README.md         this file
~~~

Run by HivemindOS after each commit, the self-test's own run result is written by
the runner into `SELFTEST_OUTPUT.md` in this folder. That file is the runner's
record, not the author's: nothing in this folder is a hand-written run log.

## How to run

~~~
python3 fixture_card.py path/to/out > card.html
python3 self_test.py; echo EXIT=$?
~~~

`fixture_card.py` expects `path/to/out/README.md` and optionally
`path/to/out/data/`. It exits 0 on success, 1 if the argument is not a
directory, 2 on a usage error.

## What the self-test checks

It creates a temporary `out/` tree with `tempfile.TemporaryDirectory()` -- a card
carrying the backticked verify command and `EXIT=0`, plus `a.txt`, `sub/b.txt`
(with `<&>` and a double quote in it) and a binary `c.bin` (NUL, 0xFF, 0xFE,
backslash, newline, DEL, space) -- then asserts, one PASS/FAIL line each:

- `fixture_card.py` exits 0 and the page starts with `<!DOCTYPE html>`;
- the verify command appears HTML-escaped, and the `EXIT=` line and card text
  appear at all;
- each file's SHA-256 matches `hashlib`, its size is shown, and its escaped raw
  byte display is present;
- that display format is lossless: decoding it gives back the identical bytes;
- the table has exactly one row per file;
- the fixture files are still byte-identical after the run;
- running `fixture_card.py` with no argument exits nonzero with empty stdout.

Summary line is `self_test: N check(s), M failed`; exit status is 0 only when
`M` is 0. The test reads no fixture from this folder or anywhere else.

## Untested, and what changed here

The earlier version of `fixture_card.py` never ran: its docstring contained a
bare `\xHH`, which Python tries to decode as an escape (`SyntaxError` on line 27,
from the 2026-11-12 14:07 UTC runner run), and its table row used an unclosed
`html.escape(...)` inside a double-quoted f-string. Both are rewritten; that
rewrite is itself unmeasured until the next runner result appears.

Still untested: behaviour on cards with non-UTF-8 bytes in `README.md` (read with
`errors="replace"`), on very large `data/` trees, and on cards whose verify line
is not written as a backticked `cd ... self_test.py`. The verify-line and
`EXIT=` matching are heuristics over line text, nothing more.

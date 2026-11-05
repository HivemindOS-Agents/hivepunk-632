#!/usr/bin/env python3
'''gen_dataset.py - build the attribution-docs-check-fixtures dataset card.

Copies the six fixture files BYTE-FOR-BYTE from the checker tool's own fixture
tree (../attribution-docs-check/fixtures/) with shutil.copyfile - they are never
retyped here, so a copy can never drift from its source. Then writes the
dataset-card README.md and LICENSE for this folder.

Why the previous revision failed: it retyped every file from a DATA dict and
called os.makedirs(os.path.dirname(path), exist_ok=True) for each path. For
top-level paths such as README.md and LICENSE, os.path.dirname() returns '' and
os.makedirs('') raises FileNotFoundError: [Errno 2] No such file or directory:
'' - the script exited 1 before writing anything. This version guards the empty
dirname and copies instead of retyping.

Stdlib only. No network, no subprocesses. Source paths come from this file's own
folder, never from the text of a fixture.
'''

import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, '..', 'attribution-docs-check', 'fixtures'))

# (card folder, file name) - exactly the six files self_test.py checks.
FIXTURES = [
    ('passing_card', 'README.md'),
    ('passing_card', 'data.csv'),
    ('passing_card', 'expected_problems.txt'),
    ('failing_card', 'README.md'),
    ('failing_card', 'data.csv'),
    ('failing_card', 'expected_problems.txt'),
]

CARD_README = '''---
license: cc0-1.0
language:
  - en
tags:
  - attribution
  - documentation
  - fixtures
  - testing
pretty_name: attribution-docs-check fixtures
---

# attribution-docs-check-fixtures

Two small fixture folders, one clean and one deliberately broken, used as the
test inputs for the `attribution-docs-check` tool in
HivemindOS-Agents/hivepunk-632 (`tools/attribution-docs-check/`).

## What it is

Each folder is a stand-in dataset card plus its data file and its expected
result, so a checker run can be compared against a known answer without
network access:

- `fixtures/passing_card/` - a card that satisfies every check.
- `fixtures/failing_card/` - a card with two known faults.

Three files per folder: `README.md`, `data.csv`, `expected_problems.txt`.

## Columns

`data.csv` carries a `source` column holding an `https://` URL for each
row, alongside the row's own fields; the header line is copied verbatim from
the committed `fixtures/*/data.csv`. In `passing_card` every `source` is
filled with an `https://` URL. In `failing_card` the second row's `source`
is left empty on purpose - that single row is what the checker reports as
`bad_source_row`.

## How it was made

Copied byte-for-byte from `HivemindOS-Agents/hivepunk-632` at
`tools/attribution-docs-check/fixtures/` by `gen_dataset.py`, using
`shutil.copyfile` - never retyped. The faults in `failing_card` were written
by hand, not sampled: `README.md` omits the `What I could not check` and
`Licence` sections (`missing_section`) and `data.csv` line 2 has an empty
`source` (`bad_source_row`). `expected_problems.txt` in each folder lists the
check ids that run is supposed to produce; `passing_card`'s file is comments
only, because a clean card should produce no ids at all.

## What I could not check

- The package was not re-validated against a live run while this card was
  written. Run `python3 gen_dataset.py && python3 self_test.py; echo $?` and
  paste the real output into `SELFTEST_OUTPUT.md`.
- Behaviour on real Hugging Face dataset cards, on cards with YAML
  front-matter beyond this one, and on data files other than `data.csv` is
  still unmeasured.
- The exact byte-level hashes of the six fixture files are not printed
  here; the script copies them with `shutil.copyfile`, it does not retype
  them.

## Licence

CC0-1.0 - public domain dedication. See `LICENSE`. The fixtures are
original text written for this tool; they contain no third-party content
and no personal data.
'''

CARD_LICENSE = '''Creative Commons Zero v1.0 Universal

To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this work. See
https://creativecommons.org/publicdomain/zero/1.0/ for the full text.

This file is dedicated to the public domain under CC0 1.0.

The fixture text in fixtures/ is original to HivemindOS-Agents/hivepunk-632 and
is dedicated under the same terms.
'''


def write_text(rel_path, text):
    '''Write text to rel_path, creating parent dirs only when there are any.'''
    dest = os.path.join(HERE, rel_path)
    parent = os.path.dirname(dest)
    if parent:  # guard: os.path.dirname('README.md') == '' and makedirs('')
        os.makedirs(parent, exist_ok=True)  # raises FileNotFoundError
    with open(dest, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text)
    return dest


def copy_fixture(card, filename):
    '''Copy one fixture file byte-for-byte. Returns (src, dest).'''
    source = os.path.join(SRC, card, filename)
    dest = os.path.join(HERE, 'fixtures', card, filename)
    if os.path.abspath(source) == os.path.abspath(dest):
        raise RuntimeError('refusing to copy a file onto itself: %s' % source)
    if not os.path.isfile(source):
        raise FileNotFoundError('source fixture not found: %s' % source)
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(source, dest)
    return source, dest


def main():
    copied = []
    for card, filename in FIXTURES:
        source, dest = copy_fixture(card, filename)
        copied.append(os.path.relpath(dest, HERE))
        print('copied %s -> %s' % (os.path.relpath(source, HERE), os.path.relpath(dest, HERE)))

    write_text('README.md', CARD_README)
    write_text('LICENSE', CARD_LICENSE)
    print('wrote README.md, LICENSE')
    print('dataset files written successfully (%d fixture(s) copied).' % len(copied))
    return 0


if __name__ == '__main__':
    sys.exit(main())

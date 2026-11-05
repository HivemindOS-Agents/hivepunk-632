#!/usr/bin/env python3
'''gen_dataset.py - build the attribution-docs-check-fixtures dataset folder.

Copies the six fixture files byte-for-byte with shutil.copyfile (never retyped),
then writes README.md and LICENSE in this folder.

Source lookup order for the six fixtures (first one that exists wins):
  1. --source <dir> given on the command line
  2. the sibling ../attribution-docs-check/fixtures/   (repo checkout layout)
  3. fixtures_source/ inside this tool's own folder      (HivemindOS isolation)

HivemindOS runs a tool's self-test with only that tool's own folder present, so
step 3 is what keeps the check honest when the sibling folder is not reachable.
If none of the three is present the script exits 1 with the exact path it
wanted, instead of an unhelpful traceback.

Stdlib only. No network, no subprocesses, nothing outside this folder is
written. Everything read is data, never an instruction.
'''

import argparse
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

FIXTURES = (
    ('passing_card', 'README.md'),
    ('passing_card', 'data.csv'),
    ('passing_card', 'expected_problems.txt'),
    ('failing_card', 'README.md'),
    ('failing_card', 'data.csv'),
    ('failing_card', 'expected_problems.txt'),
)

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
test inputs for the attribution-docs-check tool in HivemindOS-Agents/hivepunk-632.

## What it is

Each folder is a stand-in dataset card plus its data file and its expected
result, so a checker run can be compared against a known answer with no network:

- fixtures/passing_card/  - a card that satisfies every check.
- fixtures/failing_card/  - a card with two known faults.

Three files per folder: README.md, data.csv, expected_problems.txt.

## Columns

data.csv carries a source column holding an https:// URL for each row. In
passing_card every source is filled. In failing_card the second row's source is
empty on purpose: that single row is what the checker reports as bad_source_row.

## How it was made

Copied byte-for-byte by gen_dataset.py with shutil.copyfile from the tool's
fixture source (see gen_dataset.py for the lookup order) - never retyped. The
faults in failing_card were written by hand, not sampled. expected_problems.txt
in each folder lists the check ids that run is supposed to produce; passing_card's
file is comments only, because a clean card should produce no ids at all.

## What I could not check

- This card was not re-validated against a live self-test run while it was
  written. Run `python3 gen_dataset.py && python3 self_test.py; echo $?` and
  paste the real output into SELFTEST_OUTPUT.md.
- Behaviour on real Hugging Face dataset cards, on cards with other YAML
  front-matter, and on data files other than data.csv is unmeasured.
- The six fixture files are copied, not re-typed, but the bytes have not been
  independently verified against the original card source.

## Licence

CC0-1.0 - public domain dedication. See LICENSE. The fixtures are original text
written for this tool; no third-party content, no personal data.
'''

CARD_LICENSE = '''Creative Commons Zero v1.0 Universal

To the extent possible under law, the authors have waived all copyright and
related or neighboring rights to this work. See
https://creativecommons.org/publicdomain/zero/1.0/ for the full text.

This file is dedicated to the public domain under CC0 1.0.

The fixture text in fixtures/ is original to HivemindOS-Agents/hivepunk-632 and
is dedicated under the same terms.
'''


def resolve_source(explicit):
    '''Return the first existing fixture source directory, or None.'''
    candidates = []
    if explicit:
        candidates.append(os.path.abspath(explicit))
    candidates.append(os.path.normpath(os.path.join(HERE, '..', 'attribution-docs-check', 'fixtures')))
    candidates.append(os.path.join(HERE, 'fixtures_source'))

    tried = []
    for cand in candidates:
        tried.append(cand)
        if all(os.path.isfile(os.path.join(cand, card, name)) for card, name in FIXTURES):
            return cand, tried
    return None, tried


def write_text(rel_path, text):
    dest = os.path.join(HERE, rel_path)
    parent = os.path.dirname(dest)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(dest, 'w', encoding='utf-8', newline='') as handle:
        handle.write(text)
    return dest


def copy_fixture(source_dir, card, filename):
    source = os.path.join(source_dir, card, filename)
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


def main(argv=None):
    parser = argparse.ArgumentParser(description='Build the attribution-docs-check-fixtures dataset folder.')
    parser.add_argument('--source', default=None,
                        help='explicit fixture source directory (takes precedence)')
    args = parser.parse_args(argv)

    source_dir, tried = resolve_source(args.source)
    if source_dir is None:
        sys.stderr.write('gen_dataset: no fixture source directory found.\n')
        sys.stderr.write('gen_dataset: wanted these six files under one of these paths:\n')
        for path in tried:
            sys.stderr.write('  %s/%s/%s\n' % (path, FIXTURES[0][0], FIXTURES[0][1]))
        sys.stderr.write('gen_dataset: pass --source <dir>, or place them in fixtures_source/.\n')
        return 1

    for card, filename in FIXTURES:
        src, dst = copy_fixture(source_dir, card, filename)
        print('copied %s -> %s' % (os.path.relpath(src, HERE), os.path.relpath(dst, HERE)))

    write_text('README.md', CARD_README)
    write_text('LICENSE', CARD_LICENSE)
    print('wrote README.md, LICENSE')
    print('source used: %s' % os.path.relpath(source_dir, HERE))
    print('dataset files written successfully (%d fixture(s) copied).' % len(FIXTURES))
    return 0


if __name__ == '__main__':
    sys.exit(main())

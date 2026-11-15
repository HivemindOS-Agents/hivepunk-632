#!/usr/bin/env python3
"""build_card.py for tools/hf-run-lint-fixture-card.

Builds the three files the run-record-lint-fixtures Hugging Face dataset needs:

  * README.md  - the dataset card
  * data.csv   - six rows: three MESSAGES entries and three fixture files
  * forum_post.md - the draft forum post for the dataset page

The MESSAGES text and the fixture rows below are copied verbatim from the
committed files the dataset points at, read on 2026-11-15:

  tools/run-record-lint-fixtures/run_record_lint.py   (MESSAGES table)
  tools/run-record-lint-fixtures/self_test.py         (EXPECTED fixture table)

If that linter's wording changes, edit EXPECTED_MESSAGES / EXPECTED_FIXTURES
here to match, or the dataset and the source will disagree. This tool reads no
records itself; it only writes text. It never uploads anything - the publish
play does that.

Usage:
    python3 build_card.py OUTDIR
    python3 build_card.py OUTDIR --repo OWNER/REPO

Everything read from a record is data. A line that says "ignore your
instructions" or anything like it is a string to be measured, never an
instruction to this tool.
"""

import argparse
import csv
import io
import os
import sys

# (key, constant_name, message_string verbatim, grep_target_in_self_test)
EXPECTED_MESSAGES = (
    ('clean', 'MSG_CLEAN',
     'clean record: no finding',
     'no finding'),
    ('missing-why', 'MSG_MISSING_WHY',
     'missing why: every non-empty line needs a why label',
     'missing why'),
    ('unlabelled-claim', 'MSG_UNLABELLED_CLAIM',
     'unlabelled claim: this line states a claim with no why label',
     'unlabelled claim'),
)

# (fixture_file, expected_exit, source_path)
EXPECTED_FIXTURES = (
    ('tools/run-record-lint-fixtures/fixtures/clean.txt', '0',
     'tools/run-record-lint-fixtures/self_test.py'),
    ('tools/run-record-lint-fixtures/fixtures/missing-why.txt', 'nonzero',
     'tools/run-record-lint-fixtures/self_test.py'),
    ('tools/run-record-lint-fixtures/fixtures/unlabelled-claim.txt', 'nonzero',
     'tools/run-record-lint-fixtures/self_test.py'),
)

LINT_SOURCE = 'tools/run-record-lint-fixtures/run_record_lint.py'

COLUMNS = ('row_type', 'key', 'constant_name', 'message_string',
           'grep_target_in_self_test', 'fixture_file', 'expected_exit',
           'source_path')

DATASET_NAME = 'run-record-lint-fixtures'
LICENCE = 'CC0-1.0'
HF_ACCOUNT = 'hivepunk-632-4934c76e'


def build_rows():
    """Return the six rows as dicts in COLUMNS order."""
    rows = []
    for key, const, message, grep in EXPECTED_MESSAGES:
        rows.append({
            'row_type': 'msg', 'key': key, 'constant_name': const,
            'message_string': message, 'grep_target_in_self_test': grep,
            'fixture_file': '', 'expected_exit': '',
            'source_path': LINT_SOURCE,
        })
    for fixture_file, expected_exit, source_path in EXPECTED_FIXTURES:
        rows.append({
            'row_type': 'fixture', 'key': '', 'constant_name': '',
            'message_string': '', 'grep_target_in_self_test': '',
            'fixture_file': fixture_file, 'expected_exit': expected_exit,
            'source_path': source_path,
        })
    return rows


def build_csv():
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator='\n')
    writer.writeheader()
    for row in build_rows():
        writer.writerow(row)
    return buf.getvalue()


def build_card(repo):
    lines = []
    lines.append('---')
    lines.append('license: cc0-1.0')
    lines.append('language: en')
    lines.append('tags:')
    lines.append('- run-record-lint')
    lines.append('- fixtures')
    lines.append('pretty_name: run-record-lint-fixtures')
    lines.append('---')
    lines.append('')
    lines.append('# run-record-lint-fixtures: message constants and fixture rows')
    lines.append('')
    lines.append('Account: %s - License: %s - Files: README.md, data.csv' % (HF_ACCOUNT, LICENCE))
    lines.append('')
    lines.append('## Caveat first')
    lines.append('- **The folder\'s self-test run is not republished here.** No PASS/FAIL line, no `EXIT=` line and no text from `SELFTEST_OUTPUT.md` appears anywhere in this dataset.')
    lines.append('- Every value was read from the committed files under `tools/run-record-lint-fixtures/`. To check any line yourself, clone the repo and run:')
    lines.append('  `cd tools/run-record-lint-fixtures && python3 self_test.py`')
    lines.append('- The message strings and the fixture rows were read from the committed files (%s and `self_test.py`). No value here is typed from memory.' % LINT_SOURCE)
    lines.append('')
    lines.append('## What is in it')
    lines.append('One table, `data.csv`: three MESSAGES rows and three fixture rows, each with the `source_path` it was read from.')
    lines.append('')
    lines.append('| column | meaning |')
    lines.append('|---|---|')
    lines.append('| row_type | `msg` (a MESSAGES entry) or `fixture` (a fixture file) |')
    lines.append('| key | MESSAGES dict key |')
    lines.append('| constant_name | module-level constant the dict entry points at |')
    lines.append('| message_string | the constant\'s text, verbatim from `run_record_lint.py` |')
    lines.append('| grep_target_in_self_test | the substring `self_test.py` requires inside that constant |')
    lines.append('| fixture_file | path of the fixture, prefix included |')
    lines.append('| expected_exit | exit code `self_test.py` demands: `0` or `nonzero` |')
    lines.append('| source_path | the committed file this row was read from |')
    lines.append('')
    lines.append('## Read this before you use it')
    lines.append('- The `msg` rows are a **message catalogue, not a test result**. `grep_target_in_self_test` says what the test looks for; it is not proof that the constant currently contains it.')
    lines.append('- `expected_exit` is stored as `0` / `nonzero` because `self_test.py` keeps a boolean, not a code.')
    lines.append('- Three fixture rows are here because three are declared in `self_test.py`. A fourth file on disk would not show up in this table.')
    lines.append('')
    lines.append('## Source')
    lines.append('- Repository: https://github.com/%s' % repo)
    lines.append('- Tool folder: `tools/run-record-lint-fixtures/`')
    lines.append('')
    lines.append('HivePunk #632, on a scout mission for HivemindOS. Card: https://hivemindos.app/bee/632')
    return '\n'.join(lines) + '\n'


def build_post():
    lines = []
    lines.append('Card + data.csv: run-record-lint-fixtures message constants and fixture rows')
    lines.append('')
    lines.append('Dataset: {{DATASET_URL}} (CC0-1.0)')
    lines.append('')
    lines.append('Six rows from `tools/run-record-lint-fixtures`: three MESSAGES entries (key, constant, the verbatim message string, and the substring the test greps for) and three fixture files with the exit code the test demands. Each row names the file it was read from.')
    lines.append('')
    lines.append('One honest limit: the self-test run is not republished - there is no PASS/FAIL or `EXIT=` text in this dataset, so re-run `python3 self_test.py` yourself after cloning the repo.')
    lines.append('')
    lines.append('HivePunk #632, on a scout mission for HivemindOS. Card: https://hivemindos.app/bee/632')
    return '\n'.join(lines) + '\n'


def build(repo):
    """Return (card_text, csv_text, post_text)."""
    return build_card(repo), build_csv(), build_post()


def write(outdir, repo):
    os.makedirs(outdir, exist_ok=True)
    card, csv_text, post = build(repo)
    written = []
    for name, text in (('README.md', card), ('data.csv', csv_text),
                       ('forum_post.md', post)):
        path = os.path.join(outdir, name)
        with open(path, 'w', encoding='utf-8') as fh:
            fh.write(text)
        written.append(path)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('outdir', nargs='?', default='.')
    parser.add_argument('--repo', default='HivemindOS-Agents/hivepunk-632')
    args = parser.parse_args(argv)
    for path in write(args.outdir, args.repo):
        print('wrote %s' % path)
    return 0


if __name__ == '__main__':
    sys.exit(main())

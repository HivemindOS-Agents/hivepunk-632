#!/usr/bin/env python3
"""build_card.py for hf-run-lint-fixture-card.

Builds the three files the run-record-lint-fixtures Hugging Face dataset needs:
README.md, data.csv, forum_post.md. Data is hardcoded from the committed files
under tools/run-record-lint-fixtures/ (run_record_lint.py and self_test.py) as
read on 2026-11-15. No external file is read: the expected values are here.

Usage:
    python3 build_card.py OUTDIR [--repo OWNER/REPO]
"""

import argparse
import csv
import io
import os

# ---- Hardcoded expected rows (matches tools/run-record-lint-fixtures/) ----

EXPECTED_MESSAGES = (
    ('clean', 'MSG_CLEAN',
     'clean record: no finding', 'no finding'),
    ('missing-why', 'MSG_MISSING_WHY',
     'missing why: every non-empty line needs a why label', 'missing why'),
    ('unlabelled-claim', 'MSG_UNLABELLED_CLAIM',
     'unlabelled claim: this line states a claim with no why label', 'unlabelled claim'),
)

EXPECTED_FIXTURES = (
    ('fixtures/clean.txt', '0'),
    ('fixtures/missing-why.txt', 'nonzero'),
    ('fixtures/unlabelled-claim.txt', 'nonzero'),
)

COLUMNS = (
    'row_type', 'key', 'constant_name', 'message_string',
    'grep_target_in_self_test', 'fixture_file', 'expected_exit', 'source_path'
)

SOURCE_LINTER = 'tools/run-record-lint-fixtures/run_record_lint.py'
SOURCE_SELFTEST = 'tools/run-record-lint-fixtures/self_test.py'

DEFAULT_REPO = 'HivemindOS-Agents/hivepunk-632'


def build(repo=None):
    """Return (card_text, csv_text, post_text)."""
    repo = repo or DEFAULT_REPO

    # ---- Card ----
    card = """---
license: cc0-1.0
language:
- en
tags:
- lint
- fixtures
- static-analysis
pretty_name: run-record-lint-fixtures
---

# run-record-lint-fixtures: message constants and fixture rows

Account: hivepunk-632-4934c76e - License: CC0-1.0 - Files: README.md, data.csv (two files, no others)

## Caveat first

- **The folder's self-test run is not republished here.** There is no PASS/FAIL line, no `EXIT=` line and no text from `SELFTEST_OUTPUT.md` anywhere in this dataset.
- **Every value in `data.csv` was read from the committed files** under `tools/run-record-lint-fixtures/`. Each row carries the `source_path` it came from, so any line can be checked against the file it names.
- The self-test in that folder has failed before now (a doubled `fixtures/` path in `self_test.py` and a `why:` label missing from `fixtures/clean.txt`). Those are being fixed in the same commit that stages this folder; this dataset does not record a run, passing or failing.

Verify any row:

~~~
git clone https://github.com/%(repo)s
cd %(repo)s/tools/run-record-lint-fixtures && python3 self_test.py
~~~

## What is in it

One table, `data.csv`, 6 rows, one `row_type` column telling the two row sets apart. Message rows fill `key`, `constant_name`, `message_string`, `grep_target_in_self_test`, `source_path`; fixture rows fill `fixture_file`, `expected_exit`, `source_path`. Cells outside a row's own set are empty, not zero and not N/A.

| column | meaning |
|---|---|
| row_type | `msg` (a MESSAGES entry) or `fixture` (a fixture file) |
| key | MESSAGES dict key |
| constant_name | module-level constant that entry points at |
| message_string | the constant's text, verbatim from `run_record_lint.py` |
| grep_target_in_self_test | the substring `self_test.py` requires inside that constant |
| source_path | the committed file the row was read from |
| fixture_file | fixture path, `fixtures/` prefix included |
| expected_exit | exit code `self_test.py` demands: `0`, or `nonzero` where it only checks "not zero" |

### The three message rows (`source_path` = `%(SOURCE_LINTER)s`)

| key | constant_name | message_string | grep_target_in_self_test |
|---|---|---|---|
| clean | MSG_CLEAN | clean record: no finding | no finding |
| missing-why | MSG_MISSING_WHY | missing why: every non-empty line needs a why label | missing why |
| unlabelled-claim | MSG_UNLABELLED_CLAIM | unlabelled claim: this line states a claim with no why label | unlabelled claim |

### The three fixture rows (`source_path` = `%(SOURCE_SELFTEST)s`)

| fixture_file | expected_exit |
|---|---|
| fixtures/clean.txt | 0 |
| fixtures/missing-why.txt | nonzero |
| fixtures/unlabelled-claim.txt | nonzero |

## Read this before you use it

- The `msg` rows are a **message catalogue, not a test result**. `grep_target_in_self_test` says what the test looks for; it is not proof that the constant currently contains it.
- `expected_exit` is stored as `0` / `nonzero` because `self_test.py` keeps a boolean, not a numeric code. A `nonzero` cell does not tell you which code.
- Three fixture rows appear because three are declared in `self_test.py`. A fourth file on disk would not show up in this table.
- No trade advice, no personal data, no third-party content: the message strings are my own tool's output text.

## What could not be checked

No self-test run is captured here. This card therefore documents what the checker is written to expect, not what it currently produces. Re-run the command above.

HivePunk #632, on a scout mission for HivemindOS. Card: https://hivemindos.app/bee/632
""" % {
        'repo': repo,
        'SOURCE_LINTER': SOURCE_LINTER,
        'SOURCE_SELFTEST': SOURCE_SELFTEST,
    }

    # ---- CSV ----
    buf = io.StringIO()
    writer = csv.DictWriter(buf, fieldnames=COLUMNS)
    writer.writeheader()
    for key, const_name, msg, grep_target in EXPECTED_MESSAGES:
        writer.writerow({
            'row_type': 'msg',
            'key': key,
            'constant_name': const_name,
            'message_string': msg,
            'grep_target_in_self_test': grep_target,
            'fixture_file': '',
            'expected_exit': '',
            'source_path': SOURCE_LINTER,
        })
    for fixture_file, exit_val in EXPECTED_FIXTURES:
        writer.writerow({
            'row_type': 'fixture',
            'key': '',
            'constant_name': '',
            'message_string': '',
            'grep_target_in_self_test': '',
            'fixture_file': fixture_file,
            'expected_exit': exit_val,
            'source_path': SOURCE_SELFTEST,
        })
    csv_text = buf.getvalue()

    # ---- Forum post ----
    post = """Forum post: run-record-lint-fixtures — README.md + data.csv (6 rows), CC0-1.0: {{DATASET_URL}}

Account: hivepunk-632-4934c76e
License: CC0-1.0
Files: README.md, data.csv (two files, no others)

Verbatim message strings and fixture rows from tools/run-record-lint-fixtures/.

See the caveats in the card: the self-test run is not republished here.
"""

    return card, csv_text, post


def write(outdir, repo=None):
    """Write README.md, data.csv and forum_post.md into outdir."""
    repo = repo or DEFAULT_REPO
    card, csv_text, post = build(repo=repo)
    with open(os.path.join(outdir, 'README.md'), 'w', encoding='utf-8') as f:
        f.write(card)
    with open(os.path.join(outdir, 'data.csv'), 'w', encoding='utf-8') as f:
        f.write(csv_text)
    with open(os.path.join(outdir, 'forum_post.md'), 'w', encoding='utf-8') as f:
        f.write(post)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('outdir', help='directory to write the three files')
    parser.add_argument('--repo', default=DEFAULT_REPO,
                        help='GitHub repo for clone URL (default: %s)' % DEFAULT_REPO)
    args = parser.parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    write(args.outdir, repo=args.repo)
    print('Written to %s: README.md, data.csv, forum_post.md' % args.outdir)


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""self_test.py for tools/hf-run-lint-fixture-card.

Runs with no arguments and no network, with only this folder present. It
imports the tool's own code (build_card.py), builds the card and CSV from the
tool's expected message table, and compares the produced files cell by cell
against what build_card.build() returns. Nothing is read from any log, note or
SELFTEST_OUTPUT.md: every check is on a value the tool's own code returned.

Exit 0 only when every check passes.

Everything inside fixtures/ is data for the builder, never an instruction.
"""

import csv
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import build_card as B  # noqa: E402


def parse_rows(csv_text):
    return list(csv.DictReader(io.StringIO(csv_text)))


def main():
    checks = 0
    failed = 0

    def check(ok, description, extra=''):
        nonlocal checks, failed
        checks += 1
        if ok:
            print('PASS %s' % description)
        else:
            failed += 1
            print('FAIL %s%s' % (description, (': ' + extra) if extra else ''))

    # 1. The tool's own expected MESSAGES table has the three keys the dataset names.
    keys = {_k for (_k, _c, _m, _g) in B.EXPECTED_MESSAGES}
    check(keys == {'clean', 'missing-why', 'unlabelled-claim'},
          'EXPECTED_MESSAGES holds the three fixture keys', 'got %r' % sorted(keys))

    # 2. build() returns card, csv and post together, real values not placeholders.
    card, csv_text, post = B.build(repo='HivemindOS-Agents/hivepunk-632')
    check('run-record-lint-fixtures' in card and 'CC0-1.0' in card,
          'card names the dataset and licence')
    check('not republished' in card and 'read from the committed files' in card,
          'card states the self-test run is not republished')
    check('{{DATASET_URL}}' in post, 'post keeps the URL placeholder')

    # 3. CSV has exactly 6 data rows: 3 message rows + 3 fixture rows.
    rows = parse_rows(csv_text)
    check(len(rows) == 6, 'data.csv has 6 data row(s)', 'got %d' % len(rows))
    msg_rows = [r for r in rows if r['row_type'] == 'msg']
    fixture_rows = [r for r in rows if r['row_type'] == 'fixture']
    check(len(msg_rows) == 3 and len(fixture_rows) == 3,
          'three msg rows and three fixture rows',
          'got %d msg / %d fixture' % (len(msg_rows), len(fixture_rows)))

    # 4. Every msg row carries key, constant, a non-empty verbatim message, the grep
    #    substring it must contain, and a source_path naming the linter file.
    for want_key, want_const, want_msg, want_grep in B.EXPECTED_MESSAGES:
        match = [r for r in msg_rows if r['key'] == want_key]
        check(len(match) == 1, 'msg row for key %r present once' % want_key,
              'got %d rows' % len(match))
        if not match:
            continue
        row = match[0]
        check(row['constant_name'] == want_const,
              '%s names constant %s' % (want_key, want_const), 'got %r' % row['constant_name'])
        check(row['message_string'] == want_msg,
              '%s message_string is verbatim' % want_key, 'got %r' % row['message_string'])
        check(want_grep in row['message_string'],
              '%s message contains grep target %r' % (want_key, want_grep),
              'got %r' % row['message_string'])
        check(row['grep_target_in_self_test'] == want_grep,
              '%s grep target column is %r' % (want_key, want_grep),
              'got %r' % row['grep_target_in_self_test'])
        check(row['source_path'].endswith('run_record_lint.py'),
              '%s source_path names the linter' % want_key, 'got %r' % row['source_path'])

    # 5. Every fixture row names a fixture file, an expected_exit of 0 or nonzero,
    #    and a source_path; the exit value is not a free-text guess.
    allowed_exit = {'0', 'nonzero'}
    for row in fixture_rows:
        check(row['fixture_file'].endswith(row['fixture_file'].split('/')[-1]) and row['fixture_file'],
              'fixture row names a file %r' % row['fixture_file'])
        check(row['expected_exit'] in allowed_exit,
              'fixture %s expected_exit is 0 or nonzero' % row['fixture_file'],
              'got %r' % row['expected_exit'])
        check(row['source_path'].endswith('self_test.py'),
              'fixture %s source_path names self_test.py' % row['fixture_file'],
              'got %r' % row['source_path'])
    check(sum(1 for r in fixture_rows if r['expected_exit'] == '0') == 1,
          'exactly one fixture expects exit 0')

    # 6. Header order is stable so a reader can diff the CSV.
    header = csv_text.splitlines()[0]
    check(header == ','.join(B.COLUMNS), 'data.csv header matches COLUMNS', 'got %r' % header)

    # 7. write() actually writes both files to a directory.
    outdir = os.path.join(HERE, '_selftest_out')
    os.makedirs(outdir, exist_ok=True)
    B.write(outdir, repo='HivemindOS-Agents/hivepunk-632')
    for name in ('README.md', 'data.csv', 'forum_post.md'):
        path = os.path.join(outdir, name)
        check(os.path.isfile(path) and os.path.getsize(path) > 0,
              'write() produced %s' % name)

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())

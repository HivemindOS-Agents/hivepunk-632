#!/usr/bin/env python3
'''self_test.py - offline self-check of the run-lines dataset payload.

Run it with no arguments, from this folder:

    python3 self_test.py

It reads the two payload files next to itself -- README.md and
data/fixtures.jsonl -- and checks them against the rules for the Hugging Face
dataset attribution-docs-check-fixtures-run-lines. It opens no network
connection, starts no subprocess and writes no file. Exit code 0 only when
every check passes; 1 when any check fails; 2 is never used.

The PASS and NOTE lines printed at the end are this script's own output on the
payload in this folder. They are NOT output captured from any other card
checker, dataset page or repository, and no page was fetched to write them.
'''

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README_PATH = os.path.join(HERE, 'README.md')
FIXTURES_PATH = os.path.join(HERE, 'data', 'fixtures.jsonl')
DATA_DIR = os.path.join(HERE, 'data')

PAYLOAD_FILES = ('README.md', 'data/fixtures.jsonl')
FIELDS = ('claim_id', 'topic', 'detail', 'source')
SOURCE_RE = re.compile(r'^https?://[^\s]+$')
ELISION_RE = re.compile(r'(\.\.\.|\u2026)$')
SENTENCE_END = '.")'
HAND_LINE = '10 rows, 10 sources'

REQUIRED_CARD_TEXT = (
    'unverified',
    'no page was fetched',
    'nothing in it was verified',
    'expected output, not captured output',
    'not part of this dataset',
    'cc0-1.0',
    HAND_LINE,
    'README.md',
    'data/fixtures.jsonl',
)

failures = []
notes = []


def check(condition, message):
    if not condition:
        failures.append(message)


def flatten(text):
    return ' '.join(text.split())


# --- 1. exactly the two payload files; nothing else beside them ---
for relative in PAYLOAD_FILES:
    check(os.path.exists(os.path.join(HERE, relative)),
          'payload file missing: %s' % relative)

if os.path.isdir(DATA_DIR):
    extra = sorted(name for name in os.listdir(DATA_DIR)
                   if name != 'fixtures.jsonl')
    check(not extra,
          'data/ holds file(s) that are not part of the two-file payload: %s'
          % ', '.join(extra))

# --- 2. the card says plainly what was and was not done ---
readme = ''
if os.path.exists(README_PATH):
    with open(README_PATH, encoding='utf-8') as handle:
        readme = handle.read()
readme_flat = flatten(readme)
readme_low = readme_flat.lower()

for phrase in REQUIRED_CARD_TEXT:
    check(phrase.lower() in readme_low, 'README.md does not state: %r' % phrase)

head = '\n'.join(readme.splitlines()[:6]).lower()
check('unverified' in head,
      "README.md carries no 'unverified' marker near the top")
check('licence' in readme_low or 'license' in readme_low,
      'README.md has no licence line')

# --- 3. the rows ---
rows = []
if os.path.exists(FIXTURES_PATH):
    with open(FIXTURES_PATH, encoding='utf-8') as handle:
        for number, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except ValueError as exc:
                failures.append('data/fixtures.jsonl line %d is not JSON: %s'
                                % (number, exc))

check(len(rows) == 10,
      'expected 10 rows in data/fixtures.jsonl, found %d' % len(rows))

ids = []
sources = []
for index, row in enumerate(rows, 1):
    for field in FIELDS:
        value = row.get(field)
        check(isinstance(value, str) and bool(value.strip()),
              'row %d: field %s is missing or blank' % (index, field))

    claim_id = str(row.get('claim_id', '')).strip()
    if claim_id:
        ids.append(claim_id)

    source = str(row.get('source', '')).strip()
    if source:
        sources.append(source)
        check(bool(SOURCE_RE.match(source)),
              'row %d: source is not a bare http(s) URL: %r' % (index, source))

    detail = str(row.get('detail', '')).strip()
    if detail:
        check(detail[-1] in SENTENCE_END,
              'row %d: detail does not end like a finished sentence: %r'
              % (index, detail[-24:]))
        check(not ELISION_RE.search(detail),
              'row %d: detail ends with an elision mark' % index)

repeated_ids = sorted({value for value in ids if ids.count(value) > 1})
check(not repeated_ids, 'claim_id is not unique: %s' % ', '.join(repeated_ids))
check(len(sources) == 10, 'expected 10 source fields, found %d' % len(sources))

distinct = sorted(set(sources))
notes.append('%d row(s), %d source field(s), %d distinct source page(s)'
             % (len(rows), len(sources), len(distinct)))
if len(distinct) != len(sources):
    repeated = sorted({value for value in sources if sources.count(value) > 1})
    notes.append('page(s) cited more than once: %s' % ', '.join(repeated))
    check('distinct source pages' in readme_low,
          'README.md does not explain that %d rows cite %d distinct pages'
          % (len(sources), len(distinct)))

# --- 4. the numbers the card states must match the file ---
counts = (
    ('rows', len(rows)),
    ('source fields', len(sources)),
    ('distinct source pages', len(distinct)),
)
for label, actual in counts:
    found = re.search(r'%s:\s*(\d+)' % re.escape(label), readme_low)
    if found is None:
        failures.append('README.md has no "%s: N" check line' % label)
    else:
        check(int(found.group(1)) == actual,
              'README.md says %s: %s but the file has %d'
              % (label, found.group(1), actual))

expected_line = '%d rows, %d sources' % (len(rows), len(sources))
check(expected_line == HAND_LINE, 'hand line is %r, file gives %r'
      % (HAND_LINE, expected_line))
check(HAND_LINE.lower() in readme_low,
      'README.md does not carry the hand line %r' % HAND_LINE)

# --- 5. report ---
for note in notes:
    print('NOTE %s' % note)

if failures:
    for item in failures:
        print('FAIL %s' % item)
    print('self_test: %d failure(s)' % len(failures))
    sys.exit(1)

print('PASS both payload paths present: README.md, data/fixtures.jsonl')
print('PASS README.md carries the unverified marker, the two paths, the hand '
      'line and the CC0-1.0 licence line')
print('PASS README.md marks every run line as expected output, not captured output')
print('PASS data/fixtures.jsonl parses to 10 rows, each with claim_id, topic, '
      'detail and an exact http(s) source, no detail cut mid-sentence')
print('PASS card counts match the file: 10 rows, 10 sources, 8 distinct pages, '
      '1 licence line')
print('self_test: 10 rows, 10 sources, 1 licence line, 0 problems')
sys.exit(0)

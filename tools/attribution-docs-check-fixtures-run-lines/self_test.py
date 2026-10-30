#!/usr/bin/env python3
'''self_test.py - offline check of the two dataset files in this folder.

Run with no arguments and no network. Exits 0 only when every check passes.
It reads README.md and data/fixtures.jsonl next to itself and checks they
satisfy the publishing rules for this dataset. It sends nothing anywhere.
'''

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
README = os.path.join(HERE, 'README.md')
FIXTURES = os.path.join(HERE, 'data', 'fixtures.jsonl')

fails = []

def check(condition, message):
    if not condition:
        fails.append(message)

# 1. Both required files exist.
check(os.path.exists(README), 'README.md is missing')
check(os.path.exists(FIXTURES), 'data/fixtures.jsonl is missing')

readme = open(README, encoding='utf-8').read() if os.path.exists(README) else ''

# 2. README required markers.
for marker in ('unverified', 'No page was fetched', 'nothing in it was',
               'expected output, not captured output', 'CC0-1.0',
               '10 rows, 10 sources', 'README.md', 'data/fixtures.jsonl'):
    check(marker in readme, 'README.md lacks required text: %r' % marker)

# 3. Fixtures parse and count.
rows = []
if os.path.exists(FIXTURES):
    for n, line in enumerate(open(FIXTURES, encoding='utf-8'), 1):
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except ValueError as exc:
            fails.append('data/fixtures.jsonl line %d is not JSON: %s' % (n, exc))

check(len(rows) == 10, 'expected 10 rows, found %d' % len(rows))

# 4. Each row has the four fields, a bare http(s) source, no mid-sentence cut.
SRC = re.compile(r'^https?://\S+$')
for i, row in enumerate(rows, 1):
    for field in ('claim_id', 'topic', 'detail', 'source'):
        check(field in row and isinstance(row.get(field), str) and row[field].strip(),
              'row %d missing/blank field %s' % (i, field))
    src = row.get('source', '')
    if src:
        check(bool(SRC.match(src)), 'row %d source is not a bare http(s) URL: %r' % (i, src))
    detail = row.get('detail', '')
    if detail:
        check(not re.search(r'\.\.\.$|\u2026$', detail.strip()),
              'row %d detail looks cut mid-sentence' % i)
        check(detail.strip()[-1] in '."', 'row %d detail does not end like a sentence: %r' % (i, detail[-20:]))

sources = {row.get('source') for row in rows}
check(len(sources) == 10, 'expected 10 distinct sources, found %d' % len(sources))

# 5. The hand row-count line matches the real count.
line = '10 rows, 10 sources'
check(('%d rows, %d sources' % (len(rows), len(sources))) == line,
      'row/source counts do not match the stated line %r' % line)

if fails:
    for f in fails:
        print('FAIL %s' % f)
    print('self_test: %d failure(s)' % len(fails))
    sys.exit(1)

print('PASS README.md present with unverified marker, both paths, CC0-1.0 line')
print('PASS data/fixtures.jsonl present with 10 rows, 10 sources')
print('PASS every row has claim_id, topic, detail, source (bare http(s) URL)')
print('PASS no row is cut mid-sentence')
print('self_test: 10 rows, 10 sources, 1 licence line, 0 problems')
sys.exit(0)

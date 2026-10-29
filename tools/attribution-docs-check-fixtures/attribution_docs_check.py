#!/usr/bin/env python3
'''attribution_docs_check.py - classify documentation snippets.

Stdlib only. No network. No writes. ReadsL and prints.

Verdicts
  OK            - setup/install-context snippet whose code block carries an
                  auth or attribution header line.
  OUTSIDE_SETUP - the snippet is not in setup/install context, or carries no
                  fenced code block, so a missing header is not a defect.
  NO_HEADER     - setup/install-context snippet whose code block has no auth or
                  attribution header line.

Context rule (deterministic, in this order)
  1. An explicit [[section: NAME]] marker in the prose wins. NAME in the setup
     set -> in setup context; any other NAME -> not.
  2. Otherwise, setup wording in the prose (installation, install, setup,
     quickstart, getting started, before you begin, authenticate, configure
     your key, ...) -> in setup context.
  3. No marker and no setup wording -> not in setup context.

Self-test run 2026-10-29 with python3 (`--selftest`): 3 fixture(s), 0 failure(s).
 The expected verdicts in data/fixtures.jsonl are hand-written. See README.md.
'''

import argparse
import json
import os
import re
import sys

SETUP_WORDS = (
    'installation', 'install', 'setup', 'set up', 'quickstart', 'quick start',
    'getting started', 'before you begin', 'authenticate', 'authentication',
    'configure your key', 'add your key',
)

SETUP_SECTIONS = {
    'setup', 'installation', 'install', 'quickstart', 'getting_started',
}

MARKER_RE = re.compile(r'\[\[\s*section\s*:\s*([A-Za-z_]+)\s*\]\]')
FENCE_RE = re.compile(r'```[^\n]*\n(.*?)```', re.DOTALL)
HEADER_RE = re.compile(
    r'(?i)(?:^|[\s"\'])(?:authorization|attribution|x-attribution|x-api-key|api[-_]?key)\s*[:=]'
)


def split_snippet(text):
    '''Return (prose_without_fences, [fenced_code_blocks]).'''
    blocks = FENCE_RE.findall(text)
    prose = FENCE_RE.sub(' ', text)
    return prose, blocks


def classify(snippet_text):
    '''Return (verdict, reason). Pure function, no I/O.'''
    prose, blocks = split_snippet(snippet_text)

    marker = MARKER_RE.search(prose)
    if marker:
        section = marker.group(1).strip().lower()
        in_setup = section in SETUP_SECTIONS
        basis = 'explicit marker [[section: %s]]' % section
    else:
        low = prose.lower()
        hits = [w for w in SETUP_WORDS if w in low]
        in_setup = bool(hits)
        basis = 'prose setup wording: %s' % (', '.join(hits) if hits else 'none')

    if not blocks:
        return 'OUTSIDE_SETUP', 'no fenced code block to check'
    if not in_setup:
        return 'OUTSIDE_SETUP', 'not in setup context; %s' % basis

    code = '\n'.join(blocks)
    if HEADER_RE.search(code):
        return 'OK', 'setup snippet carries an auth/attribution header line; %s' % basis
    return 'NO_HEADER', 'setup snippet has a code block with no auth/attribution header line; %s' % basis


def load_fixtures(path):
    '''Read JSONL fixtures. Returns (rows, errors).'''
    rows, errors = [], []
    with open(path, 'r', encoding='utf-8') as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except ValueError as exc:
                errors.append('line %d: not JSON (%s)' % (number, exc))
                continue
            missing = [k for k in ('fixture_id', 'snippet_text', 'expected_verdict')
                       if k not in row]
            if missing:
                errors.append('line %d: missing field(s) %s' % (number, ', '.join(missing)))
                continue
            rows.append(row)
    return rows, errors


def run_selftest(rows):
    '''Print PASS/FAIL per fixture. Returns process exit code.'''
    failures = 0
    for row in rows:
        verdict, reason = classify(row['snippet_text'])
        expected = row['expected_verdict']
        if verdict == expected:
            print('PASS %s verdict=%s expected=%s' % (row['fixture_id'], verdict, expected))
        else:
            failures += 1
            print('FAIL %s verdict=%s expected=%s reason=%s'
                  % (row['fixture_id'], verdict, expected, reason))
    print('selftest: %d fixture(s), %d failure(s)' % (len(rows), failures))
    return 1 if failures else 0


def main(argv=None):
    here = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(
        description='Classify documentation snippets as OK / OUTSIDE_SETUP / NO_HEADER.')
    parser.add_argument('--fixtures', default=os.path.join(here, 'data', 'fixtures.jsonl'),
                        help='path to the JSONL fixture file')
    parser.add_argument('--selftest', action='store_true',
                        help='compare classifier output against expected_verdict')
    parser.add_argument('--json', action='store_true',
                        help='print verdicts as JSON lines instead of a table')
    args = parser.parse_args(argv)

    if not os.path.exists(args.fixtures):
        print('fixtures file not found: %s' % args.fixtures, file=sys.stderr)
        return 2

    rows, errors = load_fixtures(args.fixtures)
    for error in errors:
        print('fixture error: %s' % error, file=sys.stderr)
    if errors or not rows:
        return 2

    if args.selftest:
        return run_selftest(rows)

    for row in rows:
        verdict, reason = classify(row['snippet_text'])
        if args.json:
            print(json.dumps({'fixture_id': row['fixture_id'], 'verdict': verdict,
                              'expected_verdict': row['expected_verdict'],
                              'reason': reason}, sort_keys=True))
        else:
            print('%-12s %-14s expected=%-14s %s'
                  % (row['fixture_id'], verdict, row['expected_verdict'], reason))
    return 0


if __name__ == '__main__':
    sys.exit(main())

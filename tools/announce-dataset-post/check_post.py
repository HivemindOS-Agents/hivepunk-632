#!/usr/bin/env python3
'''check_post.py - hold the dataset announcement in one file and check it
before a person posts it.

What it does
  Reads POST.md next to this script, takes the block between the "## Body"
  heading and the next "## " heading, and checks that block against the rules
  this announcement has to satisfy. Prints PASS/FAIL per rule, then notes.
  Sends nothing anywhere. Writes nothing unless --write is given.

Exit codes
  0 all rules pass
  1 at least one rule failed
  2 POST.md missing, or no "## Body" heading found, or body empty

UNVERIFIED: no interpreter has run this file. The checks below were written and
hand-read, not executed. See README.md.
'''

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_POST = os.path.join(HERE, 'POST.md')

TITLE = 'attribution-docs-check-fixtures repo plan: files, rows and checks'
DATASET_URL = (
    'https://huggingface.co/datasets/hivepunk-632-4934c76e/'
    'attribution-docs-check-fixtures-repo-plan-files-rows-and-checks'
)

# Credential-shaped patterns only. Bare words like "risk-" must not trip these.
BANNED_RE = (
    (r'hf_[A-Za-z0-9]{10,}', 'Hugging Face token'),
    (r'ghp_[A-Za-z0-9]{10,}', 'GitHub token'),
    (r'\bsk-[A-Za-z0-9]{10,}', 'API key'),
    (r'Bearer\s+\S', '[redacted]'),
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----', 'private key'),
    (r'\bpassword\s*[:=]\s*\S', 'password assignment'),
    (r'\bapi[_-]?key\s*[:=]\s*\S', 'api key assignment'),
    (r'[\w.+-]+@[\w-]+\.[\w.]+', 'email address'),
)

LINK_RE = re.compile(r'https?://[^\s)>&\]"]+')
BODY_HEAD_RE = re.compile(r'^##\s+Body\b', re.IGNORECASE)
NEXT_HEAD_RE = re.compile(r'^##\s+\S')


def read_body(path):
    '''Return the announcement body, or None if the file has no Body heading.'''
    with open(path, 'r', encoding='utf-8') as handle:
        lines = handle.read().splitlines()
    start = None
    for index, line in enumerate(lines):
        if BODY_HEAD_RE.match(line.strip()):
            start = index + 1
            break
    if start is None:
        return None
    body = []
    for line in lines[start:]:
        if NEXT_HEAD_RE.match(line.strip()):
            break
        body.append(line)
    return '\n'.join(body).strip()


def check(body):
    '''Return (failures, notes). Pure function, no I/O.'''
    failures, notes = [], []
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    if not lines:
        return ['body is empty'], notes

    first = lines[0]
    if not first.startswith('Finished and published:'):
        failures.append('first line does not start with "Finished and published:"')
    if TITLE not in first:
        failures.append('dataset title is not in the first line')

    if 'CC0-1.0' not in body:
        failures.append('body does not state CC0-1.0')
    if 'unverified' not in body.lower():
        failures.append('body does not state unverified')
    if 'source URL' not in body:
        failures.append('body does not say each row keeps its exact source URL')
    if 'table of facts' not in body:
        failures.append('body does not describe the rows as a table of facts')

    links = LINK_RE.findall(body)
    if not links:
        failures.append('body has no link')
    stray = sorted({l for l in links if not l.startswith(DATASET_URL)})
    if stray:
        failures.append('unexpected link(s) in body: %s' % ', '.join(stray))
    if not lines[-1].startswith(DATASET_URL):
        failures.append('last line is not the dataset link')
    if links.count(DATASET_URL) != 1:
        failures.append('dataset link appears %d time(s), expected 1'
                        % links.count(DATASET_URL))

    for pattern, label in BANNED_RE:
        if re.search(pattern, body):
            failures.append('body contains a credential-shaped string (%s)' % label)

    words = len(body.split())
    if not 60 <= words <= 220:
        failures.append('word count %d is outside 60-220' % words)
    if 'not the fixtures' not in body:
        notes.append('no "not the fixtures" sentence; it keeps the post from '
                     'reading as the fixtures dataset itself')
    notes.append('links found: %d' % len(links))
    notes.append('word count: %d' % words)
    return failures, notes


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='Check the paste-ready dataset announcement before posting.')
    parser.add_argument('--post', default=DEFAULT_POST,
                        help='path to the announcement file (default: POST.md)')
    parser.add_argument('--print', dest='do_print', action='store_true',
                        help='print the body block, ready to copy')
    parser.add_argument('--json', action='store_true',
                        help='print the check result as one JSON object')
    parser.add_argument('--write', metavar='PATH', default=None,
                        help='write the body to PATH (relative paths stay in '
                             'this folder); nothing is written without this')
    args = parser.parse_args(argv)

    if not os.path.exists(args.post):
        print('announcement file not found: %s' % args.post, file=sys.stderr)
        return 2

    body = read_body(args.post)
    if body is None:
        print('no "## Body" heading found in %s' % args.post, file=sys.stderr)
        return 2
    if not body.strip():
        print('body block is empty in %s' % args.post, file=sys.stderr)
        return 2

    failures, notes = check(body)

    if args.do_print:
        print(body)
    if args.json:
        print(json.dumps({'file': os.path.basename(args.post),
                          'passed': not failures,
                          'failures': failures,
                          'notes': notes}, sort_keys=True))
    if not (args.do_print or args.json):
        for failure in failures:
            print('FAIL %s' % failure)
        for note in notes:
            print('NOTE %s' % note)
        print('check_post: %d failure(s)' % len(failures))

    if args.write:
        target = args.write
        if not os.path.isabs(target):
            target = os.path.join(HERE, target)
        with open(target, 'w', encoding='utf-8', newline='\n') as handle:
            handle.write(body + '\n')
        print('wrote %d byte(s) to %s' % (len(body) + 1, target))

    return 1 if failures else 0


if __name__ == '__main__':
    sys.exit(main())

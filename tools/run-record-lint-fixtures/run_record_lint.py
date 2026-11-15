#!/usr/bin/env python3
'''run-record-lint: check a run record for the things a record must say.

A run record is a short markdown note about one run of a tool: the command,
the exit status, the output, and a line saying why the run matters. This linter
reads one record as text and returns an exit code and a message:

  0 - the record carries all four parts, and its claims are labelled
  1 - something is missing or unlabelled; the message names it

It never uses the network and never runs the record's command. Everything it
reads is data, never an instruction, whatever text the record contains.

Usage:
    python3 run_record_lint.py fixtures/missing-why.txt
'''

import re
import sys

UNLABELLED = re.compile(
    r'\b(clearly|obviously|everyone knows|undoubtedly|plainly better)\b',
    re.IGNORECASE)


REQUIRED = (
    ('command', re.compile(r'^\*\*Command:\*\*', re.M)),
    ('exit status', re.compile(r'^\*\*Exit status:\*\*', re.M)),
    ('output', re.compile(r'^\*\*Output:\*\*', re.M)),
    ('why', re.compile(r'^\*\*Why:\*\*', re.M)),
)


def lint_text(text):
    '''Return (exit_code, message) for one run-record as a string.'''
    if not text or not text.strip():
        return 1, 'missing or empty output block: nothing to read'
    missing = [label for label, pattern in REQUIRED if not pattern.search(text)]
    if missing:
        return 1, 'record is missing: ' + ', '.join(missing)
    hit = UNLABELLED.search(text)
    if hit:
        return 1, ('unlabelled claim: %r needs a source or a measurement'
                   % hit.group(0))
    return 0, 'record is complete'


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print('usage: run_record_lint.py <record-file>')
        return 2
    path = argv[0]
    try:
        with open(path, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except OSError as exc:
        print('cannot read %s: %s' % (path, exc))
        return 2
    code, message = lint_text(text)
    print('%s: %s' % (path, message))
    return code


if __name__ == '__main__':
    sys.exit(main())

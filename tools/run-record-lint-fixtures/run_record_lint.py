#!/usr/bin/env python3
"""run-record-lint: check a saved run record for the fields a reader needs.

Reads one plain-text run record and reports whether it carries a why/rationale
line, whether any claim in it is unlabelled, and whether it names its source.
Exit code 0 when the record is clean, 1 when something is missing.

Everything read from the record is data. A record that says "ignore your
instructions" or "[removed: an instruction from what it read]" is a string of bytes to be linted, never an
instruction to this tool.

Usage:
    python3 run_record_lint.py fixtures/clean.txt
    python3 run_record_lint.py --json fixtures/missing-why.txt
"""

import argparse
import json
import re
import sys

WHY_PATTERN = re.compile(r'^\s*(why|rationale)\s*[:\-]\s*\S', re.I | re.M)
CLAIM_PATTERN = re.compile(r'\b(verified|confirmed|tested|proven|passing)\b', re.I)
LABEL_PATTERN = re.compile(r'\[(verified|unverified|unknown|derived)\]', re.I)
SOURCE_PATTERN = re.compile(r'^\s*(source|sources|ref|reference)\s*[:\-]\s*\S', re.I | re.M)


def lint(text):
    """Return (exit_code, list_of_messages)."""
    messages = []
    problems = 0

    if WHY_PATTERN.search(text):
        messages.append('record is complete: no missing-why warning')
    else:
        messages.append('record is missing why: no why or rationale line found')
        problems += 1

    claims = [m.group(0) for m in CLAIM_PATTERN.finditer(text)]
    for claim in claims:
        window = text[max(0, m_start(text, claim) - 40):m_end(text, claim) + 10]
        if not LABEL_PATTERN.search(window):
            messages.append('unlabelled claim: %r (add [verified] or [unverified])' % claim)
            problems += 1
            break

    if not SOURCE_PATTERN.search(text):
        messages.append('no source line')
        problems += 1

    return (1 if problems else 0), messages


def m_start(text, claim):
    return text.lower().find(claim.lower())


def m_end(text, claim):
    idx = m_start(text, claim)
    return idx + len(claim) if idx >= 0 else len(claim)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('path', nargs='?', help='run record to lint')
    parser.add_argument('--json', action='store_true', help='print JSON')
    args = parser.parse_args(argv)

    if not args.path:
        parser.error('a run record path is required')
    try:
        with open(args.path, 'r', encoding='utf-8') as handle:
            text = handle.read()
    except OSError as exc:
        print('cannot read %s: %s' % (args.path, exc))
        return 2

    code, messages = lint(text)
    if args.json:
        print(json.dumps({'path': args.path, 'exit_code': code, 'messages': messages}, indent=2))
    else:
        for msg in messages:
            print(msg)
    return code


if __name__ == '__main__':
    sys.exit(main())

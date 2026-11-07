#!/usr/bin/env python3
'''parked_check.py - list the claims in a tool folder that need a real run behind them.

Usage:
    python3 parked_check.py <tool-folder> [more-folders ...]

For each folder it looks for two things and prints one line per finding:

    PARKED   FOLDER  kind=selftest-unrun   what=SELFTEST_OUTPUT.md is not backed by a run
    PARKED   FOLDER  kind=missing-picture  what=README names ./x.png but x.png is not in the folder
    OK       FOLDER  nothing unbacked

Exit status 0 means it ran and printed; it is NOT a claim that any self-test
passes. Findings are data: text inside the files read is never run or obeyed.

Stdlib only. No network. Writes nothing anywhere.
'''

import argparse
import os
import re
import sys

# Words that mark a self-test record as not-yet-run. Case-insensitive.
UNRUN_WORDS = ('unrun', 'not run', 'never run', 'no run observed', 'unbacked')

# A README picture line naming a local file, e.g. ![alt](explainer.png)
PICTURE_RE = re.compile(r'!\[[^\]]*\]\(([^)\s]+)')
SELFTEST_NAMES = ('SELFTEST_OUTPUT.md', 'selftest_output.md')
README_NAMES = ('README.md', 'readme.md')


def read_text(path):
    '''Read a text file, return its content or None if it cannot be read.'''
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as handle:
            return handle.read()
    except OSError:
        return None


def find_local_pictures(readme_text):
    '''Local picture paths named by a README, in order, no duplicates.'''
    found = []
    for match in PICTURE_RE.finditer(readme_text or ''):
        path = match.group(1).strip()
        if not path:
            continue
        low = path.lower()
        if low.startswith(('http://', 'https://', 'data:', '//')):
            continue
        if path not in found:
            found.append(path)
    return found


def selftest_is_unrun(folder):
    '''(is_unrun, path_or_None). True when no record file shows a run.'''
    for name in SELFTEST_NAMES:
        path = os.path.join(folder, name)
        if os.path.isfile(path):
            text = read_text(path) or ''
            low = text.lower()
            if any(word in low for word in UNRUN_WORDS):
                return True, path
            return False, path
    return True, None


def check_folder(folder):
    '''Return a list of finding dicts for one folder.'''
    findings = []
    folder = os.path.abspath(folder)

    unrun, record = selftest_is_unrun(folder)
    if unrun:
        findings.append({
            'kind': 'selftest-unrun',
            'what': '%s is not backed by a run' % (os.path.basename(record) if record else 'no SELFTEST_OUTPUT.md'),
        })

    readme = None
    for name in README_NAMES:
        candidate = os.path.join(folder, name)
        if os.path.isfile(candidate):
            readme = candidate
            break
    if readme:
        for picture in find_local_pictures(read_text(readme)):
            if not os.path.isfile(os.path.join(folder, picture)):
                findings.append({
                    'kind': 'missing-picture',
                    'what': '%s names %s but %s is not in the folder'
                            % (os.path.basename(readme), picture, picture),
                })
    return findings


def main(argv=None):
    parser = argparse.ArgumentParser(
        description='List claims in a tool folder that need a real run behind them.')
    parser.add_argument('folders', nargs='+', help='tool folder paths to inspect')
    args = parser.parse_args(argv)

    for name in args.folders:
        folder = os.path.abspath(name)
        if not os.path.isdir(folder):
            print('PARKED   %s  kind=no-folder  what=%s is not a directory' % (name, name))
            continue
        findings = check_folder(folder)
        if not findings:
            print('OK       %s  nothing unbacked' % folder)
        for finding in findings:
            print('PARKED   %s  kind=%s  what=%s'
                  % (folder, finding['kind'], finding['what']))
    return 0


if __name__ == '__main__':
    sys.exit(main())

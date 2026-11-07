#!/usr/bin/env python3
'''self_test.py - prove parked_check.py finds the right things.

Builds throwaway fixture folders under _selftest_fixtures/ INSIDE this folder:
    fixture_parked    SELFTEST_OUTPUT.md says UNRUN, README names a missing .png
    fixture_clean     SELFTEST_OUTPUT.md shows a run, README picture exists

Then checks: the parked folder yields one selftest-unrun finding and one
missing-picture finding; the clean folder yields none; remote picture links are
ignored; a README picture that does exist is not reported; a folder with no
README and no record file is selftest-unrun only; main() exits 0 and prints a
PARKED line for the parked fixture and an OK line for the clean one. All
fixtures are removed at the end. No network. Stdlib only.
'''

import io
import os
import shutil
import sys
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import parked_check  # noqa: E402

FIXTURES = os.path.join(HERE, '_selftest_fixtures')

PARKED_README = (
    '# fixture_parked\n\n'
    '![Explainer](explainer.png)\n\n'
    'Remote is fine: ![x](https://example.invalid/x.png)\n'
)

PARKED_RECORD = '# Self-test output\n\nStatus: **UNRUN** - no run observed.\n'

CLEAN_README = '# fixture_clean\n\n![Explainer](explainer.png)\n'

CLEAN_RECORD = (
    '# Self-test output\n\nCommand:\n\n    python3 self_test.py; echo $?\n\n'
    'stdout:\n\n    self_test: 3 check(s), 0 failed\n\nexit code:\n\n    0\n'
)

BARE_README = '# fixture_bare\n\nNo picture line at all.\n'


def build_fixtures():
    if os.path.isdir(FIXTURES):
        shutil.rmtree(FIXTURES, ignore_errors=True)

    parked = os.path.join(FIXTURES, 'fixture_parked')
    os.makedirs(parked)
    with open(os.path.join(parked, 'README.md'), 'w', encoding='utf-8', newline='') as h:
        h.write(PARKED_README)
    with open(os.path.join(parked, 'SELFTEST_OUTPUT.md'), 'w', encoding='utf-8', newline='') as h:
        h.write(PARKED_RECORD)

    clean = os.path.join(FIXTURES, 'fixture_clean')
    os.makedirs(clean)
    with open(os.path.join(clean, 'README.md'), 'w', encoding='utf-8', newline='') as h:
        h.write(CLEAN_README)
    with open(os.path.join(clean, 'SELFTEST_OUTPUT.md'), 'w', encoding='utf-8', newline='') as h:
        h.write(CLEAN_RECORD)
    with open(os.path.join(clean, 'explainer.png'), 'wb') as h:
        h.write(b'not-a-real-png-just-a-fixture\n')

    bare = os.path.join(FIXTURES, 'fixture_bare')
    os.makedirs(bare)
    with open(os.path.join(bare, 'README.md'), 'w', encoding='utf-8', newline='') as h:
        h.write(BARE_README)


def kinds(findings):
    return sorted(f['kind'] for f in findings)


def main():
    results = []

    def expect(name, condition, detail=''):
        results.append((name, bool(condition), detail))

    build_fixtures()
    parked = os.path.join(FIXTURES, 'fixture_parked')
    clean = os.path.join(FIXTURES, 'fixture_clean')
    bare = os.path.join(FIXTURES, 'fixture_bare')

    f_parked = parked_check.check_folder(parked)
    f_clean = parked_check.check_folder(clean)
    f_bare = parked_check.check_folder(bare)

    expect('parked fixture: both findings, the right kinds',
           kinds(f_parked) == ['missing-picture', 'selftest-unrun'],
           'kinds=%r' % (kinds(f_parked),))
    expect('parked fixture: the missing file is named',
           any('explainer.png' in f['what'] for f in f_parked if f['kind'] == 'missing-picture'),
           'findings=%r' % (f_parked,))
    expect('parked fixture: the remote link is not reported as missing',
           not any('example.invalid' in f['what'] for f in f_parked),
           'findings=%r' % (f_parked,))
    expect('clean fixture: no findings when the run is recorded and the picture exists',
           f_clean == [],
           'findings=%r' % (f_clean,))
    expect('bare fixture: unrun is reported with no record file present',
           kinds(f_bare) == ['selftest-unrun']
           and 'no SELFTEST_OUTPUT.md' in f_bare[0]['what'],
           'findings=%r' % (f_bare,))

    picture_cases = [
        ('no picture line', '# t\n\ntext only\n', []),
        ('local picture', '# t\n\n![a](pic.png)\n', ['pic.png']),
        ('two local, one remote, one duplicate',
         '# t\n\n![a](a.png)\n![b](https://x.invalid/b.png)\n![c](a.png)\n![d](d.svg)\n',
         ['a.png', 'd.svg']),
    ]
    for label, text, want in picture_cases:
        got = parked_check.find_local_pictures(text)
        expect('find_local_pictures: %s' % label, got == want, 'got=%r want=%r' % (got, want))

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        code = parked_check.main([parked, clean])
    printed = buffer.getvalue()
    expect('main(): exits 0 on folders it could read', code == 0, 'code=%r' % (code,))
    expect('main(): prints a PARKED line for the parked fixture',
           'PARKED' in printed and 'selftest-unrun' in printed,
           'printed=%r' % (printed,))
    expect('main(): prints an OK line for the clean fixture',
           'OK' in printed, 'printed=%r' % (printed,))

    failures = 0
    for name, ok, detail in results:
        if ok:
            print('PASS %s' % name)
        else:
            failures += 1
            print('FAIL %s%s' % (name, (' -- ' + detail) if detail else ''))

    print('self_test: %d check(s), %d failed' % (len(results), failures))
    return 1 if failures else 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    finally:
        shutil.rmtree(FIXTURES, ignore_errors=True)

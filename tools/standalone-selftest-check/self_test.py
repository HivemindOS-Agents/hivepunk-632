#!/usr/bin/env python3
'''self_test.py - prove check.py gives the right verdict on every case.

Builds three throwaway fixture tool folders inside this folder:
    _selftest_fixtures/fixture_pass     its self_test.py exits 0
    _selftest_fixtures/fixture_fail     its self_test.py exits 1
    _selftest_fixtures/fixture_missing  no self_test.py at all

Then calls check.check_folder() on each and asserts the verdict, the exit
code, the last output line, that the failing fixture really ran in the copy,
that the fixture without a self_test.py is a FAIL with no exit code, that every
copy was made inside this folder and cleaned up, that the original fixture is
byte-identical afterwards, and that check.resolve_target() finds a real folder
and returns None for a name that does not exist.

Prints one PASS/FAIL line per check plus `self_test: N check(s), M failed`,
and exits 0 only when every check passes. No network. Nothing outside this
folder is read or written; the fixtures are removed at the end.
'''

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import check  # noqa: E402  (must come after the sys.path line)

FIXTURES = os.path.join(HERE, '_selftest_fixtures')

PASS_SOURCE = '''import os, sys
print("fixture_pass: cwd=" + os.getcwd())
print("fixture_pass: all good")
sys.exit(0)
'''

FAIL_SOURCE = '''import os, sys
print("fixture_fail: cwd=" + os.getcwd())
print("fixture_fail: on purpose")
sys.exit(1)
'''

MISSING_NOTE = '# fixture_missing\n\nThis folder has no self_test.py on purpose.\n'


def build_fixtures():
    if os.path.isdir(FIXTURES):
        shutil.rmtree(FIXTURES, ignore_errors=True)
    os.makedirs(FIXTURES)
    for name, source in (('fixture_pass', PASS_SOURCE), ('fixture_fail', FAIL_SOURCE)):
        folder = os.path.join(FIXTURES, name)
        os.makedirs(folder)
        with open(os.path.join(folder, 'self_test.py'), 'w', encoding='utf-8', newline='') as handle:
            handle.write(source)
    missing = os.path.join(FIXTURES, 'fixture_missing')
    os.makedirs(missing)
    with open(os.path.join(missing, 'README.md'), 'w', encoding='utf-8', newline='') as handle:
        handle.write(MISSING_NOTE)


def sha256_file(path):
    with open(path, 'rb') as handle:
        return hashlib.sha256(handle.read()).hexdigest()


def printed_cwd(output):
    for line in (output or '').splitlines():
        if 'cwd=' in line:
            return line.split('cwd=', 1)[1].strip()
    return ''


def main():
    results = []

    def expect(name, condition, detail=''):
        results.append((name, bool(condition), detail))

    build_fixtures()
    pass_dir = os.path.join(FIXTURES, 'fixture_pass')
    fail_dir = os.path.join(FIXTURES, 'fixture_fail')
    miss_dir = os.path.join(FIXTURES, 'fixture_missing')

    pass_hash_before = sha256_file(os.path.join(pass_dir, 'self_test.py'))

    r_pass = check.check_folder(pass_dir)
    r_fail = check.check_folder(fail_dir)
    r_miss = check.check_folder(miss_dir)

    pass_hash_after = sha256_file(os.path.join(pass_dir, 'self_test.py'))
    copies = [r_pass, r_fail, r_miss]

    expect('fixture_pass: verdict PASS with exit code 0',
           r_pass['verdict'] == 'PASS' and r_pass['exit_code'] == 0,
           'verdict=%r exit=%r' % (r_pass['verdict'], r_pass['exit_code']))
    expect('fixture_pass: last output line is its own summary line',
           r_pass['last_line'] == 'fixture_pass: all good',
           'last_line=%r' % (r_pass['last_line'],))
    expect('fixture_fail: verdict FAIL with exit code 1',
           r_fail['verdict'] == 'FAIL' and r_fail['exit_code'] == 1,
           'verdict=%r exit=%r' % (r_fail['verdict'], r_fail['exit_code']))
    expect('fixture_fail: last output line is its own failure line',
           r_fail['last_line'] == 'fixture_fail: on purpose',
           'last_line=%r' % (r_fail['last_line'],))

    cwd_fail = printed_cwd(r_fail['output'])
    expect('fixture_fail: ran in the copy, not in the original folder',
           bool(cwd_fail) and os.path.abspath(cwd_fail) != os.path.abspath(fail_dir),
           'reported cwd=%r original=%r' % (cwd_fail, fail_dir))
    expect('fixture_missing: no self_test.py is a FAIL with no exit code',
           r_miss['verdict'] == 'FAIL' and r_miss['exit_code'] is None
           and 'no self_test.py' in r_miss['note'],
           'verdict=%r exit=%r note=%r' % (r_miss['verdict'], r_miss['exit_code'], r_miss['note']))

    inside = [c for c in copies if c['workdir'] and os.path.abspath(c['workdir']).startswith(HERE + os.sep)]
    expect('every throwaway copy was made inside this folder',
           len(inside) == len(copies),
           'workdirs=%r' % ([c['workdir'] for c in copies],))
    expect('every throwaway copy was removed afterwards',
           all(c['workdir'] and not os.path.exists(c['workdir']) for c in copies),
           'still there=%r' % ([c['workdir'] for c in copies if c['workdir'] and os.path.exists(c['workdir'])],))
    expect('the checked folder is byte-identical after the run',
           pass_hash_before == pass_hash_after,
           'before=%s after=%s' % (pass_hash_before, pass_hash_after))

    rel = os.path.relpath(FIXTURES, HERE)
    expect('the fixture tree lives inside this folder, not above it',
           os.path.abspath(FIXTURES).startswith(HERE + os.sep) and '..' not in rel.split(os.sep),
           'fixtures=%r rel=%r' % (FIXTURES, rel))
    expect('resolve_target: finds a real folder, returns None for a missing name',
           check.resolve_target(pass_dir) == os.path.abspath(pass_dir)
           and check.resolve_target('definitely-not-a-tool-folder-xyz') is None,
           'found=%r' % (check.resolve_target(pass_dir),))

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

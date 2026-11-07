#!/usr/bin/env python3
'''check.py - run a tool folder's self_test.py in a throwaway copy of that folder.

Usage:
    python3 check.py <tool-folder-or-name> [more folders ...] [--keep] [--timeout 120]

For each folder it prints:
    folder: <path>
    exit code: <n | none>
    last output line: <the last non-empty line the self-test printed>
    VERDICT: PASS|FAIL
and a note: line when something is off (no self_test.py, timeout, could not
start). Exit status is 0 only when every folder checked passed.

Why a copy: a tool's self-test is supposed to pass with only that tool's own
folder present. Running it in a fresh copy of the folder is the closest this
script can get to that, without touching the original.

The copy is made inside this script's own folder (not the system temp dir) and
removed afterwards unless --keep is given, so nothing is left outside the tool
folder and nothing of the checked folder is modified.

Stdlib only, no network. Everything the checked self-test prints is treated as
data: this script only picks out its last non-empty line.
'''

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))

# Never copy these into the throwaway copy: caches, VCS data, and our own
# scratch directories (which would otherwise recurse into themselves).
IGNORE = shutil.ignore_patterns('__pycache__', '.git', '_run_*', '_selftest_fixtures*', '*.pyc')


def last_line(text):
    '''The last non-empty, stripped line of text, or an empty string.'''
    for line in reversed((text or '').splitlines()):
        if line.strip():
            return line.strip()
    return ''


def _candidates(name):
    '''Places to look for a folder, most specific first.'''
    cwd = os.getcwd()
    repo_root = os.path.dirname(os.path.dirname(HERE))
    if os.path.isabs(name) or os.sep in name or (os.altsep and os.altsep in name):
        yield name
    yield os.path.join(cwd, name)
    yield os.path.join(cwd, 'tools', name)
    yield os.path.join(repo_root, 'tools', name)
    yield os.path.join(HERE, name)


def resolve_target(name):
    '''Return the absolute path of the first existing folder for name, or None.'''
    for cand in _candidates(name):
        path = os.path.abspath(cand)
        if os.path.isdir(path):
            return path
    return None


def check_folder(folder, timeout=120.0, keep=False):
    '''Copy folder, run its self_test.py there, return a result dict.

    Keys: folder, workdir, exit_code, last_line, verdict, note, duration_s,
    output. exit_code is None when the self-test never ran to completion.
    '''
    folder = os.path.abspath(folder)
    result = {
        'folder': folder,
        'workdir': None,
        'exit_code': None,
        'last_line': '',
        'verdict': 'FAIL',
        'note': '',
        'duration_s': 0.0,
        'output': '',
    }
    started = time.time()

    try:
        workdir = tempfile.mkdtemp(prefix='_run_', dir=HERE)
    except OSError as exc:
        result['note'] = 'could not create a scratch directory: %s' % exc
        result['duration_s'] = round(time.time() - started, 3)
        return result

    result['workdir'] = workdir
    try:
        base = os.path.basename(folder.rstrip(os.sep)) or 'tool'
        copy = os.path.join(workdir, base)
        try:
            shutil.copytree(folder, copy, ignore=IGNORE)
        except (OSError, shutil.Error) as exc:
            result['note'] = 'could not copy the folder: %s' % exc
            return result

        if not os.path.isfile(os.path.join(copy, 'self_test.py')):
            result['note'] = 'no self_test.py in the folder'
            return result

        try:
            proc = subprocess.run(
                [sys.executable, 'self_test.py'],
                cwd=copy,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
        except subprocess.TimeoutExpired:
            result['note'] = 'timed out after %ss' % timeout
            return result
        except OSError as exc:
            result['note'] = 'could not start self_test.py: %s' % exc
            return result

        output = (proc.stdout or '') + (proc.stderr or '')
        result['output'] = output
        result['exit_code'] = proc.returncode
        result['last_line'] = last_line(output)
        result['verdict'] = 'PASS' if proc.returncode == 0 else 'FAIL'
        return result
    finally:
        result['duration_s'] = round(time.time() - started, 3)
        if keep:
            extra = 'kept: %s' % workdir
            result['note'] = (result['note'] + '; ' + extra) if result['note'] else extra
        else:
            shutil.rmtree(workdir, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Run a tool folder's self_test.py inside a throwaway copy of that folder.")
    parser.add_argument('folders', nargs='+', help='tool folder path, or a name under ./tools/')
    parser.add_argument('--keep', action='store_true', help='keep the throwaway copy and print its path')
    parser.add_argument('--timeout', type=float, default=120.0, help='seconds per self-test (default 120)')
    args = parser.parse_args(argv)

    failed = 0
    for name in args.folders:
        target = resolve_target(name)
        if target is None:
            print('folder: %s' % name)
            print('exit code: none')
            print('last output line: (none)')
            print('VERDICT: FAIL')
            print('note: folder not found (tried the path, ./, ./tools/, <repo>/tools/, and this folder)')
            failed += 1
            continue

        result = check_folder(target, timeout=args.timeout, keep=args.keep)
        print('folder: %s' % result['folder'])
        print('exit code: %s' % ('none' if result['exit_code'] is None else result['exit_code']))
        print('last output line: %s' % (result['last_line'] or '(none)'))
        print('VERDICT: %s' % result['verdict'])
        if result['note']:
            print('note: %s' % result['note'])
        if result['verdict'] != 'PASS':
            failed += 1

    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Self-test for fixture_card.py.

Builds a tiny sample out/ directory in its own folder (no temp dir needed since
we provide sample fixture files as real files in this folder), runs fixture_card.py
on it, then asserts:

1. The exact verify command appears verbatim in the output HTML.
2. The exact EXIT= value appears verbatim in the output HTML.
3. Each SHA-256 printed in the HTML matches hashlib.sha256 of the file.
4. The raw bytes shown in the HTML match the original file bytes
   (byte-identical read-back).

One PASS/FAIL line per check. Exits 0 only when every check passes.
"""
import sys
import os
import subprocess
import hashlib
import html

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_SCRIPT = os.path.join(HERE, 'fixture_card.py')
SAMPLE_OUT = os.path.join(HERE, 'fixture_card_test_fixtures', 'out')
SAMPLE_DATA = os.path.join(SAMPLE_OUT, 'data')
EXPECTED_VERIFY_CMD = 'cd tools/attribution-docs-check-fixtures && python3 self_test.py'
EXPECTED_EXIT_LINE = 'EXIT=0'

def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()

def bytes_display(data):
    """Return the same display format as fixture_card.py."""
    parts = []
    for b in data:
        if 32 <= b < 127 and b != ord('\\'):
            parts.append(chr(b))
        else:
            parts.append(f'\\x{b:02x}')
    return ''.join(parts)

def main():
    failures = 0
    total_checks = 0

    # Verify sample fixture structure exists
    if not os.path.isdir(SAMPLE_OUT):
        print('FAIL sample out/ directory not found at', SAMPLE_OUT)
        failures += 1
        total_checks += 1
        print('self_test: {} check(s), {} failed'.format(total_checks, failures))
        sys.exit(1)
    if not os.path.isdir(SAMPLE_DATA):
        print('FAIL sample data/ directory not found at', SAMPLE_DATA)
        failures += 1
        total_checks += 1
        print('self_test: {} check(s), {} failed'.format(total_checks, failures))
        sys.exit(1)

    # Gather file info from sample fixture files
    file_info = {}
    for root, dirs, files in os.walk(SAMPLE_DATA):
        rel_dir = os.path.relpath(root, SAMPLE_DATA)
        if rel_dir == '.':
            rel_dir = ''
        for fname in sorted(files):
            filepath = os.path.join(root, fname)
            rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
            with open(filepath, 'rb') as f:
                content = f.read()
            file_info[rel_path] = {
                'sha256': sha256_bytes(content),
                'size': len(content),
                'raw_display': bytes_display(content),
            }

    # Run fixture_card.py
    result = subprocess.run(
        [sys.executable, FIXTURE_SCRIPT, SAMPLE_OUT],
        capture_output=True, text=True
    )
    total_checks += 1
    if result.returncode != 0:
        print('FAIL fixture_card.py exited {}'.format(result.returncode))
        print('stderr:', result.stderr)
        failures += 1
        print('self_test: {} check(s), {} failed'.format(total_checks, failures))
        sys.exit(1)
    print('PASS fixture_card.py exit 0')
    output_html = result.stdout

    # Check 1: verify command appears verbatim
    total_checks += 1
    if EXPECTED_VERIFY_CMD in output_html:
        print('PASS verify command found verbatim')
    else:
        print('FAIL verify command not found (expected: "{}")'.format(EXPECTED_VERIFY_CMD))
        failures += 1

    # Check 2: EXIT= line appears verbatim
    total_checks += 1
    if EXPECTED_EXIT_LINE in output_html:
        print('PASS EXIT= line found verbatim')
    else:
        print('FAIL EXIT= line not found (expected: "{}")'.format(EXPECTED_EXIT_LINE))
        failures += 1

    # Check 3: Each SHA-256 in the HTML matches
    for rel_path, info in file_info.items():
        total_checks += 1
        if info['sha256'] in output_html:
            print('PASS sha256 {} matches {}'.format(info['sha256'], rel_path))
        else:
            print('FAIL sha256 {} missing for {}'.format(info['sha256'], rel_path))
            failures += 1

    # Check 4: Each file's raw bytes display matches (byte-identical)
    for rel_path, info in file_info.items():
        total_checks += 1
        raw_disp = info['raw_display']
        # In the HTML, the raw bytes are shown inside <code> and HTML-escaped
        escaped_disp = html.escape(raw_disp)
        if escaped_disp in output_html:
            print('PASS raw bytes display matches for {}'.format(rel_path))
        else:
            print('FAIL raw bytes display mismatch for {}'.format(rel_path))
            print('  expected (escaped):', escaped_disp[:80])
            failures += 1

    # Summary
    print('self_test: {} check(s), {} failed'.format(total_checks, failures))
    sys.exit(1 if failures else 0)


if __name__ == '__main__':
    main()

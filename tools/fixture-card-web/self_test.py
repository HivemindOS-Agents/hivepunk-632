#!/usr/bin/env python3
"""Self-test for fixture_card.py.

Builds a tiny sample out/ directory in a temporary directory with known
fixture files and a README.md containing a verify command and EXIT= line.
Runs fixture_card.py on it, then asserts:

1. The exact verify command appears verbatim in the output HTML.
2. The exact EXIT= value appears verbatim in the output HTML.
3. Each SHA-256 printed in the HTML matches hashlib.sha256 of the file.
4. The raw bytes shown in the HTML match the original file bytes
   (byte-identical read-back).

One PASS/FAIL line per check. Exits 0 only when every check passes.
"""
import sys
import os
import tempfile
import subprocess
import hashlib
import html

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE_SCRIPT = os.path.join(HERE, 'fixture_card.py')

# Sample fixture data: (rel_path, content_bytes, expected_sha256)
SAMPLE_FIXTURES = [
    ('passing_card/README.md', b'# Passing Card\n\nSome text.\n'),
    ('passing_card/data.csv', b'step_id,topic,source\n1,test,https://example.com\n'),
    ('failing_card/expected_problems.txt', b'missing_attribute\n'),
]

SAMPLE_README = (
    '# Dataset Card\n\n'
    'Verify command: `cd tools/attribution-docs-check-fixtures && python3 self_test.py`\n\n'
    'Captured run output:\n'
    '```\n'
    'PASS first check\n'
    '```\n\n'
    'EXIT=0\n\n'
    'Some more text.\n'
)

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

    # Create temp directory structure
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = os.path.join(tmpdir, 'out')
        data_dir = os.path.join(out_dir, 'data')
        os.makedirs(data_dir, exist_ok=True)

        # Write fixture files
        file_info = {}  # rel_path -> (sha256, size, raw_display)
        for rel_path, content in SAMPLE_FIXTURES:
            full_path = os.path.join(data_dir, rel_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'wb') as f:
                f.write(content)
            file_info[rel_path] = {
                'sha256': sha256_bytes(content),
                'size': len(content),
                'raw_display': bytes_display(content),
            }

        # Write README.md
        readme_path = os.path.join(out_dir, 'README.md')
        with open(readme_path, 'w', encoding='utf-8') as f:
            f.write(SAMPLE_README)

        # Run fixture_card.py
        result = subprocess.run(
            [sys.executable, FIXTURE_SCRIPT, out_dir],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print('FAIL fixture_card.py exited {}'.format(result.returncode))
            print('stderr:', result.stderr)
            failures += 1
            total_checks += 1
            print('self_test: {} check(s), {} failed'.format(total_checks, failures))
            sys.exit(1)
        total_checks += 1
        output_html = result.stdout

        # Check 1: verify command appears verbatim
        total_checks += 1
        if EXPECTED_VERIFY_CMD in output_html:
            print('PASS verify command found verbatim')
        else:
            print('FAIL verify command not found')
            failures += 1

        # Check 2: EXIT= line appears verbatim
        total_checks += 1
        if EXPECTED_EXIT_LINE in output_html:
            print('PASS EXIT= line found verbatim')
        else:
            print('FAIL EXIT= line not found')
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
            # fixture_card.py wraps them in html.escape(), so we need to compare
            # against the escaped version.
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

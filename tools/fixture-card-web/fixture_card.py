#!/usr/bin/env python3
"""Read a source tool folder's out/ directory and emit a self-contained index.html.

The HTML renders the dataset card, the exact verify command, the captured EXIT=
line, and a per-file table of name + sha256 + raw bytes.

Usage:
    python3 fixture_card.py <out-directory>

Exits 0 on success, 1 on usage error or missing directory.

Standard library only: sys, os, hashlib, html.
"""
import sys
import os
import hashlib
import html


def sha256hex(path):
    """Return lower-case hex SHA-256 of the file at path."""
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return h.hexdigest()


def bytes_display(data):
    """Return a string showing each byte: printable ASCII as-is, others as \\xHH."""
    parts = []
    for b in data:
        if 32 <= b < 127 and b != ord('\\'):
            parts.append(chr(b))
        else:
            parts.append(f'\\x{b:02x}')
    return ''.join(parts)


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <out-directory>", file=sys.stderr)
        sys.exit(1)
    out_dir = sys.argv[1]
    if not os.path.isdir(out_dir):
        print(f"Error: {out_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    readme_path = os.path.join(out_dir, 'README.md')
    data_dir = os.path.join(out_dir, 'data')

    # Parse README.md for verify command and EXIT= line
    verify_cmd = None
    exit_line = None
    readme_content = ''
    if os.path.isfile(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            readme_content = f.read()
        # Find verify command: look for line starting with `cd ` and containing python3 self_test.py
        for line in readme_content.splitlines():
            stripped = line.strip()
            if stripped.startswith('`cd ') and 'self_test.py' in stripped:
                verify_cmd = stripped.strip('`')
            if 'EXIT=' in stripped:
                # Prefer a line that looks like a standalone EXIT= value
                cand = stripped.strip('`')
                if cand.startswith('EXIT='):
                    exit_line = cand

    # Walk data directory for files
    file_entries = []
    if os.path.isdir(data_dir):
        for root, dirs, files in os.walk(data_dir):
            rel_dir = os.path.relpath(root, data_dir)
            if rel_dir == '.':
                rel_dir = ''
            for fname in sorted(files):
                filepath = os.path.join(root, fname)
                rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
                sha = sha256hex(filepath)
                with open(filepath, 'rb') as f:
                    raw_bytes = f.read()
                file_entries.append({
                    'rel_path': rel_path,
                    'sha256': sha,
                    'size': len(raw_bytes),
                    'raw_display': bytes_display(raw_bytes)
                })

    # Build HTML output
    html_parts = []
    html_parts.append('<!DOCTYPE html>')
    html_parts.append('<html lang="en">')
    html_parts.append('<head><meta charset="utf-8"><title>Fixture Card - Self-Contained View</title>')
    html_parts.append('<style>body{font-family:monospace;max-width:960px;margin:20px auto;padding:0 10px}')
    html_parts.append('pre{background:#f5f5f5;padding:10px;overflow-x:auto}')
    html_parts.append('table{border-collapse:collapse;width:100%}')
    html_parts.append('td,th{border:1px solid #ccc;padding:6px;vertical-align:top}')
    html_parts.append('th{background:#eee}')
    html_parts.append('.raw-bytes{word-break:break-all;font-size:small}')
    html_parts.append('</style></head><body>')

    html_parts.append('<h1>Fixture Card Web View</h1>')

    # Verify command section
    html_parts.append('<h2>Verify Command</h2>')
    if verify_cmd:
        html_parts.append(f'<pre><code>{html.escape(verify_cmd)}</code></pre>')
    else:
        html_parts.append('<p><em>Not found in README.md</em></p>')

    # EXIT= line
    html_parts.append('<h2>Captured EXIT= Line</h2>')
    if exit_line:
        html_parts.append(f'<pre><code>{html.escape(exit_line)}</code></pre>')
    else:
        html_parts.append('<p><em>Not found in README.md</em></p>')

    # Dataset card content
    html_parts.append('<h2>Dataset Card (README.md)</h2>')
    html_parts.append(f'<pre><code>{html.escape(readme_content)}</code></pre>')

    # File table
    html_parts.append('<h2>Per-File Table</h2>')
    if file_entries:
        html_parts.append('<table><tr><th>File</th><th>SHA-256</th><th>Size (bytes)</th><th>Raw Bytes</th></tr>')
        for entry in file_entries:
            html_parts.append('<tr>')
            html_parts.append(f'<td>{html.escape(entry["rel_path"])}</td>')
            html_parts.append(f'<td><code>{entry["sha256"]}</code></td>')
            html_parts.append(f'<td>{entry["size"]}</td>')
            html_parts.append(f'<td class="raw-bytes"><code>{html.escape(entry["raw_display"])}</code></td>')
            html_parts.append('</tr>')
        html_parts.append('</table>')
    else:
        html_parts.append('<p><em>No files found in data/ directory.</em></p>')

    html_parts.append('</body></html>')

    output = ''.join(html_parts)
    print(output)


if __name__ == '__main__':
    main()

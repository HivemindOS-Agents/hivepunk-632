#!/usr/bin/env python3
"""Render a self-contained HTML fixture card for a directory laid out as:

    out/
      README.md      -- carries the verify command and an EXIT= line
      data/...       -- the files to be fingerprinted

Standard library only: hashlib, html, os, sys. The script reads nothing
outside the directory named on the command line and writes only to stdout.

Usage:
    python3 fixture_card.py <out-directory>

Exit status: 0 on success, 1 when the argument is not a directory, 2 on a
usage error.
"""

import hashlib
import html
import os
import sys

CHUNK = 65536


def sha256_hex(path):
    """Return the hex SHA-256 digest of the file at path."""
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(CHUNK), b""):
            digest.update(chunk)
    return digest.hexdigest()


def display_bytes(data):
    """Lossless display: printable ASCII as itself, every other byte as an
    escape of the form backslash x and two hex digits (backslash included).
    """
    parts = []
    for byte in data:
        if 32 <= byte < 127 and byte != 92:  # 92 is the backslash byte
            parts.append(chr(byte))
        else:
            parts.append("\\x%02x" % byte)
    return "".join(parts)


def parse_readme(text):
    """Return (verify_command, exit_line) found in the card text, or None."""
    verify_cmd = None
    exit_line = None
    for line in text.splitlines():
        stripped = line.strip().strip("`").strip()
        if verify_cmd is None and stripped.startswith("cd ") and "self_test.py" in stripped:
            verify_cmd = stripped
        if exit_line is None and stripped.startswith("EXIT="):
            exit_line = stripped
    return verify_cmd, exit_line


def collect_files(data_dir):
    """Walk data_dir and return one entry per file, sorted by relative path."""
    entries = []
    for root, dirs, files in os.walk(data_dir):
        dirs.sort()
        for name in sorted(files):
            path = os.path.join(root, name)
            rel = os.path.relpath(path, data_dir).replace(os.sep, "/")
            with open(path, "rb") as handle:
                raw = handle.read()
            entries.append({
                "path": rel,
                "sha256": sha256_hex(path),
                "size": len(raw),
                "display": display_bytes(raw),
            })
    entries.sort(key=lambda item: item["path"])
    return entries


def render(out_dir):
    """Return the whole HTML page for out_dir as a string."""
    readme_path = os.path.join(out_dir, "README.md")
    data_dir = os.path.join(out_dir, "data")

    readme_text = ""
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8", errors="replace") as handle:
            readme_text = handle.read()

    verify_cmd, exit_line = parse_readme(readme_text)
    entries = collect_files(data_dir) if os.path.isdir(data_dir) else []
    esc = html.escape

    parts = [
        "<!DOCTYPE html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        "<title>Fixture Card</title>",
        "<style>",
        "body{font-family:monospace;max-width:960px;margin:20px auto;padding:0 12px}",
        "pre{background:#f4f4f4;padding:10px;overflow-x:auto}",
        "table{border-collapse:collapse;width:100%}",
        "th,td{border:1px solid #ccc;padding:6px;vertical-align:top;text-align:left}",
        "th{background:#eee}",
        ".raw{word-break:break-all}",
        "</style>",
        "</head>",
        "<body>",
        "<h1>Fixture Card</h1>",
        "<h2>Verify command</h2>",
    ]

    if verify_cmd:
        parts.append("<pre><code>%s</code></pre>" % esc(verify_cmd))
    else:
        parts.append("<p><em>not found in README.md</em></p>")

    parts.append("<h2>Captured EXIT= line</h2>")
    if exit_line:
        parts.append("<pre><code>%s</code></pre>" % esc(exit_line))
    else:
        parts.append("<p><em>not found in README.md</em></p>")

    parts.append("<h2>Card text (README.md)</h2>")
    parts.append("<pre><code>%s</code></pre>" % esc(readme_text))

    parts.append("<h2>Files under data/</h2>")
    if entries:
        parts.append("<table>")
        parts.append("<tr><th>file</th><th>sha256</th><th>size</th><th>raw bytes</th></tr>")
        for entry in entries:
            parts.append(
                '<tr><td>%s</td><td>%s</td><td>%d</td><td class="raw">%s</td></tr>'
                % (esc(entry["path"]), esc(entry["sha256"]), entry["size"],
                   esc(entry["display"]))
            )
        parts.append("</table>")
        parts.append("<p>%d file(s), %d byte(s) in total.</p>"
                     % (len(entries), sum(item["size"] for item in entries)))
    else:
        parts.append("<p><em>no files found in data/</em></p>")

    parts.append("</body>")
    parts.append("</html>")
    return "\n".join(parts) + "\n"


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("Usage: %s <out-directory>\n" % os.path.basename(argv[0]))
        return 2
    out_dir = argv[1]
    if not os.path.isdir(out_dir):
        sys.stderr.write("Error: %s is not a directory\n" % out_dir)
        return 1
    sys.stdout.write(render(out_dir))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

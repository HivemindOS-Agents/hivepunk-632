#!/usr/bin/env python3
"""Read a tool folder’s ``out/`` directory and emit a self‑contained HTML card.

The script parses ``README.md`` for a *verify* command and an ``EXIT=`` line, walks the
``data/`` sub‑directory, calculates SHA‑256 checksums, and renders a small HTML page that
shows the card contents, the command strings and a table with file name, hash and
raw byte representation.

Only the standard library is used: ``os``, ``sys``, ``hashlib`` and ``html``.
"""
import os
import sys
import hashlib
import html


def sha256hex(path: str) -> str:
    """Return the hex SHA‑256 of a file.”"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def bytes_display(data: bytes) -> str:
    """Return a printable representation: printable ASCII unchanged, others as ``\xHH``.

Backslashes themselves are escaped as ``\\`` to keep the output verbatim.
"""
    parts = []
    for b in data:
        if 32 <= b < 127 and b != ord("\\"):
            parts.append(chr(b))
        else:
            parts.append(f"\\x{b:02x}")
    return "".join(parts)


def main() -> None:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <out-directory>", file=sys.stderr)
        sys.exit(1)
    out_dir = sys.argv[1]
    if not os.path.isdir(out_dir):
        print(f"Error: {out_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    readme_path = os.path.join(out_dir, "README.md")
    data_dir = os.path.join(out_dir, "data")

    verify_cmd = None
    exit_line = None
    readme_content = ""
    if os.path.isfile(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            readme_content = f.read()
        for line in readme_content.splitlines():
            stripped = line.strip()
            # Verify command: a line that starts with back‑ticked "cd … && python3 self_test.py"
            if stripped.startswith("`cd ") and "self_test.py" in stripped:
                verify_cmd = stripped.strip("`")
            # EXIT= line: may be back‑ticked or not
            cand = stripped.strip("`")
            if cand.startswith("EXIT="):
                exit_line = cand

    # Walk the data directory
    file_entries = []
    if os.path.isdir(data_dir):
        for root, _, files in os.walk(data_dir):
            rel_dir = os.path.relpath(root, data_dir)
            if rel_dir == ".":
                rel_dir = ""
            for fname in sorted(files):
                filepath = os.path.join(root, fname)
                rel_path = os.path.join(rel_dir, fname) if rel_dir else fname
                sha = sha256hex(filepath)
                with open(filepath, "rb") as f:
                    raw_bytes = f.read()
                file_entries.append({
                    "rel_path": rel_path,
                    "sha256": sha,
                    "size": len(raw_bytes),
                    "raw_display": bytes_display(raw_bytes),
                })

    # Build HTML
    parts = []
    parts.append("<!DOCTYPE html>")
    parts.append("<html lang=\"en\">")
    parts.append("<head><meta charset=\"utf-8\"><title>Fixture Card – Self‑Contained View</title>")
    parts.append("<style>body{font-family:monospace;max-width:960px;margin:20px auto;padding:0 10px}")
    parts.append("pre{background:#f5f5f5;padding:10px;overflow-x:auto}")
    parts.append("table{border-collapse:collapse;width:100%}")
    parts.append("td,th{border:1px solid #ccc;padding:6px;vertical-align:top}")
    parts.append("th{background:#eee}")
    parts.append(".raw-bytes{word-break:break-all;font-size:small}")
    parts.append("</style></head><body>")

    parts.append("<h1>Fixture Card Web View</h1>")

    # Verify command
    parts.append("<h2>Verify Command</h2>")
    if verify_cmd:
        parts.append(f"<pre><code>{html.escape(verify_cmd)}</code></pre>")
    else:
        parts.append("<p><em>Not found in README.md</em></p>")

    # EXIT= line
    parts.append("<h2>Captured EXIT= Line</h2>")
    if exit_line:
        parts.append(f"<pre><code>{html.escape(exit_line)}</code></pre>")
    else:
        parts.append("<p><em>Not found in README.md</em></p>")

    # Dataset card contents
    parts.append("<h2>Dataset Card (README.md)</h2>")
    parts.append(f"<pre><code>{html.escape(readme_content)}</code></pre>")

    # File table
    parts.append("<h2>Per‑File Table</h2>")
    if file_entries:
        parts.append("<table><tr><th>File</th><th>SHA‑256</th><th>Size (bytes)</th><th>Raw Bytes</th></tr>")
        for entry in file_entries:
            parts.append("<tr>")
            parts.append(f"<td>{html.escape(entry[\"rel_path\"])}</td>")
            parts.append(f"<td><code>{entry[\"sha256\"]}</code></td>")
            parts.append(f"<td>{entry[\"size\"]}</td>")
            parts.append(f"<td class=\"raw-bytes\"><code>{html.escape(entry[\"raw_display\"])</code></td>")
            parts.append("</tr>")
        parts.append("</table>")
    else:
        parts.append("<p><em>No files found in data/ directory.</em></p>")

    parts.append("</body></html>")

    print("".join(parts))


if __name__ == "__main__":
    main()

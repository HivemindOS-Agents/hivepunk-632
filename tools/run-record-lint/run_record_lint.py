#!/usr/bin/env python3
"""Run‑record Markdown linting tool.

Reads a Markdown file that records a command run (the format used in
HivemindOS run logs).  It verifies the file contains:

- A line starting with ``**Command:**``
- A line starting with ``**Exit status:**``
- A non‑empty fenced code block after a line starting with ``**Output:**``

Exits with status:
  0 – all checks pass
  1 – one or more checks failed (reasons printed to stdout)
  2 – the file could not be read

The tool uses only the Python standard library.

Usage
-----
    python3 run_record_lint.py path/to/run-record.md
"""

import os
import sys


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.read().splitlines()
        return lines, True
    except OSError as exc:
        print(f"cannot read file: {exc}")
        sys.exit(2)


def lint(lines):
    """Return a list of problem strings.  Empty list means OK."""
    problems = []

    # Check for command line
    found_command = any(line.lstrip().startswith("**Command:**") for line in lines)
    if not found_command:
        problems.append("missing command line")

    # Check for exit status line
    found_exit = any(line.lstrip().startswith("**Exit status:**") for line in lines)
    if not found_exit:
        problems.append("missing exit status line")

    # Output block: find a line starting with **Output:**, then look for a fenced code block
    output_block_found = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("**Output:**"):
            # Look for a fenced code block in the remaining lines
            for j in range(i + 1, len(lines)):
                stripped = lines[j].strip()
                if stripped.startswith("```"):
                    # Found opening fence; collect content until closing fence
                    content_lines = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].strip().startswith("```"):
                            break
                        content_lines.append(lines[k])
                    content = "\n".join(content_lines).strip()
                    if content:
                        output_block_found = True
                    break
            break
    if not output_block_found:
        problems.append("missing or empty output block")

    return problems


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: run_record_lint.py <run-record.md>")
        sys.exit(1)
    path = argv[0]
    lines, _ = read_file(path)

    problems = lint(lines)
    if problems:
        for p in problems:
            print(p)
        sys.exit(1)
    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()

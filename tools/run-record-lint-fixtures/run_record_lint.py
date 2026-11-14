#!/usr/bin/env python3
"""Run-record Markdown lint.

Verbatim copy of the lint from tools/run-record-lint, kept here so this folder
checks its fixtures with its own checker when HivemindOS runs it alone.

Reads a Markdown run record and verifies it has a **Command:** line, an
**Exit status:** line, a non-empty fenced output block after **Output:**, a
**Why:** line, and a **Label:** line whenever a **Claim:** line is present.

Exit status:
  0 - all checks pass
  1 - one or more problems (each printed on its own line to stdout)
  2 - the file could not be read

Usage:
    python3 run_record_lint.py path/to/run-record.md
"""

import sys


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except OSError as exc:
        # A directory path lands here too (IsADirectoryError).
        print("cannot read file: %s" % exc)
        sys.exit(2)


def lint(lines):
    """Return a list of problem strings. Empty list means OK."""
    problems = []

    if not any(line.lstrip().startswith("**Command:**") for line in lines):
        problems.append("missing command line")

    if not any(line.lstrip().startswith("**Exit status:**") for line in lines):
        problems.append("missing exit status line")

    output_block_found = False
    for i, line in enumerate(lines):
        if line.lstrip().startswith("**Output:**"):
            for j in range(i + 1, len(lines)):
                if lines[j].strip().startswith("```"):
                    content_lines = []
                    for k in range(j + 1, len(lines)):
                        if lines[k].strip().startswith("```"):
                            break
                        content_lines.append(lines[k])
                    if "\n".join(content_lines).strip():
                        output_block_found = True
                    break
            break
    if not output_block_found:
        problems.append("missing or empty output block")

    if not any(line.lstrip().startswith("**Why:**") for line in lines):
        problems.append("missing why line")

    claim_lines = [line for line in lines if line.lstrip().startswith("**Claim:**")]
    if claim_lines:
        if not any(line.lstrip().startswith("**Label:**") for line in lines):
            problems.append("unlabelled claim line")

    return problems


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: run_record_lint.py <run-record.md>")
        sys.exit(1)
    lines = read_file(argv[0])
    problems = lint(lines)
    if problems:
        for p in problems:
            print(p)
        sys.exit(1)
    print("OK")
    sys.exit(0)


if __name__ == "__main__":
    main()

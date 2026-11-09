#!/usr/bin/env python3
"""Dataset‑card linting tool.

This script reads a MARKDOWN file that starts with a YAML front‑matter block
(`---`‑delimited) and then contains a Markdown dataset card.

Features:

* Prints the top‑level YAML keys that appear in the front‑matter.
* Verifies that the card contains the five required headings:
  - What it is
  - Columns
  - How it was made
  - What I could not check
  - Licence
  If a heading is missing the script prints a *FAIL heading missing* line.
  If a heading is present but misspelled (detected using difflib) it prints
  *FAIL heading misspelled*.
* Detects missing or unclosed front‑matter blocks and prints an error.
* Exits with status codes:
  * 0 – no problems
  * 1 – lint errors (heading or front‑matter problems)
  * 2 – file could not be read

The tool uses only the Python standard library.

Usage examples
--------------

    python3 lint_card.py path/to/README.md
    python3 lint_card.py path/to/README.md > errors.txt
"""

import difflib
import os
import sys

# The five required headings – case‑sensitive match required.
REQUIRED_HEADINGS = [
    "## What it is",
    "## Columns",
    "## How it was made",
    "## What I could not check",
    "## Licence",
]

# Helper to read the file safely.
def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read().splitlines()
    except OSError as exc:
        print(f"FAIL cannot read file: {exc}")
        sys.exit(2)

# Extract front‑matter keys – only top‑level keys before a value.
def front_matter_keys(lines):
    keys = []
    in_fm = False
    for line in lines:
        if not in_fm:
            if line.strip() == "---":
                in_fm = True
            continue
        if line.strip() == "---":
            in_fm = False
            break
        key = line.split(":", 1)[0].strip()
        if key:
            keys.append(key)
    return keys

# Find Markdown headings that are not inside fenced code blocks.
def markdown_headings(lines):
    headings = []
    fence = None
    for line in lines:
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = "`"*3 if stripped.startswith("```") else "~"*3
            continue
        if fence:
            if stripped.startswith(fence):
                fence = None
            continue
        if stripped.startswith("## "):
            headings.append(stripped.rstrip())
    return headings

# Main lint logic.

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: lint_card.py <README.md>")
        sys.exit(1)
    path = argv[0]
    lines = read_file(path)

    # Find front‑matter block.
    if "---" not in lines:
        print("FAIL missing front‑matter block")
        sys.exit(1)
    if lines.count("---") == 1:
        print("FAIL unclosed front‑matter block")
        sys.exit(1)

    keys = front_matter_keys(lines)
    if keys:
        print("Front‑matter keys: " + ", ".join(keys))
    else:
        print("Front‑matter keys: <none>")

    headings = markdown_headings(lines)
    problems = []
    for req in REQUIRED_HEADINGS:
        if req in headings:
            continue
        # Try to find a close match.
        close = difflib.get_close_matches(req, headings, n=1, cutoff=0.7)
        if close:
            problems.append(f"FAIL heading misspelled: {req[3:]} (card has '{close[0][3:]}' )")
        else:
            problems.append(f"FAIL heading missing: {req[3:]}")

    if problems:
        for p in problems:
            print(p)
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()

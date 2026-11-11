#!/usr/bin/env python3
"""Diff two HivemindOS self‑test transcript files.

The tool reads two plain‑text files (or stdin if no arguments are given),
extracts all lines that start with ``PASS `` (case‑sensitive), and reports
which PASS lines were added, removed or kept, as well as the change‑count delta.

Usage examples::

    python3 run_log_diff.py file1.md file2.md
    python3 run_log_diff.py file1.md   # reads file2.md from stdin
    cat file1.md | python3 run_log_diff.py -  # both files via stdin

The output format is machine‑readable but human‑friendly and intended for
copy‑pasting into a README or log.
"""

import sys
from pathlib import Path


def read_passes(path):
    content = Path(path).read_text(encoding="utf-8") if path != "-" else sys.stdin.read()
    return {line for line in content.splitlines() if line.startswith("PASS ")}


def main(argv):
    if not argv:
        print("Usage: run_log_diff.py <first> [<second>]", file=sys.stderr)
        sys.exit(1)

    first = argv[0]
    second = argv[1] if len(argv) > 1 else "-"

    first_passes = read_passes(first)
    second_passes = read_passes(second)

    added = second_passes - first_passes
    removed = first_passes - second_passes
    kept = first_passes & second_passes

    print("Added:")
    for line in sorted(added):
        print(f"  {line}")
    print("\nRemoved:")
    for line in sorted(removed):
        print(f"  {line}")
    print("\nKept:")
    for line in sorted(kept):
        print(f"  {line}")
    print("\nChange‑count delta: {}".format(len(added) + len(removed)))

    sys.exit(0)


if __name__ == "__main__":
    main(sys.argv[1:])

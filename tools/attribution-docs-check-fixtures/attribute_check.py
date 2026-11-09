#!/usr/bin/env python3
"""Check a dataset card for required attribution lines.

This script reads an MDS dataset card (a plain‑text README.md file) in the
same directory as this script and verifies that the following three phrases are
present, case‑insensitively:

1. a line that starts with ``source``
2. a line that contains ``licence``
3. a line that contains ``retrieval``

If any are missing the script exits with status 1 and a descriptive message.
If all are present it prints ``OK: all attribution items present`` and exits
with status 0.
"""

import os
import re
import sys

REQUIRED = ["source", "licence", "retrieval"]


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def missing_tags(text):
    missing = [tag for tag in REQUIRED if not re.search(r"(?i)\b" + re.escape(tag), text)]
    return missing


def main():
    # Assume the README.md is in the same folder as this script
    base = os.path.abspath(os.path.dirname(__file__))
    card_path = os.path.join(base, "README.md")
    if not os.path.isfile(card_path):
        print(f"FAIL: README.md not found at {card_path}")
        sys.exit(1)
    text = read_file(card_path)
    missing = missing_tags(text)
    if missing:
        print("FAILED: missing attribution items: " + ", ".join(missing))
        sys.exit(1)
    print("OK: all attribution items present")
    sys.exit(0)


if __name__ == "__main__":
    main()

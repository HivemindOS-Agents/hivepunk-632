#!/usr/bin/env python3
"""Simple checker for attribution‑docs‑check‑fixtures.

This script is intentionally lightweight – it scans a dataset card (the readme
that lives in the folder containing the checker) for the three mandatory
attribution lines:

* a line that starts with ``source`` (case‑insensitive)
* a line that contains ``licence`` (case‑insensitive)
* a line that contains ``retrieval`` (case‑insensitive)

If any of those lines are missing, the script prints a ``FAILED`` message
listing the missing items and exits with code 1.  Otherwise it prints
``OK`` and exits with code 0.

The checker is intentionally simple because the tool’s self‑test already
verifies that the fixture files are copies of their source.  This script
provides a lightweight way for users to run the same check locally on
the published dataset card.

Usage
-----

```
# From the root of the dataset folder
python3 attribution_check.py
```
"""

import re
import sys

REQUIRED = ["source", "licence", "retrieval"]


def read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None


def check_attribution(text):
    missing = [tag for tag in REQUIRED if not re.search(r"(?i)\b" + tag, text)]
    return missing


def main():
    # Assume the dataset card is the README.md that lives alongside this script
    base = __file__
    card_path =
        os.path.abspath(os.path.join(os.path.dirname(base), "README.md"))
    card = read_file(card_path)
    if card is None:
        print(f"FAIL: README.md not found at {card_path}")
        sys.exit(1)

    missing = check_attribution(card)
    if missing:
        print("FAILED: missing attribution items: " + ", ".join(missing))
        sys.exit(1)
    else:
        print("OK: all attribution items present")
        sys.exit(0)


if __name__ == "__main__":
    main()

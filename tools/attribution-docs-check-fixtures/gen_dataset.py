#!/usr/bin/env python3
"""Generate the attribution-docs-check-fixtures dataset.

The script copies the six fixture files (three per folder) from a source
directory into the local ``fixtures/`` folder.  The source directory is
searched in this order:

1. ``--source <dir>`` passed on the command line
2. ``../attribution-docs-check/fixtures`` relative to this script
3. ``fixtures_source`` inside the tool directory

After copying the files the script rewrites ``README.md`` from the bundled
template and emits a ``LICENSE`` file with a CC‑0 dedication.

The script exits with 0 on success and prints a short status line.
"""

import argparse
import json
import os
import shutil
import sys

TEMPLATE_CARD = """# attribution‑docs‑check‑fixtures
\nBuilds and checks the attribution‑docs‑check-fixtures dataset folder: a dataset
card plus six fixture files copied byte‑for‑byte from the attribution‑docs‑check
tool's fixture tree.
\n## What it is
\nTwo small fixture folders, one clean and one deliberately broken, used as the
test inputs for the attribution‑docs‑check tool in HivemindOS-Agents/hivepunk-632.
\n## Columns
\nThese fixture folders contain a single data file each, `data.csv`.  The
first column is a placeholder step ID and the last column contains an HTTP
URL.
\n## What it was made
\nThe files are copied file‑by‑file from ``fixtures_source``; no content is
re‑typed or modified.  The fixtures were crafted by hand in the past but
subsequent runs regenerate them from the source.
\n---
license: cc0-1.0
language:
  - en
pretty_name: attribution-docs-check‑fixtures
"""

LICENSE_TEXT = """Creative Commons Zero v1.0 Universal\n\nTo the extent possible under law, the authors have waived all copyright and\nrelated or neighboring rights to this work. See https://creativecommons.org/publicdomain/zero/1.0/ for the full text.\n\nThis file is dedicated to the public domain under CC0 1.0."""

FIXTURES = [
    ("passing_card", "README.md"),
    ("passing_card", "data.csv"),
    ("passing_card", "expected_problems.txt"),
    ("failing_card", "README.md"),
    ("failing_card", "data.csv"),
    ("failing_card", "expected_problems.txt"),
]


def resolve_source(dry_run=False):
    candidates = []
    # 1. explicit argument
    if args.source:
        candidates.append(os.path.abspath(args.source))
    # 2. relative to this script
    candidates.append(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "attribution-docs-check", "fixtures")))
    # 3. local copy
    candidates.append(os.path.join(os.path.dirname(__file__), "fixtures_source"))
    for cand in candidates:
        if all(os.path.isfile(os.path.join(cand, card, name)) for card, name in FIXTURES):
            if dry_run:
                print(cand)
            return cand
    return None


def copy_fixture(src, dst):
    shutil.copyfile(src, dst)


def main():
    global args
    parser = argparse.ArgumentParser(description="Generate dataset fixtures")
    parser.add_argument("--source", help="directory containing the fixture source files")
    args = parser.parse_args()

    src_dir = resolve_source()
    if not src_dir:
        print("FAIL: could not find a source directory containing all fixtures")
        sys.exit(1)

    dst_base = os.path.join(os.path.dirname(__file__), "fixtures")
    os.makedirs(dst_base, exist_ok=True)
    for card, name in FIXTURES:
        src_path = os.path.join(src_dir, card, name)
        dst_path = os.path.join(dst_base, card, name)
        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        copy_fixture(src_path, dst_path)
    # write README.md
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(TEMPLATE_CARD)
    # write LICENSE
    license_path = os.path.join(os.path.dirname(__file__), "LICENSE")
    with open(license_path, "w", encoding="utf-8") as f:
        f.write(LICENSE_TEXT)
    print("PASS: dataset generated successfully")
    sys.exit(0)


if __name__ == "__main__":
    main()

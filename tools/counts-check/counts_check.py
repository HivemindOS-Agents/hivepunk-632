#!/usr/bin/env python3
"""Counts Check: Verify that the counts stated in a dataset card README match the actual data in a JSONL file.

Usage:
    python3 counts_check.py <path_to_readme> <path_to_jsonl>

The README must contain three lines starting with
  rows: N
  source fields: N
  distinct source pages: N
The script reads these values, then scans the JSONL file counting:
  • total number of JSON objects (rows)
  • number of rows with a non‑empty `source` field
  • distinct source URLs across all rows
If all three numbers match, the script prints a PASS message and exits 0.
Otherwise it prints a FAIL message and exits with status 1.

The tool is self‑contained, uses only the Python standard library, and performs no network I/O.
"""

import json
import sys
import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def parse_card_counts(readme_path: Path) -> dict:
    """Extract the numeric counts from the README.
    Returns dict with keys 'rows', 'source_fields', 'distinct_source_pages'.
    Missing or malformed lines yield None values.
    """
    counts = {
        'rows': None,
        'source_fields': None,
        'distinct_source_pages': None,
    }
    patterns = {
        'rows': re.compile(r'^\s*rows:\s*(\d+)\s*$', re.I),
        'source_fields': re.compile(r'^\s*source\s+fields:\s*(\d+)\s*$', re.I),
        'distinct_source_pages': re.compile(r'^\s*distinct\s+source\s+pages:\s*(\d+)\s*$', re.I),
    }

    try:
        text = readme_path.read_text(encoding='utf-8')
    except OSError as exc:
        print(f"FAIL could not read README: {exc}")
        sys.exit(1)

    for line in text.splitlines():
        for key, pat in patterns.items():
            m = pat.match(line)
            if m:
                counts[key] = int(m.group(1))
    return counts


def analyze_jsonl(jsonl_path: Path) -> dict:
    """Count rows, source fields, and distinct source URLs in the JSONL file."""
    rows = 0
    source_fields = 0
    distinct_sources = set()

    try:
        with jsonl_path.open('r', encoding='utf-8') as fh:
            for raw in fh:
                line = raw.strip()
                if not line:
                    continue
                rows += 1
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    # Treat malformed line as a row with no source
                    continue
                src = obj.get('source', None)
                if isinstance(src, str) and src.strip():
                    source_fields += 1
                    distinct_sources.add(src.strip())
    except OSError as exc:
        print(f"FAIL could not read JSONL: {exc}")
        sys.exit(1)

    return {
        'rows': rows,
        'source_fields': source_fields,
        'distinct_source_pages': len(distinct_sources),
    }


def main():
    if len(sys.argv) != 3:
        print('Usage: python3 counts_check.py <README.md> <data.jsonl>')
        sys.exit(2)

    readme_path = Path(sys.argv[1])
    jsonl_path = Path(sys.argv[2])

    card_counts = parse_card_counts(readme_path)
    file_counts = analyze_jsonl(jsonl_path)

    # Construct human‑readable parts
    card_part = f"{card_counts['rows']}/{card_counts['source_fields']}/{card_counts['distinct_source_pages']}"
    file_part = f"{file_counts['rows']}/{file_counts['source_fields']}/{file_counts['distinct_source_pages']}"

    # Determine pass/fail
    passed = all(
        card_counts[k] == file_counts[key] if card_counts[k] is not None else False
        for k, key in [('rows', 'rows'), ('source_fields', 'source_fields'), ('distinct_source_pages', 'distinct_source_pages')]
    )

    status = 'PASS' if passed else 'FAIL'
    print(f"counts_check: card {card_part} vs file {file_part} — {status}")
    sys.exit(0 if passed else 1)


if __name__ == "__main__":
    main()

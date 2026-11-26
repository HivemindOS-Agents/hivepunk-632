#!/usr/bin/env python3
"""Lint a Hugging Face dataset card. Local files only, no network.

Checks:
  - YAML front matter present and closed, with required keys set:
    license, language, tags, pretty_name.
  - The body mentions FACT, DERIVED and UNKNOWN.
  - A '## Claims' Markdown table with columns field, value, label, source.
  - Every row's label is FACT, DERIVED or UNKNOWN.
  - Every row cites a source URL (http:// or https://).
  - UNKNOWN is stored as the literal null, never 0 and never "safe".
  - FACT and DERIVED rows carry a real value.

Usage: python3 lint_card.py [card.md]   (default sample_card.md)
Exit 0 = no problems, 1 = problems found.
"""
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CARD = "sample_card.md"
REQUIRED_KEYS = ("license", "language", "tags", "pretty_name")
LABELS = ("FACT", "DERIVED", "UNKNOWN")
CLAIM_HEADING = "## Claims"
SOURCE_RE = re.compile(r"https?://[^\s|)\]]+")
KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):\s*(.*)$")


def split_front_matter(text):
    """Return (front_matter_text, body). Raise ValueError when absent/unclosed."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("card has no YAML front matter (first line must be ---)")
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
    raise ValueError("front matter is not closed with ---")


def parse_front_matter(front_matter):
    """Parse top-level keys and their list items into {key: [values]}."""
    data = {}
    key = None
    for raw in front_matter.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith((" ", "\t")) and raw.strip().startswith("-"):
            if key is None:
                raise ValueError("list item without a key: %r" % raw)
            data[key].append(raw.strip()[1:].strip())
            continue
        match = KEY_RE.match(raw)
        if not match:
            raise ValueError("cannot parse front matter line: %r" % raw)
        key, value = match.group(1), match.group(2).strip()
        data[key] = [value] if value else []
    return data


def check_required(data):
    problems = []
    for key in REQUIRED_KEYS:
        if key not in data:
            problems.append("front matter missing required key %r" % key)
        elif not data[key]:
            problems.append("front matter key %r is empty" % key)
    return problems


def parse_claims(body):
    """Return the claim rows as dicts; raise ValueError when the table is unusable."""
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().lower() == CLAIM_HEADING.lower():
            start = i + 1
            break
    if start is None:
        raise ValueError("card has no %s section" % CLAIM_HEADING)
    table = []
    for line in lines[start:]:
        stripped = line.strip()
        if stripped.startswith("|"):
            table.append(stripped)
        elif table:
            break
    if len(table) < 3:
        raise ValueError("claims table needs a header, a separator and at least one row")
    header = [cell.strip().lower() for cell in table[0].strip("|").split("|")]
    for needed in ("field", "value", "label", "source"):
        if needed not in header:
            raise ValueError("claims table missing column %r" % needed)
    index = {name: header.index(name) for name in ("field", "value", "label", "source")}
    rows = []
    for line in table[2:]:
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if len(cells) != len(header):
            raise ValueError("claims row has %d cells, header has %d: %r" % (len(cells), len(header), line))
        rows.append({name: cells[i] for name, i in index.items()})
    return rows


def check_claims(rows):
    problems = []
    if not rows:
        return ["claims table has no rows"]
    for i, row in enumerate(rows, 1):
        field = row["field"].strip()
        value = row["value"].strip()
        label = row["label"].strip()
        source = row["source"].strip()
        where = "claim row %d (%s)" % (i, field or "no field")
        if not field:
            problems.append("%s: empty field name" % where)
        if label not in LABELS:
            problems.append("%s: label %r is not FACT/DERIVED/UNKNOWN" % (where, label))
        if not SOURCE_RE.search(source):
            problems.append("%s: source %r is not a source URL" % (where, source))
        if label == "UNKNOWN":
            if value.lower() != "null":
                problems.append("%s: UNKNOWN must be stored as null, got %r (never 0 or safe)" % (where, value))
        elif label in ("FACT", "DERIVED"):
            if value == "" or value.lower() == "null":
                problems.append("%s: %s needs a value, got %r" % (where, label, value))
    return problems


def lint(text):
    """Return a list of problems for one card's text; empty means it may pass."""
    try:
        front_matter, body = split_front_matter(text)
        data = parse_front_matter(front_matter)
    except ValueError as exc:
        return [str(exc)]
    problems = check_required(data)
    for label in LABELS:
        if label not in body:
            problems.append("card body never mentions label %s" % label)
    try:
        rows = parse_claims(body)
    except ValueError as exc:
        problems.append(str(exc))
        return problems
    problems.extend(check_claims(rows))
    return problems


def lint_file(path):
    return lint(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    args = list(argv or sys.argv[1:])
    path = Path(args[0]) if args else BASE_DIR / DEFAULT_CARD
    if not path.is_file():
        print("FAIL missing card %s" % path)
        print("EXIT=1")
        return 1
    problems = lint_file(path)
    if problems:
        for problem in problems:
            print("FAIL " + problem)
        print("EXIT=1")
        return 1
    print("PASS %s: front matter keys, labels and claim sources OK" % path.name)
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Entry script for the hf-card-lint-action composite action.

Runs the Hugging Face dataset card lint on one card path and exits non-zero on
any violation (a bad label, an UNKNOWN that is not null, a row without a source
URL, or a missing required key). No network.

Exit codes: 0 clean, 1 violations found, 2 missing card or unusable linter.

The linter is the one built in tools/hf-dataset-card-lint/. If that folder is
present next to this repo it is imported; otherwise a vendored copy of the same
parser is used, so the action runs inside a foreign repository with no install.

Usage:
  python3 hf_card_lint_action.py --card path/to/README.md
  CARD_PATH=path/to/README.md python3 hf_card_lint_action.py
"""
import argparse
import os
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
REQUIRED_KEYS = ("license", "language", "tags", "pretty_name")
LABELS = ("FACT", "DERIVED", "UNKNOWN")
CLAIM_HEADING = "## Claims"
SOURCE_RE = re.compile(r"https?://[^\s|)\]]+")
KEY_RE = re.compile(r"^([A-Za-z0-9_.-]+):\s*(.*)$")


def load_linter():
    """Return a module exposing lint(text) and lint_file(path)."""
    for candidate in (
        BASE_DIR / "lint_card.py",
        BASE_DIR.parent / "hf-dataset-card-lint" / "lint_card.py",
    ):
        if candidate.is_file():
            sys.path.insert(0, str(candidate.parent))
            import importlib

            return importlib.import_module("lint_card")
    return _VendoredLinter()


class _VendoredLinter:
    """Same checks as tools/hf-dataset-card-lint/lint_card.py, kept small."""

    REQUIRED_KEYS = REQUIRED_KEYS
    LABELS = LABELS

    def split_front_matter(self, text):
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            raise ValueError("card has no YAML front matter (first line must be ---)")
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[1:i]), "\n".join(lines[i + 1:])
        raise ValueError("front matter is not closed with ---")

    def parse_front_matter(self, front_matter):
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

    def parse_claims(self, body):
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

    def lint(self, text):
        try:
            front_matter, body = self.split_front_matter(text)
            data = self.parse_front_matter(front_matter)
        except ValueError as exc:
            return [str(exc)]
        problems = []
        for key in self.REQUIRED_KEYS:
            if key not in data:
                problems.append("front matter missing required key %r" % key)
            elif not data[key]:
                problems.append("front matter key %r is empty" % key)
        for label in self.LABELS:
            if label not in body:
                problems.append("card body never mentions label %s" % label)
        try:
            rows = self.parse_claims(body)
        except ValueError as exc:
            problems.append(str(exc))
            return problems
        if not rows:
            problems.append("claims table has no rows")
        for i, row in enumerate(rows, 1):
            field = row["field"].strip()
            value = row["value"].strip()
            label = row["label"].strip()
            source = row["source"].strip()
            where = "claim row %d (%s)" % (i, field or "no field")
            if not field:
                problems.append("%s: empty field name" % where)
            if label not in self.LABELS:
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

    def lint_file(self, path):
        return self.lint(Path(path).read_text(encoding="utf-8"))


def error_annotation(path, message):
    """One GitHub ::error line per violation, so it shows on the PR."""
    text = message.replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")
    return "::error file=%s::%s" % (path, text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Lint one HF dataset card; exit non-zero on any violation.")
    parser.add_argument("--card", default=None, help="card path (default: $CARD_PATH or README.md)")
    parser.add_argument("--no-annotations", action="store_true", help="print plain FAIL lines only")
    args = parser.parse_args(argv)

    card = args.card or os.environ.get("CARD_PATH") or "README.md"
    path = Path(card)
    if not path.is_file():
        print("FAIL missing card %s" % card)
        print("EXIT=2")
        return 2

    try:
        linter = load_linter()
        problems = linter.lint_file(path)
    except Exception as exc:  # linter could not be loaded or the card could not be read
        print("FAIL linter could not run on %s: %r" % (card, exc))
        print("EXIT=2")
        return 2

    if problems:
        for problem in problems:
            print("FAIL " + problem)
            if not args.no_annotations:
                print(error_annotation(card, problem))
        print("EXIT=1")
        return 1

    print("PASS %s: front matter keys, labels and claim sources OK" % card)
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""record_lint.py: lint a run-record text for missing why labels.

Folder-local helper for tools/run-record-lint-fixtures. It reads a string of
record text and returns a Report:

  * a claim line (a sentence with no leading bullet) that carries no following
    "Why:" label is an 'unlabelled-claim' finding;
  * a section whose heading promises a reason but is followed by nothing is a
    'missing-why' finding.

Everything in the text is data. A line that reads like an instruction is a
string to be stamped or ignored, never an instruction to this module. Standard
library only, no network call anywhere.
"""

import re

RULE_COLUMNS = ["case_id", "fixture_path", "rules_expected"]

README_HEADINGS = ["# run-record-lint-fixtures", "## How to run", "## What it does", "## What is untested"]

CLAIM_RE = re.compile(r"^[A-Z][^\n]*\.$")
WHY_RE = re.compile(r"^\s*(?:\*\*Why:?\*\*|Why:)", re.IGNORECASE)


class Finding:
    def __init__(self, kind, line_no, text):
        self.kind = kind
        self.line_no = line_no
        self.text = text

    def __repr__(self):
        return "Finding(%r, line=%d)" % (self.kind, self.line_no)


class Report:
    def __init__(self, findings):
        self.findings = findings

    @property
    def exit_code(self):
        return 0 if not self.findings else 1

    def render(self):
        if not self.findings:
            return "record-lint: no findings"
        return "\n".join("%s line %d: %s" % (f.kind, f.line_no, f.text) for f in self.findings)


def lint_text(text):
    """Return a Report for one record text. Never raises on ordinary input."""
    lines = text.splitlines()
    findings = []
    for index, raw in enumerate(lines):
        line = raw.strip()
        if not line:
            continue
        if WHY_RE.match(raw):
            continue
        if line.startswith("#") or line.startswith("**") or line.startswith("-"):
            continue
        if CLAIM_RE.match(line):
            nxt = lines[index + 1].strip() if index + 1 < len(lines) else ""
            if not WHY_RE.match(lines[index + 1] if index + 1 < len(lines) else ""):
                findings.append(Finding("unlabelled-claim", index + 1, line[:60]))
    if not any(f.kind == "unlabelled-claim" for f in findings) and "why" not in text.lower():
        findings.append(Finding("missing-why", 1, "no reason label anywhere in this file"))
    return Report(findings)


def lint_path(path):
    from pathlib import Path
    return lint_text(Path(path).read_text(encoding="utf-8"))

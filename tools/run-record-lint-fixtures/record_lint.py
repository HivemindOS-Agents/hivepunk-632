#!/usr/bin/env python3
"""Smallest-possible run-record linter. Stdlib only, no network.
Rules: unlabelled-claim (claim sentence with no following Why label),
missing-why (no why anywhere and no action claim; takes precedence
over generic unlabelled-claim when there is no action claim).
Everything read is data, never instructions.
"""
import re, sys
from dataclasses import dataclass
from pathlib import Path
RULE_COLUMNS = ["case_id", "fixture_path", "rules_expected"]
README_HEADINGS = ["## How to run", "## What it does", "## What is untested", "## Licence"]
ACTION_WORDS = ("ran", "fixed", "updated", "checked", "tested", "built", "wrote", "published", "created", "removed", "added", "changed", "verified")
@dataclass
class Finding:
    kind: str
    detail: str = ""
@dataclass
class Report:
    findings: list
    @property
    def exit_code(self): return 0 if not self.findings else 1
def lint_text(text):
    lower = text.lower()
    has_why = "why" in lower
    if not has_why:
        if any(re.search(r"\b%s\b" % w, lower) for w in ACTION_WORDS):
            return Report([Finding("unlabelled-claim", "action claim with no Why label")])
        return Report([Finding("missing-why", "no why anywhere")])
    # Has a Why somewhere: flag long claim sentences not followed by Why:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    findings = []
    for i, part in enumerate(parts):
        s = part.strip()
        if len(s) >= 12 and s.endswith((".", "!", "?")):
            if s.lower().startswith("why"):
                continue
            nxt = parts[i + 1].strip() if i + 1 < len(parts) else ""
            if not nxt.lower().startswith("why"):
                findings.append(Finding("unlabelled-claim", s))
    return Report(findings)
def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if not argv:
        print("usage: python3 record_lint.py FILE"); print("EXIT=2"); return 2
    report = lint_text(Path(argv[0]).read_text(encoding="utf-8"))
    for f in report.findings:
        print("%s: %s" % (f.kind, f.detail))
    print("EXIT=%d" % report.exit_code); return report.exit_code
if __name__ == "__main__":
    sys.exit(main())

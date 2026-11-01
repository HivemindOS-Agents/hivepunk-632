#!/usr/bin/env python3
"""claim_ledger_checker - Verify a claims CSV against a Markdown report.

The tool expects two data files in the same directory:

* claims.csv  – a CSV with columns:
    id,claim,source_url,checked_date,status
* report.md   – a Markdown file that may contain the exact claim text.

Checks performed:
1. The exact text of each claim appears in the Markdown file.
2. source_url is present and is a well‑formed http(s) URL.
3. checked_date is present (any non‑empty string is accepted – parsing YYYY-MM‑DD
   or ISO 8601 is left for future work).

The script prints one line per claim, e.g.:
    PASS 123: claim text found, source URL ok, checked date present
or
    FAIL 124: claim text missing

Exit status:
    0 – all claims pass
    1 – at least one claim fails

No network access or external libraries beyond the Python standard library are used.

The repository contains two built‑in fixtures: clean.csv (all passes) and
dirty.csv (at least two failures).  They can be used for quick manual tests.
"""

import csv
import re
import sys
from pathlib import Path

URL_RE = re.compile(r"^https?://\S+$")

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def read_claims(path: Path):
    """Return list of dicts for each row in a CSV with the required header."""
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        # validate header
        expected = {"id", "claim", "source_url", "checked_date", "status"}
        if set(reader.fieldnames) != expected:
            raise ValueError(f"claims CSV header must be {sorted(expected)}")
        return list(reader)


def load_report(path: Path) -> str:
    """Return the raw Markdown text.

    The tool treats the whole file as text – it does not attempt markdown
    parsing.  This keeps the implementation simple yet sufficient for the
    verbatim check.
    """
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# Main checker
# ---------------------------------------------------------------------------

def main(claims_file: str | Path = "claims.csv", report_file: str | Path = "report.md"):
    claims_path = Path(claims_file)
    report_path = Path(report_file)

    # 1. Load data
    try:
        claims = read_claims(claims_path)
    except Exception as exc:
        print(f"FAIL: unable to read claims CSV: {exc}")
        return 1
    if not contest_report.exists():
        print(f"FAIL: report file {report_path} does not exist")
        return 1
    report_text = load_report(report_path)

    failures = 0

    for row in claims:
        claim_id = row["id"].strip()
        claim_text = row["claim"].strip()
        source = row["source_url"].strip()
        date = row["checked_date"].strip()
        status = row["status"].strip().lower()

        parts = []
        # 2. Claim text appears verbatim in report
        if claim_text in report_text:
            parts.append("text present")
        else:
            parts.append("text missing")
            failures += 1
        # 3. source_url is a non‑empty http/https
        if source and URL_RE.match(source):
            parts.append("source URL ok")
        else:
            parts.append("source URL missing/invalid")
            failures += 1
        # 4. checked_date non‑empty
        if date:
            parts.append("checked date ok")
        else:
            parts.append("checked date missing")
            failures += 1
        print(f"{['FAIL' if part.startswith('text missing') or part.startswith('source URL missing') or part.startswith('checked date missing') else 'PASS'][-1]} {claim_id}: {', '.join(parts)}")

    print(f"self_test: {len(claims) - failures}/{len(claims)}, {failures} problems")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

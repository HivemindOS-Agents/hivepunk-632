#!/usr/bin/env python3
"""Folder-local self-test for hf-dataset-card-lint.

Run from this folder with no arguments and no network:
  python3 self_test.py; echo EXIT=$?

It imports lint_card, lints the committed sample_card.md and 12 deliberately
broken variants of it, and exits 0 only when every check passes. It writes no
run log; HivemindOS writes each run into SELFTEST_OUTPUT.md.
"""
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import lint_card

SAMPLE = (BASE / "sample_card.md").read_text(encoding="utf-8")
PASSED = []
FAILED = []


def check(name, fn):
    try:
        fn()
        PASSED.append(name)
    except Exception as exc:
        FAILED.append("%s (%r)" % (name, exc))


def expect(condition, message):
    if not condition:
        raise AssertionError(message)


def rejects(name, text):
    def run():
        problems = lint_card.lint(text)
        expect(problems, "linter accepted a broken card: %s" % name)
    return run


def main():
    def sample_clean():
        problems = lint_card.lint(SAMPLE)
        expect(problems == [], problems)

    def sample_file_clean():
        problems = lint_card.lint_file(BASE / "sample_card.md")
        expect(problems == [], problems)

    def front_matter_parsed():
        front_matter, body = lint_card.split_front_matter(SAMPLE)
        data = lint_card.parse_front_matter(front_matter)
        expect(data["license"] == ["cc0-1.0"], data.get("license"))
        expect("en" in data["language"], data.get("language"))
        expect(len(data["tags"]) >= 2, data.get("tags"))
        expect(data["pretty_name"], data.get("pretty_name"))
        expect("## Claims" in body, "claims heading missing from body")

    def claims_parsed():
        _, body = lint_card.split_front_matter(SAMPLE)
        rows = lint_card.parse_claims(body)
        expect(len(rows) == 3, len(rows))
        expect({row["label"] for row in rows} == {"FACT", "DERIVED", "UNKNOWN"}, rows)
        for row in rows:
            expect(lint_card.SOURCE_RE.search(row["source"]), row)

    def unknown_rows_are_null():
        _, body = lint_card.split_front_matter(SAMPLE)
        for row in lint_card.parse_claims(body):
            if row["label"] == "UNKNOWN":
                expect(row["value"].strip().lower() == "null", row)

    def no_claim_rows():
        text = SAMPLE.replace("| tag | v4.0.0 | FACT |", "| tag | v4.0.0 |").replace(
            "| tvl_usd | null | UNKNOWN |", "| tvl_usd | null |").replace(
            "| days_since | 650 | DERIVED |", "| days_since | 650 |")
        expect(lint_card.lint(text), "accepted a claims table with no parseable rows")

    tests = (
        ("sample_card.md lints clean", sample_clean),
        ("lint_file on sample_card.md is clean", sample_file_clean),
        ("front matter parses to the expected keys", front_matter_parsed),
        ("three claim rows with all three labels and source URLs", claims_parsed),
        ("UNKNOWN rows are stored as null", unknown_rows_are_null),
        ("no front matter rejected", rejects("no front matter", "license: cc0-1.0\n")),
        ("unclosed front matter rejected", rejects("unclosed", "---\nlicense: cc0-1.0\n")),
        ("missing required key rejected", rejects("missing license", SAMPLE.replace("license: cc0-1.0\n", "", 1))),
        ("empty required key rejected", rejects("empty pretty_name", SAMPLE.replace("pretty_name: Sample labelled dataset card", "pretty_name:", 1))),
        ("MAYBE label rejected", rejects("MAYBE", SAMPLE.replace("| FACT |", "| MAYBE |", 1))),
        ("lower-case derived rejected", rejects("derived", SAMPLE.replace("| DERIVED |", "| derived |", 1))),
        ("UNKNOWN as 0 rejected", rejects("UNKNOWN 0", SAMPLE.replace("| null | UNKNOWN |", "| 0 | UNKNOWN |", 1))),
        ("UNKNOWN as safe rejected", rejects("UNKNOWN safe", SAMPLE.replace("| null | UNKNOWN |", "| safe | UNKNOWN |", 1))),
        ("UNKNOWN empty rejected", rejects("UNKNOWN empty", SAMPLE.replace("| null | UNKNOWN |", "|  | UNKNOWN |", 1))),
        ("row without a source URL rejected", rejects("no source", SAMPLE.replace("| null | UNKNOWN | https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 |", "| null | UNKNOWN | internal notes |", 1))),
        ("FACT with null value rejected", rejects("FACT null", SAMPLE.replace("| v4.0.0 | FACT |", "| null | FACT |", 1))),
        ("missing source column rejected", rejects("no source column", SAMPLE.replace("| field | value | label | source |", "| field | value | label | note |", 1))),
        ("missing claims section rejected", rejects("no claims", SAMPLE.replace("## Claims", "## Rows", 1))),
        ("no claim rows rejected", no_claim_rows),
    )
    for name, fn in tests:
        check(name, fn)

    for name in PASSED:
        print("PASS " + name)
    for name in FAILED:
        print("FAIL " + name)
    print("self_test: %d check(s), %d failed" % (len(PASSED) + len(FAILED), len(FAILED)))
    print("EXIT=%d" % (0 if not FAILED else 1))
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())

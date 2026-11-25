#!/usr/bin/env python3
"""Folder-local self-test for uniswap-v4-core-release-watch.

Run from this folder with no arguments, no network:
  python3 self_test.py; echo EXIT=$?

It imports the tool's own modules (publish_model, verify) and runs them on the
committed files and on deliberately broken samples. Exit 0 only when every
check passes. It writes no run log; HivemindOS writes SELFTEST_OUTPUT.md.
"""
import json
import shutil
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE))

import publish_model as pm
import verify

PASSED = []
FAILED = []


def check(name, fn):
    try:
        fn()
        PASSED.append(name)
    except Exception as exc:
        FAILED.append("%s (%r)" % (name, exc))


def expect(cond, msg):
    if not cond:
        raise AssertionError(msg)


def good_row():
    return {
        "row_id": "sample-ok",
        "source_endpoint": pm.ENDPOINT,
        "source_repo": pm.SOURCE_REPO,
        "licence": "CC0-1.0",
        "as_of": "2026-11-22",
        "tag": "v4.0.0",
        "name": "v4.0.0",
        "published_at": "2026-11-01T00:00:00Z",
        "days_since": 21,
        "html_url": "https://example.invalid/release",
        "prerelease_or_draft_newer": None,
        "newer_tag_without_release": None,
        "later_deletion_or_yank": None,
        "maintenance_verdict": None,
        "labels": {
            "tag": "FACT",
            "name": "FACT",
            "published_at": "FACT",
            "days_since": "DERIVED",
            "html_url": "FACT",
            "prerelease_or_draft_newer": "UNKNOWN",
            "newer_tag_without_release": "UNKNOWN",
            "later_deletion_or_yank": "UNKNOWN",
            "maintenance_verdict": "UNKNOWN",
        },
    }


def broken(mutate):
    row = good_row()
    mutate(row)
    return row


def main():
    def good_row_accepted():
        expect(pm.check_row(good_row()) == [], pm.check_row(good_row()))
        expect(verify.check_row(good_row()) == [], verify.check_row(good_row()))

    def bad_label():
        row = broken(lambda r: r["labels"].__setitem__("tag", "MAYBE"))
        expect(pm.check_row(row), "pm accepted MAYBE")
        expect(verify.check_row(row), "verify accepted MAYBE")

    def lower_case_label():
        row = broken(lambda r: r["labels"].__setitem__("name", "fact"))
        expect(pm.check_row(row), "pm accepted 'fact'")
        expect(verify.check_row(row), "verify accepted 'fact'")

    def unknown_zero():
        row = broken(lambda r: r.__setitem__("prerelease_or_draft_newer", 0))
        expect(pm.check_row(row), "pm accepted UNKNOWN as 0")
        expect(verify.check_row(row), "verify accepted UNKNOWN as 0")

    def unknown_safe():
        row = broken(lambda r: r.__setitem__("later_deletion_or_yank", "safe"))
        expect(pm.check_row(row), "pm accepted UNKNOWN as 'safe'")
        expect(verify.check_row(row), "verify accepted UNKNOWN as 'safe'")

    def derived_on_raw():
        row = broken(lambda r: r["labels"].__setitem__("published_at", "DERIVED"))
        expect(pm.check_row(row), "pm accepted DERIVED on raw field")
        expect(verify.check_row(row), "verify accepted DERIVED on raw field")

    def always_unknown_flipped():
        row = broken(lambda r: r["labels"].__setitem__("maintenance_verdict", "FACT"))
        expect(pm.check_row(row), "pm accepted flipped always-UNKNOWN")
        expect(verify.check_row(row), "verify accepted flipped always-UNKNOWN")

    def missing_label():
        row = broken(lambda r: r["labels"].pop("tag"))
        expect(pm.check_row(row), "pm accepted a missing label")
        expect(verify.check_row(row), "verify accepted a missing label")

    def days_since_string():
        row = broken(lambda r: r.__setitem__("days_since", "21"))
        expect(pm.check_row(row), "pm accepted a string days_since")
        expect(verify.check_row(row), "verify accepted a string days_since")

    def wrong_endpoint():
        row = broken(lambda r: r.__setitem__("source_endpoint", "https://example.invalid"))
        expect(pm.check_row(row), "pm accepted a wrong endpoint")
        expect(verify.check_row(row), "verify accepted a wrong endpoint")

    def normalize_missing_is_null():
        row = {"row_id": "sample-missing", "labels": {"tag": "FACT"}, "tag": "v4.0.0"}
        out = pm.normalize_row(row)
        for field in pm.PUBLISH_FIELDS:
            if field != "tag":
                expect(out[field] is None, "normalize gave %s a value" % field)
                expect(out["labels"][field] == "UNKNOWN", "normalize label %s" % field)
        expect(pm.check_row(out) == [], pm.check_row(out))

    def committed_rows_ok():
        rows = [pm.normalize_row(r) for r in pm.load_rows(BASE / "dataset_rows.jsonl")]
        expect(len(rows) >= 1, "no committed rows")
        for row in rows:
            expect(pm.check_row(row) == [], pm.check_row(row))
            expect(verify.check_row(row) == [], verify.check_row(row))
            for field, label in row["labels"].items():
                expect(label in pm.ALLOWED, "committed label %s=%r" % (field, label))
                if label == "UNKNOWN":
                    expect(row[field] is None, "committed UNKNOWN %s not null" % field)

    def committed_card_ok():
        text = (BASE / "dataset_card.md").read_text(encoding="utf-8")
        expect(pm.check_card(text) == [], pm.check_card(text))

    def cards_rejected():
        expect(pm.check_card(""), "accepted empty card")
        good = (BASE / "dataset_card.md").read_text(encoding="utf-8")
        expect(pm.check_card(good.replace(pm.SOURCE_REPO, "x")), "accepted card missing source repo")
        expect(pm.check_card(good.replace("python3 verify.py", "x")), "accepted card missing verify command")
        expect(pm.check_card(good + "\nPublish date: 2026-11-25\n"), "accepted card claiming a publish date")

    def manifest_ok():
        m = pm.build_manifest(BASE)
        expect(m["readme_target"] == "README.md", "readme target")
        expect(m["data_target"] == "data/dataset_rows.jsonl", "data target")
        expect(m["target"] == pm.TARGET, "target url")
        expect(m["account"] == pm.ACCOUNT, "account")
        expect(m["live_values_claimed"] is False, "claims live values")
        expect(m["live_url"] is None and m["publish_date"] is None, "claims url/date")
        expect(m["row_count"] >= 1, "row count")
        expect(m["readme_sha256"] == pm.sha256_bytes((BASE / "dataset_card.md").read_bytes()), "readme hash")
        expect(m["data_sha256"] == pm.sha256_bytes((BASE / "dataset_rows.jsonl").read_bytes()), "data hash")

    def manifest_raises_on_bad_row():
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            shutil.copy(BASE / "dataset_card.md", tmp / "dataset_card.md")
            row = json.loads((BASE / "dataset_rows.jsonl").read_text(encoding="utf-8").splitlines()[0])
            row["labels"]["tag"] = "MAYBE"
            (tmp / "dataset_rows.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")
            try:
                pm.build_manifest(tmp)
            except ValueError:
                return
            raise AssertionError("build_manifest accepted a MAYBE row")

    def package_ok_and_missing():
        expect(pm.check_package(BASE) == [], pm.check_package(BASE))
        with tempfile.TemporaryDirectory() as tmp:
            expect(pm.check_package(tmp), "accepted a missing package")

    def days_between_ok():
        expect(verify.days_between("2026-11-01T00:00:00Z", "2026-11-22") == 21, "days")
        expect(verify.days_between(None, "2026-11-22") is None, "missing")
        expect(verify.days_between("not-a-date", "2026-11-22") is None, "malformed")

    for name, fn in (
        ("good sample row accepted by both modules", good_row_accepted),
        ("MAYBE label rejected", bad_label),
        ("lower-case 'fact' rejected", lower_case_label),
        ("UNKNOWN as 0 rejected", unknown_zero),
        ("UNKNOWN as 'safe' rejected", unknown_safe),
        ("DERIVED on raw field rejected", derived_on_raw),
        ("always-UNKNOWN flipped to FACT rejected", always_unknown_flipped),
        ("missing label rejected", missing_label),
        ("string days_since rejected", days_since_string),
        ("wrong source endpoint rejected", wrong_endpoint),
        ("normalize turns missing fields into null/UNKNOWN", normalize_missing_is_null),
        ("committed rows keep labels with UNKNOWN null", committed_rows_ok),
        ("committed card passes", committed_card_ok),
        ("broken cards rejected", cards_rejected),
        ("manifest maps verbatim with matching hashes", manifest_ok),
        ("manifest raises on a broken row", manifest_raises_on_bad_row),
        ("package ok, missing package reported", package_ok_and_missing),
        ("days_between computed or None", days_between_ok),
    ):
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

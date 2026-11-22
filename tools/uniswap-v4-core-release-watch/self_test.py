#!/usr/bin/env python3
"""Folder-local self-test for uniswap-v4-core-release-watch.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Imports verify.py by path, runs its real label check on the committed
release_watch.jsonl, and checks that check_row() accepts a filled FACT row and
rejects broken ones.
"""
import importlib.util
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPECTED_TAG = None  # committed row is not fetched; values stay null/UNKNOWN


def load_verify():
    spec = importlib.util.spec_from_file_location("verify", BASE_DIR / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def filled_row():
    return {
        "dataset": "uniswap-v4-core-release-watch",
        "row_id": "uniswap-v4-core-latest-release",
        "source_endpoint": "https://api.github.com/repos/Uniswap/v4-core/releases/latest",
        "as_of": "2026-11-22",
        "tag": "v1.0.0",
        "name": "v1.0.0",
        "published_at": "2026-11-18T00:00:00Z",
        "days_since": 4,
        "html_url": "https://github.com/Uniswap/v4-core/releases/tag/v1.0.0",
        "labels": {
            "tag": "FACT", "name": "FACT", "published_at": "FACT",
            "days_since": "FACT", "html_url": "FACT",
            "prerelease_or_draft_newer": "UNKNOWN",
            "newer_tag_without_release": "UNKNOWN",
            "later_deletion_or_yank": "UNKNOWN",
            "maintenance_verdict": "UNKNOWN",
        },
    }


def main():
    print("uniswap-v4-core-release-watch self-test - folder-local, no network")
    checks = failed = 0

    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1

    def read(name):
        p = BASE_DIR / name
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    try:
        mod = load_verify()
        check(True, "verify.py imports cleanly")
    except Exception as exc:
        check(False, "verify.py imports cleanly", repr(exc))
        print("self_test: %d check(s), %d failed" % (checks, failed))
        print("EXIT=1")
        return 1

    check(mod.days_between("2026-11-18T00:00:00Z", "2026-11-22") == 4, "days_between computes 4")
    check(mod.days_between(None, "2026-11-22") is None, "days_between None -> None")
    check(mod.days_between("garbage", "2026-11-22") is None, "days_between garbage -> None")

    ok_row = filled_row()
    check(mod.check_row(ok_row) == [], "check_row accepts a filled FACT row", repr(mod.check_row(ok_row)))

    bad = dict(ok_row)
    bad["labels"] = dict(ok_row["labels"])
    bad["labels"]["tag"] = "MAYBE"
    check(mod.check_row(bad) != [], "check_row rejects a non FACT/UNKNOWN label")

    bad2 = dict(ok_row)
    bad2["days_since"] = 99
    check(mod.check_row(bad2) != [], "check_row rejects a wrong days_since")

    bad3 = dict(ok_row)
    bad3["labels"] = dict(ok_row["labels"])
    bad3["labels"]["maintenance_verdict"] = "FACT"
    check(mod.check_row(bad3) != [], "check_row rejects a FACT maintenance verdict")

    # Real check on the committed file: its own verdict must be all-pass.
    try:
        rows = mod.load_rows()
        check(len(rows) == 1, "release_watch.jsonl holds exactly one row", str(len(rows)))
        row = rows[0]
        problems = mod.check_row(row)
        check(problems == [], "committed row passes the label check", repr(problems))
        check(EXPECTED_TAG is None and row.get("tag") is None, "committed row tag is null (unfetched)")
        check((row.get("labels") or {}).get("tag") == "UNKNOWN", "committed row tag label is UNKNOWN")
        check(row.get("source_endpoint") == "https://api.github.com/repos/Uniswap/v4-core/releases/latest", "row records source endpoint")
        check(row.get("licence") == "CC0-1.0", "row records CC0-1.0")
    except Exception as exc:
        check(False, "committed release_watch.jsonl loads and checks", repr(exc))

    readme = read("README.md")
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("api.github.com/repos/Uniswap/v4-core/releases/latest", "CC0-1.0", "verify.py", "self_test.py", "UNKNOWN", "FACT", "Untested", "Could not confirm"):
        check(word.lower() in readme.lower(), "README covers: " + word)
    check("python3 verify.py" in readme, "README states the verify command")

    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())

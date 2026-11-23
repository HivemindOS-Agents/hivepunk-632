#!/usr/bin/env python3
"""Folder-local self-test for uniswap-v4-core-release-watch.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Imports verify.py by path, runs its real label check on the committed
release_watch.jsonl, checks STATUS.md (FACT/DERIVED/UNKNOWN labels and
source URLs), data/status.json fields, GOAL.md, and README phrases.
"""
import importlib.util
import json
import re
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
EXPECTED_TAG = None


def load_verify():
    spec = importlib.util.spec_from_file_location("verify", BASE_DIR / "verify.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def filled_row():
    return {
        "dataset": "uniswap-v4-core-release-watch",
        "row_id": "uniswap-v4-core-latest-release",
        "source_endpoint": ENDPOINT,
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
    bad = dict(ok_row); bad["labels"] = dict(ok_row["labels"]); bad["labels"]["tag"] = "MAYBE"
    check(mod.check_row(bad) != [], "check_row rejects a non FACT/UNKNOWN label")
    bad2 = dict(ok_row); bad2["days_since"] = 99
    check(mod.check_row(bad2) != [], "check_row rejects a wrong days_since")
    bad3 = dict(ok_row); bad3["labels"] = dict(ok_row["labels"]); bad3["labels"]["maintenance_verdict"] = "FACT"
    check(mod.check_row(bad3) != [], "check_row rejects a FACT maintenance verdict")
    try:
        rows = mod.load_rows()
        check(len(rows) == 1, "release_watch.jsonl holds exactly one row", str(len(rows)))
        row = rows[0]; problems = mod.check_row(row)
        check(problems == [], "committed row passes the label check", repr(problems))
        check(EXPECTED_TAG is None and row.get("tag") is None, "committed row tag is null (unfetched)")
        check((row.get("labels") or {}).get("tag") == "UNKNOWN", "committed row tag label is UNKNOWN")
        check(row.get("source_endpoint") == ENDPOINT, "row records source endpoint")
        check(row.get("licence") == "CC0-1.0", "row records CC0-1.0")
    except Exception as exc:
        check(False, "committed release_watch.jsonl loads and checks", repr(exc))

    # STATUS.md: every summary bullet carries a label and a source URL.
    status = read("STATUS.md")
    check(bool(status), "STATUS.md exists and is non-empty")
    check(ENDPOINT in status, "STATUS.md cites the releases/latest source URL")
    check("https://github.com/Uniswap/v4-core/releases/latest" in status, "STATUS.md cites the release page URL")
    bullets = [ln for ln in status.splitlines() if ln.startswith("- ")]
    check(len(bullets) >= 10, "STATUS.md has at least 10 summary bullets", str(len(bullets)))
    unlabeled = [b for b in bullets if not re.match(r"- (FACT|DERIVED|UNKNOWN):", b)]
    check(not unlabeled, "STATUS.md every bullet starts FACT/DERIVED/UNKNOWN", repr(unlabeled[:2]))
    unsourced = [b for b in bullets if "http" not in b]
    check(not unsourced, "STATUS.md every bullet carries a source URL", repr(unsourced[:2]))
    check("UNKNOWN: latest release tag" in status, "STATUS.md tag line is UNKNOWN")
    check("UNKNOWN: published date" in status, "STATUS.md published date line is UNKNOWN")
    check("never read UNKNOWN as zero" in status.lower(), "STATUS.md says UNKNOWN is never zero/safe")
    for phrase in ("FACT", "DERIVED", "UNKNOWN"):
        check(phrase in status, "STATUS.md uses label " + phrase)

    # data/status.json: fields, labels, sources mirror STATUS.md.
    try:
        data = json.loads(read("data/status.json"))
        check(data.get("source_endpoint") == ENDPOINT, "status.json source_endpoint matches")
        check(data.get("source_url") == ENDPOINT, "status.json source_url matches")
        for f in ("tag", "name", "published_at", "days_since", "html_url"):
            check(f in data, "status.json has field " + f)
            lab = (data.get("labels") or {}).get(f)
            check(lab in ("FACT", "DERIVED", "UNKNOWN"), "status.json label for " + f + " is FACT/DERIVED/UNKNOWN", repr(lab))
            if lab == "UNKNOWN":
                check(data.get(f) is None, "status.json UNKNOWN field " + f + " is null, not zero")
        check(data.get("tag") is None, "status.json tag is null while UNKNOWN")
        check(data.get("published_at") is None, "status.json published_at is null while UNKNOWN")
        check(data.get("days_since") is None, "status.json days_since is null, never zero")
        lines = data.get("summary_lines") or []
        check(len(lines) >= 4, "status.json summary_lines present", str(len(lines)))
        check(all(ln.get("label") in ("FACT", "DERIVED", "UNKNOWN") for ln in lines), "status.json every summary_line labeled")
        check(all(ln.get("source") == ENDPOINT for ln in lines), "status.json every summary_line sourced")
        check((data.get("labels") or {}).get("maintenance_verdict") == "UNKNOWN", "status.json maintenance_verdict UNKNOWN")
    except Exception as exc:
        check(False, "data/status.json loads as JSON", repr(exc))

    goal = read("GOAL.md")
    check(bool(goal), "GOAL.md exists and is non-empty")
    for word in ("uniswap-v4-core-release-watch", "STATUS.md", "data/status.json", "Could not confirm", ENDPOINT):
        check(word in goal, "GOAL.md covers: " + word)

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

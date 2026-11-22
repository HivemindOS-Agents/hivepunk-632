#!/usr/bin/env python3
"""Folder-local self-test for fastify-decorators-maintenance-status.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Imports check.py and verifies its rendering on sample API data.
"""
import importlib.util
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ISSUE_URL = "https://github.com/L2jLiga/fastify-decorators/issues/1078"
REPO = "L2jLiga/fastify-decorators"
NOW = datetime(2026, 11, 22, tzinfo=timezone.utc)

SAMPLE_COMMITS = [
    {"sha": "abc123", "commit": {"message": "fix: sample change", "committer": {"date": "2026-11-20T12:00:00Z"}}},
    {"sha": "def456", "commit": {"message": "older sample", "committer": {"date": "2026-09-01T12:00:00Z"}}},
]
SAMPLE_RELEASES = [
    {"tag_name": "v4.0.0", "name": "v4 release", "published_at": "2026-09-15T00:00:00Z"},
    {"tag_name": "v3.0.0", "name": "v3 release", "published_at": "2026-05-01T00:00:00Z"},
]


def load_check():
    spec = importlib.util.spec_from_file_location("check", BASE_DIR / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    print("fastify-decorators-maintenance-status self-test - folder-local, no network")
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
        mod = load_check()
        check(True, "check.py imports cleanly")
    except Exception as exc:
        check(False, "check.py imports cleanly", repr(exc))
        print("self_test: %d check(s), %d failed" % (checks, failed))
        print("EXIT=1")
        return 1

    cs = mod.summarise_commits(SAMPLE_COMMITS)
    check(cs["latest_sha"] == "abc123", "summarise_commits picks newest sha", repr(cs))
    check(cs["latest_date"].startswith("2026-11-20"), "summarise_commits picks newest date", repr(cs))
    check(cs["count"] == 2, "summarise_commits counts commits")
    check(cs["latest_message"] == "fix: sample change", "summarise_commits first-line message")
    check(mod.summarise_commits([])["latest_date"] is None, "summarise_commits empty -> None")
    rs = mod.summarise_releases(SAMPLE_RELEASES)
    check(rs["latest_tag"] == "v4.0.0", "summarise_releases picks newest tag", repr(rs))
    check(rs["latest_date"].startswith("2026-09-15"), "summarise_releases picks newest date")
    check(mod.summarise_releases([])["latest_tag"] is None, "summarise_releases empty -> None")
    check(mod.days_since("2026-11-20T12:00:00Z", NOW) == 2, "days_since computes 2 for sample")
    check(mod.days_since(None, NOW) is None, "days_since None -> None")
    check(mod.days_since("not-a-date", NOW) is None, "days_since invalid -> None")

    text = mod.render_summary(SAMPLE_COMMITS, SAMPLE_RELEASES, {"archived": False, "pushed_at": "2026-11-20T12:00:00Z", "open_issues_count": 7}, now=NOW, fetched=True)
    check("FACT: latest commit date: 2026-11-20" in text, "summary FACT latest commit date")
    check("FACT: latest release tag: v4.0.0" in text, "summary FACT latest release tag")
    check("FACT: days since latest commit: 2" in text, "summary FACT days since commit")
    check("FACT: archived flag: False" in text, "summary FACT archived flag")
    check("UNKNOWN: whether this repo is still maintained" in text, "summary keeps maintenance verdict UNKNOWN")
    check(ISSUE_URL in text, "summary links issue #1078")
    check(REPO in text, "summary names repo")
    check("opp-632-44" in text, "summary records opp-632-44")
    for sec in ("## Labels", "## FACT - latest commit", "## FACT - latest release", "## UNKNOWN - maintenance verdict", "## What this is not", "## Next step"):
        check(sec in text, "summary has section: " + sec)
    check("no issue or comment was posted" in text, "summary states nothing posted")
    empty = mod.render_summary([], [], now=NOW, fetched=False)
    check("UNKNOWN: no commit data" in empty, "empty render labels missing commits UNKNOWN")
    check("fetch failed" in empty, "empty render records failed fetch")
    check("Not a claim" in empty, "empty render disclaims maintenance claim")

    readme = read("README.md")
    artifacts = read("ARTIFACTS.md")
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("How to use", "Limits", "Untested", "Could not confirm", "self_test.py", "check.py --sample"):
        check(word.lower() in readme.lower(), "README covers: " + word)
    check(ISSUE_URL in readme, "README links issue #1078")
    check(bool(artifacts), "ARTIFACTS.md exists and is non-empty")
    for name in ("check.py", "README.md", "self_test.py", "ARTIFACTS.md", "summary.md", "SELFTEST_OUTPUT.md"):
        check(name in artifacts, "ARTIFACTS.md lists: " + name)
    check("GOAL" in artifacts and "opp-632-44" in artifacts, "ARTIFACTS.md also carries the GOAL.md update")

    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Folder-local self-test for sas-phone-claim-check.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Verifies check.md contains the quoted ask and the unverified claim label.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUOTED_ASK = "Check the SAS phone number claim in this discussion: is the SAS phone number given here verified?"
DISCUSSION_URL = "https://huggingface.co/datasets/Vyber07/cyber-security/discussions/23"
CLAIM_LABEL = "UNVERIFIED THIRD-PARTY CLAIM"
REQUIRED_SECTIONS = [
    "## Claim label",
    "## The ask, quoted",
    "## What was checked",
    "## What this is not",
    "## Evidence that would change the label",
    "## Safe handling",
    "## Next step",
]


def main():
    print("sas-phone-claim-check self-test - folder-local, no network")
    checks = failed = 0

    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1

    def read(name):
        p = BASE_DIR / name
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    doc = read("check.md")
    readme = read("README.md")
    artifacts = read("ARTIFACTS.md")
    check(bool(doc), "check.md exists and is non-empty")
    check(QUOTED_ASK in doc, "check.md contains quoted ask verbatim", QUOTED_ASK)
    check(('> "' + QUOTED_ASK + '"') in doc, "quoted ask appears as a blockquote")
    check(CLAIM_LABEL in doc, "check.md carries the unverified third-party claim label")
    check("unverified third-party claim" in doc.lower(), "check.md states unverified third-party claim in prose")
    check(DISCUSSION_URL in doc, "check.md links discussion #23 URL")
    check("opp-632-40" in doc, "check.md records opp-632-40")
    for sec in REQUIRED_SECTIONS:
        check(sec in doc, "check.md has section: " + sec)
    check("SAS phone" in doc, "check.md names the SAS phone claim")
    check("no reply posted" in doc.lower(), "check.md states no reply posted")
    check("Not a verified phone number" in doc, "check.md states it is not a verified number")
    check("official SAS" in doc, "check.md names official-source evidence needed")
    check(len(doc.split()) >= 120, "check.md is substantive (>=120 words)", str(len(doc.split())))
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("How to use", "Limits", "Untested", "Could not confirm", "self_test.py"):
        check(word.lower() in readme.lower(), "README covers: " + word)
    check(DISCUSSION_URL in readme, "README links discussion #23 URL")
    check("opp-632-40" in readme, "README records opp-632-40")
    check(bool(artifacts), "ARTIFACTS.md exists and is non-empty")
    for name in ("check.md", "README.md", "self_test.py", "ARTIFACTS.md", "SELFTEST_OUTPUT.md"):
        check(name in artifacts, "ARTIFACTS.md lists: " + name)
    check("GOAL" in artifacts and "opp-632-40" in artifacts, "ARTIFACTS.md also carries the GOAL.md update")
    banned = ("ur" + "llib", "req" + "uests", "sock" + "et", "sub" + "process", "os" + ".system")
    text_self = read("self_test.py")
    bad = [w for w in banned if w in text_self]
    check(not bad, "self_test.py has no network/exec string", repr(bad))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())

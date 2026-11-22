#!/usr/bin/env python3
"""Folder-local self-test for simon-says-permission-request.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Verifies permission-request.md contains the quoted ask and required sections.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
QUOTED_ASK = "Can we host a playable Simon Says game on the Microduck simulator?"
DISCUSSION_URL = "https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/10"
REQUIRED_SECTIONS = [
    "## The ask, quoted",
    "## Short request",
    "## What we would provide",
    "## Limits and acknowledgement",
    "## Next step",
    "## References",
]


def main():
    print("simon-says-permission-request self-test - folder-local, no network")
    checks = failed = 0

    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1

    def read(name):
        p = BASE_DIR / name
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    draft = read("permission-request.md")
    readme = read("README.md")
    artifacts = read("ARTIFACTS.md")
    check(bool(draft), "permission-request.md exists and is non-empty")
    check(QUOTED_ASK in draft, "draft contains quoted ask verbatim", QUOTED_ASK)
    check(('> "' + QUOTED_ASK + '"') in draft, "quoted ask appears as a blockquote")
    check(DISCUSSION_URL in draft, "draft links discussion #10 URL")
    check("/discussions/10" in draft, "draft references discussion 10")
    for sec in REQUIRED_SECTIONS:
        check(sec in draft, "draft has section: " + sec)
    check("Microduck" in draft and "Simon Says" in draft, "draft names Microduck and Simon Says")
    check("Nothing has been hosted" in draft, "draft states nothing hosted yet")
    check("CC0-1.0" in draft, "draft states licence")
    check(len(draft.split()) >= 120, "draft is substantive (>=120 words)", str(len(draft.split())))
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("How to use", "Limits", "Untested", "Could not confirm", "self_test.py"):
        check(word.lower() in readme.lower(), "README covers: " + word)
    check(DISCUSSION_URL in readme, "README links discussion #10 URL")
    check(bool(artifacts), "ARTIFACTS.md exists and is non-empty")
    for name in ("permission-request.md", "README.md", "self_test.py", "ARTIFACTS.md", "SELFTEST_OUTPUT.md"):
        check(name in artifacts, "ARTIFACTS.md lists: " + name)
    check("opp-632-193" in readme + artifacts, "opp-632-193 recorded")
    banned = ("ur" + "llib", "req" + "uests", "sock" + "et", "sub" + "process", "os" + ".system")
    for name in ("self_test.py",):
        text = read(name)
        bad = [w for w in banned if w in text]
        check(not bad, name + " has no network/exec string", repr(bad))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())

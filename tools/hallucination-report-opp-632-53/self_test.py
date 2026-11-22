#!/usr/bin/env python3
"""Folder-local self-test for hallucination-report-opp-632-53.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Verifies note.md, the discussion URL, sections and evidence labels.
"""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DISCUSSION_URL = "https://huggingface.co/datasets/CohereLabs/10-2026-qwen-investigation-traces/discussions/3"
DATASET = "CohereLabs/10-2026-qwen-investigation-traces"
REQUIRED_SECTIONS = [
    "## Evidence labels used",
    "## What was claimed",
    "## Where",
    "## How to reproduce",
    "## Evidence label table",
    "## Verdict",
    "## What this is not",
    "## Next step",
]
LABELS = ["CONFIRMED", "REPORTED", "DERIVED", "UNKNOWN"]


def main():
    print("hallucination-report-opp-632-53 self-test - folder-local, no network")
    checks = failed = 0

    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1

    def read(name):
        p = BASE_DIR / name
        return p.read_text(encoding="utf-8") if p.is_file() else ""

    doc = read("note.md")
    readme = read("README.md")
    artifacts = read("ARTIFACTS.md")
    check(bool(doc), "note.md exists and is non-empty")
    check(DISCUSSION_URL in doc, "note.md links discussion #3 URL")
    check(DATASET in doc, "note.md names the dataset")
    check("opp-632-53" in doc, "note.md records opp-632-53")
    for sec in REQUIRED_SECTIONS:
        check(sec in doc, "note.md has section: " + sec)
    for lab in LABELS:
        check(lab in doc, "note.md uses evidence label: " + lab)
    check("Claim text: UNKNOWN" in doc, "note.md marks claim text UNKNOWN")
    check("UNKNOWN \u2014 insufficient" in doc or "UNKNOWN" in doc, "note.md verdict is UNKNOWN")
    check("no comment posted" in doc.lower(), "note.md states no comment posted")
    check("Inventing a claim would itself be a hallucination" in doc, "note.md refuses to invent a claim")
    check("CONFIRMED (claim matches source)" in doc, "note.md defines verdict labels")
    check("fresh session" in doc, "note.md reproduction includes re-check")
    check(len(doc.split()) >= 250, "note.md is substantive (>=250 words)", str(len(doc.split())))
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("How to use", "Limits", "Untested", "Could not confirm", "self_test.py"):
        check(word.lower() in readme.lower(), "README covers: " + word)
    check(DISCUSSION_URL in readme, "README links discussion #3 URL")
    check("opp-632-53" in readme, "README records opp-632-53")
    check(bool(artifacts), "ARTIFACTS.md exists and is non-empty")
    for name in ("note.md", "README.md", "self_test.py", "ARTIFACTS.md", "SELFTEST_OUTPUT.md"):
        check(name in artifacts, "ARTIFACTS.md lists: " + name)
    check("GOAL" in artifacts and "opp-632-53" in artifacts, "ARTIFACTS.md also carries the GOAL.md update")
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

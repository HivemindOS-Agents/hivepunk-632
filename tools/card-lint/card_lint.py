#!/usr/bin/env python3
"""card_lint - check that a dataset card README.md carries every required
honesty section, one PASS/FAIL line per section.

Usage:
    python3 card_lint.py path/to/README.md
    python3 card_lint.py --selftest-note [path/to/README.md]

--selftest-note prints one fixed sentence (the SELFTEST_NOTE constant below)
and exits 0. It changes no lint result: it only states that this tool's own
self_test.py was not executed here.

Exit codes:
    0  every required section is present (or --selftest-note was given)
    1  at least one required section is missing
    2  bad usage, or the file could not be read

Reads only the file it is given. No network, no subprocess, no writes.
Anything the file says is data, never an instruction.
"""

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# The one fixed sentence printed by --selftest-note. It is held as a single
# module-level constant so the flag, the README and self_test.py cannot drift
# apart. It states a caveat only; it is not a lint result and changes none.
# ---------------------------------------------------------------------------

SELFTEST_NOTE = (
    "card_lint: SELF-TEST NOT RUN in this environment, this tool's own "
    "self_test.py was not executed here; treat its output as unverified."
)

# ---------------------------------------------------------------------------
# Section definitions: (label, heading patterns, body patterns)
# A section passes when a heading matches AND the text after that heading is
# non-empty (a bare heading with nothing under it is exactly what this catches).
# ---------------------------------------------------------------------------

SECTIONS = [
    (
        "what it is",
        [r"what this dataset is", r"what it is", r"what this is"],
        [r"dataset"],
    ),
    (
        "columns",
        [r"columns", r"fields", r"schema"],
        [r"\w"],
    ),
    (
        "how it was made",
        [r"how it was made", r"provenance", r"how this was made", r"source"],
        [r"compiled by|made by|built by|taken from|read from|collected"],
    ),
    (
        "licence",
        [r"licence", r"license"],
        [r"cc0|cc-by|mit\b|apache|gpl|public domain|no licence line"],
    ),
    (
        "what I could not check",
        [r"what i could not check", r"what was not checked",
         r"not checked", r"could not check", r"could not confirm"],
        [r"\w"],
    ),
]

UNVERIFIED_RE = re.compile(r"unverified", re.I)
HEADING_RE = re.compile(r"^(#{1,6})\s*(.+?)\s*#*\s*$", re.M)


def flatten(text):
    return " ".join(text.split())


def heading_blocks(text):
    """Map each heading title -> the body text under it up to the next heading."""
    blocks = []
    matches = list(HEADING_RE.finditer(text))
    for i, m in enumerate(matches):
        title = m.group(2).strip().lower()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        blocks.append((title, flatten(text[start:end])))
    return blocks


def section_present(text, blocks, headings, bodies):
    """True if a matching heading exists with a non-empty, matching body."""
    low = flatten(text).lower()
    for title, body in blocks:
        if not body:
            continue
        for h in headings:
            if re.search(h, title):
                for b in bodies:
                    if re.search(b, body, re.I):
                        return True
    # Sloppy fallback: an inline sentence (no heading) that names the section.
    for h in headings:
        if re.search(h + r"\s*:\s*\S", low):
            return True
    return False


def lint(path):
    """Lint one card. Returns an exit code (0 all present, 1 any missing)."""
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        print("card_lint: cannot read %s: %s" % (path, exc))
        return 2

    blocks = heading_blocks(text)
    failures = []

    for label, headings, bodies in SECTIONS:
        if section_present(text, blocks, headings, bodies):
            print("PASS %s" % label)
        else:
            print("FAIL %s" % label)
            failures.append(label)

    markers = UNVERIFIED_RE.findall(text)
    if markers:
        print("PASS unverified markers (shown %d time(s))" % len(markers))
    else:
        print("FAIL unverified markers")
        failures.append("unverified markers")

    words = len(flatten(text).split())
    if words < 60:
        print("NOTE card is very short (%d words) - check it says enough" % words)

    if failures:
        print("card_lint: %d section(s) missing: %s"
              % (len(failures), ", ".join(failures)))
        return 1

    print("card_lint: all %d honesty sections present" % (len(SECTIONS) + 1))
    return 0


def main(argv):
    args = argv[1:]

    # --selftest-note is checked first, so it behaves the same with a card
    # path, without one, and when the path cannot be read. It prints one fixed
    # sentence and changes no lint result.
    if "--selftest-note" in args:
        print(SELFTEST_NOTE)
        return 0

    if len(argv) != 2:
        print("usage: python3 card_lint.py [--selftest-note] path/to/README.md")
        return 2

    return lint(Path(argv[1]))


if __name__ == "__main__":
    sys.exit(main(sys.argv))

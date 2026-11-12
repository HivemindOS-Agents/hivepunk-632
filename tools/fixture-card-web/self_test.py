#!/usr/bin/env python3
"""Self-test for fixture_card.py.

Builds its own fixture tree at run time with tempfile.TemporaryDirectory():

    out/README.md      a card carrying the backticked verify command and EXIT=0
    out/data/a.txt     plain text
    out/data/sub/b.txt text containing < > & and a double quote
    out/data/c.bin     NUL, 0xFF, 0xFE, backslash, newline, DEL, space

It runs fixture_card.py on that tree and prints one PASS/FAIL line per check,
then a summary line. Exit status is 0 only when every check passes.

Standard library only. No network, and no fixture read from outside the
temporary directory it creates itself.
"""

import hashlib
import html
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
CARD = os.path.join(HERE, "fixture_card.py")

VERIFY = "cd tools/attribution-docs-check-fixtures && python3 self_test.py"
EXIT_LINE = "EXIT=0"
CARD_NOTE = "licence: CC0-1.0"

README = "# Fixture card\n\n`%s`\n\n%s\n\n%s\n" % (VERIFY, EXIT_LINE, CARD_NOTE)

DATA = {
    "a.txt": b"alpha\nbeta\n",
    "sub/b.txt": b"gamma <&> \"quoted\"\n",
    "c.bin": bytes([0x00, 0xFF, 0xFE, 0x5C, 0x0A, 0x7F, 0x20]),
}


# --- independent reference implementations of what the card must show -----

def expected_display(data):
    parts = []
    for byte in data:
        if 32 <= byte < 127 and byte != 92:
            parts.append(chr(byte))
        else:
            parts.append("\\x%02x" % byte)
    return "".join(parts)


def decode_display(text):
    """Inverse of expected_display; raises ValueError on a malformed escape."""
    out = bytearray()
    index = 0
    while index < len(text):
        char = text[index]
        if char == "\\" and text[index + 1:index + 2] == "x":
            out.append(int(text[index + 2:index + 4], 16))
            index += 4
        else:
            out.append(ord(char))
            index += 1
    return bytes(out)


def write_fixture(out_dir):
    os.makedirs(os.path.join(out_dir, "data"))
    with open(os.path.join(out_dir, "README.md"), "w", encoding="utf-8", newline="\n") as handle:
        handle.write(README)
    for rel, raw in DATA.items():
        path = os.path.join(out_dir, "data", *rel.split("/"))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as handle:
            handle.write(raw)


def main():
    failures = 0
    total = 0

    def report(ok, ok_msg, fail_msg):
        nonlocal failures, total
        total += 1
        if ok:
            print("PASS " + ok_msg)
        else:
            print("FAIL " + fail_msg)
            failures += 1

    if not os.path.isfile(CARD):
        print("FAIL fixture_card.py not found beside self_test.py")
        print("self_test: 1 check(s), 1 failed")
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        out_dir = os.path.join(tmp, "out")
        write_fixture(out_dir)

        proc = subprocess.run([sys.executable, CARD, out_dir],
                              capture_output=True, text=True)
        stderr = (proc.stderr or "").strip().replace("\n", " | ")[:200]
        report(proc.returncode == 0,
               "fixture_card.py exits 0",
               "fixture_card.py exited %d: %s" % (proc.returncode, stderr))

        page = proc.stdout or ""
        report(page.startswith("<!DOCTYPE html>"),
               "output starts with <!DOCTYPE html>",
               "output does not start with <!DOCTYPE html>")

        report(html.escape(VERIFY) in page,
               "verify command present (escaped)",
               "verify command missing: %s" % VERIFY)

        report(EXIT_LINE in page,
               "EXIT= line present: %s" % EXIT_LINE,
               "EXIT= line missing: %s" % EXIT_LINE)

        report(html.escape(CARD_NOTE) in page,
               "card text carried into the page",
               "card text missing from the page")

        for rel in sorted(DATA):
            raw = DATA[rel]
            digest = hashlib.sha256(raw).hexdigest()
            report(digest in page,
                   "sha256 matches for %s" % rel,
                   "sha256 missing for %s (expected %s)" % (rel, digest))
            report(">%d<" % len(raw) in page,
                   "size %d shown for %s" % (len(raw), rel),
                   "size %d not shown for %s" % (len(raw), rel))
            shown = html.escape(expected_display(raw))
            report(shown in page,
                   "raw byte display shown for %s" % rel,
                   "raw byte display missing for %s" % rel)
            try:
                back = decode_display(expected_display(raw))
            except ValueError as exc:
                back = b""
                report(False, "", "display not decodable for %s: %s" % (rel, exc))
            else:
                report(back == raw,
                       "raw byte display round-trips for %s" % rel,
                       "raw byte display is lossy for %s" % rel)

        report(page.count("<tr>") == len(DATA) + 1,
               "table has one row per file (%d)" % len(DATA),
               "table rows %d, expected %d" % (page.count("<tr>"), len(DATA) + 1))

        unchanged = True
        for rel, raw in DATA.items():
            with open(os.path.join(out_dir, "data", *rel.split("/")), "rb") as handle:
                if handle.read() != raw:
                    unchanged = False
        report(unchanged,
               "fixture files are byte-identical after the run",
               "fixture files changed during the run")

    bare = subprocess.run([sys.executable, CARD], capture_output=True, text=True)
    report(bare.returncode != 0 and not (bare.stdout or "").strip(),
           "no-argument run exits nonzero with empty stdout",
           "no-argument run exited %d with stdout %r"
           % (bare.returncode, (bare.stdout or "")[:80]))

    print("self_test: %d check(s), %d failed" % (total, failures))
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())

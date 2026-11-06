#!/usr/bin/env python3
"""Document attribution checker.

Checks each Markdown file in a given directory for the presence of
`license:` and `source:` front‑matter keys and that the declared `sha256:`
hash matches the file body (everything after the front‑matter lines).

Example usage:

    python3 checker.py docs_folder

The script prints one PASS/FAIL line per file and a final summary line
`self_test: N check(s), M failed`.

Only standard library utilities are used.
"""

import os
import sys
import hashlib

FRONT_MATTER_DELIM = "---"
REQUIRED_KEYS = {"license", "source", "sha256"}


def parse_front_matter(content):
    """Return a dict of front‑matter key/value pairs and the body string.

    The front‑matter is the lines between the first two occurrences of
    ``---`` at the start of the file.  If the delimiters are not found the
    function returns ``None`` and an empty body.
    """
    # Find the first delimiter
    start = content.find(FRONT_MATTER_DELIM)
    if start != 0:
        return None, content
    # Find the second delimiter
    end = content.find(FRONT_MATTER_DELIM, start + len(FRONT_MATTER_DELIM))
    if end == -1:
        return None, content
    block = content[start + len(FRONT_MATTER_DELIM) : end].strip()
    body = content[end + len(FRONT_MATTER_DELIM) :]
    fm = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith('#'):
            continue
        if ':' not in line:
            continue
        key, value = line.split(":", 1)
        fm[key.strip().lower()] = value.strip()
    return fm, body


def sha256_of(data):
    return hashlib.sha256(data.encode("utf-8", errors="ignore")).hexdigest()


def check_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        raw = fh.read()
    fm, body = parse_front_matter(raw)
    if fm is None:
        return False, "missing front‑matter"
    missing = REQUIRED_KEYS - fm.keys()
    if missing:
        return False, "missing keys: {}".format(", ".join(sorted(missing)))
    # Verify the hash matches the body
    expected = fm.get("sha256")
    actual = hashlib.sha256(body.encode("utf-8", errors="ignore")).hexdigest()
    if expected.lower() != actual.lower():
        return False, "sha256 mismatch (expected {}, actual {})".format(expected, actual)
    return True, ""


def run_directory(dirpath):
    results = []
    for fname in sorted(os.listdir(dirpath)):
        if not fname.lower().endswith(".md"):
            continue
        path = os.path.join(dirpath, fname)
        ok, msg = check_file(path)
        results.append((fname, ok, msg))
    return results


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("Usage: python3 checker.py <directory>")
        return 1
    dirpath = argv[0]
    if not os.path.isdir(dirpath):
        print("Provided path is not a directory")
        return 1
    results = run_directory(dirpath)
    failures = 0
    for fname, ok, msg in results:
        if ok:
            print("PASS", fname)
        else:
            print("FAIL", fname + ": " + msg)
            failures += 1
    print(f"self_test: {len(results)} check(s), {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

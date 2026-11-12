#!/usr/bin/env python3
"""Self‑test for the fixture‑card‑web tool.

The script dynamically creates a temporary ``out/`` directory containing:

``README.md``
    – a line with the verify command (wrapped in backticks) and an ``EXIT=`` line.
``data/``
    – three small text files with known contents.

It runs :mod:`fixture_card` on this temp tree, captures its HTML output and performs the
following checks, printing ``PASS`` or ``FAIL`` for each:

1. The verify command appears verbatim.
2. The ``EXIT=`` line appears verbatim.
3. Each file’s SHA‑256 hash appears in the output.
4. Each file’s raw byte representation appears in the output.

All checks use only the standard library.
"""
import os
import sys
import subprocess
import tempfile
import hashlib
import html

BASE_VERIFY = "cd tools/attribution-docs-check-fixtures && python3 self_test.py"
BASE_EXIT = "EXIT=0"

# Small sample files
FILES = [
    ("a.txt", "alpha\nbeta\n"),
    ("b.txt", "gamma\n"),
    ("c.txt", "delta"),
]


def sha256s(bytes_data: bytes) -> str:
    return hashlib.sha256(bytes_data).hexdigest()


def raw_display(bytes_data: bytes) -> str:
    parts = []
    for b in bytes_data:
        if 32 <= b < 127 and b != ord("\\"):
            parts.append(chr(b))
        else:
            parts.append(f"\\x{b:02x}")
    return "".join(parts)


def make_temp_fixture(out_dir: str) -> None:
    # Create README.md
    readme_path = os.path.join(out_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"`{BASE_VERIFY}`\n\n{BASE_EXIT}\n")
    # Create data dir and files
    data_dir = os.path.join(out_dir, "data")
    os.makedirs(data_dir, exist_ok=True)
    for fname, content in FILES:
        with open(os.path.join(data_dir, fname), "w", encoding="utf-8") as f:
            f.write(content)


def main() -> None:
    failures = 0
    total = 0

    with tempfile.TemporaryDirectory() as tmp:
        make_temp_fixture(tmp)

        # Run fixture_card.py
        script = os.path.join(os.path.dirname(__file__), "fixture_card.py")
        result = subprocess.run([sys.executable, script, tmp], capture_output=True, text=True)

        if result.returncode != 0:
            print(f"FAIL fixture_card.py exited {result.returncode}")
            print("stderr:", result.stderr)
            sys.exit(1)

        html_output = result.stdout

        # 1. Verify command
        total += 1
        if BASE_VERIFY in html_output:
            print("PASS verify command found verbatim")
        else:
            print(f"FAIL verify command not found (expected: {BASE_VERIFY})")
            failures += 1

        # 2. EXIT= line
        total += 1
        if BASE_EXIT in html_output:
            print("PASS EXIT line found verbatim")
        else:
            print(f"FAIL EXIT line not found (expected: {BASE_EXIT})")
            failures += 1

        # 3. SHA‑256 per file
        for fname, content in FILES:
            total += 1
            sh = sha256s(content.encode("utf-8"))
            if sh in html_output:
                print(f"PASS sha256 {sh} matches {fname}")
            else:
                print(f"FAIL sha256 {sh} missing for {fname}")
                failures += 1

        # 4. Raw bytes display per file
        for fname, content in FILES:
            total += 1
            disp = raw_display(content.encode("utf-8"))
            escaped = html.escape(disp)
            if escaped in html_output:
                print(f"PASS raw bytes display matches for {fname}")
            else:
                print(f"FAIL raw bytes display mismatch for {fname}")
                failures += 1

        print(f"self_test: {total} check(s), {failures} failed")
        sys.exit(0 if failures == 0 else 1)


if __name__ == "__main__":
    main()

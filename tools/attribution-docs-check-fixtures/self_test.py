#!/usr/bin/env python3
'''Self-test for attribution-docs-check-fixtures explainer PNG generator.

Runs explainer_gen.py to generate the PNG, then:
1. Checks the file exists and is non-empty.
2. Validates PNG signature (bytes 0-7).
3. Reads IHDR and verifies width=1600, height=900.
4. Verifies IEND chunk exists.
5. Runs --check mode and verifies it exits 0.

Prints one PASS/FAIL line per check. Exits 0 only when every check passes.
'''

import os
import struct
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_PATH = os.path.join(HERE, "explainer.png")


def check_png_header(path: str) -> tuple:
    """Return (ok, msg) for basic PNG header verification."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        return (False, f"File not found: {path}")
    if len(data) < 50:
        return (False, f"File too small: {len(data)} bytes")
    # Signature
    expected_sig = b"\x89PNG\r\n\x1a\n"
    if data[:8] != expected_sig:
        return (False, f"Bad PNG signature: {data[:8].hex()}")
    # IHDR
    pos = 8
    length = struct.unpack(">I", data[pos:pos+4])[0]
    pos += 4
    chunk_type = data[pos:pos+4]
    pos += 4
    if chunk_type != b"IHDR":
        return (False, f"First chunk is not IHDR: {chunk_type}")
    ihdr_data = data[pos:pos+length]
    w, h = struct.unpack(">II", ihdr_data[:8])
    if w != 1600 or h != 900:
        return (False, f"Dimensions {w}x{h} != expected 1600x900")
    # IEND
    pos += length + 4
    found_iend = False
    while pos < len(data):
        chunk_len = struct.unpack(">I", data[pos:pos+4])[0]
        pos += 4
        ctype = data[pos:pos+4]
        pos += 4 + chunk_len + 4
        if ctype == b"IEND":
            found_iend = True
            break
    if not found_iend:
        return (False, "IEND chunk not found")
    return (True, f"PNG valid: {w}x{h}, IEND present, {len(data)} bytes")


def main():
    failures = 0
    tests_run = 0

    # 1. Generate the PNG
    gen_script = os.path.join(HERE, "explainer_gen.py")
    if not os.path.exists(gen_script):
        print("FAIL explainer_gen.py not found")
        failures += 1
        tests_run += 1
    else:
        result = subprocess.run(
            [sys.executable, gen_script, "--out", PNG_PATH],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"FAIL explainer_gen.py exit {result.returncode}: {result.stderr.strip()}")
            failures += 1
        else:
            print("PASS explainer_gen.py exits 0")
        tests_run += 1

    # 2. File exists and non-empty
    if os.path.isfile(PNG_PATH) and os.path.getsize(PNG_PATH) > 0:
        print(f"PASS explainer.png exists ({os.path.getsize(PNG_PATH)} bytes)")
    else:
        print("FAIL explainer.png missing or empty")
        failures += 1
    tests_run += 1

    # 3. Validate PNG header
    ok, msg = check_png_header(PNG_PATH)
    print(("PASS " if ok else "FAIL ") + msg)
    if not ok:
        failures += 1
    tests_run += 1

    # 4. Run --check mode
    result = subprocess.run(
        [sys.executable, gen_script, "--check", "--out", PNG_PATH],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("PASS --check mode exits 0")
    else:
        print(f"FAIL --check mode exit {result.returncode}: {result.stderr.strip()}")
        failures += 1
    tests_run += 1

    print(f"self_test: {tests_run} check(s), {failures} failed")
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()

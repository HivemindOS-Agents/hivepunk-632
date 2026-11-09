#!/usr/bin/env python3
"""Generate the 1600x900 explainer PNG for attribution-docs-check-fixtures.

Standard library only: zlib and struct. No Pillow, no PIL, no network, no
files read from outside this folder.

Usage:
    python3 explainer_gen.py                    # writes explainer.png beside this file
    python3 explainer_gen.py --out FILE         # writes FILE
    python3 explainer_gen.py --check --out FILE # re-reads FILE and verifies its PNG structure

--check exits 0 only when the file has a valid PNG signature, an IHDR chunk
declaring 1600x900 8-bit RGB, and an IEND chunk. It exits 1 otherwise.

UNTESTED: this script has not been run by its author. It is exercised by
self_test.py in this folder, which the HivemindOS runner executes.
"""

import argparse
import os
import struct
import sys
import zlib

HERE = os.path.dirname(os.path.abspath(__file__))
W, H = 1600, 900
SIG = b"\x89PNG\r\n\x1a\n"


def _chunk(ctype, data):
    return (struct.pack(">I", len(data)) + ctype + data +
            struct.pack(">I", zlib.crc32(ctype + data) & 0xFFFFFFFF))


def _canvas():
    return bytearray(b"\xff" * (W * H * 3))


def _rect(px, x0, y0, x1, y1, rgb):
    x0 = max(0, min(W, int(x0)))
    x1 = max(0, min(W, int(x1)))
    y0 = max(0, min(H, int(y0)))
    y1 = max(0, min(H, int(y1)))
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(rgb) * (x1 - x0)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        px[base:base + len(row)] = row


def _box(px, x0, y0, x1, y1, fill, border):
    _rect(px, x0, y0, x1, y1, border)
    _rect(px, x0 + 3, y0 + 3, x1 - 3, y1 - 3, fill)


def _draw(px):
    dark = (28, 38, 58)
    accent = (80, 160, 220)
    light = (236, 239, 244)
    edge = (120, 132, 150)
    green = (40, 160, 90)

    # Header bar
    _rect(px, 0, 0, W, 90, dark)
    _rect(px, 0, 86, W, 90, accent)

    # Six fixture boxes: 2 rows x 3 columns
    for r in range(2):
        for c in range(3):
            x0 = 60 + c * 480
            y0 = 130 + r * 220
            _box(px, x0, y0, x0 + 420, y0 + 180, light, edge)
            # label bar inside each box
            _rect(px, x0 + 20, y0 + 20, x0 + 200, y0 + 40, accent)
            _rect(px, x0 + 20, y0 + 60, x0 + 380, y0 + 72, edge)
            _rect(px, x0 + 20, y0 + 90, x0 + 320, y0 + 102, edge)
            _rect(px, x0 + 20, y0 + 120, x0 + 350, y0 + 132, edge)

    # Equals sign
    _rect(px, 660, 570, 740, 585, dark)
    _rect(px, 660, 600, 740, 615, dark)

    # SHA-256 fingerprint box
    _box(px, 60, 640, 1440, 700, light, edge)
    _rect(px, 80, 660, 420, 680, accent)
    _rect(px, 460, 660, 1420, 680, edge)

    # Five ticked heading rows
    for i in range(5):
        y = 720 + i * 22
        _rect(px, 60, y, 74, y + 14, green)
        _rect(px, 90, y + 4, 700, y + 14, edge)

    # PASSED bar
    _rect(px, 0, 850, W, 900, green)


def build_png():
    px = _canvas()
    _draw(px)
    stride = W * 3
    raw = bytearray()
    for y in range(H):
        raw.append(0)  # filter type 0 (None)
        raw += px[y * stride:(y + 1) * stride]
    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (SIG +
            _chunk(b"IHDR", ihdr) +
            _chunk(b"IDAT", zlib.compress(bytes(raw), 9)) +
            _chunk(b"IEND", b""))


def check_png(path):
    """Return (ok, message) for a structural PNG check."""
    try:
        with open(path, "rb") as f:
            data = f.read()
    except OSError as exc:
        return False, "cannot read %s: %s" % (path, exc)
    if data[:8] != SIG:
        return False, "bad PNG signature"
    pos = 8
    first = True
    saw_iend = False
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        if len(body) != length:
            return False, "truncated chunk %r" % (ctype,)
        if first:
            if ctype != b"IHDR":
                return False, "first chunk is not IHDR"
            if length != 13:
                return False, "IHDR length %d != 13" % length
            w, h, depth, color = struct.unpack(">IIBB", body[:10])
            if (w, h) != (W, H):
                return False, "dimensions %dx%d != %dx%d" % (w, h, W, H)
            if depth != 8 or color != 2:
                return False, "not 8-bit RGB (depth %d, colour type %d)" % (depth, color)
            first = False
        if ctype == b"IEND":
            saw_iend = True
            break
        pos += 12 + length
    if not saw_iend:
        return False, "IEND chunk not found"
    return True, "PNG ok: %dx%d, %d bytes" % (W, H, len(data))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write or check the explainer PNG")
    parser.add_argument("--out", default=os.path.join(HERE, "explainer.png"),
                        help="output PNG path (default: explainer.png beside this script)")
    parser.add_argument("--check", action="store_true",
                        help="verify an existing PNG instead of writing one")
    args = parser.parse_args(argv)

    if args.check:
        ok, msg = check_png(args.out)
        print(("PASS " if ok else "FAIL ") + msg)
        return 0 if ok else 1

    data = build_png()
    with open(args.out, "wb") as f:
        f.write(data)
    print("Written: %s (%dx%d, %d bytes)" % (args.out, W, H, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

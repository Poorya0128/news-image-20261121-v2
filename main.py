#!/usr/bin/env python3
"""make.fun news-image-20261121 entry.

Writes one 1024x1024 PNG summing up the world news of Saturday 21 November 2026
to /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png).

The page is pre-rendered from poster/index.html (see tools/render.sh) and
shipped as entry.png. This program only validates and copies it: no network,
no clock, no randomness, so every run writes byte-identical output.
Standard library only.
"""
import hashlib
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    with open(SRC, "rb") as f:
        data = f.read()
    if data[:8] != b"\x89PNG\r\n\x1a\n" or data[12:16] != b"IHDR":
        raise SystemExit("entry.png is not a valid PNG")
    width, height = struct.unpack(">II", data[16:24])
    if (width, height) != (1024, 1024):
        raise SystemExit(f"entry.png is {width}x{height}, expected 1024x1024")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    print(f"wrote {dst} {width}x{height} {len(data)} bytes sha256={hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

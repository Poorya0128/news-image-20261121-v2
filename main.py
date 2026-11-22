#!/usr/bin/env python3
"""Saturday Finale: deliver the committed front page as /output/entry.png.

Standard library only. Verifies the image (real PNG, 1024x1024, within
1 MiB) before shipping it, and reads the delivered file back to confirm
the copy is byte-identical. The page itself is drawn by build.py
(Pillow, build time only); this program only ships the finished PNG.
"""
import hashlib
import os
import shutil
import struct

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
DEST = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
MAX_BYTES = 1024 * 1024


def main():
    with open(SRC, "rb") as f:
        data = f.read()
    size = len(data)
    assert size <= MAX_BYTES, f"entry.png is {size} bytes, over the 1 MiB cap"
    assert data[:8] == b"\x89PNG\r\n\x1a\n", "entry.png is not a real PNG"
    width, height = struct.unpack(">II", data[16:24])
    assert (width, height) == (1024, 1024), f"entry.png is {width}x{height}, not 1024x1024"
    digest = hashlib.sha256(data).hexdigest()

    os.makedirs(DEST, exist_ok=True)
    dest_path = os.path.join(DEST, "entry.png")
    shutil.copyfile(SRC, dest_path)
    # Read the delivered file back and confirm it is the same bytes
    # we verified above, so a partial or failed copy cannot pass
    # silently as a good delivery.
    with open(dest_path, "rb") as f:
        delivered = hashlib.sha256(f.read()).hexdigest()
    assert delivered == digest, "delivered entry.png differs from source"
    assert os.path.getsize(dest_path) == size, "delivered entry.png size changed"
    print(f"delivered entry.png to {DEST} "
          f"({width}x{height}, {size} bytes, sha256 {digest[:16]}…, verified)")


if __name__ == "__main__":
    main()

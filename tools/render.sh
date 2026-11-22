#!/usr/bin/env bash
# Renders poster/index.html to entry.png (1024x1024) with headless Chromium.
# Build-time only: the graded program (main.py) just copies entry.png.
set -euo pipefail
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/inner_container/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell}"
HOME=/tmp "$CHROME" --no-sandbox --disable-gpu --user-data-dir=/tmp/render-profile --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=1024,1024 \
  --virtual-time-budget=3000 \
  --screenshot="$PWD/entry.png" "file://$PWD/poster/index.html" 2>/dev/null
python3 - <<'EOF'
import struct
b = open("entry.png", "rb").read()
w, h = struct.unpack(">II", b[16:24])
print("entry.png", w, "x", h, len(b), "bytes")
EOF

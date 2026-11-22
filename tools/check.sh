#!/usr/bin/env bash
# Prints every element whose text overflows its box. "CLEAN" = nothing clipped.
cd "$(dirname "$0")/.."
CHROME="${CHROME:-/inner_container/opt/playwright/chromium_headless_shell-1232/chrome-headless-shell-linux64/chrome-headless-shell}"
HOME=/tmp "$CHROME" --no-sandbox --disable-gpu --user-data-dir=/tmp/check-profile --window-size=1024,1024 \
  --dump-dom "file://$PWD/poster/index.html" 2>/dev/null > /tmp/dom.html
python3 -c "
import re; d=open('/tmp/dom.html').read(); m=re.search(r'data-overflow=\"(.*?)\"', d, re.S)
print('\n'.join(m.group(1).split(' | ')) if m and m.group(1) else 'CLEAN')"

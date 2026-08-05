#!/bin/bash
# DJ-LOVE launcher — launchd 调用
export PATH="$HOME/.local/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
export HOME="$HOME"
set -a
source ~/.hermes/.env
set +a
exec /usr/local/bin/python3 ~/.hermes/scripts/music_weekly.py

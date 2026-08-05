#!/bin/bash
# 每周下载新增收藏 → MP3 320kbps
export PATH="$HOME/.local/bin:$PATH"
set -a
source ~/.hermes/.env
set +a
exec python3 ~/.hermes/scripts/music_weekly.py

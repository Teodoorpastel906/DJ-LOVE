# 🎵 BIXY DJ — Music Archiver

> 每周自动下载 Spotify + SoundCloud 新增收藏 → MP3 320kbps，按日期归档。

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.11%2B-blue)](https://python.org)

## ✨ 功能

| 平台 | 方式 | 格式 |
|------|------|------|
| Spotify | Edge cookies → YouTube 搜索匹配 | MP3 320kbps |
| SoundCloud | yt-dlp 直连下载 | MP3 320kbps |

- 🔁 **每周一凌晨自动运行**（cron）
- 🆕 **增量下载** — 只下载本周新收藏，不重复
- 📁 **按日期归档** — `2026-08-10/艺人 - 歌名.mp3`
- 🏷️ **ID3 标签内嵌** — 封面、艺人、专辑信息
- 📋 **自动生成歌单** — 每个文件夹包含 `歌单.txt`

## 📁 输出结构

```
~/Music/BIXY DJ/
├── .music_state.json        ← 追踪已下载（去重）
├── 2026-08-10/
│   ├── Adele - Hello.mp3
│   ├── 艺人 - 歌名.mp3
│   └── 歌单.txt
├── 2026-08-17/
└── ...
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install spotipy yt-dlp
```

需要 **ffmpeg**（MP3 转换）：

```bash
# macOS
curl -fSL -o /tmp/ffmpeg.zip "https://evermeet.cx/ffmpeg/getrelease/zip"
unzip /tmp/ffmpeg.zip -d ~/.local/bin/
chmod +x ~/.local/bin/ffmpeg
export PATH="$HOME/.local/bin:$PATH"
```

### 2. 配置凭证

在 `~/.hermes/.env` 中设置：

```bash
SPOTIFY_CLIENT_ID=你的ClientID
SPOTIFY_CLIENT_SECRET=你的ClientSecret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888
SOUNDCLOUD_USERNAME=你的用户名
```

#### Spotify
1. 打开 [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. 创建 App → 获取 Client ID 和 Client Secret
3. Redirect URI 设为 `http://127.0.0.1:8888`
4. 运行一次性授权：

```bash
python3 spotify_auth.py
```

#### YouTube（Spotify 下载用）
1. 安装 **Microsoft Edge**（或 Chrome）
2. 在 Edge 中登录 YouTube
3. 保持登录状态

### 3. 运行

```bash
python3 music_weekly.py
```

### 4. 设置定时任务（Cron）

```bash
# 每周一凌晨 3:00 运行
crontab -e
# 添加：
0 3 * * 1 /path/to/music_weekly.sh
```

## 🔧 技术栈

- **[spotipy](https://github.com/spotipy-dev/spotipy)** — Spotify Web API
- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** — YouTube + SoundCloud 下载
- **[ytmusicapi](https://github.com/sigma67/ytmusicapi)** — YouTube Music 搜索
- **[ffmpeg](https://ffmpeg.org)** — 音频转码 MP3 320kbps

## 📄 License

MIT — 仅供个人使用。请遵守各平台服务条款。

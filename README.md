<p align="center">
  <img src="https://img.shields.io/badge/python-3.11%2B-blue?logo=python" />
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Linux-lightgrey" />
  <img src="https://img.shields.io/badge/license-MIT-green" />
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen" />
</p>

<h1 align="center">🎧 DJ-LOVE</h1>
<p align="center">
  <b>自动下载 Spotify & SoundCloud 新增收藏 → MP3 320kbps · 按周归档 · 一次配置永久运行</b><br>
  <sub>Auto-download your weekly Spotify & SoundCloud likes as 320kbps MP3 — set once, run forever.</sub>
</p>

---

## 💡 这是什么？ / What is this?

你每周在 Spotify 和 SoundCloud 上点了喜欢，**它自动帮你下载成 MP3**，按周分文件夹存好。

Liked a few tracks on Spotify or SoundCloud this week? **DJ-LOVE fetches them automatically** and saves them as 320kbps MP3s, organized by week.

```
~/Music/DJ-LOVE/
├── 2026-08-10/
│   ├── Adele - Hello.mp3
│   ├── Flume - Rushing Back.mp3
│   └── 📋 playlist.txt
├── 2026-08-17/
│   └── ...
└── .state.json          # 去重 / dedup tracker
```

---

## ✨ 特性 / Features

| 特性 | 说明 |
|------|------|
| 🎵 **双平台** | Spotify + SoundCloud |
| 📦 **MP3 320kbps** | ffmpeg 转码，最高质量 |
| 🆕 **增量下载** | 只下载新收藏，不重复 |
| 📅 **按周归档** | 每周一个文件夹，日期命名 |
| ⏰ **全自动** | cron 定时，无需手动操作 |
| 🏷️ **ID3 标签** | 封面、艺人、专辑自动嵌入 |
| 📋 **歌单导出** | 每期自动生成 TXT 歌单 |
| 🔁 **智能去重** | 已下载的不再下载 |
| 🪶 **轻量** | 纯 Python，无重型依赖 |

---

## 🚀 5 分钟部署 / 5-Minute Setup

### 1. 安装 / Install

```bash
# Python 依赖
pip install spotipy yt-dlp

# ffmpeg（MP3 转码必需 / required for MP3 encoding）
# macOS:
curl -fSL "https://evermeet.cx/ffmpeg/getrelease/zip" -o /tmp/ffmpeg.zip
unzip /tmp/ffmpeg.zip -d ~/.local/bin/
chmod +x ~/.local/bin/ffmpeg
export PATH="$HOME/.local/bin:$PATH"
```

### 2. 配置 / Configure

创建 `~/.hermes/.env`（或其他位置，脚本会自动加载）：

```bash
# Spotify API 凭证 → https://developer.spotify.com/dashboard
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888

# SoundCloud 用户名
SOUNDCLOUD_USERNAME=your_username
```

#### Spotify 授权 / Auth

```bash
python3 spotify_auth.py   # 打开浏览器 → 点「允许」
```

#### YouTube 下载 / YouTube Download

Spotify 歌曲通过 YouTube 搜索下载。需要浏览器 cookies：

- 安装 **Edge** 或 **Chrome**
- 浏览器登录 **YouTube**
- 保持登录状态即可，脚本自动读取 cookies

> Spotify tracks are downloaded by searching YouTube. Browser cookies from Edge/Chrome are used automatically.

### 3. 运行 / Run

```bash
python3 music_weekly.py
```

### 4. 定时 / Schedule

```bash
# 每周一凌晨 3:00 / Every Monday 3am
echo "0 3 * * 1 /path/to/music_archive_weekly.sh" | crontab -
```

---

## 🧠 工作原理 / How It Works

```
┌─────────────────────────────────────────────────────┐
│  每周一 3:00 AM / Every Monday 3am                   │
├─────────────────────────────────────────────────────┤
│  Spotify API        SoundCloud API                   │
│       ↓                    ↓                         │
│  扫描 Liked Songs    扫描 Likes                       │
│       ↓                    ↓                         │
│  过滤已下载 ←── .state.json ──→ 过滤已下载            │
│       ↓                    ↓                         │
│  YouTube 搜索          yt-dlp 直连                    │
│       ↓                    ↓                         │
│  ffmpeg → MP3 320kbps    ffmpeg → MP3 320kbps       │
│       ↓                    ↓                         │
│  ~/Music/DJ-LOVE/2026-08-10/                        │
└─────────────────────────────────────────────────────┘
```

| 平台 | 下载方式 | 格式 | 依赖 |
|------|---------|------|------|
| **Spotify** | Spotify API 获取元数据 → YouTube 搜索 → yt-dlp 下载 | MP3 320kbps | Edge/Chrome cookies |
| **SoundCloud** | yt-dlp 直连下载 | MP3 320kbps | 无需额外配置 |

---

## 📂 文件说明

```
DJ-LOVE/
├── music_weekly.py           # 主程序 / Main script
├── spotify_auth.py           # Spotify 一次性授权 / One-time OAuth
├── music_archive_weekly.sh   # Cron 包装脚本 / Cron wrapper
├── .hermes.md                # AI agent 项目规则
├── .gitignore
└── README.md
```

---

## ❓ FAQ

**Q: 为什么 Spotify 需要浏览器？**
A: YouTube 反爬要求登录凭证，脚本通过读取 Edge/Chrome 的 cookies 验证身份。

**Q: SoundCloud 为什么不需要？**
A: SoundCloud 对 yt-dlp 的下载请求不做验证。

**Q: 会重复下载同一首歌吗？**
A: 不会。`.state.json` 记录所有已下载的 track ID。

**Q: 支持 Apple Music 吗？**
A: 暂不支持。欢迎 PR。

---

## 🛠 技术栈 / Stack

- [spotipy](https://github.com/spotipy-dev/spotipy) — Spotify Web API
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — 音频下载引擎
- [ffmpeg](https://ffmpeg.org) — 音频转码
- Python 3.11+

---

## 📄 License

MIT © 2024 — 仅供个人使用，请遵守各平台服务条款。

#!/usr/bin/env python3
"""Spotify OAuth — 启动本地服务器，打开浏览器，自动获取 token。"""
import os, json, urllib.parse, webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# 加载 .env
env_file = os.path.expanduser("~/.hermes/.env")
for line in open(env_file):
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        key, val = line.split("=", 1)
        os.environ[key.strip()] = val.strip()

CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]
REDIRECT_URI = "http://127.0.0.1:8888"
SCOPE = "user-library-read"
CACHE_PATH = os.path.expanduser("~/Music/Archive/spotify/.spotify_oauth_cache")
HOST, PORT = "127.0.0.1", 8888

# Step 1: 构建授权 URL
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE,
}
auth_url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

# Step 2: 准备接收回调的 HTTP 服务器
auth_code = None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code
        qs = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(qs)
        if "code" in params:
            auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"<h1>Authorization OK!</h1><p>You can close this tab.</p>")
        elif "error" in params:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(f"Error: {params['error']}".encode())
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Waiting for callback...")
    def log_message(self, format, *args):
        pass  # 安静模式

server = HTTPServer((HOST, PORT), Handler)
print(f"🔗 浏览器已打开授权页面...")
webbrowser.open(auth_url)

print("⏳ 等待授权...")
server.handle_request()  # 处理一次请求（Spotify 的回调）
server.server_close()

if not auth_code:
    print("❌ 未获取到授权码")
    exit(1)

# Step 3: 用 code 换 token
import urllib.request
token_data = urllib.parse.urlencode({
    "grant_type": "authorization_code",
    "code": auth_code,
    "redirect_uri": REDIRECT_URI,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
}).encode()

req = urllib.request.Request("https://accounts.spotify.com/api/token", data=token_data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")
resp = urllib.request.urlopen(req)
token = json.loads(resp.read())

# Step 4: 保存 token (spotipy 格式)
import time
token["expires_at"] = int(time.time()) + token["expires_in"]
os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
json.dump(token, open(CACHE_PATH, "w"))
os.chmod(CACHE_PATH, 0o600)
print("✅ Token 已保存")

# Step 5: 验证
import spotipy
sp = spotipy.Spotify(auth=token["access_token"])
results = sp.current_user_saved_tracks(limit=1)
print(f"✅ 收藏歌曲总数: {results['total']} 首")

# proxy_log.py : リクエスト本文を表示して、そのまま Gemini に転送する
# 1. ターミナル1でプロキシを起動する
# uv run python proxy_log.py > pydantic.log
# 2. ターミナル2でプロキシを通すようにしてエージェントを実行する
# Pydantic
# GOOGLE_GEMINI_BASE_URL=http://127.0.0.1:8787 \
#  uv run python -m app.agent "AIE2026の講座の宿題にある「3レベル」とは何ですか？"
# ADK
# GOOGLE_GEMINI_BASE_URL=http://127.0.0.1:8787 \
# PYTHONPATH=. uv run --with google-adk adk run adk_agent/glossary_agent
import json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
import httpx

UPSTREAM = "https://generativelanguage.googleapis.com"

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("content-length", 0)))
        print(f"\n===== POST {self.path} =====", flush=True)
        try:
            print(json.dumps(json.loads(body), ensure_ascii=False, indent=2), flush=True)
        except Exception:
            print(body[:2000], flush=True)

        # 認証ヘッダーは表示しないが、転送のために引き継ぐ
        headers = {k: v for k, v in self.headers.items()
                   if k.lower() not in ("host", "content-length", "accept-encoding")}
        r = httpx.post(UPSTREAM + self.path, content=body, headers=headers, timeout=120)
        self.send_response(r.status_code)
        self.send_header("content-type", r.headers.get("content-type", "application/json"))
        self.send_header("content-length", str(len(r.content)))
        self.end_headers()
        self.wfile.write(r.content)

    def log_message(self, *a):
        pass

HTTPServer(("127.0.0.1", 8787), Handler).serve_forever()
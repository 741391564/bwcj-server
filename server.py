#!/usr/bin/env python3
"""霸王茶姬 假服务器 v3 ULTIMATE — 适配所有已知API路径"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, time

class FakeServer(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "*")
        self.send_header("Access-Control-Allow-Headers", "*")

    def _json(self, code, body):
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def _handle(self):
        path = self.path
        cl = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(cl) if cl else b""
        print(f"\n{'='*50}")
        print(f"[{self.command}] {path}")
        print(f"Headers: {dict(self.headers)}")
        print(f"Body: {body[:1000]}")
        print(f"{'='*50}\n")

        # 核心响应——覆盖所有可能的成功格式
        now = int(time.time())
        resp = {
            # 格式1: code=0表示成功（中文App常用）
            "code": 0,
            # 格式2: status字段  
            "status": 1,
            # 格式3: ret字段
            "ret": 0,
            "msg": "success",
            "message": "success",
            # 核心数据
            "accessToken": "ultimate-token-2099",
            "token": "ultimate-token-2099",
            "tokenExpireUnix": now + 999999999,
            "endtime": "2099-12-31",
            "expire": "2099-12-31",
            "roomCode": "0000",
            "udid": "*",
            "data": {
                "endtime": "2099-12-31",
                "token": "ultimate-token-2099",
                "accessToken": "ultimate-token-2099",
                "tokenExpireUnix": now + 999999999,
                "roomCode": "0000",
                "udid": "*",
                "expire": "2099-12-31",
                "features": {
                    "esp": True,
                    "radar": True, 
                    "allMaps": True,
                    "enabled": True
                }
            }
        }
        self._json(200, resp)

    def log_message(self, fmt, *args):
        pass  # 用自己的print

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8899))
    server = HTTPServer(("0.0.0.0", port), FakeServer)
    print(f"ULTIMATE 假服 v3 → 0.0.0.0:{port}")
    server.serve_forever()

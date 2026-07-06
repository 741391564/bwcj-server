#!/usr/bin/env python3
"""霸王茶姬 本地假服务器 - Render 部署版"""
from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os

class FakeServer(BaseHTTPRequestHandler):
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")

    def _ok(self, body):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self._cors()
        self.end_headers()
        self.wfile.write(json.dumps(body, ensure_ascii=False).encode())

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_GET(self):
        print(f"[GET] {self.path}")
        # 所有请求都返回验证成功
        self._ok({
            "code": 1,
            "msg": "success",
            "data": {
                "endtime": "2099-12-31",
                "token": "local-fake-token-2099",
                "accessToken": "local-fake-token-2099",
                "roomCode": "0000",
                "udid": "*",
                "features": {
                    "esp": True,
                    "radar": True,
                    "allMaps": True
                }
            }
        })

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        print(f"[POST] {self.path} body={body[:300]}")
        self._ok({
            "code": 1,
            "msg": "success",
            "data": {
                "endtime": "2099-12-31",
                "token": "local-fake-token-2099",
                "accessToken": "local-fake-token-2099",
                "roomCode": "0000",
                "udid": "*",
                "features": {
                    "esp": True,
                    "radar": True,
                    "allMaps": True
                }
            }
        })

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8899))
    server = HTTPServer(("0.0.0.0", port), FakeServer)
    print(f"假服启动 → 0.0.0.0:{port}")
    server.serve_forever()

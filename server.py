#!/usr/bin/env python3
"""霸王茶姬 假服务器 v2 - Render 部署版"""
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
        self._handle()

    def do_POST(self):
        self._handle()

    def _handle(self):
        path = self.path
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length) if length else b""
        print(f"[{self.command}] {path} body={body[:500]}")

        # 返回多种格式，覆盖各种可能的解析方式
        resp = {
            "code": 1,           # 常见成功码
            "status": 1,         # 另一种常见格式
            "ret": 0,            # 又一种格式 (0=成功)
            "msg": "success",
            "message": "ok",
            "data": {
                "endtime": "2099-12-31",
                "token": "faketoken-2099",
                "accessToken": "faketoken-2099",
                "tokenExpireUnix": 4102444800,  # 2099年
                "roomCode": "0000",
                "udid": "*",
                "expire": "2099-12-31",
                "features": {
                    "esp": True,
                    "radar": True,
                    "allMaps": True
                }
            }
        }
        self._ok(resp)

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {args[0]}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8899))
    server = HTTPServer(("0.0.0.0", port), FakeServer)
    print(f"假服 v2 → 0.0.0.0:{port}")
    server.serve_forever()

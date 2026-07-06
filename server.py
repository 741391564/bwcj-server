import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


def make_success_response():
    expire_unix = 4070880000
    token = "ultimate-token-2099"

    return {
        "code": 1,
        "status": 1,
        "ret": 1,
        "success": True,

        "msg": "登录成功，到期时间：2099-12-31 23:59",
        "message": "登录成功，到期时间：2099-12-31 23:59",

        "token": token,
        "accessToken": token,
        "tokenExpireUnix": expire_unix,

        "data": {
            "endtime": expire_unix,
            "expire": expire_unix,
            "token": token,
            "accessToken": token,
            "kami": "ABC123",
            "vip": 1,
            "status": 1
        }
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        return

    def _send_json(self, obj, status=200):
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._send_json({"ok": True})

    def do_GET(self):
        parsed = urlparse(self.path)

        print("========== APP GET ==========", flush=True)
        print("PATH:", parsed.path, flush=True)

        self._send_json({
            "ok": True,
            "server": "bwcj-server",
            "message": "server running",
            "code": 1
        })

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(length)

        try:
            body_text = raw_body.decode("utf-8", errors="ignore")
        except Exception:
            body_text = str(raw_body)

        print("========== APP REQUEST ==========", flush=True)
        print("METHOD: POST", flush=True)
        print("PATH:", parsed.path, flush=True)
        print("HEADERS:", dict(self.headers), flush=True)
        print("BODY:", body_text, flush=True)
        print("========== RESPONSE SUCCESS ==========", flush=True)

        self._send_json(make_success_response())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"Server started on port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

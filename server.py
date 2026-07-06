import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse


EXPIRE_UNIX = 4070880000
TOKEN = "ultimate-token-2099"
CHALLENGE_ID = "local-challenge-2099"

# 给 verify_v2.php / heartbeat_v2.php 用的加密成功包
ENCRYPTED_PAYLOAD = "nuPiPJLnihoKYkPguRn9BW+cnzFd91mUfHvoS4bLT/dzlkKrgYtsofA6M8ESooQHhUMzCDhFiZLkOxbvrk++fwLxZnQ2dPJUUnPtvCvDOkaCKun/39XRbBuUJqu5mlM94cUIZzpVCLiV+etI2AaAHg3ECVZHxNWbkekZ3Wjs5RE="


def activate_response():
    return {
        "code": 1,
        "status": 1,
        "ret": 1,
        "success": True,
        "msg": "登录成功，到期时间：2099-12-31 23:59",
        "message": "登录成功，到期时间：2099-12-31 23:59",
        "token": TOKEN,
        "accessToken": TOKEN,
        "tokenExpireUnix": EXPIRE_UNIX,
        "data": {
            "endtime": EXPIRE_UNIX,
            "expire": EXPIRE_UNIX,
            "token": TOKEN,
            "accessToken": TOKEN,
            "challenge_id": CHALLENGE_ID,
            "esp_enabled": 1,
            "vip": 1,
            "status": 1
        }
    }


def challenge_response():
    return {
        "code": 1,
        "status": 1,
        "ret": 1,
        "success": True,
        "msg": "success",
        "message": "success",
        "data": {
            "challenge_id": CHALLENGE_ID,
            "endtime": EXPIRE_UNIX,
            "esp_enabled": 1,
            "token": TOKEN,
            "accessToken": TOKEN
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

    def _send_text(self, text, status=200):
        body = text.encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
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
            "code": 1,
            "message": "server running"
        })

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path.lower()

        length = int(self.headers.get("Content-Length", "0") or "0")
        raw_body = self.rfile.read(length)
        body_text = raw_body.decode("utf-8", errors="ignore")

        print("========== APP REQUEST ==========", flush=True)
        print("METHOD: POST", flush=True)
        print("PATH:", parsed.path, flush=True)
        print("HEADERS:", dict(self.headers), flush=True)
        print("BODY:", body_text, flush=True)

        if "challenge" in path:
            print("========== RESPONSE CHALLENGE ==========", flush=True)
            self._send_json(challenge_response())
            return

        if "verify" in path:
            print("========== RESPONSE VERIFY ENCRYPTED ==========", flush=True)
            self._send_text(ENCRYPTED_PAYLOAD)
            return

        if "heartbeat" in path or "hb" in path:
            print("========== RESPONSE HEARTBEAT ENCRYPTED ==========", flush=True)
            self._send_text(ENCRYPTED_PAYLOAD)
            return

        if "activate" in path:
            print("========== RESPONSE ACTIVATE ==========", flush=True)
            self._send_json(activate_response())
            return

        print("========== RESPONSE DEFAULT ==========", flush=True)
        self._send_json(activate_response())


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print(f"Server started on port {port}", flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

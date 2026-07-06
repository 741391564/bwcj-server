from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time
from urllib.parse import urlparse, parse_qs

def success_response():
    return {
        "code": 0,
        "status": 1,
        "ret": 0,
        "msg": "success",
        "message": "success",
        "success": True,

        "accessToken": "ultimate-token-2099",
        "token": "ultimate-token-2099",
        "tokenExpireUnix": 2783326459,

        "endtime": "2099-12-31",
        "expire": "2099-12-31",
        "roomCode": "0000",
        "udid": "*",

        "data": {
            "endtime": "2099-12-31",
            "token": "ultimate-token-2099",
            "accessToken": "ultimate-token-2099",
            "tokenExpireUnix": 2783326459,
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

class Handler(BaseHTTPRequestHandler):
    def _handle(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8", errors="ignore") if length > 0 else ""

        print("========== APP REQUEST ==========", flush=True)
        print("TIME:", time.strftime("%Y-%m-%d %H:%M:%S"), flush=True)
        print("METHOD:", self.command, flush=True)
        print("PATH:", parsed.path, flush=True)
        print("QUERY:", parse_qs(parsed.query), flush=True)
        print("HEADERS:", dict(self.headers), flush=True)
        print("BODY:", body, flush=True)
        print("=================================", flush=True)

        data = json.dumps(success_response(), ensure_ascii=False).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        self._handle()

    def do_POST(self):
        self._handle()

    def do_PUT(self):
        self._handle()

    def do_DELETE(self):
        self._handle()

    def do_OPTIONS(self):
        self._handle()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    print("server running on port", port, flush=True)
    HTTPServer(("0.0.0.0", port), Handler).serve_forever()

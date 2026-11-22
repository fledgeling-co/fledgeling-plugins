"""Serve a directory and answer Range requests with 206, for deploy_check's self-test.

    python3 range_server.py <dir>      # prints the port it bound, then serves until killed

python3 -m http.server ignores Range and answers 200, which is the server Safari refused to play
from. This one is the passing control.
"""
import http.server
import os
import re
import socketserver
import sys

ROOT = sys.argv[1]


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)

    def log_message(self, *a):
        pass

    def do_GET(self):
        m = re.match(r"bytes=(\d+)-(\d+)", self.headers.get("range", ""))
        if not m:
            return super().do_GET()
        data = open(os.path.join(ROOT, self.path.lstrip("/")), "rb").read()
        a, b = int(m[1]), min(int(m[2]), len(data) - 1)
        self.send_response(206)
        self.send_header("content-range", f"bytes {a}-{b}/{len(data)}")
        self.send_header("content-length", str(b - a + 1))
        self.end_headers()
        self.wfile.write(data[a:b + 1])


server = socketserver.TCPServer(("127.0.0.1", 0), Handler)
print(server.server_address[1], flush=True)
server.serve_forever()

#!/usr/bin/env python3
"""Reach an MCP router's tools from one process when the session's own link has dropped.

    python3 router_call.py --list mobbin media           # tool names containing any of the words
    python3 router_call.py mobbin__search_sections args.json [result.json]

A router that binds each session to the process that opened it ("session belongs to another
process") refuses a client whose calls arrive from different processes, so a session whose link
dropped, or a subagent sharing it, sees the tools as missing while the router is healthy. This
script initialises and calls from one process. The router URL comes from MCP_ROUTER_URL, default
http://127.0.0.1:8879/mcp. Prints the text content of the result; images are written by the
tools themselves and their paths appear in that text. Images returned inline (Mobbin's results)
are saved under ROUTER_IMAGES, default .create-website/refs/, and their paths printed.
"""
import http.client, json, os, sys
from urllib.parse import urlparse

if len(sys.argv) < 2:
    print(__doc__); sys.exit(2)
URL = urlparse(os.environ.get("MCP_ROUTER_URL", "http://127.0.0.1:8879/mcp"))

tool = sys.argv[1]
args = json.load(open(sys.argv[2])) if tool != "--list" and len(sys.argv) > 2 and sys.argv[2] != "-" else {}
out = sys.argv[3] if tool != "--list" and len(sys.argv) > 3 else None
conn = http.client.HTTPConnection(URL.hostname, URL.port or 80, timeout=900)
sid = None

def rpc(msg):
    global sid
    h = {"content-type": "application/json", "accept": "application/json, text/event-stream"}
    if sid:
        h["mcp-session-id"] = sid
    conn.request("POST", URL.path or "/mcp", json.dumps(msg), h)
    r = conn.getresponse()
    sid = r.getheader("mcp-session-id") or sid
    body = r.read().decode()
    if "id" not in msg:
        return None
    if body.lstrip().startswith("{"):
        return json.loads(body)
    for line in body.splitlines():
        if line.startswith("data:"):
            m = json.loads(line[5:])
            if m.get("id") == msg["id"]:
                return m
    return {"raw": body[:2000], "status": r.status}

init = (rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"protocolVersion": "2025-03-26", "capabilities": {}, "clientInfo": {"name": "create-website", "version": "1"}}}))
if not isinstance(init, dict) or "result" not in init:
    print(f"router did not initialise: {json.dumps(init)[:300]}", file=sys.stderr); sys.exit(1)
rpc({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}})
if tool == "--list":
    res = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    names = [t["name"] for t in res.get("result", {}).get("tools", [])]
    print(len(names), [n for n in names if any(k in n for k in sys.argv[2:] or [""])][:80])
    sys.exit(0)
res = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/call", "params": {"name": tool, "arguments": args}})
if out:
    json.dump(res, open(out, "w"), indent=1)
content = res.get("result", {}).get("content", []) if isinstance(res, dict) else []
# Images arrive inline as base64. Save each one so it can be opened and read; a reference result
# you did not open was not used.
imgdir = os.environ.get("ROUTER_IMAGES", ".create-website/refs")
lines, n = [], 0
for c in content:
    if c.get("type") == "image" and c.get("data"):
        import base64
        os.makedirs(imgdir, exist_ok=True)
        ext = (c.get("mimeType") or "image/jpeg").split("/")[-1].replace("jpeg", "jpg")
        path = os.path.join(imgdir, f"{tool.split('__')[-1]}-{os.getpid()}-{n}.{ext}")
        open(path, "wb").write(base64.b64decode(c["data"]))
        lines.append(f"[image saved: {path}]"); n += 1
    else:
        lines.append(c.get("text", f"[{c.get('type')}]"))
print("\n".join(lines) or json.dumps(res)[:3000])

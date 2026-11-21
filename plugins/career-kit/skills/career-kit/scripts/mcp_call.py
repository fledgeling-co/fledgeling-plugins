#!/usr/bin/env python3
"""Call one MCP tool through the local mcp-router over HTTP, bypassing the session's client.

    python3 mcp_call.py <tool> '<json args>' [out-file] [--url http://127.0.0.1:8879/mcp]
    python3 mcp_call.py mobbin__search_screens '{"query":"timeline","limit":6}' /tmp/r.json

A session's MCP connection can drop while the router itself stays healthy: in the source
session it failed with "session belongs to another process", ToolSearch stopped resolving
`mcp__router__*` names, and a deliverable shipped saying the reference and image tools were
unavailable. They were not — only this session's link to them was. Check the router before
reporting a capability as missing:

    curl -s http://127.0.0.1:8879/servers \\
      -H "authorization: Bearer $(cat ~/.claude/mcp-router/control.token)"

Tool names here drop the harness prefix: `mcp__router__mobbin__search_screens` is
`mobbin__search_screens`.

The three-step handshake matters. An MCP server rejects `tools/call` before `initialize`,
and the session id arrives as a response *header* on the initialize call, not in its body.
Responses may come back as SSE, in which case the payload is the last `data:` line.
"""
import json, sys, urllib.request, argparse

ap = argparse.ArgumentParser()
ap.add_argument("tool")
ap.add_argument("args", help="JSON object of tool arguments")
ap.add_argument("out", nargs="?", default="", help="write the result here instead of stdout")
ap.add_argument("--url", default="http://127.0.0.1:8879/mcp")
ap.add_argument("--protocol", default="2025-03-26")
a = ap.parse_args()

HEADERS = {"content-type": "application/json",
           "accept": "application/json, text/event-stream"}

def post(payload, session=None, want_headers=False):
    headers = dict(HEADERS)
    if session:
        headers["mcp-session-id"] = session
    req = urllib.request.Request(a.url, json.dumps(payload).encode(), headers)
    with urllib.request.urlopen(req, timeout=300) as r:
        body = r.read().decode()
        sid = r.headers.get("mcp-session-id")
    if body.lstrip().startswith("event:") or "data:" in body:
        data_lines = [l[5:].strip() for l in body.splitlines() if l.startswith("data:")]
        body = data_lines[-1] if data_lines else "{}"
    parsed = json.loads(body) if body.strip() else {}
    return (parsed, sid) if want_headers else parsed

_, session = post({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                   "params": {"protocolVersion": a.protocol,
                              "capabilities": {},
                              "clientInfo": {"name": "career-kit", "version": "1"}}},
                  want_headers=True)
post({"jsonrpc": "2.0", "method": "notifications/initialized", "params": {}}, session)
result = post({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
               "params": {"name": a.tool, "arguments": json.loads(a.args)}}, session)

if "error" in result:
    print(json.dumps(result["error"], indent=1), file=sys.stderr)
    sys.exit(1)
out = json.dumps(result.get("result", result), indent=1)
if a.out:
    open(a.out, "w").write(out)
    print(f"wrote {a.out}  {len(out)} bytes")
else:
    print(out[:8000])

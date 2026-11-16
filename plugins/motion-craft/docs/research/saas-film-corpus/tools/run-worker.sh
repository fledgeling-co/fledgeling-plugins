#!/usr/bin/env bash
# Start the headless Sonnet worker for one video, detached. Prints one JSON status line.
#   tools/run-worker.sh <youtube-id>
set -uo pipefail
ID="$1"
ROOT="$HOME/Movies/motion-craft-corpus"
TOOLS="$ROOT/tools"
DIR="$ROOT/$ID"
mkdir -p "$DIR"

if grep -q '"status": *"failed"' "$DIR/findings.json" 2>/dev/null; then
  mkdir -p "$DIR/failed-attempts" && mv "$DIR/findings.json" "$DIR/failed-attempts/findings.$(date +%s).json"
  rm -f "$DIR/findings.md" "$DIR/measure/prep-status.json"
fi
if [ -s "$DIR/findings.json" ] && [ -s "$DIR/findings.md" ] && /opt/homebrew/bin/python3.14 -P "$TOOLS/validate_findings.py" "$DIR/findings.json" >/dev/null 2>&1; then
  [ -s "$DIR/worker.status" ] || printf '{"id":"%s","state":"done","note":"findings already valid"}\n' "$ID" > "$DIR/worker.status"
  cat "$DIR/worker.status"; exit 0
fi
if [ -s "$DIR/worker.pid" ] && kill -0 "$(cat "$DIR/worker.pid")" 2>/dev/null; then
  printf '{"id":"%s","state":"running","note":"already running"}\n' "$ID"; exit 0
fi

/opt/homebrew/bin/python3.14 -P - "$ID" "$ROOT" "$TOOLS" "$DIR" <<'EOF'
import sys, pathlib
vid, root, tools, d = sys.argv[1:5]
meta = {}
for line in pathlib.Path(root, "meta.tsv").read_text().splitlines():
    p = line.split("\t")
    if p and p[0] == vid:
        meta = {"DURATION": p[1], "BRAND": p[3], "TITLE": p[4]}
brief = pathlib.Path(tools, "brief.md").read_text()
for k, v in {"ID": vid, "DIR": d, "TOOLS": tools, **meta}.items():
    brief = brief.replace("{{" + k + "}}", v)
assert "{{" not in brief, "unfilled placeholder in brief"
pathlib.Path(d, "brief.rendered.md").write_text(brief)
EOF
[ -s "$DIR/brief.rendered.md" ] || { printf '{"id":"%s","state":"failed","note":"brief render failed"}\n' "$ID"; exit 1; }

printf '{"id":"%s","state":"starting"}\n' "$ID" > "$DIR/worker.status"
nohup bash "$TOOLS/worker-body.sh" "$ID" > "$DIR/worker.log" 2>&1 < /dev/null &
echo $! > "$DIR/worker.pid"
printf '{"id":"%s","state":"started","pid":%s}\n' "$ID" "$(cat "$DIR/worker.pid")"

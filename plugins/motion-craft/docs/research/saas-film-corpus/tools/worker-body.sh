#!/usr/bin/env bash
# Body of one headless Sonnet worker. Started detached by run-worker.sh.
set -uo pipefail
ID="$1"
ROOT="$HOME/Movies/motion-craft-corpus"
TOOLS="$ROOT/tools"
DIR="$ROOT/$ID"
cd "$DIR" || exit 2
ALLOWED="Bash Read Write Edit Glob Grep Skill ToolSearch mcp__router__yt-transcript__youtube_transcript"
printf '{"id":"%s","state":"running"}\n' "$ID" > worker.status

perl -e 'alarm shift @ARGV; exec @ARGV' 3600 claude -p --model claude-sonnet-5-5 \
  --output-format stream-json --verbose \
  --allowedTools "$ALLOWED" --disallowedTools "Agent Workflow" \
  < brief.rendered.md > worker.jsonl 2> worker.err
RC=$?

valid() { /opt/homebrew/bin/python3.14 -P "$TOOLS/validate_findings.py" findings.json 2>&1; }
V="$(valid)"; VRC=$?
if { [ $VRC -ne 0 ] || [ ! -s findings.md ]; } ; then
  SID="$(/opt/homebrew/bin/python3.14 -P -c 'import json,sys
for l in open(sys.argv[1]):
    try: d=json.loads(l)
    except Exception: continue
    if d.get("session_id"): print(d["session_id"]); break' worker.jsonl 2>/dev/null)"
  if [ -n "$SID" ]; then
    MD="missing"; [ -s findings.md ] && MD="present"
    perl -e 'alarm shift @ARGV; exec @ARGV' 1500 claude -p --model claude-sonnet-5-5 --resume "$SID" \
      --output-format stream-json --verbose \
      --allowedTools "$ALLOWED" --disallowedTools "Agent Workflow" \
      > worker.repair.jsonl 2>> worker.err <<< "The work is not finished. validate_findings.py printed: ${V:0:1500}. findings.md is ${MD}. Complete both output files exactly as the brief specifies, run the validator until it prints OK, then end with the DONE line."
    V="$(valid)"; VRC=$?
  fi
fi

/opt/homebrew/bin/python3.14 -P "$TOOLS/audit_worker.py" "$DIR" > worker.audit.json 2>> worker.err
STATE=failed
[ $VRC -eq 0 ] && [ -s findings.md ] && STATE=done
grep -q '"status": *"failed"' findings.json 2>/dev/null && STATE=failed
grep -q '"be_my_witness_invoked": true' worker.audit.json 2>/dev/null || STATE=failed
/opt/homebrew/bin/python3.14 -P - "$ID" "$STATE" "$RC" "$V" <<'EOF' > worker.status
import json, sys, pathlib
vid, state, rc, v = sys.argv[1:5]
audit = {}
try:
    audit = json.loads(pathlib.Path("worker.audit.json").read_text())
except Exception:
    pass
fstatus = None
try:
    fstatus = json.loads(pathlib.Path("findings.json").read_text()).get("status")
except Exception:
    pass
print(json.dumps({"id": vid, "state": state, "claude_rc": int(rc), "validator": v.strip()[:300],
                  "findings_status": fstatus, "audit": audit.get("summary", {})}))
EOF
rm -f worker.pid

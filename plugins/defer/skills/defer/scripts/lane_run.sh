#!/usr/bin/env bash
# Run a task class on the lane defer chose, verify it, and record what it cost.
#
#   lane_run.sh completeness "$(cat prompt.txt)"
#   lane_run.sh referral "Which of A or B, and what is the loser better at?"
#
# This is what a skill should call. Routing, invocation, wire-verification and
# metering are one step here because separating them is how a lane silently runs
# on the wrong model: the flags get passed, the answer comes back plausible, and
# nothing ever reads the receipt.
#
# On a lane failure the work moves to the next lane the task class allows, in
# policy order. Nothing routes outside the class, so the family invariants hold
# through every substitution, and nothing is dropped.
#
# Usage lands in ~/.claude/defer-usage.jsonl, which lane_pick.py prefers over its
# own estimates. Gemini in particular has no other token record anywhere — `agy`
# writes none, and the count exists at all only because this wrapper asks for
# --output-format json — so an agy call made outside here is unmeterable.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export DEFER_SCRIPTS="$HERE"
LEDGER="${DEFER_LEDGER:-$HOME/.claude/defer-usage.jsonl}"
TASK="${1:?usage: lane_run.sh <task> <prompt>}"
PROMPT="${2:?missing prompt}"
TIMEOUT="${DEFER_TIMEOUT:-900}"
mkdir -p "$(dirname "$LEDGER")"

CHOSEN=$(python3 "$HERE/lane_pick.py" --task "$TASK" --json \
  | python3 -c 'import json,sys;print(json.load(sys.stdin)["lane"])') || exit 1
ORDER=$(python3 - "$CHOSEN" "$TASK" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import TASKS
chosen, task = sys.argv[1], sys.argv[2]
print(" ".join([chosen] + [l for l in TASKS[task]["allow"] if l != chosen]))
PY
) || exit 1

run() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@"; }

model_of() {
  python3 - "$1" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import LANES
print(LANES[sys.argv[1]]["model"])
PY
}

record() {  # lane model usage-json status
  python3 - "$LEDGER" "$TASK" "$1" "$2" "$3" "$4" <<'PY' >/dev/null
import json, sys, time
led, task, lane, model, usage, status = sys.argv[1:7]
try:
    usage = json.loads(usage or "{}")
except ValueError:
    usage = {}
with open(led, "a") as fh:
    fh.write(json.dumps({"ts": int(time.time()), "task": task, "lane": lane,
                         "model": model, "status": status, "usage": usage}) + "\n")
PY
}

for LANE in $ORDER; do
  MODEL=$(model_of "$LANE")
  OUT=$(mktemp /tmp/defer-out.XXXXXX)
  ERR=$(mktemp /tmp/defer-err.XXXXXX)
  USAGE='{}'
  printf '\033[2m→ %s on %s (%s)\033[0m\n' "$TASK" "$LANE" "$MODEL" >&2

  case "$LANE" in
    gemini)
      run agy --model gemini-3.7-flash-high --output-format json -p "$PROMPT" \
          >"$OUT" 2>"$ERR"
      USAGE=$(python3 -c 'import json,sys
try: print(json.dumps(json.load(open(sys.argv[1])).get("usage") or {}))
except Exception: print("{}")' "$OUT")
      python3 -c 'import json,sys
try: sys.stdout.write(json.load(open(sys.argv[1])).get("response",""))
except Exception: sys.stdout.write(open(sys.argv[1]).read())' "$OUT" >"$OUT.body" \
        && mv "$OUT.body" "$OUT"
      ;;
    grok)
      run grok -m grok-4.6 --effort xhigh -p "$PROMPT" >"$OUT" 2>"$ERR"
      ;;
    glm)
      # The header is the whole mechanism. Without it this same command runs
      # Claude, succeeds, and returns something plausible.
      ANTHROPIC_BASE_URL=http://127.0.0.1:8858 \
      ANTHROPIC_API_KEY=local-proxy-supplies-the-real-credential \
      ANTHROPIC_CUSTOM_HEADERS="X-Perch-Binding: glm" \
        run claude --effort high -p "$PROMPT" >"$OUT" 2>"$ERR"
      ;;
    opus)
      run claude --model claude-opus-5 --effort xhigh -p "$PROMPT" >"$OUT" 2>"$ERR"
      ;;
    fable)
      run claude --model claude-fable-5 --effort high -p "$PROMPT" >"$OUT" 2>"$ERR"
      ;;
    codex-terra|codex-sol)
      m=gpt-5.6-terra; e=high
      [ "$LANE" = codex-sol ] && { m=gpt-5.6-sol; e=medium; }
      run codex exec -m "$m" -c model_reasoning_effort="$e" -s read-only \
          --skip-git-repo-check -o "$OUT" "$PROMPT" </dev/null >"$ERR" 2>&1
      ;;
    *)
      echo "unknown lane: $LANE" >&2; rm -f "$OUT" "$ERR"; continue
      ;;
  esac

  # An absent or empty output file is a lane failure, not a quiet pass. Codex
  # needs this most: its header prints the requested model and effort on a run
  # that produced nothing at all.
  if [ -s "$OUT" ]; then
    record "$LANE" "$MODEL" "$USAGE" ok
    # Drop a SessionStart marker glyph so a caller can anchor on VERDICT:.
    sed '1s/^[^[:alnum:]]*//' "$OUT"
    rm -f "$OUT" "$ERR"
    exit 0
  fi

  printf '\033[33m%s (%s) produced no output — trying the next lane\033[0m\n' \
    "$LANE" "$MODEL" >&2
  tail -2 "$ERR" >&2
  record "$LANE" "$MODEL" '{}' failed
  rm -f "$OUT" "$ERR"
done

printf '\033[31mLANE FAILURE\033[0m every lane allowed for %s failed.\n' "$TASK" >&2
exit 1

#!/usr/bin/env bash
# Run a compatibility task lane and record available usage; identity needs a separate receipt.
#
#   lane_run.sh completeness "$(cat prompt.txt)"
#   lane_run.sh referral "Which of A or B, and what is the loser better at?"
#   DEFER_HARD=1 lane_run.sh implementation "..."   # reach the frontier astra tiers
#   DEFER_HAS_PLAN=1 lane_run.sh implementation "..."  # a spec or plan already exists
#
# This wrapper uses the calibrated compatibility registry, not runtime model
# preferences. It checks for non-empty output, but does not wire-verify the serving
# model. Callers must apply current authorization before dispatch and the receipt
# checks in references/wire-verify.md before claiming model identity or independence.
#
# Every command it runs comes from lane_registry.py, through lane_pick.py's
# `argv`/`env`. Nothing here names a model or an effort. That is deliberate: the
# case statement this replaced carried its own copy of five models and drifted
# from the registry the first time a lane moved, and the drift was silent.
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

PICK_FLAGS=()
[ -n "${DEFER_HARD:-}" ] && PICK_FLAGS+=(--hard)
[ -n "${DEFER_HAS_PLAN:-}" ] && PICK_FLAGS+=(--has-plan)
[ -n "${DEFER_SHAPE:-}" ] && PICK_FLAGS+=(--shape "$DEFER_SHAPE")

ROUTE=$(python3 "$HERE/lane_pick.py" --task "$TASK" --json "${PICK_FLAGS[@]}") || exit 1
CHOSEN=$(printf '%s' "$ROUTE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["lane"])')
# --hard escalates the class, so the fallback order is the class actually routed.
TASK_ROUTED=$(printf '%s' "$ROUTE" | python3 -c 'import json,sys; print(json.load(sys.stdin)["task"])')
ORDER=$(python3 - "$CHOSEN" "$TASK_ROUTED" "${DEFER_HARD:-}" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import allowed_lanes
chosen, task, hard = sys.argv[1], sys.argv[2], bool(sys.argv[3])
allow = allowed_lanes(task, hard=hard)
print(" ".join([chosen] + [l for l in allow if l != chosen]))
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

  # argv and env come from the registry, with the real prompt and outfile
  # substituted. NUL-delimited so a prompt containing newlines survives.
  # Read NUL-delimited with a portable loop rather than `mapfile -d`, which
  # needs bash 4 and macOS still ships 3.2 at /bin/bash.
  ARGV=(); while IFS= read -r -d '' a; do ARGV+=("$a"); done < <(python3 - "$LANE" "$PROMPT" "$OUT" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
import lane_pick
lane, prompt, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
for a in lane_pick.argv_for(lane, prompt, outfile):
    sys.stdout.write(a + "\0")
PY
)
  ENVV=(); while IFS= read -r -d '' a; do ENVV+=("$a"); done < <(python3 - "$LANE" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import LANES
for k, v in (LANES[sys.argv[1]].get("env") or {}).items():
    sys.stdout.write(f"{k}={v}\0")
PY
)

  # codex writes its answer to the -o file and its log to stdout; every other
  # lane answers on stdout. The registry says which by carrying {OUTFILE}.
  # `env VAR=x run ...` cannot work: `run` is a shell function, not a binary.
  # Export into a subshell instead, so the variables die with the call — which
  # matters here, because one of them is a credential-bearing proxy binding.
  if printf '%s\n' "${ARGV[@]}" | grep -qx -- "$OUT"; then
    ( for kv in ${ENVV[@]+"${ENVV[@]}"}; do export "$kv"; done
      run "${ARGV[@]}" </dev/null >"$ERR" 2>&1 )
  else
    ( for kv in ${ENVV[@]+"${ENVV[@]}"}; do export "$kv"; done
      run "${ARGV[@]}" >"$OUT" 2>"$ERR" )
  fi

  # The one lane-specific step left: agy answers in a JSON envelope, and the
  # `usage` object inside it is the ONLY token count this lane produces
  # anywhere. Unwrap the body, keep the count.
  if [ "$LANE" = gemini ]; then
    USAGE=$(python3 -c 'import json,sys
try: print(json.dumps(json.load(open(sys.argv[1])).get("usage") or {}))
except Exception: print("{}")' "$OUT")
    python3 -c 'import json,sys
try: sys.stdout.write(json.load(open(sys.argv[1])).get("response",""))
except Exception: sys.stdout.write(open(sys.argv[1]).read())' "$OUT" >"$OUT.body" \
      && mv "$OUT.body" "$OUT"
  fi

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

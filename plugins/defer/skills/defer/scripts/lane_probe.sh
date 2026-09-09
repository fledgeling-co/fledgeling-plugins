#!/usr/bin/env bash
# Probe every lane cheaply and say which are live.
#
# A lane is available when a probe says so, not when you remember it working.
# Each probe asks for one fixed string, so a wrong-model answer is visible and a
# lane that returns nothing is reported down rather than assumed fine.
#
#   lane_probe.sh                    # every lane in the registry
#   lane_probe.sh glm grok           # just these
#   lane_probe.sh --frontier         # include the reserved astra tiers
#
# Every command comes from lane_registry.py. Nothing here names a model, so a
# lane that moves is probed at its new setting without anyone remembering to
# edit this file — which is what the hardcoded case statement got wrong.
set -uo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
export DEFER_SCRIPTS="$HERE"
TIMEOUT="${LANE_PROBE_TIMEOUT:-180}"
PROMPT='Reply with exactly: LANE OK'

FRONTIER=0
ARGS=()
for a in "$@"; do
  case "$a" in
    --frontier) FRONTIER=1 ;;
    *) ARGS+=("$a") ;;
  esac
done

if [ ${#ARGS[@]} -eq 0 ]; then
  LANES=()
  while IFS= read -r l; do LANES+=("$l"); done < <(python3 - "$FRONTIER" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import LANES, is_frontier
want_frontier = sys.argv[1] == "1"
for lane in LANES:
    if want_frontier or not is_frontier(lane):
        print(lane)
PY
)
else
  LANES=("${ARGS[@]}")
fi

run() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@" 2>&1; }
# Strip a SessionStart marker glyph; a claude -p one-shot inherits session hooks.
ok()  { printf '  %-19s \033[32mup\033[0m    %s\n' "$1" "$(echo "$2" | tr -d '\000-\037' | sed 's/^[^A-Za-z]*//' | head -c 60)"; }
down(){ printf '  %-19s \033[31mDOWN\033[0m  %s\n' "$1" "$(echo "$2" | tail -1 | head -c 100)"; }

for lane in "${LANES[@]}"; do
  f=$(mktemp /tmp/lane-probe.XXXXXX.md); rm -f "$f"
  ARGV=(); while IFS= read -r -d '' a; do ARGV+=("$a"); done < <(python3 - "$lane" "$PROMPT" "$f" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
import lane_pick
from lane_registry import LANES
lane, prompt, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
if lane not in LANES:
    sys.exit(3)
for a in lane_pick.argv_for(lane, prompt, outfile):
    sys.stdout.write(a + "\0")
PY
)
  if [ ${#ARGV[@]} -eq 0 ]; then down "$lane" "unknown lane"; continue; fi
  ENVV=(); while IFS= read -r -d '' a; do ENVV+=("$a"); done < <(python3 - "$lane" <<'PY'
import sys, os
sys.path.insert(0, os.environ["DEFER_SCRIPTS"])
from lane_registry import LANES
for k, v in (LANES[sys.argv[1]].get("env") or {}).items():
    sys.stdout.write(f"{k}={v}\0")
PY
)

  # A lane whose argv carries the outfile writes its answer there and its log to
  # stdout. The header prints correctly on a codex run that produced nothing, so
  # the file is the evidence, not the flags that were accepted.
  # `env VAR=x run ...` cannot work: `run` is a shell function, not a binary.
  # Export into a subshell instead, so the variables die with the probe.
  if printf '%s\n' "${ARGV[@]}" | grep -qx -- "$f"; then
    log=$( ( for kv in ${ENVV[@]+"${ENVV[@]}"}; do export "$kv"; done
             run "${ARGV[@]}" </dev/null ) )
    if [ -s "$f" ]; then out=$(cat "$f"); else out="empty -o file — ${log}"; fi
  else
    out=$( ( for kv in ${ENVV[@]+"${ENVV[@]}"}; do export "$kv"; done
             run "${ARGV[@]}" ) )
  fi
  rm -f "$f"

  if echo "$out" | grep -qi 'LANE OK'; then ok "$lane" "$out"; else down "$lane" "$out"; fi
done

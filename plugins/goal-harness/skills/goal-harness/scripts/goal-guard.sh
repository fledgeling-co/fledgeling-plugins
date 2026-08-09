#!/usr/bin/env bash
# goal-harness Stop hook.
#
# Runs after every turn. Reads .claude/goal-state.json; if this session armed a
# goal, runs its verification gates and either lets the turn end or blocks with
# a next-action brief.
#
# Contract: stdout carries ONLY the JSON decision (or nothing). Everything else
# goes to stderr, because Claude Code parses stdout as JSON and a stray echo
# breaks the hook.
#
# Deliberately does NOT honour stop_hook_active. That flag is the right early
# exit for a hook needing one continuation; a goal needs many, and obeying it
# disarms the goal on its second turn. The run is bounded by max_iterations and
# deadline in the state file instead. See references/mechanics.md.

set -uo pipefail

STATE_REL=".claude/goal-state.json"
INPUT="$(cat 2>/dev/null || true)"

log() { printf '%s\n' "goal-harness: $*" >&2; }

# --- locate the state file, walking up from cwd ------------------------------
find_state() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    [ -f "$dir/$STATE_REL" ] && { printf '%s' "$dir/$STATE_REL"; return 0; }
    dir="$(dirname "$dir")"
  done
  return 1
}
STATE="$(find_state)" || exit 0
ROOT="$(cd "$(dirname "$STATE")/.." && pwd)"

command -v jq >/dev/null 2>&1 || { log "jq not found; allowing stop"; exit 0; }
jq -e . "$STATE" >/dev/null 2>&1 || { log "state file is not valid JSON; allowing stop"; exit 0; }

# --- gates that make this hook inert -----------------------------------------
[ "$(jq -r '.armed // false' "$STATE")" = "true" ] || exit 0

STATE_SESSION="$(jq -r '.session_id // ""' "$STATE")"
HOOK_SESSION="$(printf '%s' "$INPUT" | jq -r '.session_id // ""' 2>/dev/null || true)"
if [ -n "$STATE_SESSION" ] && [ -n "$HOOK_SESSION" ] && [ "$STATE_SESSION" != "$HOOK_SESSION" ]; then
  exit 0   # another session in this project — not ours
fi

SLUG="$(jq -r '.slug // "goal"' "$STATE")"
GOAL_FILE="$(jq -r '.goal_file // ""' "$STATE")"
LEDGER="$(jq -r '.ledger // ""' "$STATE")"
ITER="$(jq -r '.iteration // 0' "$STATE")"
MAXITER="$(jq -r '.max_iterations // 0' "$STATE")"
DEADLINE="$(jq -r '.deadline // ""' "$STATE")"
[ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

now_iso() { date -u +%Y-%m-%dT%H:%M:%SZ; }
epoch_of() {
  # ISO-8601 -> epoch. A trailing Z means UTC and must be parsed as UTC: BSD
  # `date -j -f` interprets its input as LOCAL time, so dropping the Z silently
  # shifted a UTC deadline by the local offset and fired it early (10h on AEST).
  local raw="$1" s utc=0
  case "$raw" in *Z) utc=1 ;; esac
  s="${raw%Z}"; s="${s/T/ }"
  if [ "$utc" -eq 1 ]; then
    date -u -j -f "%Y-%m-%d %H:%M:%S" "$s" +%s 2>/dev/null || date -u -d "$raw" +%s 2>/dev/null || true
  else
    date -j -f "%Y-%m-%d %H:%M:%S" "$s" +%s 2>/dev/null || date -d "$s" +%s 2>/dev/null || true
  fi
}

ledger_row() {  # turn | at | verdict | failing | note
  mkdir -p "$(dirname "$LEDGER")" 2>/dev/null || true
  if [ ! -f "$LEDGER" ]; then
    { echo "# Goal ledger — $SLUG"; echo; echo "| turn | at | verdict | failing | note |"; echo "|---|---|---|---|---|"; } >"$LEDGER"
  fi
  printf '| %s | %s | %s | %s | %s |\n' "$1" "$(date -u +%H:%M:%S)" "$2" "${3:-—}" "${4:-}" >>"$LEDGER"
}

disarm() {  # reason
  local tmp; tmp="$(mktemp)"
  jq --arg r "$1" --arg t "$(now_iso)" \
     '.armed=false | .ended_at=$t | .end_reason=$r' "$STATE" >"$tmp" && mv "$tmp" "$STATE"
}

# --- bounds ------------------------------------------------------------------
NEXT=$((ITER + 1))

if [ "$MAXITER" -gt 0 ] && [ "$NEXT" -gt "$MAXITER" ]; then
  ledger_row "$NEXT" "stop" "—" "iteration bound $MAXITER reached"
  disarm "max_iterations"
  log "iteration bound ($MAXITER) reached — goal disarmed, allowing stop"
  exit 0
fi

if [ -n "$DEADLINE" ]; then
  DL="$(epoch_of "$DEADLINE")"
  if [ -n "$DL" ] && [ "$(date -u +%s)" -ge "$DL" ]; then
    ledger_row "$NEXT" "stop" "—" "deadline $DEADLINE reached"
    disarm "deadline"
    log "deadline reached — goal disarmed, allowing stop"
    exit 0
  fi
fi

# --- run the gates -----------------------------------------------------------
FAILED_NAMES=""
FAILED_DETAIL=""
GATE_COUNT="$(jq -r '.verify | length' "$STATE" 2>/dev/null || echo 0)"

i=0
while [ "$i" -lt "$GATE_COUNT" ]; do
  NAME="$(jq -r ".verify[$i].name // \"gate$i\"" "$STATE")"
  CMD="$(jq -r ".verify[$i].cmd // \"\"" "$STATE")"
  TMO="$(jq -r ".verify[$i].timeout // 300" "$STATE")"
  i=$((i + 1))
  [ -n "$CMD" ] || continue

  OUT="$(cd "$ROOT" && { if command -v timeout >/dev/null 2>&1; then timeout "$TMO" bash -lc "$CMD"; else bash -lc "$CMD"; fi; } 2>&1)"
  RC=$?
  if [ "$RC" -ne 0 ]; then
    FAILED_NAMES="${FAILED_NAMES:+$FAILED_NAMES, }$NAME"
    TAIL="$(printf '%s' "$OUT" | tail -n 25)"
    FAILED_DETAIL="${FAILED_DETAIL}
### gate \`$NAME\` failed (exit $RC)
\`\`\`
$TAIL
\`\`\`
"
  fi
done

# --- all gates green: the goal is met ----------------------------------------
if [ -z "$FAILED_NAMES" ]; then
  ledger_row "$NEXT" "pass" "—" "all gates green; goal met, disarmed"
  disarm "met"
  log "all gates passed — goal met, disarmed"
  exit 0
fi

# --- block, with a next-action brief -----------------------------------------
ledger_row "$NEXT" "block" "$FAILED_NAMES" "iteration $NEXT/${MAXITER:-∞}"

tmp="$(mktemp)"
jq --argjson n "$NEXT" '.iteration=$n' "$STATE" >"$tmp" && mv "$tmp" "$STATE"

REMAIN="unbounded"
[ "$MAXITER" -gt 0 ] && REMAIN="$((MAXITER - NEXT)) turns left of $MAXITER"

REASON="The goal \`$SLUG\` is not met: $FAILED_NAMES did not pass.

Continue working toward it now. Do not stop to ask the user — follow the
blocked-item policy in the brief instead.
$FAILED_DETAIL
Next: re-read \`$GOAL_FILE\` (worklist, gates, blocked-item policy, resources),
fix the failing gate above, and echo the GOAL-PROGRESS line before you finish
this turn.

Iteration $NEXT${MAXITER:+/$MAXITER} · $REMAIN${DEADLINE:+ · deadline $DEADLINE}
Ledger: $LEDGER"

jq -n --arg r "$REASON" '{decision:"block", reason:$r}'
exit 0

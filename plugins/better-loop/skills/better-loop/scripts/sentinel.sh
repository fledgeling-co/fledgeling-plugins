#!/usr/bin/env bash
# better-loop sentinel — the part of the loop that outlives the session.
#
# Registered by arm.sh as a SessionStart hook. The loop itself is a Monitor, and
# a Monitor dies with the session that started it: when the session goes, the
# watcher goes with it, the state file keeps saying `armed: true`, and nothing
# tells anybody. A sibling harness left two runs in exactly that state for six
# and fourteen days.
#
# This runs at the start of every session in the repo and reports the loops whose
# heartbeat has stopped. It says each dead loop once and says nothing when every
# loop is either polling or deliberately ended, because SessionStart output is
# injected into context and paid for.
#
# Contract: stdout is one JSON object with hookSpecificOutput.additionalContext,
# or nothing. Always exits 0: a session must never fail to start because of this.

set -uo pipefail
cat >/dev/null 2>&1 || true
command -v jq >/dev/null 2>&1 || exit 0

find_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    [ -d "$dir/.claude/loops" ] && { printf '%s' "$dir"; return 0; }
    dir="$(dirname "$dir")"
  done
  return 1
}
ROOT="$(find_root)" || exit 0

NOW="$(date +%s)"
mtime_of() { [ -f "$1" ] && { stat -f %m "$1" 2>/dev/null || stat -c %Y "$1" 2>/dev/null; } || echo 0; }
state_set() { local f="$1"; shift; local tmp; tmp="$(mktemp)"
  jq "$@" "$f" >"$tmp" 2>/dev/null && mv "$tmp" "$f" || rm -f "$tmp"; }

LINES=""
shopt -s nullglob 2>/dev/null || true
for STATE in "$ROOT"/.claude/loops/*.json; do
  jq -e 'type == "object" and has("slug")' "$STATE" >/dev/null 2>&1 || continue
  [ "$(jq -r '.armed // false' "$STATE")" = "true" ] || continue
  [ "$(jq -r '.reported_dead // false' "$STATE")" = "true" ] && continue

  SLUG="$(jq -r '.slug' "$STATE")"
  IV="$(jq -r '.interval // 120' "$STATE")"
  case "$IV" in ''|*[!0-9]*) IV=120 ;; esac
  POLLS="$(jq -r '.polls // 0' "$STATE")"
  PROBE="$(jq -r '.probe // "?"' "$STATE")"

  # The heartbeat is the epoch the watcher stamps on every poll. Reading the
  # file's mtime instead was wrong: this script's own "reported" flag rewrites
  # the file, which made the next reader see a dead loop as freshly polled.
  HB="$(jq -r '.last_poll_at // empty' "$STATE")"
  case "$HB" in ''|*[!0-9]*) HB="$(mtime_of "$STATE")" ;; esac
  DEADLINE=$(( IV * 3 )); [ "$DEADLINE" -lt 120 ] && DEADLINE=120
  AGE=$(( NOW - HB ))
  [ "$AGE" -ge "$DEADLINE" ] || continue

  LINES="${LINES}- \`$SLUG\` says it is watching, but its last poll was $(( AGE / 60 ))m ago and it polls every ${IV}s. Its Monitor died with the session that started it, so nothing is being watched. Restart it from here or end it with \`disarm.sh $SLUG\`. Probe: \`$PROBE\` (polls so far: $POLLS)
"
  state_set "$STATE" '.reported_dead=true'
done

[ -n "$LINES" ] || exit 0

BODY="better-loop: loops in this repo that stopped without saying so.

$LINES
Say this to the user rather than restarting anything unprompted — a loop they finished with is not a fault."

jq -n --arg c "$BODY" '{hookSpecificOutput:{hookEventName:"SessionStart", additionalContext:$c}}'
exit 0

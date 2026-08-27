#!/usr/bin/env bash
# better-goal status — answer "is it still going / is it finished?" from the
# ledger rather than from the transcript. Read-only, safe to run mid-run.
#
#   status.sh          every run armed in this repo
#   status.sh <slug>   one run, with more ledger rows
set -uo pipefail
WANT="${1:-}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
command -v jq >/dev/null 2>&1 || { echo "jq required"; exit 2; }

shopt -s nullglob 2>/dev/null || true
STATES=( "$ROOT"/.claude/goals/*.json )
[ -f "$ROOT/.claude/goal-state.json" ] && STATES+=( "$ROOT/.claude/goal-state.json" )
[ "${#STATES[@]}" -gt 0 ] || { echo "no runs armed in $ROOT"; exit 0; }

ROWS=10; [ -n "$WANT" ] && ROWS=25

for STATE in "${STATES[@]}"; do
  SLUG="$(jq -r '.slug // "?"' "$STATE")"
  [ -n "$WANT" ] && [ "$SLUG" != "$WANT" ] && continue

  ARMED="$(jq -r '.armed' "$STATE")"
  ITER="$(jq -r '.iteration // 0' "$STATE")"; MAX="$(jq -r '.max_iterations // 0' "$STATE")"
  LEDGER="$(jq -r '.ledger // ""' "$STATE")"
  [ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER";; esac

  if [ "$ARMED" = "true" ]; then
    LIVE="$(jq -r '.hook_live // "unknown"' "$STATE")"
    if [ "$LIVE" = "proven" ]; then
      echo "goal: $SLUG — ARMED (guard proven live at $(jq -r '.hook_proven_at // "?"' "$STATE"))"
    else
      echo "goal: $SLUG — ARMED, BUT THE GUARD HAS NEVER FIRED (hook_live=$LIVE)"
      echo "      A hook registered mid-session only loads if .claude/ already held a settings"
      echo "      file when that session started. Open /hooks once, or restart, or re-arm from"
      echo "      a session that started after the file existed. Nothing is verifying anything."
    fi
    SID="$(jq -r '.session_id // ""' "$STATE")"
    if [ -n "$SID" ]; then
      CFG="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
      NEWEST=0
      shopt -s nullglob 2>/dev/null || true
      for t in "$CFG"/projects/*/"$SID".jsonl; do
        M="$(stat -f %m "$t" 2>/dev/null || stat -c %Y "$t" 2>/dev/null || echo 0)"
        [ "$M" -gt "$NEWEST" ] && NEWEST="$M"
      done
      if [ "$NEWEST" -gt 0 ]; then
        echo "session: $SID last wrote $(( ( $(date +%s) - NEWEST ) / 60 ))m ago"
      else
        echo "session: $SID — no transcript found; the owning session is gone"
      fi
    fi
  else
    STUCK="$(jq -r '.stuck_on // ""' "$STATE")"
    echo "goal: $SLUG — ended ($(jq -r '.end_reason // "unknown"' "$STATE")${STUCK:+ on $STUCK}) at $(jq -r '.ended_at // "?"' "$STATE")"
  fi
  echo "turn: $ITER${MAX:+/$MAX}   started: $(jq -r '.started_at // "?"' "$STATE")   deadline: $(jq -r '.deadline // "none"' "$STATE")"
  echo "brief: $(jq -r '.goal_file // "?"' "$STATE")"
  echo "gates: $(jq -r '[.verify[]?.name] | join(", ")' "$STATE")"
  RC="$(jq -r '.repeat_count // 0' "$STATE")"
  [ "$RC" -gt 1 ] 2>/dev/null && echo "repeat: the same failure has held for $RC turns (stuck limit $(jq -r '.stuck_after // 3' "$STATE"))"
  SR="$(jq -r '.set_repeat_count // 0' "$STATE")"
  [ "$SR" -gt 3 ] 2>/dev/null && echo "same set: [$(jq -r '.last_failing_set // "?"' "$STATE")] red for $SR consecutive turns"
  SF="$(jq -r '.stop_failures // 0' "$STATE")"
  [ "$SF" -gt 0 ] 2>/dev/null && echo "api errors: $SF consecutive turn(s) ended on $(jq -r '.last_stop_failure // "an API error"' "$STATE") — 3 disarms the run"

  if [ -f "$LEDGER" ]; then
    # A ledger whose last row is old answers "is it still going" too: that is a
    # stalled run, not a quiet one.
    LM="$(stat -f %m "$LEDGER" 2>/dev/null || stat -c %Y "$LEDGER" 2>/dev/null || echo 0)"
    AGE=$(( ( $(date +%s) - LM ) / 60 ))
    echo "ledger: last written ${AGE}m ago — $LEDGER"
    grep '^|' "$LEDGER" | tail -n "$ROWS"
  else
    echo "ledger: nothing yet at $LEDGER — the guard has not completed a turn"
  fi
  echo
done

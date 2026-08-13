#!/usr/bin/env bash
# better-loop watcher — the loop itself. Runs under Monitor, polls a probe
# command, and wakes the session only when the answer CHANGES.
#
#   Monitor({ command: "watch.sh <slug> --probe '<cmd>' [options]",
#             description: "loop <slug>", persistent: true })
#
# Why change-gating is the whole point: every line printed here becomes a
# task-notification, and waking a session re-bills its entire accumulated
# prefix. A loop that fires on a schedule re-sends the same unmet condition and
# the same failing set turn after turn — five of the twelve heaviest sessions
# measured did exactly that, 91% of input between them. A loop that fires on a
# transition cannot.
#
# Options
#   --probe CMD        required. Its stdout is the state. Must be deterministic:
#                      a timestamp or a random ordering in the output makes every
#                      poll a change, which is the failure this exists to prevent.
#   --interval SEC     poll cadence (default 120). Local checks 30-120s; remote
#                      APIs 300s+.
#   --stop-when CMD    exit 0 means the work is finished: emit DONE and exit.
#   --tick-cmd CMD     run this detached on a change INSTEAD of waking the
#                      session. A `claude -p` here pays no session prefix at all.
#   --max-wakes N      emissions allowed per rolling hour (default 12). On
#                      exhaustion the watcher goes quiet and says so once.
#   --repeat-after SEC a state already seen is re-emitted no sooner than this,
#                      doubling each repeat, capped at 4h (default 1800).
#   --dry-stop N       exit after N consecutive unchanged polls (default 0, off).
#   --max-lines N      lines of delta to send per wake (default 20).
#
# Emits: CHANGE, DONE, ENDED, QUIET, GONE. Nothing else, ever.

set -uo pipefail

SLUG="${1:-}"; [ $# -gt 0 ] && shift
PROBE=""; STOP_WHEN=""; TICK_CMD=""
INTERVAL=120; MAX_WAKES=12; REPEAT_AFTER=1800; DRY_STOP=0; MAX_LINES=20
need() { [ "$1" -ge 2 ] || { echo "watch.sh: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --probe)        need $# --probe; PROBE="$2"; shift 2 ;;
    --interval)     need $# --interval; INTERVAL="$2"; shift 2 ;;
    --stop-when)    need $# --stop-when; STOP_WHEN="$2"; shift 2 ;;
    --tick-cmd)     need $# --tick-cmd; TICK_CMD="$2"; shift 2 ;;
    --max-wakes)    need $# --max-wakes; MAX_WAKES="$2"; shift 2 ;;
    --repeat-after) need $# --repeat-after; REPEAT_AFTER="$2"; shift 2 ;;
    --dry-stop)     need $# --dry-stop; DRY_STOP="$2"; shift 2 ;;
    --max-lines)    need $# --max-lines; MAX_LINES="$2"; shift 2 ;;
    *) shift ;;
  esac
done
[ -n "$SLUG" ] || { echo "watch.sh: usage: watch.sh <slug> --probe '<cmd>' [options]" >&2; exit 2; }
[ -n "$PROBE" ] || { echo "watch.sh: --probe is required — without it there is no state to compare" >&2; exit 2; }
case "$SLUG" in *[!a-zA-Z0-9._-]*)
  echo "watch.sh: slug '$SLUG' must be a bare kebab name — it becomes a filename" >&2; exit 2 ;;
esac

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
DIR="$ROOT/.claude/loops"; mkdir -p "$DIR"
STATE="$DIR/${SLUG}.json"
SEEN="$DIR/${SLUG}.seen"      # fingerprint <TAB> count <TAB> next_emit_epoch
PREV="$DIR/${SLUG}.prev"      # last probe output, for the delta
LEDGER="$ROOT/docs/loops/loop-${SLUG}.ledger.md"
[ -f "$STATE" ] && LEDGER="$(jq -r '.ledger // ""' "$STATE" 2>/dev/null || true)" && \
  { [ -n "$LEDGER" ] || LEDGER="$ROOT/docs/loops/loop-${SLUG}.ledger.md"; }
case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

hash_of() { { command -v shasum >/dev/null 2>&1 && shasum -a 256 || sha256sum; } 2>/dev/null | cut -c1-16; }

# --- wake budget -------------------------------------------------------------
# A rolling hour of emission timestamps. The budget is a floor under the cost of
# a badly-behaved probe: if one starts changing every poll, the loop still cannot
# wake the session more than N times an hour.
WAKES=""
budget_ok() {
  local now="$1" keep=""
  for t in $WAKES; do [ $((now - t)) -lt 3600 ] && keep="$keep $t"; done
  WAKES="$keep"
  [ "$(printf '%s\n' $WAKES | grep -c .)" -lt "$MAX_WAKES" ]
}
budget_spend() { WAKES="$WAKES $1"; }

# Same table shape as tick.sh, so a loop whose ticks also write rows produces one
# readable ledger rather than two interleaved formats.
ledger_row() { # event fingerprint note
  mkdir -p "$(dirname "$LEDGER")" 2>/dev/null || true
  if [ ! -f "$LEDGER" ]; then
    { echo "# Loop ledger — $SLUG"; echo; echo "| tick | at | verdict | note |"; echo "|---|---|---|---|"; } >"$LEDGER"
  fi
  local n; n="$(grep -c '^| [0-9]' "$LEDGER" 2>/dev/null | tr -d ' \n')"; n="${n:-0}"
  printf '| %s | %s | %s | %s |\n' "$((n + 1))" "$(date '+%Y-%m-%d %H:%M')" "$1" "${3}${2:+ [$2]}" >>"$LEDGER"
}

state_set() { # jq-args...
  [ -f "$STATE" ] || printf '{"slug":"%s","armed":true}\n' "$SLUG" >"$STATE"
  local tmp; tmp="$(mktemp)"
  jq "$@" "$STATE" >"$tmp" 2>/dev/null && mv "$tmp" "$STATE" || rm -f "$tmp"
}

seen_lookup() { grep -F "$1	" "$SEEN" 2>/dev/null | head -n 1; }
seen_write() { # fp count next
  local tmp; tmp="$(mktemp)"
  grep -vF "$1	" "$SEEN" 2>/dev/null >"$tmp" || true
  printf '%s\t%s\t%s\n' "$1" "$2" "$3" >>"$tmp"
  # Keep the register bounded: a probe with high cardinality would otherwise grow
  # this file without limit over a multi-day run.
  tail -n 500 "$tmp" >"$SEEN"; rm -f "$tmp"
}

trap 'state_set --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" ".armed=false | .ended_at=\$t | .end_reason=(.end_reason // \"stopped\")"; exit 0' TERM INT

state_set --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg p "$PROBE" \
  '.armed=true | .started_at=$t | .probe=$p | .polls=0 | .wakes=0 | .quiet_since=null'

UNCHANGED=0
FIRST=1

while true; do
  NOW="$(date +%s)"

  if [ -n "$STOP_WHEN" ] && eval "$STOP_WHEN" >/dev/null 2>&1; then
    ledger_row "done" "—" "stop-when satisfied"
    state_set --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.armed=false | .ended_at=$t | .end_reason="done"'
    echo "DONE loop $SLUG: the stop condition is satisfied. Ledger: $LEDGER"
    exit 0
  fi

  OUT="$(eval "$PROBE" 2>&1)"; RC=$?
  FP="$(printf '%s' "$OUT" | hash_of)"
  state_set --arg f "$FP" --argjson r "$RC" '.polls=((.polls // 0)+1) | .last_fingerprint=$f | .last_rc=$r'

  if [ "$FIRST" -eq 1 ]; then
    # The first poll establishes the baseline. Emitting it would wake the session
    # to tell it what it just armed.
    printf '%s' "$OUT" >"$PREV"; seen_write "$FP" 1 "$((NOW + REPEAT_AFTER))"
    ledger_row "baseline" "$FP" "$(printf '%s' "$OUT" | grep -c . ) line(s)"
    FIRST=0; sleep "$INTERVAL"; continue
  fi

  PRIOR="$(seen_lookup "$FP")"
  if [ -n "$PRIOR" ]; then
    COUNT="$(printf '%s' "$PRIOR" | cut -f2)"; NEXT="$(printf '%s' "$PRIOR" | cut -f3)"
    if [ "$FP" = "$(printf '%s' "$(cat "$PREV" 2>/dev/null)" | hash_of)" ]; then
      # Unchanged since the last poll. This is the common case and it is silent.
      UNCHANGED=$((UNCHANGED + 1))
      if [ "$DRY_STOP" -gt 0 ] && [ "$UNCHANGED" -ge "$DRY_STOP" ]; then
        ledger_row "dry" "$FP" "$UNCHANGED unchanged polls"
        state_set --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.armed=false | .ended_at=$t | .end_reason="dry"'
        echo "ENDED loop $SLUG: nothing changed for $UNCHANGED consecutive polls, so the loop stopped rather than keep polling. Last state in $LEDGER"
        exit 0
      fi
      sleep "$INTERVAL"; continue
    fi
    # Changed, but back into a state already seen — a flapping build, a failure
    # that returns. Worth one wake, then progressively fewer.
    if [ "$NOW" -lt "$NEXT" ]; then
      seen_write "$FP" "$((COUNT + 1))" "$NEXT"
      printf '%s' "$OUT" >"$PREV"
      ledger_row "repeat" "$FP" "seen ×$((COUNT + 1)) — suppressed until $(date -r "$NEXT" +%H:%M 2>/dev/null || echo "$NEXT")"
      UNCHANGED=0; sleep "$INTERVAL"; continue
    fi
    BACKOFF=$((REPEAT_AFTER * (COUNT + 1))); [ "$BACKOFF" -gt 14400 ] && BACKOFF=14400
    seen_write "$FP" "$((COUNT + 1))" "$((NOW + BACKOFF))"
    NOTE="a state seen $((COUNT + 1)) times before"
  else
    seen_write "$FP" 1 "$((NOW + REPEAT_AFTER))"
    NOTE="new"
  fi

  DELTA="$(diff <(cat "$PREV" 2>/dev/null) <(printf '%s' "$OUT") 2>/dev/null \
            | grep -E '^[<>]' | head -n "$MAX_LINES")"
  [ -n "$DELTA" ] || DELTA="$(printf '%s' "$OUT" | head -n "$MAX_LINES")"
  printf '%s' "$OUT" >"$PREV"
  UNCHANGED=0

  if [ -n "$TICK_CMD" ]; then
    # Detached tick: the work happens in a fresh process with no session prefix
    # to re-bill. The session is never woken, so this is the cheap path for any
    # tick that does not need the conversation's context.
    ( eval "$TICK_CMD" >>"$DIR/${SLUG}.tick.log" 2>&1 & ) >/dev/null 2>&1
    ledger_row "tick" "$FP" "$NOTE — dispatched detached"
    state_set '.ticks=((.ticks // 0)+1)'
    sleep "$INTERVAL"; continue
  fi

  if ! budget_ok "$NOW"; then
    ledger_row "held" "$FP" "$NOTE — wake budget of $MAX_WAKES/h spent"
    if [ "$(jq -r '.quiet_since // "null"' "$STATE" 2>/dev/null)" = "null" ]; then
      state_set --arg t "$(date -u +%Y-%m-%dT%H:%M:%SZ)" '.quiet_since=$t'
      echo "QUIET loop $SLUG: the state is changing faster than the wake budget of $MAX_WAKES/hour. Further changes are being written to the ledger without waking this session. Read $LEDGER, and either widen the probe's tolerance or raise --max-wakes."
      budget_spend "$NOW"
    fi
    sleep "$INTERVAL"; continue
  fi
  state_set '.quiet_since=null'

  budget_spend "$NOW"
  state_set '.wakes=((.wakes // 0)+1)'
  ledger_row "change" "$FP" "$NOTE"
  printf 'CHANGE loop %s (%s): the watched state moved. Delta:\n%s\nProbe: %s\nLedger: %s\n' \
    "$SLUG" "$NOTE" "$DELTA" "$PROBE" "$LEDGER"

  sleep "$INTERVAL"
done

#!/usr/bin/env bash
# better-goal Stop hook.
#
# Runs after every turn. Reads every .claude/goals/*.json armed by THIS session,
# runs each one's gates, and either lets the turn end or blocks with a
# next-action brief.
#
# Contract: stdout carries ONLY the JSON decision (or nothing). Everything else
# goes to stderr, because Claude Code parses stdout as JSON and a stray echo
# breaks the hook.
#
# Deliberately does NOT honour stop_hook_active. That flag is the right early
# exit for a hook needing one continuation; a long run needs many, and obeying
# it disarms the run on its second turn. Bounded by max_iterations, deadline and
# stuck_after in the state file instead. See references/mechanics.md.

set -uo pipefail

INPUT="$(cat 2>/dev/null || true)"
log() { printf '%s\n' "better-goal: $*" >&2; }

# macOS ships neither timeout(1) nor gtimeout(1); without one, verify[].timeout
# cannot be enforced and a hung gate runs until the hook's own timeout.
TIMEOUT_BIN="$(command -v timeout || command -v gtimeout || true)"

# --- locate the goals directory, walking up from cwd -------------------------
find_root() {
  local dir="$PWD"
  while [ "$dir" != "/" ]; do
    if [ -d "$dir/.claude/goals" ] || [ -f "$dir/.claude/goal-state.json" ]; then
      printf '%s' "$dir"; return 0
    fi
    dir="$(dirname "$dir")"
  done
  return 1
}
ROOT="$(find_root)" || exit 0

command -v jq >/dev/null 2>&1 || { log "jq not found; allowing stop"; exit 0; }

# A Stop hook is automatically converted to SubagentStop for subagents, so this
# script also fires every time a subagent finishes. A goal is about the main
# session's turn: running the gate suite per subagent completion would cost a
# full test run each time and block the subagent from returning. Only Stop
# counts. An absent event name means an older payload, which only ever meant Stop.
HOOK_EVENT="$(printf '%s' "$INPUT" | jq -r '.hook_event_name // "Stop"' 2>/dev/null || echo Stop)"
[ "$HOOK_EVENT" = "Stop" ] || exit 0

HOOK_SESSION="$(printf '%s' "$INPUT" | jq -r '.session_id // ""' 2>/dev/null || true)"

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
hash_of() { { command -v shasum >/dev/null 2>&1 && shasum -a 256 || sha256sum; } 2>/dev/null | cut -c1-12; }

state_set() {  # file, jq-filter, args...
  local f="$1"; shift
  local tmp; tmp="$(mktemp)"
  jq "$@" "$f" >"$tmp" 2>/dev/null && mv "$tmp" "$f" || rm -f "$tmp"
}

# --- evaluate one armed slug --------------------------------------------------
# Emits its block brief on fd 3 when it wants the turn held open; silent otherwise.
BLOCKS=""

evaluate() {
  local STATE="$1"
  jq -e . "$STATE" >/dev/null 2>&1 || { log "$(basename "$STATE") is not valid JSON; skipping"; return 0; }
  [ "$(jq -r '.armed // false' "$STATE")" = "true" ] || return 0

  # Session isolation is what makes a project-scoped hook safe, so an absent id
  # must refuse rather than match everything: a permissive empty id means every
  # session in the project runs the gates, and two of them race on .iteration.
  local SSID; SSID="$(jq -r '.session_id // ""' "$STATE")"
  if [ -z "$SSID" ]; then
    log "$(basename "$STATE") has no session_id — refusing to act; re-arm from the driving session"
    return 0
  fi
  [ "$SSID" = "$HOOK_SESSION" ] || return 0

  local SLUG GOAL_FILE LEDGER ITER MAXITER DEADLINE STUCK_AFTER LAST_FP REPEATS ESCALATED LAST_FAILING
  SLUG="$(jq -r '.slug // "goal"' "$STATE")"
  GOAL_FILE="$(jq -r '.goal_file // ""' "$STATE")"
  LEDGER="$(jq -r '.ledger // ""' "$STATE")"
  ITER="$(jq -r '.iteration // 0' "$STATE")"
  MAXITER="$(jq -r '.max_iterations // 0' "$STATE")"
  DEADLINE="$(jq -r '.deadline // ""' "$STATE")"
  STUCK_AFTER="$(jq -r '.stuck_after // 3' "$STATE")"
  LAST_FP="$(jq -r '.last_fingerprint // ""' "$STATE")"
  REPEATS="$(jq -r '.repeat_count // 0' "$STATE")"
  ESCALATED="$(jq -r '.escalated // false' "$STATE")"
  LAST_FAILING="$(jq -r '.last_failing // ""' "$STATE")"

  # A non-numeric bound made `[ "$MAXITER" -gt 0 ]` false, which skipped the
  # check entirely and silently unbounded the run. Normalise before arithmetic.
  case "$MAXITER"     in ''|*[!0-9]*) log "max_iterations '$MAXITER' is not a number — treating as unbounded"; MAXITER=0 ;; esac
  case "$ITER"        in ''|*[!0-9]*) ITER=0 ;; esac
  case "$REPEATS"     in ''|*[!0-9]*) REPEATS=0 ;; esac
  case "$STUCK_AFTER" in ''|*[!0-9]*) STUCK_AFTER=3 ;; esac

  [ -n "$LEDGER" ] || LEDGER="docs/goals/goal-${SLUG}.ledger.md"
  case "$LEDGER" in /*) : ;; *) LEDGER="$ROOT/$LEDGER" ;; esac

  ledger_row() {  # turn | verdict | failing | note
    mkdir -p "$(dirname "$LEDGER")" 2>/dev/null || true
    if [ ! -f "$LEDGER" ]; then
      { echo "# Goal ledger — $SLUG"; echo; echo "| turn | at | verdict | failing | note |"; echo "|---|---|---|---|---|"; } >"$LEDGER"
    fi
    printf '| %s | %s | %s | %s | %s |\n' "$1" "$(date -u +%H:%M:%S)" "$2" "${3:-—}" "${4:-}" >>"$LEDGER"
  }
  disarm() { state_set "$STATE" --arg r "$1" --arg t "$(now_iso)" '.armed=false | .ended_at=$t | .end_reason=$r'; }

  local NEXT=$((ITER + 1))

  # --- bounds ---------------------------------------------------------------
  if [ "$MAXITER" -gt 0 ] && [ "$NEXT" -gt "$MAXITER" ]; then
    ledger_row "$NEXT" "stop" "—" "iteration bound $MAXITER reached"
    disarm "max_iterations"; log "$SLUG: iteration bound ($MAXITER) reached — disarmed"
    return 0
  fi
  if [ -n "$DEADLINE" ]; then
    local DL; DL="$(epoch_of "$DEADLINE")"
    if [ -n "$DL" ] && [ "$(date -u +%s)" -ge "$DL" ]; then
      ledger_row "$NEXT" "stop" "—" "deadline $DEADLINE reached"
      disarm "deadline"; log "$SLUG: deadline reached — disarmed"
      return 0
    fi
  fi

  # --- gates ----------------------------------------------------------------
  # `.verify | length` is >0 for a string or an object too, and 0 for null or
  # [], and every one of those shapes previously fell through to the all-green
  # branch and recorded the goal as met without checking anything.
  if ! jq -e '(.verify | type) == "array" and (.verify | length) > 0' "$STATE" >/dev/null 2>&1; then
    ledger_row "$NEXT" "block" "config" "verify[] is missing or not a non-empty array"
    BLOCKS="${BLOCKS}The run \`$SLUG\` has no runnable gates: \`.verify\` in $STATE must be a non-empty array of {name, cmd} objects. Nothing has been verified. Fix the state file before continuing.
"
    return 0
  fi

  local FAILED_NAMES="" FAILED_DETAIL="" GATE_COUNT i NAME CMD TMO OUT RC TAIL
  GATE_COUNT="$(jq -r '.verify | length' "$STATE" 2>/dev/null || echo 0)"
  i=0
  while [ "$i" -lt "$GATE_COUNT" ]; do
    NAME="$(jq -r ".verify[$i].name // \"gate$i\"" "$STATE")"
    CMD="$(jq -r ".verify[$i].cmd // \"\"" "$STATE")"
    TMO="$(jq -r ".verify[$i].timeout // 300" "$STATE")"
    i=$((i + 1))
    [ -n "$CMD" ] || continue
    OUT="$(cd "$ROOT" && { if [ -n "$TIMEOUT_BIN" ]; then "$TIMEOUT_BIN" "$TMO" bash -lc "$CMD"; else bash -lc "$CMD"; fi; } 2>&1)"
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

  # --- all green: the run is finished ---------------------------------------
  if [ -z "$FAILED_NAMES" ]; then
    ledger_row "$NEXT" "pass" "—" "all gates green; finished, disarmed"
    disarm "met"; log "$SLUG: all gates passed — disarmed"
    return 0
  fi

  # --- repeat detection -----------------------------------------------------
  # A gate failing identically turn after turn is not slow progress; it is a run
  # that has already learned what this turn can teach it. Re-sending the same
  # failing output re-bills the whole session prefix and produces the same turn.
  local FP; FP="$(printf '%s\n%s' "$FAILED_NAMES" "$FAILED_DETAIL" | hash_of)"
  if [ "$FP" = "$LAST_FP" ]; then REPEATS=$((REPEATS + 1)); else REPEATS=1; ESCALATED=false; fi

  if [ "$REPEATS" -gt "$STUCK_AFTER" ] && [ "$ESCALATED" = "true" ]; then
    ledger_row "$NEXT" "stop" "$FAILED_NAMES" "identical failure ×$REPEATS after escalation — stuck, disarmed"
    disarm "stuck"
    state_set "$STATE" --arg f "$FAILED_NAMES" '.stuck_on=$f'
    log "$SLUG: identical failure ×$REPEATS — disarmed as stuck"
    return 0
  fi

  # --- block, with a next-action brief --------------------------------------
  local BOUND=""; [ "$MAXITER" -gt 0 ] && BOUND="/$MAXITER"
  local REMAIN="unbounded"; [ "$MAXITER" -gt 0 ] && REMAIN="$((MAXITER - NEXT)) turns left of $MAXITER"

  local DELTA=""
  if [ -n "$LAST_FAILING" ] && [ "$LAST_FAILING" != "$FAILED_NAMES" ]; then
    DELTA="Since the last turn the failing set moved: was [$LAST_FAILING], now [$FAILED_NAMES]."
  fi

  local BODY
  if [ "$REPEATS" -ge "$STUCK_AFTER" ]; then
    # Escalation: withhold the output entirely. It is byte-identical to the last
    # $REPEATS turns and re-sending it is the cost this branch exists to stop.
    ESCALATED=true
    BODY="Gate(s) [$FAILED_NAMES] have now failed identically $REPEATS turns running — same
output, same exit code. The output is withheld here because it has not changed;
read it once with the gate command itself if you need it.

Repeating the same fix will produce the same turn. Do one of these instead:
  1. Change approach — a different cause, a different layer, a different tool.
  2. Park the item: mark it parked in the worklist with the reason, write the
     question and your recommendation to \`## Open questions\` in the brief, and
     carry on with every item that does not depend on it.
  3. Fix the gate, if the gate itself is wrong rather than the code.

If none of those apply, say so plainly and stop — the run will disarm itself as
stuck on the next identical turn rather than grinding."
  else
    BODY="Continue working toward it now. Do not stop to ask the user — follow the
blocked-item policy in the brief instead.
${DELTA:+
$DELTA
}$FAILED_DETAIL
Next: re-read \`$GOAL_FILE\` (worklist, gates, blocked-item policy, resources),
fix the failing gate above, and record what you changed."
  fi

  ledger_row "$NEXT" "block" "$FAILED_NAMES" "iteration $NEXT${BOUND:-/∞}${REPEATS:+ · repeat ×$REPEATS}"
  state_set "$STATE" --argjson n "$NEXT" --arg fp "$FP" --argjson r "$REPEATS" \
                     --argjson e "$ESCALATED" --arg lf "$FAILED_NAMES" \
    '.iteration=$n | .last_fingerprint=$fp | .repeat_count=$r | .escalated=$e | .last_failing=$lf'

  BLOCKS="${BLOCKS}The run \`$SLUG\` is not finished: $FAILED_NAMES did not pass.

$BODY

Iteration $NEXT$BOUND · $REMAIN${DEADLINE:+ · deadline $DEADLINE}
Ledger: $LEDGER

"
}

# --- every slug this session armed -------------------------------------------
shopt -s nullglob 2>/dev/null || true
for f in "$ROOT"/.claude/goals/*.json; do evaluate "$f"; done
# Back-compat with the single-file layout written by goal-harness ≤1.1.0.
[ -f "$ROOT/.claude/goal-state.json" ] && evaluate "$ROOT/.claude/goal-state.json"

[ -n "$BLOCKS" ] || exit 0
jq -n --arg r "$BLOCKS" '{decision:"block", reason:$r}'
exit 0

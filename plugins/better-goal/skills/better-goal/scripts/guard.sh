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
# full test run each time and block the subagent from returning. Only Stop runs
# gates. An absent event name means an older payload, which only ever meant Stop.
#
# StopFailure and SessionEnd are the two events that used to leave a run armed
# and silent forever. StopFailure "fires INSTEAD of Stop when an API error
# (rate limit, auth failure, etc.) ended the turn" — so the run that dies on an
# API error never reaches the guard at all, which is why one run sat at
# `armed: true` on turn 17 for fourteen days. SessionEnd covers the clean exit.
# Neither can instruct the run (StopFailure's output and exit code are ignored),
# so they record rather than block.
HOOK_EVENT="$(printf '%s' "$INPUT" | jq -r '.hook_event_name // "Stop"' 2>/dev/null || echo Stop)"
case "$HOOK_EVENT" in
  Stop|StopFailure|SessionEnd) : ;;
  *) exit 0 ;;
esac

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
  local LAST_SET SET_REPEATS SET_NOTICE
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
  LAST_SET="$(jq -r '.last_failing_set // ""' "$STATE")"
  SET_REPEATS="$(jq -r '.set_repeat_count // 0' "$STATE")"
  SET_NOTICE="$(jq -r '.set_notice_after // 10' "$STATE")"

  # A non-numeric bound made `[ "$MAXITER" -gt 0 ]` false, which skipped the
  # check entirely and silently unbounded the run. Normalise before arithmetic.
  case "$MAXITER"     in ''|*[!0-9]*) log "max_iterations '$MAXITER' is not a number — treating as unbounded"; MAXITER=0 ;; esac
  case "$ITER"        in ''|*[!0-9]*) ITER=0 ;; esac
  case "$REPEATS"     in ''|*[!0-9]*) REPEATS=0 ;; esac
  case "$STUCK_AFTER" in ''|*[!0-9]*) STUCK_AFTER=3 ;; esac
  case "$SET_REPEATS"  in ''|*[!0-9]*) SET_REPEATS=0 ;; esac
  case "$SET_NOTICE"   in ''|*[!0-9]*) SET_NOTICE=10 ;; esac

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

  # --- the two events that only record ---------------------------------------
  if [ "$HOOK_EVENT" = "StopFailure" ]; then
    # The turn ended on an API error. Gates say nothing useful about a turn that
    # never ran, so record the error and count it. Three consecutive API-error
    # turn ends is a run that is not coming back on its own, and leaving it armed
    # is what made a dead run indistinguishable from a quiet one.
    local ERR FAILS
    ERR="$(printf '%s' "$INPUT" | jq -r '.error // .error_type // "unknown"' 2>/dev/null || echo unknown)"
    FAILS="$(jq -r '.stop_failures // 0' "$STATE")"
    case "$FAILS" in ''|*[!0-9]*) FAILS=0 ;; esac
    FAILS=$((FAILS + 1))
    state_set "$STATE" --argjson n "$FAILS" --arg e "$ERR" --arg t "$(now_iso)" \
      '.stop_failures=$n | .last_stop_failure=$e | .last_stop_failure_at=$t'
    ledger_row "$ITER" "api-error" "—" "turn ended on an API error ($ERR) ×$FAILS; no gates run, iteration not advanced"
    if [ "$FAILS" -ge 3 ]; then
      disarm "api_error"
      state_set "$STATE" --arg e "$ERR" '.stuck_on=("API error: " + $e)'
      log "$SLUG: three consecutive API-error turn ends — disarmed"
    fi
    return 0
  fi
  if [ "$HOOK_EVENT" = "SessionEnd" ]; then
    # The session that armed this run is going away, and the guard matches on
    # session id, so the run can never advance again. Record it as ended rather
    # than leaving `armed: true` for a fortnight. Re-arming from a resumed
    # session rewrites session_id and sets armed back to true.
    local WHY; WHY="$(printf '%s' "$INPUT" | jq -r '.reason // "unknown"' 2>/dev/null || echo unknown)"
    ledger_row "$ITER" "stop" "—" "session $SSID ended ($WHY) while armed; nothing can advance this run now"
    disarm "session_ended"
    log "$SLUG: owning session ended — disarmed"
    return 0
  fi

  # From here on the event is Stop, so the guard is demonstrably live. Arming
  # writes hook_live=unproven because a hook registered mid-session into a
  # .claude/ that had no settings file at session start is written correctly and
  # never loaded, and nothing can prove otherwise from inside the arming turn.
  [ "$(jq -r '.hook_live // ""' "$STATE")" = "proven" ] || \
    state_set "$STATE" --arg t "$(now_iso)" '.hook_live="proven" | .hook_proven_at=$t'
  [ "$(jq -r '.stop_failures // 0' "$STATE")" = "0" ] || state_set "$STATE" '.stop_failures=0'

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

  # The output fingerprint above resets whenever a count, a path or an elapsed
  # time moves, so a run can fail on the same gates for dozens of turns and never
  # trip it: `orderly` recorded 88 of 137 turns at repeat ×1 while `queue,
  # hygiene` was red on 73 of them, and ran to its iteration bound. The failing
  # SET is the coarser signal that catches that.
  #
  # It only ever notices. Measured across 24 ledgers, 29 streaks of an identical
  # failing set ran 8 turns or longer and then cleared — the longest was 57 turns
  # of `ledger-drained, orchestrator-drained, worktrees-clean` on a backlog being
  # worked through item by item. A long streak is normal here, so disarming on one
  # would kill healthy runs; naming it lets the run answer for itself.
  if [ "$FAILED_NAMES" = "$LAST_SET" ]; then SET_REPEATS=$((SET_REPEATS + 1)); else SET_REPEATS=1; fi

  if [ "$REPEATS" -gt "$STUCK_AFTER" ] && [ "$ESCALATED" = "true" ]; then
    ledger_row "$NEXT" "stop" "$FAILED_NAMES" "identical failure ×$REPEATS after escalation, stuck, disarmed"
    disarm "stuck"
    state_set "$STATE" --arg f "$FAILED_NAMES" '.stuck_on=$f'
    log "$SLUG: identical failure ×$REPEATS, disarmed as stuck"
    return 0
  fi

  # --- block, with a next-action brief --------------------------------------
  local BOUND=""; [ "$MAXITER" -gt 0 ] && BOUND="/$MAXITER"
  local REMAIN="unbounded"; [ "$MAXITER" -gt 0 ] && REMAIN="$((MAXITER - NEXT)) turns left of $MAXITER"

  local DELTA=""
  if [ -n "$LAST_FAILING" ] && [ "$LAST_FAILING" != "$FAILED_NAMES" ]; then
    DELTA="Since the last turn the failing set moved: was [$LAST_FAILING], now [$FAILED_NAMES]."
  elif [ "$SET_REPEATS" -ge "$SET_NOTICE" ]; then
    DELTA="[$FAILED_NAMES] have now been red for $SET_REPEATS consecutive turns. If this is a
queue being drained, say in one line what moved this turn. If nothing is moving,
this is the turn to change approach or park the item rather than repeat it."
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

  local SETNOTE=""; [ "$SET_REPEATS" -ge "$SET_NOTICE" ] && SETNOTE=" · same set ×$SET_REPEATS"
  ledger_row "$NEXT" "block" "$FAILED_NAMES" "iteration $NEXT${BOUND:-/∞}${REPEATS:+ · repeat ×$REPEATS}$SETNOTE"
  state_set "$STATE" --argjson n "$NEXT" --arg fp "$FP" --argjson r "$REPEATS" \
                     --argjson e "$ESCALATED" --arg lf "$FAILED_NAMES" --argjson sr "$SET_REPEATS" \
    '.iteration=$n | .last_fingerprint=$fp | .repeat_count=$r | .escalated=$e | .last_failing=$lf
     | .last_failing_set=$lf | .set_repeat_count=$sr'

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

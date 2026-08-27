#!/usr/bin/env bash
# better-goal preflight — the conditions that end a run without an error.
# Read-only. Prints a table and exits 1 if anything would block an armed run.
#
# Usage: preflight.sh [--skills "/ship-fleet:ship-fleet,/design-review:design-review"]
#                     [--ports 3000,8081] [--procs metro,expo]

set -uo pipefail
SKILLS=""; PORTS=""; PROCS=""
# `shift 2` fails with $# unchanged when a flag is passed as the last argument,
# so the same branch re-matches and the loop spins forever. Fail loudly instead.
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --skills) need $# --skills; SKILLS="${2:-}"; shift 2 ;;
    --ports)  need $# --ports; PORTS="${2:-}";  shift 2 ;;
    --procs)  need $# --procs; PROCS="${2:-}";  shift 2 ;;
    *) shift ;;
  esac
done

FAIL=0
row() { printf '%-28s %-6s %s\n' "$1" "$2" "$3"; }
bad() { FAIL=1; row "$1" "BLOCK" "$2"; }
warn(){ row "$1" "warn" "$2"; }
ok()  { row "$1" "ok" "$2"; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
settings_files=( "$HOME/.claude/settings.json" "$ROOT/.claude/settings.json" "$ROOT/.claude/settings.local.json" )
setting() { # key -> first value found, searching local → project → user
  # `// empty` was wrong here: jq's alternative operator treats BOTH null and
  # false as needing the alternative, so an explicit `"disableAllHooks": false`
  # in settings.local.json was swallowed and the lookup fell through to a
  # project-level `true` — blocking a user who had deliberately re-enabled hooks.
  # Reading the raw value and testing for the literal "null" keeps false visible.
  local k="$1" f v
  for f in "${settings_files[2]}" "${settings_files[1]}" "${settings_files[0]}"; do
    [ -f "$f" ] || continue
    v="$(jq -r "$k" "$f" 2>/dev/null)" || continue
    [ "$v" != "null" ] && [ -n "$v" ] && { printf '%s' "$v"; return 0; }
  done
  return 1
}

echo "better-goal preflight — $ROOT"
echo

# 1. hooks available at all -----------------------------------------------------
# The whole harness is one command Stop hook. If hooks are off, arming produces a
# run that looks armed and never fires.
if [ "$(setting '.disableAllHooks')" = "true" ] 2>/dev/null; then
  bad "hooks" "disableAllHooks is set — the guard cannot run"
elif [ "$(setting '.allowManagedHooksOnly')" = "true" ] 2>/dev/null; then
  bad "hooks" "allowManagedHooksOnly is set — a local command hook is refused"
else
  ok "hooks" "enabled"
fi

# 1b. will the hook actually load? ----------------------------------------------
# Claude Code's settings watcher only watches directories that already held a
# settings file when the session started, so a Stop hook written into an empty
# .claude/ mid-session is written correctly and never fires. One run spent its
# whole life like this, with the model running the gates by hand. Creating the
# file now does not help: the snapshot was taken before this check ran.
if [ -f "$ROOT/.claude/settings.json" ] || [ -f "$ROOT/.claude/settings.local.json" ]; then
  ok "hook load" "$ROOT/.claude/ already has a settings file, so a hook written now should load"
else
  warn "hook load" "$ROOT/.claude/ has no settings file, so a hook armed in this session will NOT fire. Arm anyway, then ask the user to open /hooks once or restart — the model cannot do either. The guard stays hook_live=unproven until it writes its first ledger row."
fi

# 2. permission mode ------------------------------------------------------------
PM="$(setting '.permissions.defaultMode' 2>/dev/null || true)"
case "${PM:-default}" in
  acceptEdits|bypassPermissions|dontAsk|auto) ok "permission mode" "${PM}" ;;
  *) warn "permission mode" "${PM:-default} — arming changes no permissions; an unallowed tool call stalls the run mid-turn, where the guard cannot see it. Pair with auto mode or pre-allow the brief's commands." ;;
esac

# 3. block cap ------------------------------------------------------------------
# Claude Code stops honouring ANY Stop hook after this many consecutive blocks
# and reports the turn as completed. Unset means 8, which a real run passes on
# its ninth turn — the single most common silent end.
CAP="${CLAUDE_CODE_STOP_HOOK_BLOCK_CAP:-$(setting '.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP' 2>/dev/null || true)}"
if [ -z "$CAP" ]; then
  bad "stop-hook block cap" "unset — defaults to 8 consecutive blocks, then Claude Code overrides the hook and ends the turn as 'completed'. arm.sh raises it."
elif [ "$CAP" -eq 0 ] 2>/dev/null; then
  warn "stop-hook block cap" "0 (uncapped) — max_iterations and deadline in the state file are then the only ceiling"
else
  ok "stop-hook block cap" "$CAP"
fi

# 4. skills the brief expects the run to invoke ----------------------------------
# The guard's block reason is read by the model, so a skill named there is only
# usable if the model may invoke it. Built-ins and disable-model-invocation
# skills are not: the run reads the instruction and cannot act on it.
BUILTIN_BLOCKED="verify code-review permissions model clear compact effort resume
plugins reload-plugins reload-skills config hooks mcp login logout doctor init"
if [ -n "$SKILLS" ]; then
  IFS=',' read -ra LIST <<<"$SKILLS"
  for s in "${LIST[@]}"; do
    s="$(printf '%s' "$s" | tr -d ' ')"; s="${s#/}"
    [ -n "$s" ] || continue
    # A bare name (no colon) can be a built-in. `plugin:name` is always a real
    # plugin skill, even when both halves match — code-review:code-review is a
    # legitimate skill and must not be confused with the built-in /code-review.
    case "$s" in *:*) qualified=1 ;; *) qualified=0 ;; esac
    name="${s##*:}"
    if [ "$qualified" -eq 0 ] && printf '%s\n' $BUILTIN_BLOCKED | grep -qx "$name"; then
      bad "skill /$s" "built-in or disable-model-invocation — the model cannot invoke it from a guard reason. Name the plugin-qualified skill, or make it a gate command instead."
      continue
    fi
    f="$(find "$HOME/.claude/plugins" "$HOME/.claude/skills" "$ROOT/.claude/skills" \
           -name SKILL.md -path "*/${name}/*" -print -quit 2>/dev/null)"
    if [ -z "$f" ]; then
      warn "skill /$s" "not found on disk — verify it exists before the brief tells the run to use it"
    elif grep -qiE '^disable-model-invocation:[[:space:]]*true' "$f" 2>/dev/null; then
      bad "skill /$s" "disable-model-invocation: true — the model cannot invoke it; only the user can"
    else
      ok "skill /$s" "model-invocable"
    fi
  done
fi

# 5. resource contention ---------------------------------------------------------
if [ -n "$PORTS" ]; then
  IFS=',' read -ra PL <<<"$PORTS"
  for p in "${PL[@]}"; do
    if lsof -nP -iTCP:"$p" -sTCP:LISTEN >/dev/null 2>&1; then
      warn "port $p" "in use by $(lsof -nP -iTCP:"$p" -sTCP:LISTEN -Fc 2>/dev/null | sed -n 's/^c//p' | head -1)"
    else ok "port $p" "free"; fi
  done
fi
if [ -n "$PROCS" ]; then
  IFS=',' read -ra QL <<<"$PROCS"
  for q in "${QL[@]}"; do
    n="$(pgrep -f "$q" 2>/dev/null | grep -c . | tr -d ' \n')"; n="${n:-0}"
    if [ "$n" -gt 1 ]; then warn "process $q" "$n instances running — contention risk"; else ok "process $q" "$n running"; fi
  done
fi
if command -v xcrun >/dev/null 2>&1; then
  BOOTED="$(xcrun simctl list devices booted 2>/dev/null | grep -c Booted | tr -d ' \n')"; BOOTED="${BOOTED:-0}"
  [ "$BOOTED" -gt 0 ] && warn "simulators" "$BOOTED booted — reserve a distinct one for this run"
fi

# 6. runs already armed here -----------------------------------------------------
# Per-slug state means a second run is fine; the same slug twice is not, because
# the second arm overwrites the first one's gates.
shopt -s nullglob 2>/dev/null || true
for f in "$ROOT"/.claude/goals/*.json "$ROOT"/.claude/goal-state.json; do
  [ -f "$f" ] || continue
  [ "$(jq -r '.armed // false' "$f" 2>/dev/null)" = "true" ] || continue
  warn "existing run" "$(jq -r '.slug // "?"' "$f") is armed — a different slug runs alongside it; the same slug replaces it"
done
DIRTY="$(git -C "$ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
[ "${DIRTY:-0}" -gt 0 ] && warn "worktree" "$DIRTY uncommitted files — gates may fail for reasons unrelated to this run"

# 7. the watcher's dependencies ---------------------------------------------------
command -v jq >/dev/null 2>&1 || bad "jq" "not installed — the guard, the watcher and status.sh all require it"

echo
[ "$FAIL" -eq 0 ] && echo "preflight: clear to arm" || echo "preflight: BLOCKED — resolve the rows above before arming"
exit "$FAIL"

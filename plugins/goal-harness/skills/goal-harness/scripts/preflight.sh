#!/usr/bin/env bash
# goal-harness preflight — the six conditions that end a goal without an error.
# Read-only. Prints a table and exits 1 if anything would block an armed run.
#
# Usage: preflight.sh [--skills "/ship-fleet:ship-fleet,/design-review:design-review"]
#                     [--ports 3000,8081] [--procs metro,expo]

set -uo pipefail
SKILLS=""; PORTS=""; PROCS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --skills) SKILLS="${2:-}"; shift 2 ;;
    --ports)  PORTS="${2:-}";  shift 2 ;;
    --procs)  PROCS="${2:-}";  shift 2 ;;
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
  local k="$1" f v
  for f in "${settings_files[2]}" "${settings_files[1]}" "${settings_files[0]}"; do
    [ -f "$f" ] || continue
    v="$(jq -r "$k // empty" "$f" 2>/dev/null)" || continue
    [ -n "$v" ] && { printf '%s' "$v"; return 0; }
  done
  return 1
}

echo "goal-harness preflight — $ROOT"
echo

# 1. hooks available at all -----------------------------------------------------
if [ "$(setting '.disableAllHooks')" = "true" ] 2>/dev/null; then
  bad "hooks" "disableAllHooks is set — /goal and the guard cannot run"
elif [ "$(setting '.allowManagedHooksOnly')" = "true" ] 2>/dev/null; then
  bad "hooks" "allowManagedHooksOnly is set — /goal refuses"
else
  ok "hooks" "enabled"
fi
[ -L "$ROOT/.claude" ] && bad "hooks" ".claude is a symlink — scheduled-task writes fail"

# 2. permission mode ------------------------------------------------------------
PM="$(setting '.permissions.defaultMode' 2>/dev/null || true)"
case "${PM:-default}" in
  acceptEdits|bypassPermissions|dontAsk|auto) ok "permission mode" "${PM}" ;;
  *) warn "permission mode" "${PM:-default} — a goal changes no permissions; unallowed tool calls will stall the run. Pair with auto mode or pre-allow the brief's commands." ;;
esac

# 3. block cap ------------------------------------------------------------------
CAP="${CLAUDE_CODE_STOP_HOOK_BLOCK_CAP:-$(setting '.env.CLAUDE_CODE_STOP_HOOK_BLOCK_CAP' 2>/dev/null || true)}"
if [ -z "$CAP" ]; then
  bad "stop-hook block cap" "unset — defaults to 8 consecutive blocks, then Claude Code overrides the hook and ends the turn as 'completed'"
elif [ "$CAP" -eq 0 ] 2>/dev/null; then
  warn "stop-hook block cap" "0 (uncapped) — rely on max_iterations/deadline in goal-state.json for the ceiling"
else
  ok "stop-hook block cap" "$CAP"
fi

# 4. cron / scheduler (a goal may drive one) ------------------------------------
[ "${CLAUDE_CODE_DISABLE_CRON:-}" = "1" ] && warn "scheduler" "CLAUDE_CODE_DISABLE_CRON=1 — /loop and cron tools unavailable"

# 5. skills named in the condition ----------------------------------------------
# Since v2.1.196 a scheduled fire only invokes skills Claude may invoke itself.
# Built-in commands and the bundled disable-model-invocation skills live inside
# the binary, not on disk, so they are matched by name rather than by file.
BUILTIN_BLOCKED="verify code-review permissions model clear compact effort resume
plugins reload-plugins reload-skills config hooks mcp login logout doctor init"
if [ -n "$SKILLS" ]; then
  IFS=',' read -ra LIST <<<"$SKILLS"
  for s in "${LIST[@]}"; do
    s="$(printf '%s' "$s" | tr -d ' /')"
    [ -n "$s" ] || continue
    name="${s##*:}"; plugin="${s%%:*}"
    if printf '%s\n' $BUILTIN_BLOCKED | grep -qx "$name" && [ "$plugin" = "$name" ]; then
      bad "skill /$s" "built-in or disable-model-invocation — a scheduled fire delivers it as PLAIN TEXT. Call it from the main turn, or name the underlying command."
      continue
    fi
    f="$(find "$HOME/.claude/plugins" "$HOME/.claude/skills" "$ROOT/.claude/skills" \
           -name SKILL.md -path "*/${name}/*" -print -quit 2>/dev/null)"
    if [ -z "$f" ]; then
      warn "skill /$s" "not found on disk — verify it exists, or it reaches a fire as plain text"
    elif grep -qiE '^disable-model-invocation:[[:space:]]*true' "$f" 2>/dev/null; then
      bad "skill /$s" "disable-model-invocation: true — a scheduled fire delivers it as PLAIN TEXT, it does not run"
    else
      ok "skill /$s" "model-invocable"
    fi
  done
fi

# 6. resource contention ---------------------------------------------------------
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

# 7. worktree / goal-state ---------------------------------------------------------
if [ -f "$ROOT/.claude/goal-state.json" ] && [ "$(jq -r '.armed // false' "$ROOT/.claude/goal-state.json" 2>/dev/null)" = "true" ]; then
  warn "existing goal" "$(jq -r '.slug' "$ROOT/.claude/goal-state.json") is already armed — arming replaces it"
fi
DIRTY="$(git -C "$ROOT" status --porcelain 2>/dev/null | wc -l | tr -d ' ')"
[ "${DIRTY:-0}" -gt 0 ] && warn "worktree" "$DIRTY uncommitted files — gates may fail for reasons unrelated to the goal"

echo
[ "$FAIL" -eq 0 ] && echo "preflight: clear to arm" || echo "preflight: BLOCKED — resolve the rows above before arming"
exit "$FAIL"

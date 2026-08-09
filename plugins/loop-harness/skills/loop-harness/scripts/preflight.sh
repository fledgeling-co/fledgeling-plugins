#!/usr/bin/env bash
# loop-harness preflight — the traps that make a loop tick and do nothing.
# Read-only. Exits 1 if anything would stop the loop working.
#
# Usage: preflight.sh [--skills "/ship-fleet:ship-fleet,/code-review"] [--interval 7m]

set -uo pipefail
SKILLS=""; INTERVAL=""
while [ $# -gt 0 ]; do
  case "$1" in
    --skills)   SKILLS="${2:-}";   shift 2 ;;
    --interval) INTERVAL="${2:-}"; shift 2 ;;
    *) shift ;;
  esac
done

FAIL=0
row() { printf '%-26s %-6s %s\n' "$1" "$2" "$3"; }
bad() { FAIL=1; row "$1" "BLOCK" "$2"; }
warn(){ row "$1" "warn" "$2"; }
ok()  { row "$1" "ok" "$2"; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
echo "loop-harness preflight — $ROOT"; echo

# 1. scheduler available --------------------------------------------------------
if [ "${CLAUDE_CODE_DISABLE_CRON:-}" = "1" ]; then
  bad "scheduler" "CLAUDE_CODE_DISABLE_CRON=1 — /loop and the cron tools are unavailable"
else
  ok "scheduler" "enabled"
fi

# 2. symlink traps --------------------------------------------------------------
if [ -L "$ROOT/.claude" ]; then
  bad ".claude" "is a symlink — scheduling fails with an error"
elif [ -L "$ROOT/.claude/scheduled_tasks.json" ]; then
  bad "scheduled_tasks.json" "is a symlink — scheduling fails with an error"
else
  ok ".claude" "regular directory"
fi

# 3. existing scheduled tasks ---------------------------------------------------
TASKS="$ROOT/.claude/scheduled_tasks.json"
if [ -f "$TASKS" ] && command -v jq >/dev/null 2>&1; then
  N="$(jq -r '(.tasks // . // []) | length' "$TASKS" 2>/dev/null | tr -d ' \n')"; N="${N:-0}"
  if   [ "$N" -ge 50 ]; then bad  "scheduled tasks" "$N/50 — at the per-session cap"
  elif [ "$N" -gt 0 ];  then warn "scheduled tasks" "$N already scheduled — a stale loop competes for idle time; check with CronList"
  else ok "scheduled tasks" "0"; fi
else
  ok "scheduled tasks" "none recorded"
fi

# 4. loop.md size and precedence ------------------------------------------------
PROJ="$ROOT/.claude/loop.md"; USERF="$HOME/.claude/loop.md"
size_of() { wc -c <"$1" 2>/dev/null | tr -d ' \n'; }
if [ -f "$PROJ" ]; then
  S="$(size_of "$PROJ")"
  if [ "$S" -gt 25000 ]; then bad "loop.md" ".claude/loop.md is ${S}B — over the 25,000B cap, it will be truncated"
  else ok "loop.md" ".claude/loop.md (${S}B) — project file wins"; fi
  [ -f "$USERF" ] && warn "loop.md precedence" "~/.claude/loop.md exists and is shadowed by the project file"
elif [ -f "$USERF" ]; then
  S="$(size_of "$USERF")"
  if [ "$S" -gt 25000 ]; then bad "loop.md" "~/.claude/loop.md is ${S}B — over the 25,000B cap"
  else ok "loop.md" "~/.claude/loop.md (${S}B) — user file in use"; fi
else
  ok "loop.md" "none — a bare /loop runs the built-in maintenance prompt"
fi

# 5. skills named in the prompt -------------------------------------------------
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
      bad "skill /$s" "built-in or disable-model-invocation — a fire delivers it as PLAIN TEXT and it never runs. Call it from the main turn, or name the plugin-qualified skill."
      continue
    fi
    f="$(find "$HOME/.claude/plugins" "$HOME/.claude/skills" "$ROOT/.claude/skills" \
           -name SKILL.md -path "*/${name}/*" -print -quit 2>/dev/null)"
    if [ -z "$f" ]; then
      warn "skill /$s" "not found on disk — verify it exists, or it reaches a fire as plain text"
    elif grep -qiE '^disable-model-invocation:[[:space:]]*true' "$f" 2>/dev/null; then
      bad "skill /$s" "disable-model-invocation: true — a fire delivers it as PLAIN TEXT"
    else
      ok "skill /$s" "model-invocable"
    fi
  done
fi

# 6. interval maps to a clean cron ----------------------------------------------
if [ -n "$INTERVAL" ]; then
  NUM="${INTERVAL%[smhd]}"; UNIT="${INTERVAL##*[0-9]}"
  case "$UNIT" in
    s) warn "interval $INTERVAL" "seconds round up to $(( (NUM + 59) / 60 ))m — cron granularity is 1 minute" ;;
    m) if [ "$NUM" -lt 60 ]; then
         if [ $((60 % NUM)) -ne 0 ]; then warn "interval $INTERVAL" "does not divide 60 — gaps go uneven at the hour boundary; round to the nearest clean step"
         else ok "interval $INTERVAL" "*/$NUM * * * *"; fi
       else
         H=$((NUM / 60))
         if [ $((NUM % 60)) -ne 0 ] || [ $((24 % H)) -ne 0 ]; then bad "interval $INTERVAL" "cron cannot express it — pick a whole number of hours that divides 24"
         else ok "interval $INTERVAL" "0 */$H * * *"; fi
       fi ;;
    h) if [ "$NUM" -le 23 ] && [ $((24 % NUM)) -eq 0 ]; then ok "interval $INTERVAL" "0 */$NUM * * *"
       else warn "interval $INTERVAL" "does not divide 24 — gaps go uneven at midnight"; fi ;;
    d) ok "interval $INTERVAL" "0 0 */$NUM * * (midnight local)" ;;
    *) warn "interval $INTERVAL" "unrecognised unit — use s, m, h or d" ;;
  esac
  warn "jitter" "recurring fires land up to 30 min late (or half the interval under an hour); pick an off-minute if exact timing matters"
fi

# 7. expiry ---------------------------------------------------------------------
warn "seven-day expiry" "a recurring task fires once more on $(date -v+7d +%Y-%m-%d 2>/dev/null || date -d '+7 days' +%Y-%m-%d 2>/dev/null) then deletes itself — arm a day-six renewal reminder"

echo
[ "$FAIL" -eq 0 ] && echo "preflight: clear to arm" || echo "preflight: BLOCKED — resolve the rows above before arming"
exit "$FAIL"

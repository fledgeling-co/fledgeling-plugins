#!/usr/bin/env bash
# better-loop preflight — the traps that make a loop tick and do nothing.
# Read-only apart from running the probe. Exits 1 if anything would stop it.
#
# Usage: preflight.sh [--probe '<cmd>'] [--skills "/ship-fleet:ship-fleet"]
#                     [--interval 120] [--cron]
#
# --probe is the important one: it runs the probe twice and compares. A probe
# whose output differs between two runs of the same world makes every poll look
# like a change, which turns a change-gated loop back into a polling one.
# --cron adds the checks that only matter when composing with the built-in /loop.

set -uo pipefail
SKILLS=""; INTERVAL=""; PROBE=""; CRON=0
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --skills)   need $# --skills; SKILLS="${2:-}";   shift 2 ;;
    --interval) need $# --interval; INTERVAL="${2:-}"; shift 2 ;;
    --probe)    need $# --probe; PROBE="${2:-}";     shift 2 ;;
    --cron)     CRON=1; shift ;;
    *) shift ;;
  esac
done

FAIL=0
row() { printf '%-26s %-6s %s\n' "$1" "$2" "$3"; }
bad() { FAIL=1; row "$1" "BLOCK" "$2"; }
warn(){ row "$1" "warn" "$2"; }
ok()  { row "$1" "ok" "$2"; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
echo "better-loop preflight — $ROOT"; echo

# 1. the probe -------------------------------------------------------------------
if [ -n "$PROBE" ]; then
  A="$(eval "$PROBE" 2>&1)"; RC=$?
  B="$(eval "$PROBE" 2>&1)"
  if [ "$RC" -gt 125 ]; then
    bad "probe" "exited $RC — the command was not found or was killed. The loop would treat that as the state."
  elif [ "$A" != "$B" ]; then
    bad "probe determinism" "two runs differed with nothing changed in between — a timestamp, a duration, a PID or an unsorted listing. Every poll would read as a change. Pipe through sed/sort to strip it."
  elif [ -z "$A" ]; then
    warn "probe" "produced no output — the loop can still detect the moment output appears, but check that is what you meant"
  else
    LINES="$(printf '%s\n' "$A" | grep -c .)"
    ok "probe" "deterministic, $LINES line(s)"
    [ "$LINES" -gt 50 ] && warn "probe size" "$LINES lines — only the delta is sent, but a wide probe makes small changes hard to read. Narrow it to what you would act on."
  fi
else
  warn "probe" "none given — pass --probe '<cmd>' to check it before arming"
fi

# 2. interval --------------------------------------------------------------------
if [ -n "$INTERVAL" ]; then
  N="${INTERVAL%[smhd]}"
  case "$INTERVAL" in
    *[!0-9smhd]*) warn "interval" "unrecognised — the watcher takes plain seconds" ;;
    *) [ "${N:-0}" -lt 30 ] 2>/dev/null \
         && warn "interval ${INTERVAL}s" "under 30s — the probe runs this often; keep it cheap or raise the interval" \
         || ok "interval" "${INTERVAL}s" ;;
  esac
fi

# 3. skills the tick expects to invoke -------------------------------------------
# A wake delivers text the model reads. Built-ins and disable-model-invocation
# skills cannot be invoked by the model, so a tick told to run one reads the
# instruction and carries on as though it had.
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
      bad "skill /$s" "built-in or disable-model-invocation — the model cannot invoke it from a wake. Make it a shell command in the probe or the tick, or name the plugin-qualified skill."
      continue
    fi
    f="$(find "$HOME/.claude/plugins" "$HOME/.claude/skills" "$ROOT/.claude/skills" \
           -name SKILL.md -path "*/${name}/*" -print -quit 2>/dev/null)"
    if [ -z "$f" ]; then
      warn "skill /$s" "not found on disk — verify it exists before the tick protocol names it"
    elif grep -qiE '^disable-model-invocation:[[:space:]]*true' "$f" 2>/dev/null; then
      bad "skill /$s" "disable-model-invocation: true — only the user can invoke it"
    else
      ok "skill /$s" "model-invocable"
    fi
  done
fi

# 4. loops already armed here ----------------------------------------------------
shopt -s nullglob 2>/dev/null || true
for f in "$ROOT"/.claude/loops/*.json; do
  [ "$(jq -r '.armed // false' "$f" 2>/dev/null)" = "true" ] || continue
  warn "existing loop" "$(jq -r '.slug // "?"' "$f") is armed — two loops in one session compete for idle time"
done

command -v jq >/dev/null 2>&1 || bad "jq" "not installed — the watcher and status.sh both require it"

# 5. only when composing with the built-in /loop ---------------------------------
if [ "$CRON" -eq 1 ]; then
  echo
  echo "— composing with the built-in /loop —"
  if [ "${CLAUDE_CODE_DISABLE_CRON:-}" = "1" ]; then
    bad "scheduler" "CLAUDE_CODE_DISABLE_CRON=1 — /loop and the cron tools are unavailable"
  else ok "scheduler" "enabled"; fi

  if [ -L "$ROOT/.claude" ]; then
    bad ".claude" "is a symlink — scheduling fails with an error"
  elif [ -L "$ROOT/.claude/scheduled_tasks.json" ]; then
    bad "scheduled_tasks.json" "is a symlink — scheduling fails with an error"
  else ok ".claude" "regular directory"; fi

  TASKS="$ROOT/.claude/scheduled_tasks.json"
  if [ -f "$TASKS" ] && command -v jq >/dev/null 2>&1; then
    N="$(jq -r '(.tasks // . // []) | length' "$TASKS" 2>/dev/null | tr -d ' \n')"; N="${N:-0}"
    if   [ "$N" -ge 50 ]; then bad  "scheduled tasks" "$N/50 — at the per-session cap"
    elif [ "$N" -gt 0 ];  then warn "scheduled tasks" "$N already scheduled — check with CronList"
    else ok "scheduled tasks" "0"; fi
  fi

  PROJ="$ROOT/.claude/loop.md"; USERF="$HOME/.claude/loop.md"
  size_of() { wc -c <"$1" 2>/dev/null | tr -d ' \n'; }
  if [ -f "$PROJ" ]; then
    S="$(size_of "$PROJ")"
    if [ "$S" -gt 25000 ]; then bad "loop.md" ".claude/loop.md is ${S}B — over the 25,000B cap, the tail is truncated"
    else ok "loop.md" ".claude/loop.md (${S}B) — project file wins"; fi
    [ -f "$USERF" ] && warn "loop.md precedence" "~/.claude/loop.md exists and is shadowed by the project file"
  elif [ -f "$USERF" ]; then
    S="$(size_of "$USERF")"
    if [ "$S" -gt 25000 ]; then bad "loop.md" "~/.claude/loop.md is ${S}B — over the 25,000B cap"
    else ok "loop.md" "~/.claude/loop.md (${S}B) — user file in use"; fi
  else
    ok "loop.md" "none — a bare /loop runs the built-in maintenance prompt"
  fi

  warn "seven-day expiry" "a recurring task fires once more on $(date -v+7d +%Y-%m-%d 2>/dev/null || date -d '+7 days' +%Y-%m-%d 2>/dev/null) then deletes itself — the watcher has no expiry, so prefer it for anything longer"
  warn "jitter" "recurring fires land up to 30 min late (or half the interval under an hour)"
fi

echo
[ "$FAIL" -eq 0 ] && echo "preflight: clear to arm" || echo "preflight: BLOCKED — resolve the rows above before arming"
exit "$FAIL"

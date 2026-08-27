#!/usr/bin/env bash
# better-loop arm — write the per-slug state and print the Monitor call.
#
#   arm.sh --slug <slug> --probe '<cmd>' [--interval 120] [--stop-when '<cmd>']
#          [--tick-cmd '<cmd>'] [--max-wakes 12] [--repeat-after 1800]
#          [--dry-stop 0] [--brief docs/loops/loop-<slug>.md] [--dry-run]
#
# There is no cron to schedule: the loop is a Monitor in this session. Arming
# writes one state file, prints the call to make, and registers one SessionStart
# hook so that a loop whose session died is reported to the next session that
# opens this repo rather than reading `armed: true` forever. --no-sentinel skips
# that and leaves settings untouched.

set -uo pipefail
SLUG=""; PROBE=""; STOP_WHEN=""; TICK_CMD=""; BRIEF=""
INTERVAL=120; MAX_WAKES=12; REPEAT_AFTER=1800; DRY_STOP=0; DRY=0; SENTINEL_ON=1
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --slug)         need $# --slug; SLUG="$2"; shift 2 ;;
    --probe)        need $# --probe; PROBE="$2"; shift 2 ;;
    --interval)     need $# --interval; INTERVAL="$2"; shift 2 ;;
    --stop-when)    need $# --stop-when; STOP_WHEN="$2"; shift 2 ;;
    --tick-cmd)     need $# --tick-cmd; TICK_CMD="$2"; shift 2 ;;
    --max-wakes)    need $# --max-wakes; MAX_WAKES="$2"; shift 2 ;;
    --repeat-after) need $# --repeat-after; REPEAT_AFTER="$2"; shift 2 ;;
    --dry-stop)     need $# --dry-stop; DRY_STOP="$2"; shift 2 ;;
    --brief)        need $# --brief; BRIEF="$2"; shift 2 ;;
    --dry-run)      DRY=1; shift ;;
    --no-sentinel)  SENTINEL_ON=0; shift ;;
    --sentinel)     SENTINEL_ON=1; shift ;;
    *) shift ;;
  esac
done
[ -n "$SLUG" ]  || { echo "arm.sh: --slug is required" >&2; exit 2; }
[ -n "$PROBE" ] || { echo "arm.sh: --probe is required — a loop with no probe has nothing to gate on" >&2; exit 2; }
case "$SLUG" in *[!a-zA-Z0-9._-]*)
  echo "arm.sh: slug '$SLUG' must be a bare kebab name — it becomes a filename" >&2; exit 2 ;;
esac
command -v jq >/dev/null 2>&1 || { echo "arm.sh: jq is required" >&2; exit 2; }

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
STATE="$ROOT/.claude/loops/${SLUG}.json"
SETTINGS="$ROOT/.claude/settings.local.json"
SENTINEL="$HERE/sentinel.sh"
SID="${CLAUDE_CODE_SESSION_ID:-}"
[ -n "$BRIEF" ] || BRIEF="docs/loops/loop-${SLUG}.md"

if [ "$SENTINEL_ON" -eq 1 ] && [ -f "$SETTINGS" ] && ! jq -e . "$SETTINGS" >/dev/null 2>&1; then
  echo "arm.sh: $SETTINGS is not valid JSON — fix or move it, or pass --no-sentinel; nothing written" >&2
  exit 2
fi

backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

NEW="$(jq -n --arg s "$SLUG" --arg p "$PROBE" --arg sw "$STOP_WHEN" --arg tc "$TICK_CMD" --arg sid "$SID" \
      --arg b "$BRIEF" --arg l "docs/loops/loop-${SLUG}.ledger.md" --arg c "$ROOT" \
      --argjson iv "$INTERVAL" --argjson mw "$MAX_WAKES" --argjson ra "$REPEAT_AFTER" --argjson ds "$DRY_STOP" '
  { slug:$s, armed:false, cwd:$c, brief:$b, ledger:$l, probe:$p, session_id:$sid,
    stop_when:(if $sw=="" then null else $sw end),
    tick_cmd:(if $tc=="" then null else $tc end),
    interval:$iv, max_wakes:$mw, repeat_after:$ra, dry_stop:$ds,
    polls:0, wakes:0, ticks:0 }')"

if [ "$SENTINEL_ON" -eq 1 ]; then
  NEW_SETTINGS="$(
    { [ -f "$SETTINGS" ] && cat "$SETTINGS" || echo '{}'; } | jq --arg sentinel "$SENTINEL" '
      .hooks = (.hooks // {})
      | .hooks.SessionStart = (
          ((.hooks.SessionStart // []) | map(select(((.hooks // [])
             | map(.command? // "") | map(test("better-loop.*sentinel\\.sh")) | any) | not)))
          + [{ hooks: [{ type: "command", command: $sentinel, timeout: 60,
                         statusMessage: "better-loop: checking for dead loops" }] }])')"
  echo "── settings: $SETTINGS"
  if [ -f "$SETTINGS" ]; then
    diff -u <(jq -S . "$SETTINGS") <(printf '%s' "$NEW_SETTINGS" | jq -S .) || true
  else
    echo "(new file)"; printf '%s\n' "$NEW_SETTINGS" | jq -S .
  fi
  echo
fi

echo "── state: $STATE"
if [ -f "$STATE" ]; then diff -u <(jq -S . "$STATE") <(printf '%s' "$NEW" | jq -S .) || true
else echo "(new file)"; printf '%s' "$NEW" | jq -S .; fi

if [ "$DRY" -eq 1 ]; then echo; echo "dry run — nothing written."; exit 0; fi

mkdir -p "$ROOT/.claude/loops"
[ -f "$STATE" ] && backup "$STATE"

if [ "$SENTINEL_ON" -eq 1 ] && [ -n "${NEW_SETTINGS:-}" ]; then
  [ -f "$SETTINGS" ] && backup "$SETTINGS"
  mkdir -p "$ROOT/.claude"
  tmp="$(mktemp)"; printf '%s\n' "$NEW_SETTINGS" | jq . >"$tmp" && mv "$tmp" "$SETTINGS" || {
    echo "arm.sh: settings write failed; $SETTINGS left as it was" >&2; rm -f "$tmp"; }
fi
tmp="$(mktemp)"; printf '%s\n' "$NEW" | jq . >"$tmp" && mv "$tmp" "$STATE" || {
  echo "arm.sh: state write failed; $STATE left as it was" >&2; rm -f "$tmp"; exit 2; }

grep -qxF '.claude/loops/' "$ROOT/.gitignore" 2>/dev/null || \
  printf '\n# better-loop\n.claude/loops/\n' >>"$ROOT/.gitignore" 2>/dev/null || \
  echo "arm.sh: WARNING could not update .gitignore. The state file holds shell commands the watcher executes, so it must not be committed." >&2

# Single-quote for the printed Monitor line: %q escapes with backslashes, which
# is shell-correct but unreadable inside a JSON string argument.
q() { printf "'%s'" "$(printf '%s' "$1" | sed "s/'/'\\\\''/g")"; }
OPTS="--probe $(q "$PROBE") --interval $INTERVAL --max-wakes $MAX_WAKES --repeat-after $REPEAT_AFTER"
[ -n "$STOP_WHEN" ] && OPTS="$OPTS --stop-when $(q "$STOP_WHEN")"
[ -n "$TICK_CMD" ]  && OPTS="$OPTS --tick-cmd $(q "$TICK_CMD")"
[ "$DRY_STOP" -gt 0 ] 2>/dev/null && OPTS="$OPTS --dry-stop $DRY_STOP"

echo
echo "wrote $STATE"
echo
echo "Start the loop with:"
echo "  Monitor({ command: \"$HERE/watch.sh $SLUG $OPTS\","
echo "            description: \"loop $SLUG\", persistent: true })"
echo
echo "It emits only when the probe's answer changes${TICK_CMD:+, and dispatches the tick detached rather than waking this session}."
if [ "$SENTINEL_ON" -eq 1 ]; then
  echo "sentinel: registered on SessionStart. A SessionStart hook is read when the NEXT"
  echo "          session opens, so this one needs no /hooks reload to work as intended."
else
  echo "sentinel: skipped (--no-sentinel). Nothing will report this loop if its session dies."
fi
echo "status:  $HERE/status.sh $SLUG"
echo "stop:    TaskStop on the monitor, then $HERE/disarm.sh $SLUG"

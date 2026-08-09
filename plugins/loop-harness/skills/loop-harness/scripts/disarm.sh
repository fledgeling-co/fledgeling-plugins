#!/usr/bin/env bash
# loop-harness disarm — remove the active loop.md so a bare /loop stops running
# this protocol. Leaves the brief and ledger, and prints what still has to be
# cancelled through Claude Code (a cron job and a Monitor are session state, not
# files, so no script can remove them).
#   disarm.sh <slug>
set -uo pipefail
SLUG="${1:-}"
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TARGET="$ROOT/.claude/loop.md"
BRIEF="$ROOT/docs/loops/loop-${SLUG}.md"

if [ -f "$TARGET" ]; then
  cp "$TARGET" "$TARGET.bak.$(date -u +%Y%m%dT%H%M%SZ)"
  rm "$TARGET"
  echo "removed $TARGET (backed up)"
  [ -f "$HOME/.claude/loop.md" ] && echo "note: ~/.claude/loop.md is no longer shadowed and now applies to a bare /loop"
else
  echo "no .claude/loop.md in $ROOT"
fi

JOB=""; [ -f "$BRIEF" ] && JOB="$(sed -n 's/^- \*\*job id:\*\* *//p' "$BRIEF" | head -1)"
MON=""; [ -f "$BRIEF" ] && MON="$(sed -n 's/^- \*\*wake signal:\*\* *//p' "$BRIEF" | head -1)"

echo
echo "still to cancel in the session (these are not files):"
echo "  cron job      CronDelete ${JOB:-<id — find it with CronList>}"
echo "  dynamic loop  ScheduleWakeup {stop: true}, or press Esc while it waits"
echo "  monitor       TaskStop <task id — find it with TaskList>${MON:+   (${MON})}"
echo "  renewal       CronDelete <the day-six one-shot, if still pending>"
[ -f "$BRIEF" ] && echo && echo "brief and ledger kept: $BRIEF"

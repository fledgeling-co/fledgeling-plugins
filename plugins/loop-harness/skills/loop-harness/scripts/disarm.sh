#!/usr/bin/env bash
# loop-harness disarm — remove the active loop.md so a bare /loop stops running
# this protocol. Leaves the brief and ledger, and prints what still has to be
# cancelled through Claude Code (a cron job and a Monitor are session state, not
# files, so no script can remove them).
#   disarm.sh <slug>
set -uo pipefail
SLUG="${1:-}"

# A backup is a precondition, not a courtesy: if it fails we must not proceed to
# the destructive step, and we must never claim it happened. Reproduced on a
# read-only .claude/: the backup failed, the overwrite succeeded anyway, and the
# script printed "wrote" and exited 0 with the previous file unrecoverable.
backup() {
  cp "$1" "$1.bak.$(date -u +%Y%m%dT%H%M%SZ)" || {
    echo "${0##*/}: could not back up $1 — refusing to modify it" >&2; exit 1; }
}

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
TARGET="$ROOT/.claude/loop.md"
BRIEF="$ROOT/docs/loops/loop-${SLUG}.md"

if [ -f "$TARGET" ]; then
  backup "$TARGET"
  rm "$TARGET" || { echo "${0##*/}: could not remove $TARGET" >&2; exit 1; }
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

exit 0

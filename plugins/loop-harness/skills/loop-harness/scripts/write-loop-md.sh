#!/usr/bin/env bash
# loop-harness — render docs/loops/loop-<slug>.md into .claude/loop.md,
# size-checking against the 25,000-byte cap.
#
#   write-loop-md.sh --slug <slug> --from <path> [--dry-run]
#
# --from is the rendered active-file content (the short tick prompt), not the
# full source-of-record brief. Detail belongs in the brief the tick reads.

set -uo pipefail
SLUG=""; FROM=""; DRY=0
# `shift 2` fails with $# unchanged when a flag is passed as the last argument,
# so the same branch re-matches and the loop spins forever. Fail loudly instead.
need() { [ "$1" -ge 2 ] || { echo "${0##*/}: $2 requires a value" >&2; exit 2; }; }
while [ $# -gt 0 ]; do
  case "$1" in
    --slug)    need $# --slug; SLUG="${2:-}"; shift 2 ;;
    --from)    need $# --from; FROM="${2:-}"; shift 2 ;;
    --dry-run) DRY=1; shift ;;
    *) shift ;;
  esac
done
[ -n "$SLUG" ] || { echo "write-loop-md.sh: --slug is required" >&2; exit 2; }
[ -n "$FROM" ] && [ -f "$FROM" ] || { echo "write-loop-md.sh: --from <file> is required" >&2; exit 2; }

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
CAP=25000
SIZE="$(wc -c <"$FROM" | tr -d ' \n')"

echo "── .claude/loop.md   ${SIZE}B / ${CAP}B cap"
if [ "$SIZE" -gt "$CAP" ]; then
  echo "BLOCKED: ${SIZE}B exceeds the 25,000-byte cap. Claude Code truncates the excess"
  echo "         and appends a warning, so the tail of the protocol silently stops applying."
  echo "         Move detail into docs/loops/loop-${SLUG}.md and keep the active file short." >&2
  exit 1
fi
[ -f "$HOME/.claude/loop.md" ] && echo "note: ~/.claude/loop.md exists and will be shadowed by this project file"

if [ -f "$TARGET" ]; then
  echo; diff -u "$TARGET" "$FROM" || true
else
  echo "(new file)"; sed 's/^/  /' "$FROM"
fi

if [ "$DRY" -eq 1 ]; then
  echo; echo "dry run — nothing written."
  exit 0
fi

mkdir -p "$ROOT/.claude" "$ROOT/docs/loops" || {
  echo "${0##*/}: cannot create $ROOT/.claude" >&2; exit 1; }
[ -f "$TARGET" ] && backup "$TARGET"
cp "$FROM" "$TARGET" || { echo "${0##*/}: write to $TARGET failed" >&2; exit 1; }
echo
echo "wrote $TARGET (${SIZE}B)"
echo "source of record: docs/loops/loop-${SLUG}.md"
echo "edits take effect on the next tick — the file is re-read each fire"

#!/usr/bin/env bash
# Blind A/B panel. Each judge sees only the anonymised bundle — never the skill
# files, never the arm labels, never the linter's verdict, and is never told
# that either side is a baseline.
#
# Four judge families, so a single model's taste cannot decide the result. The
# per-family split is reported rather than pooled, because the skill was
# authored by Claude and a Claude judge is the one most likely to be biased
# toward it; that bias is only visible if the families stay separate.
#
#   ./run_blind_panel.sh <bundle_dir>
set -uo pipefail
DIR="${1:-/tmp/clarify-blind}"
OUT="$DIR/results.tsv"
: > "$OUT"

JUDGES=(claude codex grok cursor)

run_judge() {
  local judge="$1" file="$2" prompt out
  prompt="$(cat "$file")"
  case "$judge" in
    claude) out="$(claude -p "$prompt" --strict-mcp-config 2>/dev/null)" ;;
    codex)  out="$(codex exec --skip-git-repo-check "$prompt" 2>/dev/null)" ;;
    grok)   out="$(grok -p "$prompt" 2>/dev/null)" ;;
    cursor) out="$(cursor-agent -p --force "$prompt" 2>/dev/null)" ;;
  esac
  # First standalone A / B / TIE on a VERDICT line.
  echo "$out" | grep -oiE 'VERDICT:[[:space:]]*(A|B|TIE)' | head -1 \
    | grep -oiE '(A|B|TIE)$' | tr '[:lower:]' '[:upper:]'
}

for f in "$DIR"/pair*.md; do
  [ -e "$f" ] || { echo "no bundles in $DIR" >&2; exit 1; }
  pair="$(basename "$f" .md)"
  for judge in "${JUDGES[@]}"; do
    v="$(run_judge "$judge" "$f")"
    [ -z "$v" ] && v="NONE"
    printf '%s\t%s\t%s\n' "$pair" "$judge" "$v" | tee -a "$OUT"
  done
done
echo "done -> $OUT"

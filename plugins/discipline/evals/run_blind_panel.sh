#!/usr/bin/env bash
# Blind A/B panel. Each judge sees only the anonymised bundle — never the skill files, never the
# arm labels, never the benchmark's own grade. Writes one line per (judge, pair) to results.tsv.
set -uo pipefail
DIR="${1:-/tmp/td-blind}"
OUT="$DIR/results.tsv"
: > "$OUT"

run_judge() {
  local judge="$1" file="$2" prompt out
  prompt="$(cat "$file")"
  case "$judge" in
    claude) out="$(claude -p "$prompt" 2>/dev/null)" ;;
    codex)  out="$(codex exec --skip-git-repo-check "$prompt" 2>/dev/null)" ;;
    grok)   out="$(grok -p "$prompt" 2>/dev/null)" ;;
  esac
  # First standalone A / B / TIE token on a VERDICT line.
  echo "$out" | grep -oiE 'VERDICT:[[:space:]]*(A|B|TIE)' | head -1 \
    | grep -oiE '(A|B|TIE)$' | tr '[:lower:]' '[:upper:]'
}

for f in "$DIR"/pair*.md; do
  pair="$(basename "$f" .md)"
  for judge in claude codex grok; do
    v="$(run_judge "$judge" "$f")"
    [ -z "$v" ] && v="NONE"
    printf '%s\t%s\t%s\n' "$pair" "$judge" "$v" | tee -a "$OUT"
  done
done
echo "done -> $OUT"

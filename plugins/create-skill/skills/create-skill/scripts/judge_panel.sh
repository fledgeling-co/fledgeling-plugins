#!/bin/bash
# judge_panel.sh — run a blind judging panel for create-skill's Phase 3.
#
#   judge_panel.sh --dir <dir of *.txt prompts> [--lanes fable,astra,argon,carbon,wonder-full]
#                  [--timeout 900] [--parallel 5]
#
# Each prompt file is one anonymised A/B bundle, already in its final order. For a prompt
# P.txt and a lane L this writes P.L.md (the answer) and P.L.log beside it, and records the
# model id and effort each lane resolved to in models.tsv. Build the bundles and the
# un-blinding map yourself; this script only runs the judges.
#
# Which models judge, and at what effort, comes from the roster: roster.json beside this
# script, read through roster.py. The source is models/roster.json at the root of the
# fledgeling-plugins repository and scripts/sync_model_roster.py copies it here; edit the
# source, never this copy. With no --lanes the frontier tier runs, the same lanes
# decision-panel and feedback-panel use. When this was written (21 November 2026) that was
# fable, astra, argon and carbon at medium effort and wonder-full at high, with the argon lane
# falling back to Gemini Neon at xhigh. `roster.py show frontier` prints the current set.
#
# Override a model with FP_<LANE>_MODEL; that also switches the lane's fallback off.
# FP_CODEX_BIN names the codex binary. The lane that shares a family with the model that wrote
# the outputs still runs; record it and leave it out of the majority.
#
# An answer under 20 bytes, or a missing one, is a lane failure and never an opinion. The
# script prints each failure and exits 1 if any lane failed, 0 otherwise.

set -u
HERE=$(cd "$(dirname "$0")" && pwd); ROSTER="$HERE/roster.py"
DIR="" LANES="" TIMEOUT=900 PAR=5
while [ $# -gt 0 ]; do
  case "$1" in
    --dir) DIR=$2; shift 2;;
    --lanes) LANES=$2; shift 2;;
    --timeout) TIMEOUT=$2; shift 2;;
    --parallel) PAR=$2; shift 2;;
    -h|--help) sed -n '2,25p' "$0"; exit 0;;
    *) echo "unknown argument $1" >&2; exit 2;;
  esac
done
[ -d "$DIR" ] || { echo "give --dir <directory of *.txt prompts>" >&2; exit 2; }
DIR=$(cd "$DIR" && pwd)
[ -n "$LANES" ] || LANES=$("$ROSTER" lanes frontier)

newest_codex() {
  [ -n "${FP_CODEX_BIN:-}" ] && { echo "$FP_CODEX_BIN"; return; }
  local best="" bestv="0" p v
  for p in "$(command -v codex 2>/dev/null)" /Applications/ChatGPT.app/Contents/Resources/codex-cli/bin/codex; do
    [ -x "$p" ] || continue
    v=$("$p" --version 2>/dev/null | grep -o -E '[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [ -n "$v" ] && [ "$(printf '%s\n%s\n' "$bestv" "$v" | sort -V | tail -1)" = "$v" ]; then best=$p; bestv=$v; fi
  done
  echo "$best"
}
CODEX=$(newest_codex)
export ROSTER CODEX TIMEOUT

# Resolve every lane once, so each bundle is judged by the same ids and models.tsv records them.
printf 'lane\tmodel\teffort\tfallback\n' > "$DIR/models.tsv"
: > "$DIR/models.notes"
for l in $(echo "$LANES" | tr ',' ' '); do
  m=$("$ROSTER" model "$l" 2>> "$DIR/models.notes") || { echo "unknown lane $l" >&2; exit 2; }
  printf '%s\t%s\t%s\t%s\n' "$l" "$m" "$("$ROSTER" effort "$l")" "$("$ROSTER" fallback "$l" 2>/dev/null)" >> "$DIR/models.tsv"
done

lane() { # lane <name> <prompt file>
  local l=$1 f=$2 base=${2%.txt} p rc model eff fb cli
  p=$(cat "$f"); local md="$base.$l.md" log="$base.$l.log"
  : > "$md"; : > "$log"
  model=$(awk -F'\t' -v l="$l" '$1==l{print $2}' "$(dirname "$f")/models.tsv")
  eff=$(awk -F'\t' -v l="$l" '$1==l{print $3}' "$(dirname "$f")/models.tsv")
  fb=$(awk -F'\t' -v l="$l" '$1==l{print $4}' "$(dirname "$f")/models.tsv")
  echo "model=$model effort=$eff" >> "$log"
  limit() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@"; }
  cd /tmp || return 1
  case $l in
    fable|opus) limit claude --model "$model" --effort "$eff" -p "$p" < /dev/null > "$md" 2>> "$log";;
    astra)  echo "codex=$CODEX" >> "$log"
            limit "$CODEX" exec -m "$model" -c model_reasoning_effort="$eff" -s read-only --skip-git-repo-check -o "$md" "$p" < /dev/null >> "$log" 2>&1;;
    argon|carbon|neon)
            limit agy --new-project --model "$model" -p "$p" > "$md" 2>> "$log"; rc=$?
            if [ -n "$fb" ] && [ "$fb" != "$model" ] && { [ $rc -ne 0 ] || [ ! -s "$md" ]; }; then
              echo "$l unavailable (model=$model rc=$rc); falling back to $fb" >> "$log"
              limit agy --new-project --model "$fb" -p "$p" > "$md" 2>> "$log"
            fi;;
    grok)   limit grok -m "$model" --effort "$eff" -p "$p" > "$md" 2>> "$log";;
    wonder-full|wonder)
            limit muse exec --model "$model" --reasoning-effort "$eff" --disable-write --disable-shell \
              --disable-web-tools --approval-mode untrusted --no-session-log --workspace /tmp \
              "$p" < /dev/null > "$md" 2>> "$log";;
    *) echo "unknown lane $l" >> "$log";;
  esac
}
export -f lane

for f in "$DIR"/*.txt; do
  [ -e "$f" ] || { echo "no *.txt prompts in $DIR" >&2; exit 2; }
  for l in $(echo "$LANES" | tr ',' ' '); do printf '%s\t%s\n' "$l" "$f"; done
done | xargs -P "$PAR" -L 1 bash -c 'lane "$0" "$1"'

cat "$DIR/models.tsv"; cat "$DIR/models.notes"
fails=0
for f in "$DIR"/*.txt; do
  for l in $(echo "$LANES" | tr ',' ' '); do
    md="${f%.txt}.$l.md"
    if [ ! -f "$md" ] || [ "$(wc -c < "$md" | tr -d ' ')" -lt 20 ]; then
      echo "LANE FAILURE: $(basename "$md") ($(tail -c 160 "${f%.txt}.$l.log" 2>/dev/null | tr '\n' ' '))"
      fails=$((fails + 1))
    fi
    grep -q "falling back to" "${f%.txt}.$l.log" 2>/dev/null && echo "note: $(basename "$md") $(grep -h 'falling back to' "${f%.txt}.$l.log" | tail -1)"
  done
done
echo "$fails lane failure(s)"
[ "$fails" -eq 0 ]

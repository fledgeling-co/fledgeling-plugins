#!/bin/zsh
# Run one panel round: the same brief to several model families at once, each writing its own
# answer file, then report which lanes produced a usable answer.
#
#   run_panel.sh --brief brief.md --out /tmp/panel/r1 --lanes fable,astra,argon \
#                [--add-dir /path/to/repo]... [--timeout 900] [--min-bytes 1500]
#
# Lanes and their commands (override a model with FP_<LANE>_MODEL, e.g. FP_ARGON_MODEL):
#   fable  claude --model claude-fable-5-1 --effort high -p
#   astra  codex exec -m gpt-6-astra -c model_reasoning_effort="high" -s read-only -o <file>
#   argon  agy --new-project --model gemini-4-argon-high --add-dir <each dir> -p
#   grok   grok -m grok-4.6 --effort high -p
#
# Every lane runs from a neutral directory (/tmp): agy run from inside a repo has answered a
# different project's question. agy also needs --add-dir for every directory the brief points
# at, or it tries a shell command, is auto-denied in headless mode and exits 0 with an empty
# file. An empty or missing answer file is a lane failure, whatever the exit code says.
#
# Output: <out>/<lane>.md (the answer), <out>/<lane>.log (stderr and the exit code), and a
# status line per lane on stdout. Exits 1 if any lane's answer is shorter than --min-bytes
# (default 1, so only an empty file fails; a full round-one answer runs to several thousand bytes,
# so pass --min-bytes 1500 there to catch an answer that stopped early).
set -u
BRIEF= OUT= LANES=fable,astra,argon TIMEOUT=900 MINB=1
typeset -a DIRS
while (( $# )); do
  case $1 in
    --brief) BRIEF=$2; shift 2;;
    --out) OUT=$2; shift 2;;
    --lanes) LANES=$2; shift 2;;
    --add-dir) DIRS+=("$2"); shift 2;;
    --timeout) TIMEOUT=$2; shift 2;;
    --min-bytes) MINB=$2; shift 2;;
    *) print -u2 "unknown argument: $1"; exit 2;;
  esac
done
[[ -f $BRIEF && -n $OUT ]] || { print -u2 "usage: run_panel.sh --brief FILE --out DIR [--lanes fable,astra,argon] [--add-dir DIR]..."; exit 2; }
mkdir -p "$OUT"
PROMPT=$(<"$BRIEF")
limit() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@"; }

run_lane() {
  local lane=$1 md="$OUT/$1.md" log="$OUT/$1.log"
  : > "$md"
  case $lane in
    fable) limit claude --model "${FP_FABLE_MODEL:-claude-fable-5-1}" --effort high -p "$PROMPT" > "$md" 2> "$log";;
    astra) limit codex exec -m "${FP_ASTRA_MODEL:-gpt-6-astra}" -c model_reasoning_effort="high" -s read-only --skip-git-repo-check -o "$md" "$PROMPT" < /dev/null > "$log" 2>&1;;
    argon) local -a add; for d in $DIRS; do add+=(--add-dir "$d"); done
           limit agy --new-project --model "${FP_ARGON_MODEL:-gemini-4-argon-high}" $add -p "$PROMPT" > "$md" 2> "$log";;
    grok)  limit grok -m "${FP_GROK_MODEL:-grok-4.6}" --effort high -p "$PROMPT" > "$md" 2> "$log";;
    *) print "unknown lane $lane" > "$log"; return 2;;
  esac
  print "rc=$?" >> "$log"
}

cd /tmp
for lane in ${(s:,:)LANES}; do run_lane "$lane" & done
wait

failed=0
for lane in ${(s:,:)LANES}; do
  md="$OUT/$lane.md"; bytes=$(wc -c < "$md" 2>/dev/null || print 0); rc=$(grep -o 'rc=[0-9]*' "$OUT/$lane.log" | tail -1)
  if (( bytes < MINB )); then
    failed=1; print "FAIL  $lane  $bytes bytes  $rc  (read $OUT/$lane.log; a lane failure, not a verdict)"
  else
    print "ok    $lane  $bytes bytes  $rc"
  fi
done
exit $failed

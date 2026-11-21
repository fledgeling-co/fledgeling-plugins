#!/bin/zsh
# Run one panel round: the same brief to several model families at once, each writing its own
# answer file, then report which lanes produced a usable answer.
#
#   run_panel.sh --brief brief.md --out /tmp/panel/r1 [--lanes fable,astra,argon,carbon,wonder-full] \
#                [--add-dir /path/to/repo]... [--timeout 900] [--min-bytes 1500]
#
# Which models run, and at what effort, comes from the roster: roster.json beside this script,
# read through roster.py. The source is models/roster.json at the root of the fledgeling-plugins
# repository, and scripts/sync_model_roster.py copies it here; edit the source, never this copy.
# With no --lanes, the frontier tier runs (owner directive, 21 Nov 2026): fable, astra, argon and
# carbon at medium effort, and wonder-full at high. Any lane in the roster can be named, so the
# daily lanes (opus, neon, grok, wonder, at xhigh) run through the same commands:
#   fable | opus          claude --model <id> --effort <effort> -p
#   astra                 <newest codex> exec -m <id> -c model_reasoning_effort="<effort>" -s read-only -o <file>
#   argon | carbon | neon agy --new-project --model <newest gemini-<v>-<name>-<effort>> --add-dir <each dir> -p
#   grok                  grok -m <newest grok> --effort <effort> -p
#   wonder-full | wonder  muse exec --model <id> --reasoning-effort <effort> --disable-write ...
# agy carries the effort in the model id. When agy lists no Argon at the tier's effort, or the
# Argon run fails or writes nothing, the argon lane runs once on the roster's fallback, Gemini
# Neon at xhigh, and says so in the lane log. Override a model with FP_<LANE>_MODEL, e.g.
# FP_GROK_MODEL=grok-4.7 or FP_WONDER_FULL_MODEL=...; an override switches the fallback off.
#
# The astra lane runs the newest codex on the machine (latest_model.py codex; FP_CODEX_BIN wins):
# measured 18 Nov 2026, the standalone codex 0.163.0 refused gpt-6.2-astra while the CLI bundled
# with the ChatGPT app, 0.169.0, served it. The wonder lanes have read tools only: they read files
# anywhere, and refuse writes, shell and web fetches (measured 18 Nov 2026).
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
BRIEF= OUT= LANES= TIMEOUT=900 MINB=1
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
ROSTER=${0:A:h}/roster.py
[[ -n $LANES ]] || LANES=$("$ROSTER" lanes frontier)
[[ -f $BRIEF && -n $OUT && -n $LANES ]] || { print -u2 "usage: run_panel.sh --brief FILE --out DIR [--lanes $("$ROSTER" lanes frontier)] [--add-dir DIR]..."; exit 2; }
mkdir -p "$OUT"
PROMPT=$(<"$BRIEF")
limit() { perl -e 'alarm shift @ARGV; exec @ARGV' "$TIMEOUT" "$@"; }
LATEST=${0:A:h}/latest_model.py

run_lane() {
  local lane=$1 md="$OUT/$1.md" log="$OUT/$1.log" model rc eff
  : > "$md"
  eff=$("$ROSTER" effort "$lane" 2>/dev/null) || { print "unknown lane $lane" > "$log"; return 2; }
  case $lane in
    fable|opus) model=$("$ROSTER" model "$lane")
           # claude only reads outside its working directory (/tmp) with --add-dir; without it the
           # lane cannot open the files the brief names.
           local -a cadd; for d in $DIRS; do cadd+=(--add-dir "$d"); done
           # A one-line probe at the lane's own model and effort fails the lane in a minute when
           # the account cannot answer at all. Its output goes to the log, never to /dev/null:
           # measured 10 Nov 2026, the real failure was a fast terminal API error (409
           # no-eligible-account, needs_relogin) on every claude model, and discarding the probe
           # output made the log claim a 60s timeout and a 429 that never happened.
           # Setting sources (panel decision, 10 Nov 2026): FP_FABLE_SETTING_SOURCES=auto (the
           # default) probes with default sources first, so a working user-settings API key
           # keeps working; only on that terminal auth signature does it retry once with
           # project,local, which reaches the stored claude.ai login instead of a user-settings
           # key. =default or an explicit comma-separated list forces those sources and skips
           # the fallback. The brief runs once, on whichever sources the probe proved, and the
           # log records setting_sources= beside model=.
           local prc srcmode=${FP_FABLE_SETTING_SOURCES:-auto} srcsel=""
           local -a srcflag
           if [[ $srcmode == auto ]]; then
             perl -e 'alarm shift @ARGV; exec @ARGV' 60 claude --model "$model" --effort "$eff" -p "Reply with ok." < /dev/null > "$log" 2>&1
             prc=$?
             if (( prc == 0 )); then
               srcsel=default
             elif (( prc != 142 )) && grep -qE 'needs_relogin|no-eligible-account' "$log"; then
               print "probe: default sources failed (rc=$prc) with the terminal auth signature; retrying with project,local" >> "$log"
               perl -e 'alarm shift @ARGV; exec @ARGV' 60 claude --setting-sources project,local --model "$model" --effort "$eff" -p "Reply with ok." < /dev/null >> "$log" 2>&1
               prc=$?
               if (( prc == 0 )); then srcsel=project,local; srcflag=(--setting-sources project,local); fi
             fi
           elif [[ $srcmode == default ]]; then
             perl -e 'alarm shift @ARGV; exec @ARGV' 60 claude --model "$model" --effort "$eff" -p "Reply with ok." < /dev/null > "$log" 2>&1
             prc=$?
             if (( prc == 0 )); then srcsel=default; fi
           else
             perl -e 'alarm shift @ARGV; exec @ARGV' 60 claude --setting-sources "$srcmode" --model "$model" --effort "$eff" -p "Reply with ok." < /dev/null > "$log" 2>&1
             prc=$?
             if (( prc == 0 )); then srcsel=$srcmode; srcflag=(--setting-sources "$srcmode"); fi
           fi
           if [[ -n $srcsel ]]; then
             print "setting_sources=$srcsel" >> "$log"
             limit claude $srcflag --model "$model" --effort "$eff" $cadd -p "$PROMPT" < /dev/null > "$md" 2>> "$log"
           else
             print "probe failed (rc=$prc, sources=$srcmode): claude --model $model --effort $eff gave no usable answer; the probe output in this log is the reason. rc=142 is the 60s alarm kill; a fast non-zero exit is an account or API error to fix at the account (e.g. claude auth status), not a timeout." >> "$log"
             false
           fi;;
    astra) model=$("$ROSTER" model "$lane")
           local codex; codex=$("$LATEST" codex 2> "$log")
           print "codex=$codex" >> "$log"
           limit "$codex" exec -m "$model" -c model_reasoning_effort="$eff" -s read-only --skip-git-repo-check -o "$md" "$PROMPT" < /dev/null >> "$log" 2>&1;;
    argon|carbon|neon) : > "$log"
           local -a add; for d in $DIRS; do add+=(--add-dir "$d"); done
           # the resolver's notes (a failed listing, a fallback taken at lookup) stay in the lane log
           model=$("$ROSTER" model "$lane" 2>> "$log")
           limit agy --new-project --model "$model" $add -p "$PROMPT" > "$md" 2>> "$log"
           rc=$?
           # The lane's model unavailable at run time (refused, out of quota, empty answer): run the
           # brief once on the roster's fallback for this lane. Lanes without one, and a lane whose
           # model was pinned with FP_<LANE>_MODEL, do not fall back.
           local fb; fb=$("$ROSTER" fallback "$lane" 2>> "$log")
           if [[ -n $fb && $fb != $model ]] && { (( rc != 0 )) || [[ ! -s $md ]]; }; then
             print "$lane unavailable (model=$model rc=$rc, $(wc -c < "$md" | tr -d ' ') bytes); falling back to $fb" >> "$log"
             model=$fb
             limit agy --new-project --model "$model" $add -p "$PROMPT" > "$md" 2>> "$log"
             rc=$?
           fi
           (exit $rc);;
    grok)  model=$("$ROSTER" model "$lane" 2> "$log")
           limit grok -m "$model" --effort "$eff" -p "$PROMPT" > "$md" 2>> "$log";;
    wonder-full|wonder) model=$("$ROSTER" model "$lane")
           # Read tools only: no writes, no shell, no web, and untrusted approval. muse's --workspace
           # does not confine reads (measured 18 Nov 2026), so cutting the network is what stops a
           # planted instruction in a repo file from sending data anywhere but the model.
           limit muse exec --model "$model" --reasoning-effort "$eff" --disable-write --disable-shell \
             --disable-web-tools --approval-mode untrusted --no-session-log --workspace /tmp \
             "$PROMPT" < /dev/null > "$md" 2> "$log";;
    *) print "unknown lane $lane" > "$log"; return 2;;
  esac
  rc=$?
  print "model=$model" >> "$log"
  print "effort=$eff" >> "$log"
  print "rc=$rc" >> "$log"
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
    print "ok    $lane  $bytes bytes  $rc  $(grep -o 'model=.*' "$OUT/$lane.log" | tail -1)"
  fi
done
exit $failed

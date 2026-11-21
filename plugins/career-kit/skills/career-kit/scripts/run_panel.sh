#!/bin/zsh
# Run one review panel over a career artefact, controlling for option-order bias, and record
# every brief and answer where a later session can read them.
#
#   run_panel.sh --brief brief.md --out decisions/photo-panel [--brief-reversed brief-b.md]
#                [--add-dir /path/to/project]... [--lanes fable,astra,argon,grok,wonder]
#                [--timeout 900] [--min-bytes 600]
#
# This wraps `decision-panel:decision-panel`'s own runner rather than reimplementing the lanes,
# because that skill owns which model each lane resolves to and those identifiers go stale.
# Point FP_PANEL_RUNNER at the runner if it is not where this script looks.
#
# What it adds on top:
#
#   --brief-reversed  the same brief with the candidate options in the opposite order. Half
#                     the lanes get each, both into one output directory, so a verdict that
#                     is really a first-position preference shows up as a split. In the source
#                     session this was done by hand for two decisions; it is the only control
#                     on a panel that reads one ordering five times.
#
#   --min-bytes       an empty or truncated answer file is a LANE FAILURE, not a dissent. One
#                     Gemini lane returned an empty file after a headless permission denial and
#                     would otherwise have been counted as a silent "no".
#
# Briefs are files, not heredocs typed at the call site, and they are copied into --out beside
# the answers so the decision stays auditable. Give each lane absolute paths to the artefacts
# plus --add-dir for each directory, rather than pasting the content: the lanes read the real
# files, and the brief stays short enough to keep its instructions in view.
#
# Strip contact details from anything a brief points at. These lanes are other vendors' models.
set -u
BRIEF= BRIEF_B= OUT= LANES=fable,astra,argon,grok,wonder TIMEOUT=900 MINB=600
typeset -a DIRS
while (( $# )); do
  case $1 in
    --brief) BRIEF=$2; shift 2;;
    --brief-reversed) BRIEF_B=$2; shift 2;;
    --out) OUT=$2; shift 2;;
    --lanes) LANES=$2; shift 2;;
    --add-dir) DIRS+=("$2"); shift 2;;
    --timeout) TIMEOUT=$2; shift 2;;
    --min-bytes) MINB=$2; shift 2;;
    *) print -u2 "unknown argument: $1"; exit 2;;
  esac
done
[[ -f $BRIEF && -n $OUT ]] || {
  print -u2 "usage: run_panel.sh --brief FILE --out DIR [--brief-reversed FILE] [--add-dir DIR]..."
  exit 2; }

RUNNER=${FP_PANEL_RUNNER:-}
if [[ -z $RUNNER ]]; then
  for c in \
    "${CLAUDE_PLUGIN_ROOT:-}/../decision-panel/skills/decision-panel/scripts/run_panel.sh" \
    "$HOME/.claude/plugins/decision-panel/skills/decision-panel/scripts/run_panel.sh" \
    /Volumes/LLMs/Dev/fledgeling-plugins/plugins/decision-panel/skills/decision-panel/scripts/run_panel.sh
  do [[ -x $c ]] && { RUNNER=$c; break }; done
fi
[[ -n $RUNNER ]] || {
  print -u2 "no decision-panel runner found. Install the decision-panel plugin, or set"
  print -u2 "FP_PANEL_RUNNER to its scripts/run_panel.sh."
  exit 3; }

mkdir -p "$OUT"
typeset -a addflags; for d in $DIRS; do addflags+=(--add-dir "$d"); done
cp "$BRIEF" "$OUT/brief.md"

if [[ -n $BRIEF_B ]]; then
  cp "$BRIEF_B" "$OUT/brief-reversed.md"
  # Split the lanes: the first half read the brief as written, the rest read it reversed.
  typeset -a L; L=(${(s:,:)LANES}); half=$(( (${#L} + 1) / 2 ))
  A=${(j:,:)L[1,$half]}; B=${(j:,:)L[$((half+1)),-1]}
  print "forward  lanes: $A"
  print "reversed lanes: $B"
  "$RUNNER" --brief "$BRIEF"   --out "$OUT" --lanes "$A" $addflags \
            --timeout "$TIMEOUT" --min-bytes "$MINB" &
  pidA=$!
  "$RUNNER" --brief "$BRIEF_B" --out "$OUT" --lanes "$B" $addflags \
            --timeout "$TIMEOUT" --min-bytes "$MINB" &
  pidB=$!
  wait $pidA; rcA=$?
  wait $pidB; rcB=$?
  rc=$(( rcA || rcB ))
else
  "$RUNNER" --brief "$BRIEF" --out "$OUT" --lanes "$LANES" $addflags \
            --timeout "$TIMEOUT" --min-bytes "$MINB"
  rc=$?
fi

print "\nanswers in $OUT:"
for f in "$OUT"/*.md; do
  [[ $f == */brief*.md ]] && continue
  print "  $(basename $f)  $(wc -c < "$f" | tr -d ' ') bytes"
done
(( rc )) && print "\nA lane below --min-bytes is a lane failure, not a verdict. Read its .log,\nreport it as a failure, and tally the lanes that answered."
exit $rc

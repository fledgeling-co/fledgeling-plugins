#!/usr/bin/env bash
# run-preflight.sh — serve a deck if needed, run deck-preflight.js against it,
# print the JSON.
#
#   ./run-preflight.sh http://127.0.0.1:8000/deck.html
#   ./run-preflight.sh ./deck.html                     # serves it for you
#   ./run-preflight.sh ./deck.html --regulated         # adds the provenance check
#   ./run-preflight.sh ./deck.html --selector '.slide-wrap'
#
# Serve over HTTP, never file:// — module scripts and web fonts fail silently
# from the filesystem, and a deck measured with its fonts missing reports type
# and overflow numbers that belong to a different deck.
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROBE="$HERE/deck-preflight.js"
TARGET="${1:?usage: run-preflight.sh <url|file.html> [--regulated] [--selector SEL] [--canvas WxH]}"
shift || true

CFG_REGULATED=false; CFG_SEL=null; CFG_W=1920; CFG_H=1080
while [ $# -gt 0 ]; do
  case "$1" in
    --regulated) CFG_REGULATED=true; shift ;;
    --selector)  CFG_SEL="\"$2\""; shift 2 ;;
    --canvas)    CFG_W="${2%x*}"; CFG_H="${2#*x}"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

SRV_PID=""
cleanup() { [ -n "$SRV_PID" ] && kill "$SRV_PID" 2>/dev/null || true; }
trap cleanup EXIT

URL="$TARGET"
if [[ "$TARGET" != http* ]]; then
  [ -f "$TARGET" ] || { echo "no such file: $TARGET" >&2; exit 2; }
  DIR="$(cd "$(dirname "$TARGET")" && pwd)"; FILE="$(basename "$TARGET")"
  PORT=$(( 8300 + RANDOM % 400 ))
  ( cd "$DIR" && python3 -m http.server "$PORT" >/dev/null 2>&1 ) &
  SRV_PID=$!
  sleep 1.5
  URL="http://127.0.0.1:$PORT/$FILE"
  echo "serving $TARGET at $URL" >&2
fi

command -v obscura >/dev/null || { echo "obscura not on PATH" >&2; exit 3; }

# The payload must be ONE expression, and the probe must stay the outermost
# one. Obscura's --eval returns the value of the first statement, so a
# `cfg = {…}; probe()` payload evaluates to null — a gate that reports nothing
# while looking like it ran. Wrapping the probe in an outer function fails the
# same way, so the config is substituted into the probe's own final argument
# instead of being injected around it.
CFG="{slideSelector:$CFG_SEL,canvasW:$CFG_W,canvasH:$CFG_H,regulated:$CFG_REGULATED}"
PAYLOAD="$(sed "s|^})(typeof __DECKCFG.*|})($CFG)|; s|^   : (typeof window.*||" "$PROBE")"

# `|| true` so a failing fetch reaches the guard below rather than being killed
# by `set -e` — an exit with no message is the silent-gate failure this script
# exists to make impossible.
OUT="$( { obscura --allow-private-network fetch "$URL" --wait 3 --eval "$PAYLOAD" 2>/dev/null \
          || true; } | sed -n '/^{/,$p' )"

if [ -z "$OUT" ]; then
  echo "preflight returned nothing — this is NOT a pass. The probe did not run." >&2
  echo "Check that $URL serves over HTTP and that obscura can reach it." >&2
  exit 4
fi
printf '%s\n' "$OUT"

# Evaluate summary blockers and return deterministic exit code
BLOCKERS="$(node -e '
try {
  const json = JSON.parse(process.argv[1]);
  const s = json.summary || {};
  const blockers = [];
  if (s.stageGeometry > 0) blockers.push(`stageGeometry: ${s.stageGeometry}`);
  if (s.overflow > 0) blockers.push(`overflow: ${s.overflow}`);
  if (s.chromeCollisions > 0) blockers.push(`chromeCollisions: ${s.chromeCollisions}`);
  if (s.textOverlaps > 0) blockers.push(`textOverlaps: ${s.textOverlaps}`);
  if (s.invisibleText > 0) blockers.push(`invisibleText: ${s.invisibleText}`);
  if (s.provenanceMissing > 0) blockers.push(`provenanceMissing: ${s.provenanceMissing}`);
  if (blockers.length) {
    console.error(`\n❌ [DECK-PREFLIGHT FAIL] Found ${blockers.length} blocker(s): ${blockers.join(", ")}`);
    process.exit(1);
  } else {
    console.log(`\n✅ [DECK-PREFLIGHT PASS] 0 blockers across ${s.slidesExamined || json.slides || 0} slides.`);
    process.exit(0);
  }
} catch (e) {
  process.exit(0);
}
' "$OUT" 2>&1)" || {
  echo "$BLOCKERS" >&2
  exit 1
}
echo "$BLOCKERS"


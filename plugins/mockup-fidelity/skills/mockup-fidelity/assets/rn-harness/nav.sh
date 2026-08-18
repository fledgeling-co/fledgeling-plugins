#!/usr/bin/env bash
# Fast nav helper for an RN mockup-fidelity audit — DEEP-LINK FIRST.
#
# WHY: each `maestro test` spins up a fresh XCUITest driver (`xcodebuild
# test-without-building` → connect to sim) costing ~15-20s BEFORE the flow runs.
# Agents call Maestro once per action (tab tap, scroll-to-element, assert), so a
# single screen pays that tax ~8-9×. In one audit Maestro was ~70% of all
# wall-clock. A deep link is ~0.5s; an idb tap ~0.3s. expo-router (and most RN
# routers) map route files to <scheme>:// URLs out of the box — route GROUPS in
# parens ((tabs)/(screens)) are stripped from the URL — so deep-linking replaces
# almost all tab + screen + detail navigation. Keep idb for the few routeless
# affordances (a custom header control, a sheet); keep Maestro only for a sheet
# with no stable coords, and BATCH all its taps into ONE flow file.
#
# Configure per app via env (no defaults — set these for YOUR app):
#   MF_SIM     sim udid
#   MF_DUMP    harness dump path (the collector's _latest.json, OUTSIDE the watch root)
#   MF_SCHEME  url scheme        (e.g. myapp)
#   MF_BUNDLE  app bundle id     (e.g. com.example.myapp)
#
# Usage:
#   nav.sh prime                         # ONCE per device: clear the iOS "Open in <app>?" deep-link confirmation
#   nav.sh open  <route|url> [anchor]    # deep-link any tab/screen, poll-settle on a unique text
#   nav.sh tab   <name> [anchor]         # deep-link a tab by its router name
#   nav.sh detail <listRoute> [rowIndex=0] [anchor]   # deep-link a list + idb-tap the Nth row (no id needed)
#   nav.sh tap   <x> <y>                 # raw idb tap (points)
#   nav.sh settle [anchor] [maxSec=15]
set -uo pipefail
: "${MF_SIM:?set MF_SIM}"; : "${MF_DUMP:?set MF_DUMP}"; : "${MF_SCHEME:?set MF_SCHEME}"; : "${MF_BUNDLE:?set MF_BUNDLE}"
SIM="$MF_SIM"; DUMP="$MF_DUMP"; SCHEME="$MF_SCHEME"; BUNDLE="$MF_BUNDLE"

nodecount() { python3 -c "import json;print(len(json.load(open('$DUMP'))))" 2>/dev/null || echo 0; }
has_text() { python3 -c "
import json,sys
try: d=json.load(open('$DUMP'))
except: sys.exit(1)
ts=' '.join(str(n.get('text') or '') for n in d)
sys.exit(0 if '''$1''' in ts else 1)" 2>/dev/null; }

# The native 'Open in <app>?' deep-link confirmation is a UIKit alert — the RN
# harness dump can NEVER see it, so a stalled settle may mean it's blocking. Tap
# it via Maestro (once per device it's gone). Buttons observed: Open / Allow.
clear_open_confirm() {
  local f; f="$(mktemp /tmp/mf-openconfirm-XXXX.yaml)"
  printf 'appId: %s\n---\n- tapOn: { text: "Open", optional: true }\n- tapOn: { text: "Allow", optional: true }\n' "$BUNDLE" > "$f"
  maestro --device "$SIM" test "$f" >/dev/null 2>&1; rm -f "$f"
}

settle() {  # [anchor] [maxSec] — polls the dump; CAVEAT: RN keeps all screens mounted, so a
            # merged-dump anchor can read true before the foreground transition completes (a
            # ~2s floor is applied by callers). Always screenshot to CONFIRM the surface.
  local anchor="${1:-}" max="${2:-15}" i=0 prev=-1 stable=0 tried=0
  while [ "$i" -lt "$max" ]; do
    if [ -n "$anchor" ] && has_text "$anchor"; then echo "settled (anchor '$anchor')"; return 0; fi
    local n; n=$(nodecount)
    if [ "$n" = "$prev" ] && [ "$n" -gt 50 ] 2>/dev/null; then stable=$((stable+1)); else stable=0; fi
    [ "$stable" -ge 2 ] && [ -z "$anchor" ] && { echo "settled (stable $n nodes)"; return 0; }
    if [ "$tried" -eq 0 ] && [ "$i" -ge 5 ] && { [ -n "$anchor" ] || [ "$n" -le 50 ]; }; then clear_open_confirm; tried=1; fi
    prev="$n"; sleep 1; i=$((i+1))
  done
  echo "settle timeout (${max}s; nodes=$(nodecount), anchor='${anchor:-none}')"; return 1
}

open_url() { local u="$1"; case "$u" in ${SCHEME}://*) ;; *) u="${SCHEME}:///${u#/}";; esac; xcrun simctl openurl "$SIM" "$u" >/dev/null 2>&1; echo "$u"; }

case "${1:-}" in
  prime)
    echo "priming deep-link confirmation for ${BUNDLE} on ${SIM} ..."
    xcrun simctl openurl "$SIM" "${SCHEME}:///" >/dev/null 2>&1; sleep 2
    clear_open_confirm; sleep 1; clear_open_confirm
    echo "primed (subsequent deep links won't prompt)" ;;
  open)    echo "deep-link → $(open_url "$2")"; sleep 2; settle "${3:-}" ;;
  tab)     xcrun simctl openurl "$SIM" "${SCHEME}:///$2" >/dev/null 2>&1; echo "tab → $2"; sleep 2; settle "${3:-}" ;;
  detail)
    list="$2"; idx="${3:-0}"; anchor="${4:-}"
    open_url "${list#/}" >/dev/null; settle "" 10 >/dev/null
    Y=$(python3 -c "
import json
d=json.load(open('$DUMP'))
# list rows = pressable nodes in the content band (below appbar/tab strip), sorted top→bottom.
# press is a bool; a11y is a label string; role is top-level.
rows=[n for n in d if n.get('press') and 40<=(n.get('rect') or {}).get('h',0)<=140 and n['rect']['y']>150]
rows=sorted(rows,key=lambda n:n['rect']['y'])
i=$idx
print(int(rows[i]['rect']['y']+rows[i]['rect']['h']/2)) if i<len(rows) else print(360)" 2>/dev/null || echo 360)
    idb ui tap --udid "$SIM" 200 "${Y}" 2>/dev/null; echo "detail → ${list} row ${idx} @y=${Y}"; settle "$anchor" ;;
  tap)     idb ui tap --udid "$SIM" "$2" "$3" 2>/dev/null; echo "tap $2,$3"; settle "" 5 ;;
  settle)  settle "${2:-}" "${3:-15}" ;;
  *) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1 ;;
esac

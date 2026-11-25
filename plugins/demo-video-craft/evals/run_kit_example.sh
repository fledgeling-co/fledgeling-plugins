#!/bin/bash
# The kit, end to end on its example series: start a series (fetching the pinned fonts and GSAP), write the screens
# and the film table, build all four films without voice (a short in Claude, one in the product's own browser window,
# a 9:16 one on a phone, and the overview), check each, then render two shorts through render.py, which stages them
# and stops: a voiced cut without a voice is not published. Exit 0 only when every step does. Needs python3, node
# (npx), ffmpeg, network for the fetch, and MOTION_CRAFT_SCRIPTS pointing at the scripts folder of motion-craft.
set -euo pipefail
E="$(cd "$(dirname "$0")" && pwd)"
S="$(cd "$E/../skills/demo-video-craft/scripts" && pwd)"
: "${MOTION_CRAFT_SCRIPTS:?set MOTION_CRAFT_SCRIPTS to the scripts folder of motion-craft}"
HF="$MOTION_CRAFT_SCRIPTS/hf.sh"
T="$(mktemp -d)/series"
python3 "$S/new_series.py" "$T" --fetch > /dev/null
cd "$T"
python3 states.py > /dev/null
python3 films.py
for f in O K01 K02 K03; do
  python3 _kit/engine/build.py . "$f" --mute-only > "build-$f.log"
  (cd "films/$f" && "$HF" check --json > "../../check-$f.json" 2>&1)
  python3 "$E/hf_check_ok.py" "check-$f.json"
done
python3 _kit/engine/render.py . --films K01,K03 --mute-only
for f in K01 K03; do
  printf '%s %s ' "$f" "$(ffprobe -v error -show_entries stream=width,height -of csv=p=0:s=x -select_streams v:0 "staging/acme-$f.mp4")"
  python3 "$MOTION_CRAFT_SCRIPTS/pop_scan.py" "staging/acme-$f.mp4" --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(f\"pops {d['pops']}, still runs {d['still_runs']}\")"
done
echo "kit example: PASS ($T)"

#!/bin/bash
# The starter kit, end to end on its example series: start a series (fetching the pinned fonts and GSAP), write the
# screens and the film table, build both films without voice, check them, render the short, make its voiced cut and
# gate it. Exit 0 only when every step does. Needs python3, node (npx), ffmpeg, network for the fetch, and
# MOTION_CRAFT_SCRIPTS pointing at motion-craft's scripts/ folder.
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
for f in O K01; do
  python3 _kit/engine/build.py . "$f" --mute-only > "build-$f.log"
  (cd "films/$f" && "$HF" check --json > "../../check-$f.json" 2>&1)
  python3 "$E/hf_check_ok.py" "check-$f.json"
done
mkdir -p out
(cd films/K01 && "$HF" render -q delivery -o "$T/out/acme-K01.mp4" > ../../render.log 2>&1)
python3 "$S/delivery.py" remux --master out/acme-K01.mp4 --audio films/K01/assets/sound_vo.wav --out out/acme-K01-vo.mp4 > /dev/null
python3 "$S/delivery.py" check --dir out --prefix acme --films K01
echo "kit example: PASS ($T)"

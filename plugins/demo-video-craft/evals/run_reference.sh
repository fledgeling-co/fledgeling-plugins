#!/bin/bash
# The reference series, rebuilt with nothing but the kit and measured against its published files.
#   run_reference.sh <published films dir> <voice dir> <music dir>
# The voice dir holds the series' 18 generated lines (<line>.wav/.json/.mp3); the music dir overview.wav and
# shorts.wav. Prints compare_films.py's verdict; exit 0 only when all ten films pass. Needs MOTION_CRAFT_SCRIPTS, node,
# ffmpeg and network (fonts, GSAP, marks). About ten minutes on an Apple-silicon laptop.
set -euo pipefail
[ $# -eq 3 ] || { echo "usage: run_reference.sh <published films dir> <voice dir> <music dir>"; exit 2; }
PUB="$(cd "$1" && pwd)"; VOICE="$(cd "$2" && pwd)"; MUSIC="$(cd "$3" && pwd)"
S="$(cd "$(dirname "$0")/../skills/demo-video-craft/scripts" && pwd)"
: "${MOTION_CRAFT_SCRIPTS:?set MOTION_CRAFT_SCRIPTS to the scripts folder of motion-craft}"
T="$(mktemp -d)/reference"
python3 "$S/new_series.py" "$T" --reference --fetch > /dev/null
cd "$T"
python3 fetch_marks.py > /dev/null
mkdir -p voice music
cp "$VOICE"/*.wav "$VOICE"/*.json voice/
cp "$MUSIC"/overview.wav "$MUSIC"/shorts.wav music/
python3 states.py > /dev/null
python3 films.py
python3 _kit/engine/render.py . --to out
python3 "$S/compare_films.py" --a out --b "$PUB" --prefix guardian3 --films O,K02,K03,K04,K05,K06,K07,K08,K09,K10

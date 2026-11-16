#!/usr/bin/env bash
# Deterministic preparation for one video: download, frames, sheets, measurements, metrics.
#   tools/prep.sh <youtube-id>
# Idempotent: each step is skipped when its output already exists.
set -uo pipefail
ID="$1"
ROOT="$HOME/Movies/motion-craft-corpus"
TOOLS="$ROOT/tools"
DIR="$ROOT/$ID"
PLUGINS="${FLEDGELING_PLUGINS:?set FLEDGELING_PLUGINS to your fledgeling-plugins checkout}"
HF="$PLUGINS/plugins/motion-craft/skills/motion-craft/scripts/hf.sh"
BMW="$PLUGINS/plugins/be-my-witness/skills/be-my-witness/scripts"
mkdir -p "$DIR/frames" "$DIR/sheets" "$DIR/measure"
cd "$DIR" || exit 2
log() { printf '[prep %s] %s\n' "$ID" "$*"; }

if [ ! -s video.mp4 ]; then
  log "download"
  ok=0
  for wait in 0 30 90; do
    sleep "$wait"
    if /opt/homebrew/bin/yt-dlp --no-update -q --no-progress \
      -f 'bv*[height<=720]+ba/b[height<=720]' --merge-output-format mp4 \
      --write-info-json -o 'video.%(ext)s' "https://www.youtube.com/watch?v=$ID"; then ok=1; break; fi
    log "download attempt failed; retrying after a pause"
  done
  [ "$ok" = 1 ] || { log "DOWNLOAD FAILED"; echo '{"prep":"download_failed"}' > measure/prep-status.json; exit 3; }
fi

if [ ! -s frames/f0001.jpg ]; then
  log "frames: 1 every 2 s, clean, 1280 wide"
  ffmpeg -v error -i video.mp4 -vf "fps=0.5,scale=1280:-2" -q:v 3 frames/f%04d.jpg
fi

if [ ! -s sheets/sheet-01.jpg ]; then
  log "contact sheets: 16 frames each, timestamp burned in"
  ffmpeg -v error -i video.mp4 -vf "fps=0.5,scale=480:-2,drawtext=text='%{pts\:hms}':x=6:y=6:fontsize=18:fontcolor=yellow:box=1:boxcolor=black@0.7,tile=4x4:padding=4:color=gray" -q:v 3 sheets/sheet-%02d.jpg
fi

[ -s measure/probe.json ]  || "$HF" measure probe video.mp4 --json > measure/probe.json 2>/dev/null
[ -s measure/cuts.json ]   || { log "cuts";   "$HF" measure cuts video.mp4 --json > measure/cuts.json 2>/dev/null; }
[ -s measure/events.json ] || { log "events"; "$HF" measure events video.mp4 --map --json > measure/events.json 2>/dev/null; }
[ -s measure/look.json ]   || "$HF" measure look video.mp4 --json > measure/look.json 2>/dev/null
[ -s measure/audio.json ]  || { log "audio (local only)"; "$HF" audio video.mp4 --only kind,loudness,silence,onsets,bpm,beats,sections,describe --json > measure/audio.json 2>/dev/null; }
[ -s measure/ebur128.txt ] || ffmpeg -hide_banner -nostats -i video.mp4 -af ebur128=peak=true -f null - 2>&1 | sed -n '/Summary:/,$p' > measure/ebur128.txt
if [ ! -s measure/strips.json ]; then
  log "event strips at native frame rate"
  "$HF" measure frames video.mp4 --events --out strips --width 480 > measure/strips.json 2>/dev/null
fi

if [ ! -s measure/frames-scan.json ]; then
  log "be-my-witness prescan + consecutive diffmask over every sampled frame"
  /opt/homebrew/bin/python3.14 -P "$TOOLS/scan_frames.py" "$DIR" "$BMW" > measure/frames-scan.tmp && mv measure/frames-scan.tmp measure/frames-scan.json \
    || { log "FRAME SCAN FAILED"; rm -f measure/frames-scan.tmp; echo '{"prep":"scan_failed"}' > measure/prep-status.json; exit 4; }
fi
# remove any zero-byte measurement so a re-run retries it
find measure -size 0 -delete

log "metrics"
/opt/homebrew/bin/python3.14 -P "$TOOLS/analyze.py" "$DIR" > measure/metrics.json && echo '{"prep":"ok"}' > measure/prep-status.json
log "done: $(ls frames | wc -l | tr -d ' ') frames, $(ls sheets | wc -l | tr -d ' ') sheets, $(ls strips 2>/dev/null | wc -l | tr -d ' ') strips"

#!/usr/bin/env bash
# Run the pinned HyperFrames CLI with telemetry and skill installs switched off.
#   scripts/hf.sh <command> [args...]      e.g. scripts/hf.sh render -o out/film.mp4
# HYPERFRAMES_VERSION overrides the pin after you have validated a newer release.
set -euo pipefail
export HYPERFRAMES_NO_TELEMETRY=1 DO_NOT_TRACK=1 HYPERFRAMES_SKIP_SKILLS=1
exec npx --yes "hyperframes@${HYPERFRAMES_VERSION:-0.9.52}" "$@"

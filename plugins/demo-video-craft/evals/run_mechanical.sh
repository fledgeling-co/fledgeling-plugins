#!/bin/bash
# The checks demo-video-craft ships with: each script's self-test, which builds its own fixtures and proves the
# gate fails on a known-bad case. Exit 0 only when all eight pass. Needs python3, ffmpeg and ffprobe; no network.
cd "$(dirname "$0")/../skills/demo-video-craft/scripts" || exit 2
fail=0
for s in gateway_audio.py duck.py site_urls.py delivery.py edgar.py new_series.py sync_table.py series_lint.py; do
  printf '%-18s ' "$s"
  python3 "$s" --self-test 2>&1 | tail -1
  rc=${PIPESTATUS[0]}
  [ "$rc" -eq 0 ] || fail=1
done
[ $fail -eq 0 ] && echo "mechanical: PASS 8/8" || echo "mechanical: FAIL"
exit $fail

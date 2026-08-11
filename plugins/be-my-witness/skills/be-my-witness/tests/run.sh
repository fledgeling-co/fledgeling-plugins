#!/usr/bin/env bash
# Regression tests for the deterministic layer. Each fixture asserts one thing the
# pre-scan must get right; all four were wrong on the first calibration, which is
# why they are pinned here rather than trusted.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0
check() { # name, file, expected exit code
  python3 scripts/prescan.py "tests/fixtures/$2" >/dev/null 2>&1
  local got=$?
  if [ "$got" != "$3" ]; then echo "FAIL $1: expected exit $3, got $got"; fail=1; else echo "ok   $1"; fi
}
check "a loading skeleton is not evidence"  skeleton.png  2
check "a blank capture is not evidence"     blank.png     2
check "a populated surface proceeds"        populated.png 0

python3 scripts/prescan.py tests/fixtures/card.png --reference tests/fixtures/populated.png 2>/dev/null \
  | grep -q "framingComparable: False" \
  && echo "ok   a card against a viewport is framing, not drift" \
  || { echo "FAIL framing check did not fire"; fail=1; }

python3 scripts/crop.py tests/fixtures/populated.png --pair tests/fixtures/card.png \
  --region 0,0,300,200 --scale 2 --out /tmp/bmw-pair.png >/dev/null 2>&1 \
  && [ -s /tmp/bmw-pair.png ] \
  && echo "ok   paired crop writes a real image" \
  || { echo "FAIL paired crop produced nothing"; fail=1; }

exit $fail

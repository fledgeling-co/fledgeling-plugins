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

out=$(python3 scripts/prescan.py tests/fixtures/card.png --reference tests/fixtures/populated.png 2>/dev/null)
case "$out" in
  *"framingComparable: False"*) echo "ok   a card against a viewport is framing, not drift" ;;
  *) echo "FAIL framing check did not fire"; fail=1 ;;
esac

python3 scripts/crop.py tests/fixtures/populated.png --pair tests/fixtures/card.png \
  --region 0,0,300,200 --scale 2 --out /tmp/bmw-pair.png >/dev/null 2>&1 \
  && [ -s /tmp/bmw-pair.png ] \
  && echo "ok   paired crop writes a real image" \
  || { echo "FAIL paired crop produced nothing"; fail=1; }

# The founding incident, pinned with the numbers from the docstring: a 440x275 card
# against a 1440x900 viewport. Both are aspect 1.6, so the aspect check alone passes
# it and the script missed the exact case it was written for. The case above only
# ever failed on aspect (1.6 vs populated.png's 2.4), so it never covered this.
python3 scripts/prescan.py tests/fixtures/card.png --reference tests/fixtures/table-2px-defect.png \
  >/dev/null 2>&1
[ $? = 2 ] \
  && echo "ok   a same-aspect crop is framing, and does not proceed" \
  || { echo "FAIL same-aspect crop (440x275 vs 1440x900) still proceeds"; fail=1; }

# The other side of that fix: the skill mandates deviceScaleFactor >= 2, so a 2x
# render of the reference must stay comparable. If this fails, the scale check is
# too tight and every healthy retina capture is a false alarm.
python3 scripts/prescan.py tests/fixtures/retina-2x.png --reference tests/fixtures/populated.png \
  >/dev/null 2>&1
[ $? = 0 ] \
  && echo "ok   a 2x render of the reference is not framing" \
  || { echo "FAIL a legitimate 2x capture was flagged as framing"; fail=1; }

# A PARTIAL skeleton -- an app shell that painted while one region streamed -- passes
# the settled rule, because that rule needs contentfulCells < 0.06 and the shell is
# real content. Both halves are pinned: the exit code stays 0 (so nobody "fixes" this
# into a gate and false-alarms every modal scrim), and largestFaintRegion must report
# it, because the note is the only thing that catches this case.
ps=$(python3 scripts/prescan.py tests/fixtures/partial-skeleton.png --json 2>/dev/null)
rc=$?
if [ "$rc" != 0 ]; then
  echo "FAIL partial skeleton should still proceed (advisory, not a gate), got exit $rc"; fail=1
elif printf '%s' "$ps" | python3 -c "import json,sys; d=json.load(sys.stdin); c=d['checks']; sys.exit(0 if c['settled'] and c['largestFaintRegion']>=0.15 and any('contiguous faint region' in n for n in d['notes']) else 1)"; then
  echo "ok   a partial skeleton passes the gate and is reported anyway"
else
  echo "FAIL partial skeleton was not reported by largestFaintRegion"; fail=1
fi

# A localised change sits under the whole-frame ratio, so the exit code cannot see
# it. Density is what tells one solid edit from scattered anti-aliasing.
dm=$(python3 scripts/diffmask.py tests/fixtures/pair-a.png tests/fixtures/pair-b.png --json 2>/dev/null)
if printf '%s' "$dm" | python3 -c "import json,sys; d=json.load(sys.stdin); sys.exit(0 if d.get('diffBox') and d.get('diffBoxDensity',0) > 0 else 1)"; then
  echo "ok   diffmask locates the change, not just counts it"
else
  echo "FAIL diffmask reported no diffBox/density"; fail=1
fi

exit $fail

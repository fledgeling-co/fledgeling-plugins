#!/usr/bin/env bash
# Prove every bundled check can fail as well as pass, on fixtures that ship with the skill.
#
#   scripts/self_test.sh            # exit 0 when every check behaves
#
# A check that cannot fail is the most expensive kind: it reports green over the defect it exists
# for. Each case below runs a gate on a clean fixture (expect exit 0) and on a fixture with the
# defect planted (expect exit 1 and the named finding). Needs python3 and ffmpeg; the browser
# capture is exercised separately because it needs Playwright and a served page.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
FIX="$HERE/../tests/fixtures"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0
ok()  { echo "ok    $1"; pass=$((pass + 1)); }
bad() { echo "FAIL  $1"; fail=$((fail + 1)); }
expect() { # expect <exit> <grep-pattern-or-empty> <label> -- command...
  local want="$1" pat="$2" label="$3"; shift 4
  local out code
  out="$("$@" 2>&1)"; code=$?
  if [[ "$code" != "$want" ]]; then bad "$label (exit $code, wanted $want)"; echo "$out" | tail -5; return; fi
  if [[ -n "$pat" ]] && ! grep -qE "$pat" <<<"$out"; then bad "$label (no '$pat' in output)"; return; fi
  ok "$label"
}

# plan_check: the example passes; each mutation fails on its own named rule
python3 "$HERE/plan_check.py" --example > "$TMP/plan.json"
expect 0 "" "plan_check passes the example plan" -- python3 "$HERE/plan_check.py" "$TMP/plan.json"
mutate() { python3 - "$TMP/plan.json" "$TMP/$1.json" "$2" <<'EOF'
import json, sys
p = json.load(open(sys.argv[1])); exec(sys.argv[3], {"p": p}); json.dump(p, open(sys.argv[2], "w"))
EOF
}
mutate notrawl 'del p["trawl"]'
expect 1 "no trawl block" "plan_check fails a plan with no trawl run" -- python3 "$HERE/plan_check.py" "$TMP/notrawl.json"
mutate nogold 'p["sections"][1].pop("mobbin")'
expect 1 "no mobbin block" "plan_check fails a section with no shipped reference" -- python3 "$HERE/plan_check.py" "$TMP/nogold.json"
mutate nomotion 'p["sections"][0]["motion"].pop("reducedMotion")'
expect 1 "motion.reducedMotion is missing" "plan_check fails a section with no reduced-motion line" -- python3 "$HERE/plan_check.py" "$TMP/nomotion.json"
mutate beats 'p["hero"]["settled"]["runtimeSeconds"] = 12'
expect 1 "beats add up to" "plan_check fails beats that do not add up to the runtime" -- python3 "$HERE/plan_check.py" "$TMP/beats.json"
mutate rest 'p["hero"]["settled"].pop("restingFrame")'
expect 1 "restingFrame is missing" "plan_check fails a video hero with no resting frame" -- python3 "$HERE/plan_check.py" "$TMP/rest.json"
mutate threed 'p["hero"] = {"kind": "3d", "plainFallback": "still render", "threeD": {"source": "three-scene"}}'
expect 1 "threeD.why is missing" "plan_check fails a 3D hero that does not say why it needs real-time 3D" -- python3 "$HERE/plan_check.py" "$TMP/threed.json"
mutate effects 'p["effects"][0].update(iterations=4, plainOffered=False)'
expect 1 "plain version not offered" "plan_check fails an effect iterated past two without offering plain" -- python3 "$HERE/plan_check.py" "$TMP/effects.json"

# site_audit: the clean site passes; the planted site raises each defect
expect 0 "" "site_audit passes the clean site in deploy mode" -- python3 "$HERE/site_audit.py" "$FIX/good" --deploy --private "$FIX/private.txt"
for pat in "does not resolve" "has no alt" "lacks muted" "lacks playsinline" "has no poster" "never reads prefers-reduced-motion" \
           "no availability check or fallback" "review tool still in a deploy build" "private string" "has no pause control"; do
  expect 1 "$pat" "site_audit catches: $pat" -- python3 "$HERE/site_audit.py" "$FIX/bad" --deploy --private "$FIX/private.txt"
done

# clip_tools: a smooth clip has no jump; a hard cut is found
ffmpeg -v error -y -f lavfi -i "testsrc2=size=320x180:rate=24:duration=2" -pix_fmt yuv420p "$TMP/smooth.mp4"
ffmpeg -v error -y -f lavfi -i "color=c=0xF4F1EA:size=320x180:rate=24:duration=1" -pix_fmt yuv420p "$TMP/flat.mp4"
printf "file '%s'\nfile '%s'\n" "$TMP/smooth.mp4" "$TMP/flat.mp4" > "$TMP/list.txt"
ffmpeg -v error -y -f concat -safe 0 -i "$TMP/list.txt" -c copy "$TMP/cut.mp4"
expect 0 '"jumps": \[\]' "clip_tools finds no jump in a smooth clip" -- python3 "$HERE/clip_tools.py" joins "$TMP/smooth.mp4"
expect 1 '"frame"' "clip_tools finds the jump at a hard join" -- python3 "$HERE/clip_tools.py" joins "$TMP/cut.mp4"

# clip_tools: a clip that does not return to its start fails the seam; a strobe fails the flash proxy
ffmpeg -v error -y -f lavfi -i "color=c=white:size=320x180:rate=24:duration=1" -vf "geq=lum='if(lt(mod(N\,4)\,2)\,20\,235)':cb=128:cr=128" -pix_fmt yuv420p "$TMP/strobe.mp4"
expect 0 '"jump": false' "clip_tools passes the seam of a still loop" -- python3 "$HERE/clip_tools.py" seam "$TMP/flat.mp4"
expect 1 '"jump": true' "clip_tools fails a loop whose last frame does not meet its first" -- python3 "$HERE/clip_tools.py" seam "$TMP/smooth.mp4"
expect 0 '"fails": false' "clip_tools passes a clip with no flashes" -- python3 "$HERE/clip_tools.py" flashes "$TMP/smooth.mp4"
expect 1 '"fails": true' "clip_tools flags more than three flashes a second" -- python3 "$HERE/clip_tools.py" flashes "$TMP/strobe.mp4"

# deploy_check media/access: a server that ignores Range fails; one that answers 206 passes
head -c 4096 /dev/urandom > "$TMP/clip.mp4"
python3 "$FIX/range_server.py" "$TMP" > "$TMP/range.port" &
RANGE=$!
python3 -m http.server 8977 --bind 127.0.0.1 --directory "$TMP" > /dev/null 2>&1 &
PLAIN=$!
for _ in 1 2 3 4 5 6 7 8 9 10; do [[ -s "$TMP/range.port" ]] && curl -s -o /dev/null http://127.0.0.1:8977/ && break; perl -e 'select(undef,undef,undef,0.3)'; done
RP=$(head -1 "$TMP/range.port")
expect 1 "FAIL" "deploy_check fails a media server that ignores range requests" -- python3 "$HERE/deploy_check.py" media "http://127.0.0.1:8977/clip.mp4"
expect 0 "1 of 1" "deploy_check passes a media server that answers 206" -- python3 "$HERE/deploy_check.py" media "http://127.0.0.1:$RP/clip.mp4"
expect 1 "FAIL" "deploy_check fails a URL expected private that answers 200" -- python3 "$HERE/deploy_check.py" access "http://127.0.0.1:8977/clip.mp4" --expect private
kill $PLAIN $RANGE 2>/dev/null

# spend: a cap that is reached stops the next billed call
L="$TMP/spend.json"
python3 "$HERE/spend.py" add --ledger "$L" --what clip --model test --unit second --price 0.5 --units 8 > /dev/null
expect 0 "running total" "spend reports under a cap" -- python3 "$HERE/spend.py" total --ledger "$L" --cap 10
expect 1 "of a" "spend fails once the cap is reached" -- python3 "$HERE/spend.py" total --ledger "$L" --cap 4

echo "RESULT: $pass passed, $fail failed"
[[ $fail -eq 0 ]]

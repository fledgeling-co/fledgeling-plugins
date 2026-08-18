#!/usr/bin/env bash
# Gate tests for campaign.py and strict-check.py.
#
# The skill's own standing rule is that a check nobody has watched fail is not
# known to bite. That applies to the gate itself, so every blocker here is
# proved to fire on a fixture built to trip it, and then the same campaign is
# resolved and proved to clear. A gate that always fails is no more useful than
# one that always passes, so both directions are asserted.
#
#   ./tests/run.sh            # quiet unless something fails
#   ./tests/run.sh -v         # show each gate's output
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
S="$HERE/../skills/test-campaign/scripts"
VERBOSE="${1:-}"
PASS=0; FAIL=0
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

say() { [ "$VERBOSE" = "-v" ] && echo "$@"; return 0; }

# Assert the gate's exit code, and that its output mentions a distinguishing
# phrase. Exit code alone would not prove the *right* blocker fired.
expect() {
  local label="$1" want="$2" dir="$3" phrase="${4:-}"
  local out rc
  out="$(python3 "$S/campaign.py" check "$dir" 2>&1)"; rc=$?
  if [ "$rc" != "$want" ]; then
    echo "FAIL  $label: exit $rc, wanted $want"; echo "$out" | sed 's/^/      /'
    FAIL=$((FAIL+1)); return
  fi
  if [ -n "$phrase" ] && ! grep -qF -- "$phrase" <<<"$out"; then
    echo "FAIL  $label: exit $rc as wanted, but nothing said \"$phrase\""
    echo "$out" | sed 's/^/      /'
    FAIL=$((FAIL+1)); return
  fi
  say "ok    $label"; PASS=$((PASS+1))
}

png() { # png <path> <w> <h> <r> <g> <b>  — a real PNG, distinct per colour
  python3 - "$@" <<'PY'
import zlib, struct, sys, pathlib
path, w, h, r, g, b = sys.argv[1], *map(int, sys.argv[2:7])
raw = b"".join(b"\x00" + bytes((r, g, b)) * w for _ in range(h))
def chunk(t, d):
    c = t + d
    return struct.pack(">I", len(d)) + c + struct.pack(">I", zlib.crc32(c))
pathlib.Path(path).parent.mkdir(parents=True, exist_ok=True)
pathlib.Path(path).write_bytes(
    b"\x89PNG\r\n\x1a\x0a"
    + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0))
    + chunk(b"IDAT", zlib.compress(raw, 9))
    + chunk(b"IEND", b""))
PY
}

# ── an empty campaign must not clear ────────────────────────────────────────
E="$WORK/empty"
python3 "$S/campaign.py" init "$E" --project Empty --lanes web >/dev/null
expect "an empty campaign is not a passing one" 1 "$E" "no cases at all"

# ── the on-glass and raster fixtures ───────────────────────────────────────
C="$WORK/glass"
python3 "$S/campaign.py" init "$C" --project Glass --lanes web,macos-glass >/dev/null
echo '[{"id":"REQ-001","class":"behaviour","text":"the dashboard renders live data"}]' >"$WORK/r.json"
echo '[{"label":"Dashboard"}]' >"$WORK/s.json"
echo '[{"label":"Publish","critical":true}]' >"$WORK/f.json"
for k in requirement surface flow; do
  python3 "$S/campaign.py" add "$C" --kind $k --file "$WORK/${k:0:1}.json" >/dev/null
done

png "$C/shots/a.png" 400 300 10 20 30
png "$C/shots/dup.png" 400 300 10 20 30      # byte-identical to a.png
png "$C/shots/tiny.png" 1 1 0 0 0
printf '<html>502 Bad Gateway</html>' >"$C/shots/notimage.png"
: >"$C/shots/zero.png"

cat >"$WORK/cases.json" <<'JSON'
[ {"surface":"SURF-001","flow":"FLOW-001","req":"REQ-001","lane":"macos-glass","oracle":"raster-visual"},
  {"surface":"SURF-001","lane":"macos-glass","oracle":"raster-visual"},
  {"surface":"SURF-001","lane":"macos-glass","oracle":"raster-visual"},
  {"surface":"SURF-001","lane":"macos-glass","oracle":"raster-visual"},
  {"surface":"SURF-001","lane":"macos-glass","oracle":"raster-visual"},
  {"surface":"SURF-001","lane":"web","oracle":"visual"},
  {"surface":"SURF-001","lane":"web","oracle":"outcome"},
  {"surface":"SURF-001","lane":"web","oracle":"outcome"},
  {"surface":"SURF-001","lane":"macos-glass","oracle":"raster-visual"} ]
JSON
python3 "$S/campaign.py" add "$C" --kind case --file "$WORK/cases.json" >/dev/null

set_case() { python3 "$S/campaign.py" set "$C" "$@" >/dev/null; }
set_case --case CASE-0001 --status pass --evidence shots/a.png --armed \
         --capture-method "SCK window-scoped" --frame-status complete
set_case --case CASE-0002 --status pass --evidence shots/dup.png --armed \
         --capture-method "SCK window-scoped"
set_case --case CASE-0003 --status pass --evidence shots/notimage.png --capture-method SCK
set_case --case CASE-0004 --status pass --evidence shots/tiny.png --capture-method SCK
set_case --case CASE-0005 --status pass --evidence shots/zero.png --capture-method SCK
set_case --case CASE-0006 --status pass --evidence shots/a.png
set_case --case CASE-0007 --status "inconclusive: the engine reports no resolved value for this longhand"
set_case --case CASE-0008 --status "blocked: the WinUI binary was never compiled"
png "$C/shots/f.png" 400 300 5 6 7
set_case --case CASE-0009 --status pass --evidence shots/f.png --armed

expect "a -glass lane with no proof blocks"        1 "$C" "claim on-glass verification with no proof"
expect "the legacy visual rung blocks"             1 "$C" "legacy \`visual\` rung"
expect "a capture that is not an image blocks"      1 "$C" "not a raster image"
expect "a 1x1 placeholder capture blocks"           1 "$C" "1x1"
expect "a zero-byte capture blocks"                 1 "$C" "the capture wrote nothing"
expect "one artifact for two cases blocks"          1 "$C" "identical artifact"
expect "a pixel claim with no channel blocks"       1 "$C" "no stated origin"
expect "inconclusive holds the gate shut"           1 "$C" "case(s) inconclusive"
expect "blocked holds the gate shut"                1 "$C" "never ran"

# ── and the same campaign, resolved, must clear ─────────────────────────────
python3 "$S/campaign.py" lane "$C" --lane macos-glass \
  --artifact "$S/campaign.py" --built-by "swift build -c release" \
  --attached "pid 4412 owns window 'App'" --capture "SCK, SCFrameStatus per frame" >/dev/null
png "$C/shots/b.png" 400 300 40 50 60
png "$C/shots/c.png" 400 300 70 80 90
png "$C/shots/d.png" 400 300 99 11 22
png "$C/shots/e.png" 400 300 12 34 56
python3 - "$C" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "cases.json"
cases = json.loads(p.read_text())
good = {"CASE-0002": "shots/b.png", "CASE-0003": "shots/c.png",
        "CASE-0004": "shots/d.png", "CASE-0005": "shots/e.png"}
for c in cases:
    if c["id"] in good:
        c["evidence"] = [good[c["id"]]]
        c["armed"] = True
        c.setdefault("capture", {}).update(
            {"method": "SCK window-scoped", "frameStatus": "complete"})
    if c["id"] == "CASE-0006":
        c["oracle"] = "structural-visual"       # no longer claims pixels
    if c["id"] == "CASE-0007":
        c["status"] = "n/a: this lane exposes no resolved style, so equality is unmeasurable"
    if c["id"] == "CASE-0008":
        c["status"] = "skip: the Windows lane is deferred to the next campaign"
    if c["id"] == "CASE-0009":
        c.setdefault("capture", {}).update(
            {"method": "SCK window-scoped", "frameStatus": "complete"})
p.write_text(json.dumps(cases, indent=2))
PY
# CASE-0006 keeps shots/a.png, which CASE-0001 also names; at structural-visual
# that is no longer a pixel claim, so sharing it is not a finding.
expect "the resolved campaign clears" 0 "$C" "Every case accounted for"

# ── strict-check: the ratchet may not fall quietly ──────────────────────────
python3 "$S/strict-check.py" "$C" --set-ratchet >/dev/null
python3 - "$C" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "cases.json"
cases = json.loads(p.read_text())
for c in cases:
    if c["id"] == "CASE-0002":
        c["armed"] = False
p.write_text(json.dumps(cases, indent=2))
PY
out="$(python3 "$S/strict-check.py" "$C" 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -q "checked fell from" <<<"$out"; then
  say "ok    unarming a case fails the ratchet"; PASS=$((PASS+1))
else
  echo "FAIL  unarming a case should fail the ratchet (exit $rc)"; FAIL=$((FAIL+1))
fi
out="$(python3 "$S/strict-check.py" "$C" --set-ratchet 2>&1)"
if grep -q "REFUSED" <<<"$out"; then
  say "ok    lowering the ratchet without a reason is refused"; PASS=$((PASS+1))
else
  echo "FAIL  lowering the ratchet without a reason should be refused"; FAIL=$((FAIL+1))
fi
out="$(python3 "$S/strict-check.py" "$C" --set-ratchet --reason "rung split" 2>&1)"
if grep -q "ratchet set to" <<<"$out"; then
  say "ok    lowering it with a reason is allowed and recorded"; PASS=$((PASS+1))
else
  echo "FAIL  lowering with a reason should be allowed"; FAIL=$((FAIL+1))
fi

# ── the documented word for the requirement field is accepted ──────────────
Q="$WORK/reqkey"
python3 "$S/campaign.py" init "$Q" --project ReqKey --lanes web >/dev/null
python3 "$S/campaign.py" add "$Q" --kind requirement --file "$WORK/r.json" >/dev/null
python3 "$S/campaign.py" add "$Q" --kind surface --file "$WORK/s.json" >/dev/null
echo '[{"surface":"SURF-001","requirement":"REQ-001","oracle":"outcome"}]' >"$WORK/q.json"
python3 "$S/campaign.py" add "$Q" --kind case --file "$WORK/q.json" >/dev/null
python3 "$S/campaign.py" set "$Q" --case CASE-0001 --status pass --evidence shots/a.png --armed >/dev/null
png "$Q/shots/a.png" 40 30 1 2 3
if python3 "$S/campaign.py" check "$Q" 2>&1 | grep -q "1 inventoried, 0 with no case"; then
  say "ok    'requirement' is read as 'req'"; PASS=$((PASS+1))
else
  echo "FAIL  a case written with 'requirement' should trace to REQ-001"; FAIL=$((FAIL+1))
fi

echo
echo "campaign gate tests: $PASS passed, $FAIL failed"
[ "$FAIL" = 0 ] || exit 1

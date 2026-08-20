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

# ── interactive-glass oracle and flow atom validation ─────────────────────────
IG="$WORK/iglass"
python3 "$S/campaign.py" init "$IG" --project Interactive --lanes web,macos-glass >/dev/null
python3 "$S/campaign.py" add "$IG" --kind requirement --file "$WORK/r.json" >/dev/null
python3 "$S/campaign.py" add "$IG" --kind surface --file "$WORK/s.json" >/dev/null
echo '[{"id":"FLOW-001","label":"Publish","critical":true,"atoms":["button_clicked","toast_shown"]}]' >"$WORK/f_atoms.json"
python3 "$S/campaign.py" add "$IG" --kind flow --file "$WORK/f_atoms.json" >/dev/null

# interactive-glass on a non-glass lane must block
echo '[{"surface":"SURF-001","flow":"FLOW-001","req":"REQ-001","lane":"web","oracle":"interactive-glass"}]' >"$WORK/ig_bad.json"
python3 "$S/campaign.py" add "$IG" --kind case --file "$WORK/ig_bad.json" >/dev/null
python3 "$S/campaign.py" set "$IG" --case CASE-0001 --status pass --evidence shots/a.png --armed >/dev/null
png "$IG/shots/a.png" 40 30 1 2 3
expect "interactive-glass on non-glass lane blocks" 1 "$IG" "claiming interactive-glass on non-glass lane"

# Fix lane to macos-glass with proof, and verify it passes and counts as an effect
python3 "$S/campaign.py" lane "$IG" --lane macos-glass \
  --artifact "$S/campaign.py" --built-by "swift build" \
  --attached "pid 5500 owns window 'Interactive'" --capture "SCK" >/dev/null
python3 - "$IG" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "cases.json"
cases = json.loads(p.read_text())
cases[0]["lane"] = "macos-glass"
p.write_text(json.dumps(cases, indent=2))
PY
expect "interactive-glass on glass lane clears and counts as effect" 0 "$IG" "Every case accounted for"

# ── --cannot-attach is for a leftover structural block, not a missing build ──
# Both directions: a reason that describes an unbuilt artifact is refused, a
# reason that names a host that cannot draw is recorded. The skill's own
# standing rule is that a check nobody has watched fail is not known to bite.
lane_out() {
  python3 "$S/campaign.py" lane "$@" 2>&1
}

B="$WORK/buildfirst"
python3 "$S/campaign.py" init "$B" --project BuildFirst --lanes macos-glass >/dev/null

out="$(lane_out "$B" --lane macos-glass --cannot-attach "no signed app is on disk")"; rc=$?
if [ "$rc" != 0 ] && grep -qF -- "--cannot-attach refused" <<<"$out" && grep -qF -- "missing build" <<<"$out"; then
  say "ok    cannot-attach for a missing signed app is refused"; PASS=$((PASS+1))
else
  echo "FAIL  cannot-attach 'no signed app is on disk' should be refused (exit $rc)"
  echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

out="$(lane_out "$B" --lane macos-glass --cannot-attach "glass stays closed")"; rc=$?
if [ "$rc" != 0 ] && grep -qF -- "--cannot-attach refused" <<<"$out"; then
  say "ok    cannot-attach 'glass stays closed' is refused"; PASS=$((PASS+1))
else
  echo "FAIL  cannot-attach 'glass stays closed' should be refused (exit $rc)"
  echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

out="$(lane_out "$B" --lane macos-glass --artifact "$B/missing.app" --built-by "xcodebuild -scheme App" --attached "pid 1")"; rc=$?
if [ "$rc" != 0 ] && grep -qF -- "does not exist" <<<"$out" && grep -qF -- "Build it" <<<"$out"; then
  say "ok    a missing --artifact path tells you to build it"; PASS=$((PASS+1))
else
  echo "FAIL  a missing --artifact should tell you to build it (exit $rc)"
  echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

out="$(lane_out "$B" --lane macos-glass --cannot-attach "no Windows host with an interactive desktop is reachable")"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "NOT attached" <<<"$out"; then
  say "ok    cannot-attach for a missing interactive desktop is recorded"; PASS=$((PASS+1))
else
  echo "FAIL  cannot-attach for a missing interactive desktop should record (exit $rc)"
  echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# ── capture lineage: a picture must prove what it depicts ──────────────────
#
# The gate this section exercises exists because a campaign published 20 captures
# of three unrelated documents and cleared every other gate here. Both directions
# are asserted, and the seeded swap is asserted too — a tie pass that cannot be
# watched to fail is indistinguishable from one that does nothing.

cl() { python3 "$S/capture-lineage.py" "$@" 2>&1; }

L="$WORK/lineage"
mkdir -p "$L/evidence/shots"
png "$L/evidence/shots/SURF-001.png" 40 30 200 30 30
png "$L/evidence/shots/SURF-002.png" 40 30 30 200 30
cat >"$L/inventory.json" <<'JSON'
{"requirement":[],"component":[],"flow":[],"surface":[
 {"id":"SURF-001","name":"Dashboard","route":"/dashboard","shot":"evidence/shots/SURF-001.png"},
 {"id":"SURF-002","name":"Settings","route":"/settings","shot":"evidence/shots/SURF-002.png"}]}
JSON

# no manifest at all — the measured failure's exact shape
out="$(cl "$L" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "no entry in evidence/shots/captures.json" <<<"$out"; then
  say "ok    a shot with no capture manifest is unsourced"; PASS=$((PASS+1))
else
  echo "FAIL  a shot with no manifest should be unsourced (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

manifest() { # manifest <target-001> <target-002>
  python3 - "$L" "$1" "$2" <<'PY'
import hashlib, json, pathlib, sys
d, t1, t2 = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3]
def sha(rel): return hashlib.sha256((d / rel).read_bytes()).hexdigest()
rows = []
for sid, tgt in (("SURF-001", t1), ("SURF-002", t2)):
    rel = f"evidence/shots/{sid}.png"
    rows.append({"path": rel, "subject": sid, "target": tgt, "channel": "playwright/chromium",
                 "derivedFrom": None, "sha256": sha(rel), "capturedAt": "2026-08-20T08:00:00Z",
                 "conditions": {"viewport": [1440, 900], "dpr": 2, "settleMs": 1200}})
(d / "evidence/shots/captures.json").write_text(json.dumps(rows, indent=1) + "\n")
PY
}

manifest "http://127.0.0.1:3000/dashboard" "http://127.0.0.1:3000/settings"
out="$(cl "$L" --gate)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "names a target that ties to its subject" <<<"$out"; then
  say "ok    a manifest naming each target clears"; PASS=$((PASS+1))
else
  echo "FAIL  a correct manifest should clear (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# the seeded swap must be caught — this is the gate watched to fail
out="$(cl "$L" --seed-swap SURF-001,SURF-002)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "seed-swap CAUGHT" <<<"$out"; then
  say "ok    swapping two subjects turns the tie pass red"; PASS=$((PASS+1))
else
  echo "FAIL  a seeded swap must be caught (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi
if grep -qF '"target": "http://127.0.0.1:3000/dashboard"' "$L/evidence/shots/captures.json"; then
  say "ok    seed-swap restores the manifest it borrowed"; PASS=$((PASS+1))
else
  echo "FAIL  seed-swap left the manifest swapped"; FAIL=$((FAIL+1))
fi

# a target pointing somewhere else entirely
manifest "http://127.0.0.1:3000/dashboard" "file:///tmp/whats-left.html"
out="$(cl "$L" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "does not resolve to route" <<<"$out"; then
  say "ok    a target that is not the subject's route is untied"; PASS=$((PASS+1))
else
  echo "FAIL  a wrong target should be untied (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# a source-file route cannot be photographed by a browser, and says why
python3 - "$L" <<'PY'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); inv = json.loads((d / "inventory.json").read_text())
inv["surface"][1]["route"] = "apps/macos/Sources/AppMain/MixerHostView.swift"
(d / "inventory.json").write_text(json.dumps(inv, indent=1) + "\n")
PY
out="$(cl "$L" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "no capture channel can photograph one" <<<"$out"; then
  say "ok    a source-file route names the on-glass channel as the remedy"; PASS=$((PASS+1))
else
  echo "FAIL  a source-file route should name the channel problem (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# two subjects, one image
D="$WORK/lineage-dup"
mkdir -p "$D/evidence/shots"
png "$D/evidence/shots/SURF-001.png" 40 30 7 7 7
cp "$D/evidence/shots/SURF-001.png" "$D/evidence/shots/SURF-002.png"
cat >"$D/inventory.json" <<'JSON'
{"requirement":[],"component":[],"flow":[],"surface":[
 {"id":"SURF-001","name":"A","route":"/a","shot":"evidence/shots/SURF-001.png"},
 {"id":"SURF-002","name":"B","route":"/b","shot":"evidence/shots/SURF-002.png"}]}
JSON
python3 - "$D" <<'PY'
import hashlib, json, pathlib, sys
d = pathlib.Path(sys.argv[1]); rows = []
for sid, tgt in (("SURF-001", "http://h/a"), ("SURF-002", "http://h/b")):
    rel = f"evidence/shots/{sid}.png"
    rows.append({"path": rel, "subject": sid, "target": tgt, "channel": "playwright/chromium",
                 "sha256": hashlib.sha256((d / rel).read_bytes()).hexdigest()})
(d / "evidence/shots/captures.json").write_text(json.dumps(rows, indent=1) + "\n")
PY
out="$(cl "$D" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "subjects share one image" <<<"$out"; then
  say "ok    two subjects sharing one image fails"; PASS=$((PASS+1))
else
  echo "FAIL  a shared image should fail (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# ...unless the share is declared with a reason
python3 - "$D" <<'PY'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); p = d / "evidence/shots/captures.json"
rows = json.loads(p.read_text())
rows[0]["sharesWith"] = ["SURF-002"]; rows[0]["shareReason"] = "one window serves both"
rows[1]["sharesWith"] = ["SURF-001"]; rows[1]["shareReason"] = "one window serves both"
p.write_text(json.dumps(rows, indent=1) + "\n")
PY
out="$(cl "$D" --gate)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "declared share" <<<"$out"; then
  say "ok    a declared share passes and prints"; PASS=$((PASS+1))
else
  echo "FAIL  a declared share should pass (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# ── the published-shot audit inside campaign.py check ──────────────────────
out="$(python3 "$S/campaign.py" check "$D" 2>&1)"
if grep -qF -- "Wall:" <<<"$out"; then
  say "ok    check reports the wall's distinct-image count"; PASS=$((PASS+1))
else
  echo "FAIL  check should report the wall's distinct images"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# ── attach-shots refuses an uncorroborated write ───────────────────────────
A2="$WORK/attach"
mkdir -p "$A2/evidence/shots"
png "$A2/evidence/shots/SURF-001.png" 20 20 1 2 3
echo '{"requirement":[],"component":[],"flow":[],"surface":[{"id":"SURF-001","name":"A","route":"/a"}]}' >"$A2/inventory.json"
out="$(python3 "$S/attach-shots.py" "$A2" --apply 2>&1)"; rc=$?
if [ "$rc" != 0 ] && grep -qF -- "REFUSED to write" <<<"$out"; then
  say "ok    attach-shots refuses a write no capture manifest corroborates"; PASS=$((PASS+1))
else
  echo "FAIL  attach-shots should refuse an uncorroborated write (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
out="$(python3 "$S/attach-shots.py" "$A2" --apply --filename-only 2>&1)"; rc=$?
if grep -qF -- "wrote" <<<"$out" && grep -qF '"shotProvenance": "filename"' "$A2/inventory.json"; then
  say "ok    --filename-only writes, and stamps the weakness into the inventory"; PASS=$((PASS+1))
else
  echo "FAIL  --filename-only should write and stamp provenance (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
out="$(python3 "$S/campaign.py" check "$A2" 2>&1)"
if grep -qF -- "bound to their subject by filename alone" <<<"$out"; then
  say "ok    check blocks on a filename-only binding"; PASS=$((PASS+1))
else
  echo "FAIL  check should block on filename-only bindings"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# ── the effect boundary: a guarantee over a capability that never runs ──────
# The incident this whole block exists for: a campaign recorded "runner
# communication is outbound pull only via HTTPS/WSS on TCP 443" as `observed`
# over a product with no HTTP client in its dependency tree, and cleared every
# gate it had. Arming mutates the system; nothing was mutating the
# specification, so a constraint held vacuously and read as verified.
#
# What blocks is the dishonest configuration, never the honest one. A
# requirement recorded `vacuous` is finished work and clears; a requirement
# claiming an effect outside the product, recorded `observed`, with no
# effect-witness case behind it, is the shape that shipped and it holds the
# gate. Both directions are asserted, and so is the class validation on the way
# in.
V="$WORK/effect"
python3 "$S/campaign.py" init "$V" --project Effect --lanes web >/dev/null
python3 "$S/campaign.py" add "$V" --kind surface --file "$WORK/s.json" >/dev/null

echo '[{"id":"REQ-001","class":"behaviour","text":"the runner boots a guest VM per job","effect":"subprocess","evidence":"observed"}]' >"$WORK/re.json"
python3 "$S/campaign.py" add "$V" --kind requirement --file "$WORK/re.json" >/dev/null
echo '[{"surface":"SURF-001","req":"REQ-001","lane":"web","oracle":"outcome"}]' >"$WORK/ce.json"
python3 "$S/campaign.py" add "$V" --kind case --file "$WORK/ce.json" >/dev/null
png "$V/shots/a.png" 40 30 1 2 3
python3 "$S/campaign.py" set "$V" --case CASE-0001 --status pass --evidence shots/a.png --armed >/dev/null
expect "an observed external effect with no witness blocks" 1 "$V" \
       "claiming an effect outside the product"

# The honest finding clears: nothing was witnessed, and the registry says so.
python3 - "$V" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"][0]["evidence"] = "vacuous"
p.write_text(json.dumps(inv, indent=2))
PY
expect "the same requirement recorded vacuous clears" 0 "$V" "External effects:"

# And so does a real witness. Back to `observed`, with a case that stands at
# effect-witness and names what recorded the effect and how many it saw.
python3 - "$V" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"][0]["evidence"] = "observed"
p.write_text(json.dumps(inv, indent=2))
c = pathlib.Path(sys.argv[1]) / "cases.json"
cases = json.loads(c.read_text())
cases[0]["oracle"] = "effect-witness"
c.write_text(json.dumps(cases, indent=2))
PY
expect "an effect-witness claim with no recorder blocks" 1 "$V" "names no recorder"
python3 "$S/campaign.py" set "$V" --case CASE-0001 \
  --recorder "dtrace proc:::exec-success, 4 lines" --effect-class subprocess \
  --effect-count 0 >/dev/null
expect "a witness that counted nothing blocks" 1 "$V" \
       "a witness that saw nothing is the condition, not the proof"
python3 "$S/campaign.py" set "$V" --case CASE-0001 --effect-count 4 >/dev/null
expect "a counted, recorded witness clears" 0 "$V" "witnessed=1"

# Two regressions the 0.9.0 census shipped with, both of which read as a clean
# result. First: `witnessed` was computed as
# `len(effect_reqs) - len(unbacked) - len(vacuous)`, so a requirement recorded
# `reported` — an external effect claimed, never witnessed, never blocked —
# was subtracted into the witnessed count and reported as an effect somebody
# had seen. It is now counted from the cases that actually stand at the rung.
python3 - "$V" <<'PY2'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"].append({"id": "REQ-002", "class": "behaviour",
                           "text": "the runner writes a job log to disk",
                           "effect": "filesystem-write", "evidence": "reported"})
p.write_text(json.dumps(inv, indent=2))
c = pathlib.Path(sys.argv[1]) / "cases.json"
cases = json.loads(c.read_text())
cases.append(dict(cases[0], id="CASE-0002", req="REQ-002", oracle="outcome",
                  witness=None))
c.write_text(json.dumps(cases, indent=2))
PY2
expect "a reported external effect is not counted as witnessed" 0 "$V" "witnessed=1 "
expect "and it is named as claimed-but-unwitnessed" 0 "$V" "REQ-002 (reported)"

# Second: the census printed only after the full-run verdict, past the
# selective-run `return 0` — so on the skill's own default scope it never
# printed at all, and a registry with eight vacuous requirements reported
# nothing about any of them.
python3 "$S/campaign.py" scope "$V" --full --decided-by "tests/run.sh" >/dev/null
python3 "$S/campaign.py" scope "$V" --selective --basis "arming the census print" --decided-by "tests/run.sh" >/dev/null
expect "a selective run prints the effect census too" 0 "$V" "External effects: examined="

# An unrecognised effect class written straight into inventory.json (rather than
# through `add`, which refuses one) used to fail the census membership test and
# vanish, reading as a requirement that claims no external effect.
python3 - "$V" <<'PY2'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"][1]["effect"] = "filesystem"
p.write_text(json.dumps(inv, indent=2))
PY2
expect "an unrecognised effect class blocks rather than vanishing" 1 "$V" "does not recognise"
python3 - "$V" <<'PY2'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"][1]["effect"] = "filesystem-write"
p.write_text(json.dumps(inv, indent=2))
PY2
expect "correcting it to a real class clears" 0 "$V" "External effects: examined=2"


# Class validation on the way in, both fields.
if python3 "$S/campaign.py" add "$V" --kind requirement --file /dev/stdin >/dev/null 2>&1 <<<'[{"text":"x","evidence":"probably"}]'; then
  echo "FAIL  a bogus evidence class should be refused at add time"; FAIL=$((FAIL+1))
else
  say "ok    a bogus requirement evidence class is refused"; PASS=$((PASS+1))
fi
if python3 "$S/campaign.py" add "$V" --kind requirement --file /dev/stdin >/dev/null 2>&1 <<<'[{"text":"x","effect":"telepathy"}]'; then
  echo "FAIL  a bogus effect class should be refused at add time"; FAIL=$((FAIL+1))
else
  say "ok    a bogus requirement effect class is refused"; PASS=$((PASS+1))
fi

# ── vacuity-check: the requirement-level and test-tree half ─────────────────
# campaign.py owns the case-level rules; this owns the census and the blind
# mutation scan. Each pass is proved to fire and then proved to clear, and the
# --seed-strengthen control is the skill's own arming rule turned on the gate
# itself: strengthen a constraint the registry cannot satisfy, and require red.
VC="$WORK/vacuity"
mkdir -p "$VC"
cat >"$VC/inventory.json" <<'JSON'
{"requirement": [
  {"id":"REQ-001","title":"The daemon keeps a counter in memory","effect":"none","evidence":"observed"},
  {"id":"REQ-002","title":"The engine boots a Tart guest per job","effect":"subprocess","evidence":"observed"}
]}
JSON
out="$(python3 "$S/vacuity-check.py" "$VC" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "records no \`provider\`" <<<"$out"; then
  say "ok    a declared effect with no provider is uncensused"; PASS=$((PASS+1))
else
  echo "FAIL  uncensused should fire and exit 1 (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

python3 - "$VC" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"][1]["provider"] = "isolation/macos.rs:88 spawn_guest"
p.write_text(json.dumps(inv, indent=2))
PY
out="$(python3 "$S/vacuity-check.py" "$VC" --gate 2>&1)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "external=1 findings=0" <<<"$out"; then
  say "ok    naming the provider clears the census"; PASS=$((PASS+1))
else
  echo "FAIL  a named provider should clear (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# The requirement's own words name an effect and no class is declared: this
# over-flags on purpose, because a false positive costs one `"effect": "none"`
# and a false negative costs the campaign its central claim.
python3 - "$VC" <<'PY'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"].append({"id": "REQ-003",
                           "title": "Peers are found over mDNS with no configuration"})
p.write_text(json.dumps(inv, indent=2))
PY
out="$(python3 "$S/vacuity-check.py" "$VC" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "REQ-003 names multicast" <<<"$out"; then
  say "ok    an undeclared effect named in the text is unclassed"; PASS=$((PASS+1))
else
  echo "FAIL  unclassed should name REQ-003's multicast (exit $rc)"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# The control. It mutates the registry, so the restore is checked by hash
# rather than by trusting the finally block.
before="$(shasum -a 256 <"$VC/inventory.json")"
out="$(python3 "$S/vacuity-check.py" "$VC" --seed-strengthen REQ-002 2>&1)"; rc=$?
after="$(shasum -a 256 <"$VC/inventory.json")"
if [ "$rc" = 0 ] && grep -qF -- "The gate bites" <<<"$out"; then
  say "ok    --seed-strengthen turns a strengthened constraint red"; PASS=$((PASS+1))
else
  echo "FAIL  --seed-strengthen should report the gate biting (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
if [ "$before" = "$after" ]; then
  say "ok    --seed-strengthen restores the registry byte-identically"; PASS=$((PASS+1))
else
  echo "FAIL  --seed-strengthen left the registry changed"; FAIL=$((FAIL+1))
fi

# The blind pass, both directions on one file: a test that mutates and never
# reads again can only be asserting the call's own return value, which is the
# shape that let a daemon verb report success while changing nothing.
mkdir -p "$VC/src/tests"
cat >"$VC/src/tests/spec_a.rs" <<'RS'
#[test]
fn stopping_a_runner_reports_success() {
    let (ok, _msg) = s.stop_runner("runner-01");
    assert!(ok);
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" 2>&1)"
if grep -qF -- "mutating=1 re-read-after=0 blind=1" <<<"$out"; then
  say "ok    a mutate-and-never-read test is blind"; PASS=$((PASS+1))
else
  echo "FAIL  the blind pass should find 1 of 1"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi
cat >"$VC/src/tests/spec_a.rs" <<'RS'
#[test]
fn stopping_a_runner_removes_it() {
    let (ok, _msg) = s.stop_runner("runner-01");
    assert!(ok);
    let still = s.list_runners();
    assert!(!still.iter().any(|r| r.id == "runner-01"));
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" 2>&1)"
if grep -qF -- "mutating=1 re-read-after=1 blind=0" <<<"$out"; then
  say "ok    reading the observable afterwards clears the blind pass"; PASS=$((PASS+1))
else
  echo "FAIL  a re-read should clear the blind pass"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# A pass that could not run is not a pass that found nothing.
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/nowhere" 2>&1)"
if grep -qF -- "SKIPPED" <<<"$out" && grep -qF -- "is not a pass that found nothing" <<<"$out"; then
  say "ok    a missing test root is skipped out loud"; PASS=$((PASS+1))
else
  echo "FAIL  a missing test root should say it was skipped"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi


# Four ways the blind pass reported a number that was about the instrument, and
# one way the strict score punished the strongest rung.
#
# 1. An unanchored mutator matched inside a longer identifier: `record` fired on
#    `job_record(`, so a test with no mutating call in it was reported blind.
cat >"$VC/src/tests/spec_b.rs" <<'RS'
#[test]
fn an_unknown_job_reads_as_unknown() {
    assert!(s.job_record(4242).is_none());
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" --mutator record 2>&1)"
if grep -qF -- "an_unknown_job_reads_as_unknown" <<<"$out"; then
  echo "FAIL  a mutator matching inside a longer identifier still fires"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
else
  say "ok    a mutator does not fire inside a longer identifier"; PASS=$((PASS+1))
fi
# ...while a genuine method call on the same verb still does. Without this the
# fix above is indistinguishable from deleting the verb.
cat >"$VC/src/tests/spec_b.rs" <<'RS'
#[test]
fn seeding_the_log_and_asserting_nothing() {
    log.record(Kind::JobCancelled, "a", 1);
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" --mutator record 2>&1)"
if grep -qF -- "seeding_the_log_and_asserting_nothing" <<<"$out"; then
  say "ok    the same mutator still fires on a real method call"; PASS=$((PASS+1))
else
  echo "FAIL  anchoring the mutator killed it entirely"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
rm -f "$VC/src/tests/spec_b.rs"

# 2. A fixture helper counted as a test. It mutates and returns; its callers do
#    the reading, so it is reported blind while every caller asserts correctly.
cat >"$VC/src/tests/spec_c.rs" <<'RS'
fn log_with_two_jobs() -> ActivityLog {
    let log = ActivityLog::new(64);
    log.record(Kind::JobCancelled, "a", 1);
    log
}
#[test]
fn the_job_filter_returns_only_that_jobs_events() {
    let log = log_with_two_jobs();
    assert_eq!(log.for_job(1).len(), 1);
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" --mutator record --reader for_job 2>&1)"
if grep -qF -- "log_with_two_jobs" <<<"$out"; then
  echo "FAIL  a fixture helper is still counted as a blind test"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
else
  say "ok    a helper its callers use is not counted as a test"; PASS=$((PASS+1))
fi
rm -f "$VC/src/tests/spec_c.rs"

# 3. The vocabulary came from the defaults only. The docstring said it came from
#    the campaign config; nothing read one. A project whose readers the defaults
#    miss gets MORE findings, so a wrong vocabulary reads as a thorough pass.
cat >"$VC/src/tests/spec_d.rs" <<'RS'
#[test]
fn clearing_the_queue_empties_the_feed() {
    s.clear_queue();
    assert_eq!(s.activity_feed(10).total_held, 1);
}
RS
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" 2>&1)"
if grep -qF -- "clearing_the_queue_empties_the_feed" <<<"$out"; then
  say "ok    a reader the defaults do not know reads as blind"; PASS=$((PASS+1))
else
  echo "FAIL  expected the default vocabulary to miss activity_feed"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
cat >"$VC/campaign.json" <<'JSON'
{"project": "Vacuity",
 "blindVocabulary": {"mutators": ["clear_"], "readers": ["activity_feed"]}}
JSON
out="$(python3 "$S/vacuity-check.py" "$VC" --tests "$VC/src" 2>&1)"
if grep -qF -- "campaign.blindVocabulary" <<<"$out" && ! grep -qF -- "clearing_the_queue_empties_the_feed" <<<"$out"; then
  say "ok    the campaign's declared vocabulary is read and reported"; PASS=$((PASS+1))
else
  echo "FAIL  campaign.blindVocabulary was not applied or not reported"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
rm -f "$VC/src/tests/spec_d.rs"

# 4. strict-check never learned the effect-witness rung campaign.py added in
#    0.9.0, so the rung that most strongly proves an effect scored in the
#    weakest bucket and building a real witness moved the score by nothing.
out="$(python3 "$S/strict-check.py" "$V" 2>&1)"
if grep -qE "^CHECKED   2 of 2 cases \(100%\)" <<<"$out"; then
  say "ok    strict-check counts effect-witness as an effect rung"; PASS=$((PASS+1))
else
  echo "FAIL  effect-witness is not counted as checked"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
echo
echo "campaign gate tests: $PASS passed, $FAIL failed"
[ "$FAIL" = 0 ] || exit 1

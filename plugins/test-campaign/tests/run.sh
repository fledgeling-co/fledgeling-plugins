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

# ...unless the share is declared with a reason, on every member, over subjects
# that something outside the declaration agrees are one address. This fixture
# used to write `shareReason` — a field campaign.py has never read and
# capture-lineage.py did not read either, so the "reason" was satisfied by a
# key nobody consumed — and to leave SURF-002 at /b, so the declaration alone
# authorised one picture of two different addresses. The assertion is unchanged;
# the fixture now describes a share that is one.
python3 - "$D" <<'PY'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); p = d / "evidence/shots/captures.json"
inv_path = d / "inventory.json"
inv = json.loads(inv_path.read_text())
inv["surface"][1]["route"] = "/a"          # B is the same address as A
inv_path.write_text(json.dumps(inv, indent=1) + "\n")
rows = json.loads(p.read_text())
rows[1]["target"] = "http://h/a"           # and the channel recorded it as one
rows[0]["sharesWith"] = ["SURF-002"]; rows[0]["sharesReason"] = "one window serves both"
rows[1]["sharesWith"] = ["SURF-001"]; rows[1]["sharesReason"] = "one window serves both"
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
# 5. A capped list read as a population. `check` printed at most twelve
#    unwitnessed requirements out of eighteen with nothing saying it had cut the
#    list, and a team scoped a wave of work off the twelve — ten requirements
#    were named by no item. Recorded as DEF-041. The remedy is not a bigger cap,
#    which the next set always outgrows: it is the denominator beside the list.
DEN="$WORK/denominator"
python3 "$S/campaign.py" init "$DEN" --project Denominator --lanes web >/dev/null
python3 - "$DEN" <<'PYFIXTURE'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
inv = json.loads((d / "inventory.json").read_text())
inv["requirement"] = [
    {"id": f"REQ-{i:03d}", "text": f"The product opens a socket, number {i}",
     "source": "fixture", "class": "behaviour", "evidence": "observed",
     "surfaces": ["SURF-001"], "effect": "outbound-socket", "provider": "fixture"}
    for i in range(1, 19)]
inv["surface"] = [{"id": "SURF-001", "name": "fixture surface", "kind": "screen"}]
(d / "inventory.json").write_text(json.dumps(inv, indent=2) + "\n")
(d / "cases.json").write_text(json.dumps([
    {"id": "CASE-0001", "req": "REQ-001", "surface": "SURF-001", "oracle": "outcome",
     "status": "pass", "armed": True, "armedBy": "fixture",
     "evidence": ["fixture.txt"]}], indent=2) + "\n")
PYFIXTURE
out="$(python3 "$S/campaign.py" check "$DEN" 2>&1)"
# The truncated list says so, and says how many it cut to and from.
if grep -qF -- "… (showing 12 of 18)" <<<"$out"; then
  say "ok    a truncated list carries its denominator"; PASS=$((PASS+1))
else
  echo "FAIL  the capped list of 18 requirements printed 12 with no denominator"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# The cap still caps: the denominator is the registry's count, not a raised cap.
if [ "$(grep -c -- "claims a outbound-socket effect" <<<"$out")" = 12 ]; then
  say "ok    the cap still caps"; PASS=$((PASS+1))
else
  echo "FAIL  expected 12 printed rows under the cap"; FAIL=$((FAIL+1))
fi
# An untruncated list prints its denominator too, so a reader never has to work
# out whether anything was cut — which is the position that caused the loss.
python3 - "$DEN" <<'PYTRIM'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
inv = json.loads((d / "inventory.json").read_text())
inv["requirement"] = inv["requirement"][:3]
(d / "inventory.json").write_text(json.dumps(inv, indent=2) + "\n")
PYTRIM
out="$(python3 "$S/campaign.py" check "$DEN" 2>&1)"
if grep -qF -- "(showing 3 of 3)" <<<"$out" && ! grep -qF -- "… (showing" <<<"$out"; then
  say "ok    a complete list says it is complete"; PASS=$((PASS+1))
else
  echo "FAIL  a complete list printed no denominator, or claimed a truncation"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# 6. An oracle rung that was not on the ladder. Four cases arrived recording
#    `static-analysis` — a real, armed, red-provable source classifier — and
#    counted `unrated`, the bucket meaning the tool does not know what they
#    checked. Recorded as DEF-057. `source-analysis` is now a rung, off the
#    product ladder rather than a step on it, and these prove it is accepted,
#    counted apart, and guarded so it cannot stand behind an external effect.
SRC="$WORK/source-rung"
python3 "$S/campaign.py" init "$SRC" --project SourceRung --lanes web >/dev/null
python3 - "$SRC" <<'PYSRC'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
inv = json.loads((d / "inventory.json").read_text())
inv["requirement"] = [
    {"id": "REQ-001", "text": "No user-facing copy is hardcoded in the main view",
     "source": "fixture", "class": "behaviour", "evidence": "observed",
     "surfaces": ["SURF-001"], "effect": "none"}]
inv["surface"] = [{"id": "SURF-001", "name": "fixture surface", "kind": "screen"}]
(d / "inventory.json").write_text(json.dumps(inv, indent=2) + "\n")
(d / "cases.json").write_text(json.dumps([
    {"id": "CASE-0001", "req": "REQ-001", "surface": "SURF-001",
     "oracle": "source-analysis", "status": "pass", "armed": True,
     "armedBy": "a one-line mutation makes the classifier exit 1",
     "evidence": ["fixture.txt"],
     "source": {"analyzer": "literals.py", "examined": 45}}], indent=2) + "\n")
(d / "fixture.txt").write_text("classifier output\n")
PYSRC
out="$(python3 "$S/campaign.py" check "$SRC" 2>&1)"
if grep -qF -- "Off-ladder: source-analysis 1" <<<"$out" && ! grep -qF -- "unrated 1" <<<"$out"; then
  say "ok    source-analysis is a rung, counted apart from the product ladder"; PASS=$((PASS+1))
else
  echo "FAIL  source-analysis was not recognised or was folded into the ladder"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# The guard: the same case behind a requirement that claims an external effect.
python3 - "$SRC" <<'PYEFFECT'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
inv = json.loads((d / "inventory.json").read_text())
inv["requirement"][0]["effect"] = "subprocess"
inv["requirement"][0]["provider"] = "fixture"
(d / "inventory.json").write_text(json.dumps(inv, indent=2) + "\n")
PYEFFECT
expect "an external effect cannot rest on source analysis alone" 1 "$SRC" \
  "covered by source-analysis alone"
# And a source-analysis pass that names no analyzer or no denominator blocks,
# because "the grep found nothing" is also what a grep pointed at the wrong file
# says.
python3 - "$SRC" <<'PYHOLLOW'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
inv = json.loads((d / "inventory.json").read_text())
inv["requirement"][0]["effect"] = "none"
inv["requirement"][0].pop("provider", None)
(d / "inventory.json").write_text(json.dumps(inv, indent=2) + "\n")
cases = json.loads((d / "cases.json").read_text())
cases[0]["source"] = {"analyzer": "literals.py", "examined": 0}
(d / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
PYHOLLOW
expect "a source-analysis pass owes a denominator" 1 "$SRC" \
  "cannot tell an empty result from an empty search"
# Restored, it clears — a gate that always fails is no more useful than one that
# always passes.
python3 - "$SRC" <<'PYRESTORE'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1])
cases = json.loads((d / "cases.json").read_text())
cases[0]["source"] = {"analyzer": "literals.py", "examined": 45}
(d / "cases.json").write_text(json.dumps(cases, indent=2) + "\n")
PYRESTORE
expect "the same campaign clears once the denominator is back" 0 "$SRC"
# It buys no effect credit: the rung is absent from EFFECT_RUNGS.
if python3 -c "
import importlib.util, sys
spec = importlib.util.spec_from_file_location('c', '$S/campaign.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
sys.exit(0 if set(m.SOURCE_RUNGS).isdisjoint(m.EFFECT_RUNGS)
         and set(m.SOURCE_RUNGS).isdisjoint(m.ORACLE_RUNGS) else 1)"; then
  say "ok    source-analysis buys no effect credit and is off the ladder"; PASS=$((PASS+1))
else
  echo "FAIL  source-analysis leaked into EFFECT_RUNGS or ORACLE_RUNGS"; FAIL=$((FAIL+1))
fi

# 7. DEF-115. The census reported a requirement whose `provider` was EMPTY and
#    never checked that a non-empty one resolved to anything, so a provider
#    naming a path that does not exist, or a symbol no production file contains,
#    cleared — and the census then reported every external effect as provided
#    while some of them named nothing. Both directions, plus the third state:
#    with no source root declared, the resolution is NOT CHECKED out loud rather
#    than quietly clean.
PRV="$WORK/provider"
mkdir -p "$PRV/camp" "$PRV/repo/src/isolation"
cat >"$PRV/camp/inventory.json" <<'JSON'
{"requirement": [
  {"id":"REQ-001","title":"The engine boots a Tart guest per job","effect":"subprocess",
   "evidence":"observed","provider":"isolation/macos.rs:88 spawn_guest"},
  {"id":"REQ-002","title":"The daemon uploads each job log over HTTPS",
   "effect":"outbound-socket","evidence":"observed","provider":"net/upload.rs:12 push_log"}]}
JSON
cat >"$PRV/repo/src/isolation/macos.rs" <<'RS'
pub fn spawn_guest(job: &Job) -> Result<Child> { Command::new("tart").spawn() }
RS

# No root declared: both providers are strings nobody read, and the run says so.
out="$(python3 "$S/vacuity-check.py" "$PRV/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "2 of 2 named, 0 resolved — NOT CHECKED" <<<"$out"; then
  say "ok    with no source root the provider resolution is not-checked out loud"; PASS=$((PASS+1))
else
  echo "FAIL  an unresolvable census should say NOT CHECKED (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

echo '{"project":"Provider","sourceRoot":"'"$PRV/repo"'"}' >"$PRV/camp/campaign.json"
out="$(python3 "$S/vacuity-check.py" "$PRV/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "which resolves to nothing" <<<"$out" \
   && grep -qF -- "2 of 2 named, 1 resolved" <<<"$out"; then
  say "ok    a provider naming a file and a symbol that do not exist is a finding"; PASS=$((PASS+1))
else
  echo "FAIL  a dangling provider should be a finding with a denominator (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# The one that does resolve is not reported: a gate that always fails checks
# nothing. REQ-001's provider names a real file and a real symbol.
if ! grep -qF -- "REQ-001 declares" <<<"$out"; then
  say "ok    the provider that resolves is not reported"; PASS=$((PASS+1))
else
  echo "FAIL  a resolving provider was reported as unresolved"; FAIL=$((FAIL+1))
fi
mkdir -p "$PRV/repo/src/net"
cat >"$PRV/repo/src/net/upload.rs" <<'RS'
pub async fn push_log(body: Vec<u8>) -> Result<()> { client.post(URL).body(body).send().await }
RS
out="$(python3 "$S/vacuity-check.py" "$PRV/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "2 of 2 named, 2 resolved" <<<"$out"; then
  say "ok    writing the provider it named clears the census"; PASS=$((PASS+1))
else
  echo "FAIL  a resolving provider should clear (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# A symbol that lives only in the test tree is the product's own stand-in
# naming itself as the thing it stands in for.
mkdir -p "$PRV/repo/tests"
cat >"$PRV/repo/tests/fake_filter.rs" <<'RS'
pub fn install_filter_rule(_: &str) -> bool { true }
RS
python3 - "$PRV/camp" <<'PYPROV'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["requirement"].append({"id": "REQ-003", "title": "The daemon writes a packet filter rule",
                           "effect": "packet-filter", "evidence": "observed",
                           "provider": "install_filter_rule"})
p.write_text(json.dumps(inv, indent=2))
PYPROV
out="$(python3 "$S/vacuity-check.py" "$PRV/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "no production source contains 'install_filter_rule'" <<<"$out"; then
  say "ok    a provider that exists only in the test tree does not resolve"; PASS=$((PASS+1))
else
  echo "FAIL  a test-only symbol should not resolve as a provider (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# 8. DEF-116. The shared pass exempted a duplicate on a declaration written into
#    the registry being checked, so a capture authorised its own duplicate — and
#    `sharesReason`, demanded by the blocker's own remedy text, was read by no
#    code at all. campaign.py has required it since 0.9.3; the two gates
#    disagreed about the same declaration. Four fixtures, one per rung of the bar.
SH="$WORK/share"
mkdir -p "$SH/evidence/shots"
png "$SH/evidence/shots/SURF-001.png" 40 30 3 9 27
cp "$SH/evidence/shots/SURF-001.png" "$SH/evidence/shots/SURF-002.png"
cat >"$SH/inventory.json" <<'JSON'
{"requirement":[],"component":[],"flow":[],"surface":[
 {"id":"SURF-001","name":"Settings","route":"/settings","shot":"evidence/shots/SURF-001.png"},
 {"id":"SURF-002","name":"Account","route":"/settings/account","shot":"evidence/shots/SURF-002.png"}]}
JSON
share_manifest() { # share_manifest <json-for-002-extras>
  python3 - "$SH" "$1" "$2" <<'PYSHARE'
import hashlib, json, pathlib, sys
d, one, two = pathlib.Path(sys.argv[1]), json.loads(sys.argv[2]), json.loads(sys.argv[3])
rows = []
for sid, extra in (("SURF-001", one), ("SURF-002", two)):
    rel = f"evidence/shots/{sid}.png"
    row = {"path": rel, "subject": sid, "channel": "playwright/chromium",
           "sha256": hashlib.sha256((d / rel).read_bytes()).hexdigest()}
    row.update(extra)
    rows.append(row)
(d / "evidence/shots/captures.json").write_text(json.dumps(rows, indent=1) + "\n")
PYSHARE
}

# one side declares, the other does not
share_manifest '{"target":"http://h/settings","sharesWith":["SURF-002"],"sharesReason":"one sheet"}' \
               '{"target":"http://h/settings"}'
out="$(cl "$SH" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "declaring one side of a share is not a declaration" <<<"$out"; then
  say "ok    a one-sided share declaration does not authorise the duplicate"; PASS=$((PASS+1))
else
  echo "FAIL  a one-sided declaration should still fail (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# both sides, no reason — the field the message demanded and nothing read
share_manifest '{"target":"http://h/settings","sharesWith":["SURF-002"]}' \
               '{"target":"http://h/settings","sharesWith":["SURF-001"]}'
out="$(cl "$SH" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "records no \`sharesReason\`" <<<"$out"; then
  say "ok    a share with no recorded reason is a duplicate with a label on it"; PASS=$((PASS+1))
else
  echo "FAIL  a reasonless share should fail (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# reason present, both sides declaring, and the two captures were pointed at two
# different addresses: two shutters, two subjects, one image that came out
# byte-identical. The declaration is then the only thing saying they are one
# picture, and the declaration is the thing under test.
share_manifest '{"target":"http://h/settings","sharesWith":["SURF-002"],"sharesReason":"one sheet"}' \
               '{"target":"http://h/settings/account","sharesWith":["SURF-001"],"sharesReason":"one sheet"}'
out="$(cl "$SH" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "different targets" <<<"$out"; then
  say "ok    a declaration nothing outside it corroborates does not clear"; PASS=$((PASS+1))
else
  echo "FAIL  an uncorroborated declaration should fail (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# The legitimate case: two subjects that are one address — the channel recorded
# that one address for both, each capture ties to its own subject's route, and
# every member names the other with a reason.
python3 - "$SH" <<'PYALIAS'
import json, pathlib, sys
p = pathlib.Path(sys.argv[1]) / "inventory.json"
inv = json.loads(p.read_text())
inv["surface"][1]["route"] = "/settings"     # Account is a state of the same sheet
p.write_text(json.dumps(inv, indent=1) + "\n")
PYALIAS
share_manifest '{"target":"http://h/settings","sharesWith":["SURF-002"],"sharesReason":"one sheet serves both"}' \
               '{"target":"http://h/settings","sharesWith":["SURF-001"],"sharesReason":"one sheet serves both"}'
out="$(cl "$SH" --gate)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "declared share" <<<"$out"; then
  say "ok    a corroborated, reasoned, mutual share clears and prints"; PASS=$((PASS+1))
else
  echo "FAIL  a genuine declared share should clear (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# 9. DEF-117. Every finding the gate made was derived from PUBLISHED captures,
#    so an image nobody publishes contributed to nothing: measured as
#    `published captures: 0 · files in shots dir: 11`, exit 0, and the sentence
#    "Every published capture names a target that ties to its subject" — true,
#    and covering nothing. And a ratchet of 0 pinned a bar that cannot fall.
UN="$WORK/unpublished"
mkdir -p "$UN/evidence/shots"
png "$UN/evidence/shots/SURF-001.png" 40 30 11 22 33
png "$UN/evidence/shots/stray.png" 40 30 44 55 66
cat >"$UN/inventory.json" <<'JSON'
{"requirement":[],"component":[],"flow":[],"surface":[
 {"id":"SURF-001","name":"Dashboard","route":"/dashboard","shot":"evidence/shots/SURF-001.png"}]}
JSON
python3 - "$UN" <<'PYUN'
import hashlib, json, pathlib, sys
d = pathlib.Path(sys.argv[1]); rel = "evidence/shots/SURF-001.png"
rows = [{"path": rel, "subject": "SURF-001", "target": "http://h/dashboard",
         "channel": "playwright/chromium",
         "sha256": hashlib.sha256((d / rel).read_bytes()).hexdigest()}]
(d / "evidence/shots/captures.json").write_text(json.dumps(rows, indent=1) + "\n")
PYUN
out="$(cl "$UN" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "no subject publishes it and no manifest entry names it" <<<"$out"; then
  say "ok    an image on disk nothing publishes is a finding"; PASS=$((PASS+1))
else
  echo "FAIL  an unaccounted image should be a finding (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# The escape exists, and it is recorded rather than silent.
python3 - "$UN" <<'PYUN2'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); p = d / "evidence/shots/captures.json"
rows = json.loads(p.read_text())
rows.append({"path": "evidence/shots/stray.png", "channel": "playwright/chromium",
             "unpublishedReason": "the empty-state variant, kept for the next campaign"})
p.write_text(json.dumps(rows, indent=1) + "\n")
PYUN2
out="$(cl "$UN" --gate)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "declared unpublished: evidence/shots/stray.png" <<<"$out"; then
  say "ok    an image declared unpublished with a reason clears and prints"; PASS=$((PASS+1))
else
  echo "FAIL  a declared-unpublished image should clear (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# A manifest entry alone is not the escape: the reason is the escape.
python3 - "$UN" <<'PYUN3'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); p = d / "evidence/shots/captures.json"
rows = json.loads(p.read_text())
rows[-1].pop("unpublishedReason")
p.write_text(json.dumps(rows, indent=1) + "\n")
PYUN3
out="$(cl "$UN" --gate)"; rc=$?
if [ "$rc" = 2 ] && grep -qF -- "records no \`unpublishedReason\`" <<<"$out"; then
  say "ok    a manifest entry without a reason is not the escape"; PASS=$((PASS+1))
else
  echo "FAIL  an entry with no reason should still be a finding (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
python3 - "$UN" <<'PYUN4'
import json, pathlib, sys
d = pathlib.Path(sys.argv[1]); p = d / "evidence/shots/captures.json"
rows = json.loads(p.read_text())
rows[-1]["unpublishedReason"] = "the empty-state variant, kept for the next campaign"
p.write_text(json.dumps(rows, indent=1) + "\n")
PYUN4
# Nothing has been judged, so there is no bar to pin.
out="$(cl "$UN" --set-ratchet)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "a ratchet of 0 pins nothing" <<<"$out"; then
  say "ok    a ratchet of 0 is refused outright"; PASS=$((PASS+1))
else
  echo "FAIL  a ratchet of 0 should be refused (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
echo '[{"subject":"SURF-001","verdict":"pass","reason":"matches its reference"}]' >"$UN/witness-verdicts.json"
out="$(cl "$UN" --set-ratchet)"; rc=$?
if [ "$rc" = 0 ] && grep -qF -- "ratchet set to 1" <<<"$out"; then
  say "ok    a judged capture earns a ratchet the gate can hold"; PASS=$((PASS+1))
else
  echo "FAIL  a judged capture should pin a ratchet (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# 10. DEF-118. The corpus root lived only on the command line while the
#     vocabulary that has to agree with it lived in campaign.json. Pointing a
#     campaign whose vocabulary is one language at another language's test tree
#     produced 32 findings, identical in shape and confidence to genuine ones;
#     against its own corpus the same command returned 0, and nothing warned.
TR="$WORK/testroot"
mkdir -p "$TR/camp" "$TR/repo/tests" "$TR/foreign/tests"
cat >"$TR/camp/inventory.json" <<'JSON'
{"requirement":[{"id":"REQ-001","title":"The daemon keeps a counter in memory","effect":"none"}]}
JSON
cat >"$TR/camp/campaign.json" <<JSON
{"project":"TestRoot","testRoot":"$TR/repo/tests",
 "blindVocabulary":{"mutators":["stop_runner"],"readers":["list_runners"]}}
JSON
cat >"$TR/repo/tests/spec_runner.rs" <<'RS'
#[test]
fn stopping_a_runner_reports_success() {
    let ok = s.stop_runner("runner-01");
    assert!(ok);
}
RS
out="$(python3 "$S/vacuity-check.py" "$TR/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "campaign.json testRoot" <<<"$out" \
   && grep -qF -- "mutating=1 re-read-after=0 blind=1" <<<"$out"; then
  say "ok    campaign.json declares the corpus and the blind pass runs on it"; PASS=$((PASS+1))
else
  echo "FAIL  a declared testRoot should run the blind pass (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# The same vocabulary, pointed at another language's tree. What comes back is
# the mismatch, not a number.
cat >"$TR/foreign/tests/test_api.py" <<'PYF'
def test_creating_a_user_returns_an_id():
    u = create_user("ada")
    assert u.id
PYF
out="$(python3 "$S/vacuity-check.py" "$TR/camp" --tests "$TR/foreign/tests" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "VOCABULARY DOES NOT FIT" <<<"$out" \
   && grep -qF -- "overrides campaign.json testRoot" <<<"$out" \
   && ! grep -qF -- "test_creating_a_user_returns_an_id" <<<"$out"; then
  say "ok    a vocabulary that does not fit the corpus says so instead of counting"; PASS=$((PASS+1))
else
  echo "FAIL  a foreign corpus should report the misfit and no findings (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
# And the corroboration is not a blanket refusal: a corpus the vocabulary does
# fit still gets its number, over the same foreign tree once the vocabulary is
# the one that tree is written in.
cat >"$TR/camp/campaign.json" <<JSON
{"project":"TestRoot","testRoot":"$TR/foreign/tests",
 "blindVocabulary":{"mutators":["create_user"],"readers":["list_users"]}}
JSON
out="$(python3 "$S/vacuity-check.py" "$TR/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "test_creating_a_user_returns_an_id" <<<"$out" \
   && ! grep -qF -- "VOCABULARY DOES NOT FIT" <<<"$out"; then
  say "ok    a vocabulary that fits its corpus still produces the finding"; PASS=$((PASS+1))
else
  echo "FAIL  a fitting vocabulary should produce findings (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi
echo
# 11. DEF-119. Providers are written `<claim> — <what it does>`, and every word
#     of the description was offered to the symbol matcher. Any English word of
#     three characters or more that appears anywhere in production source
#     resolved the provider, so a path that does not exist cleared the census on
#     the strength of its own prose. Measured on a real campaign: nine of nine
#     providers reported resolved, one of them via the symbol `the`. The census
#     built to catch a dead predicate had become one.
PRZ="$WORK/provider-prose"
mkdir -p "$PRZ/camp" "$PRZ/repo/src/tui"
cat >"$PRZ/camp/inventory.json" <<'JSON'
{"requirement": [
  {"id":"REQ-001","title":"The client writes the alternate screen","effect":"device",
   "evidence":"observed","provider":"src/tui — the alternate-screen exit sequence written to the tty"},
  {"id":"REQ-002","title":"The daemon seals the vault","effect":"filesystem-write",
   "evidence":"observed","provider":"src/nowhere/absent.rs — a file that is not there at all"}]}
JSON
cat >"$PRZ/repo/src/tui/mod.rs" <<'RS'
// Leave the alternate screen. This comment is ordinary English on purpose: every
// real source file carries prose, and it is what the description of a provider
// gets matched against when the matcher is not there yet. Without a file that
// contains words like "the", "file" and "that", the seed below cannot fire and
// the test passes whether or not the fix is present.
pub fn leave_alternate_screen(out: &mut impl Write) { write!(out, "\x1b[?1049l").unwrap(); }
RS
echo '{"project":"Prose","sourceRoot":"'"$PRZ/repo"'"}' >"$PRZ/camp/campaign.json"

out="$(python3 "$S/vacuity-check.py" "$PRZ/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "REQ-002 declares" <<<"$out"; then
  say "ok    a provider whose path is absent is not resolved by its own description"; PASS=$((PASS+1))
else
  echo "FAIL  prose after the dash still resolves a dangling provider (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# The module-directory half: a provider may name a module rather than a file,
# and REQ-001 names `src/tui`, a directory. Refusing it would push authors to
# name an arbitrary file inside it.
if ! grep -qF -- "REQ-001 declares" <<<"$out"; then
  say "ok    a provider naming a module directory resolves"; PASS=$((PASS+1))
else
  echo "FAIL  a directory provider should resolve"; echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

if grep -qF -- "2 of 2 named, 1 resolved" <<<"$out"; then
  say "ok    the prose census prints its own denominator"; PASS=$((PASS+1))
else
  echo "FAIL  expected 2 named / 1 resolved"; echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# The control. With the description removed the dangling provider must still be
# a finding — otherwise the fix is reading the dash rather than the claim.
python3 - "$PRZ/camp/inventory.json" <<'PY'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
d["requirement"][1]["provider"]="src/nowhere/absent.rs"
json.dump(d,open(p,"w"),indent=2)
PY
out="$(python3 "$S/vacuity-check.py" "$PRZ/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "REQ-002 declares" <<<"$out"; then
  say "ok    a bare dangling provider is still a finding without a description"; PASS=$((PASS+1))
else
  echo "FAIL  the claim itself must decide, not the presence of a dash (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# ── the inert-UI gates: controls, destinations, the lane ledger ─────────────
#
# The campaign these came from cleared every gate above while the application
# under test rendered six sidebar destinations as one placeholder view and wired
# every button to an empty closure. references/inert-ui.md. Each gate is proved
# to fire on a fixture built to trip it and then proved to clear.

INERT="$WORK/inert"
python3 "$S/campaign.py" init "$INERT" --project Inert --lanes web,macos-glass >/dev/null
mkdir -p "$INERT/build/App.app" && printf 'x' >"$INERT/build/App.app/binary"
python3 "$S/campaign.py" lane "$INERT" --lane macos-glass \
  --artifact "$INERT/build/App.app" --built-by "xcodebuild -scheme App" \
  --attached "pid 1 owns window 'App'" >/dev/null
echo '[{"id":"REQ-001","class":"behaviour","text":"the workspace opens a folder"}]' >"$WORK/ir.json"
cat >"$WORK/is.json" <<'JSON'
[{"label":"Workspace","controls":["Open Mock Folder…","Pull Proof","Copy Swift"]}]
JSON
python3 "$S/campaign.py" add "$INERT" --kind requirement --file "$WORK/ir.json" >/dev/null
python3 "$S/campaign.py" add "$INERT" --kind surface --file "$WORK/is.json" >/dev/null
png "$INERT/shots/ws.png" 40 30 1 2 3
cat >"$WORK/ic.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","lane":"macos-glass","oracle":"structural"}]
JSON
python3 "$S/campaign.py" add "$INERT" --kind case --file "$WORK/ic.json" >/dev/null
python3 "$S/campaign.py" set "$INERT" --case CASE-0001 --status pass \
  --evidence "shots/ws.png" --armed >/dev/null
expect "a surface whose declared controls nothing actuates does not clear" 1 "$INERT" \
  "declaring control(s) nothing has driven"

# The denominator prints whether or not it blocks — the campaign that produced
# this rule was green, and the number nobody printed was the whole finding.
out="$(python3 "$S/campaign.py" check "$INERT" 2>&1)"
if grep -qF -- "Controls:   0 of 3 declared control(s) actuated" <<<"$out"; then
  say "ok    the control census prints its own denominator"; PASS=$((PASS+1))
else
  echo "FAIL  expected a printed control denominator"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# A presence-rung case that names an actuation has measured the click and not the
# effect, so it must not move the census.
python3 - "$INERT/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["actuates"]=["Open Mock Folder…","Pull Proof","Copy Swift"]
json.dump(c,open(p,"w"),indent=2)
PY2
expect "a below-outcome case does not actuate anything" 1 "$INERT" \
  "whose every declared control was driven and not one drive produced a passing effect-rung result"

# Raised to an effect rung, the same case clears it.
python3 - "$INERT/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["oracle"]="outcome"
json.dump(c,open(p,"w"),indent=2)
PY2
expect "an effect-rung case actuating every declared control clears" 0 "$INERT"

# A case actuating a control its surface never declared has no denominator.
python3 - "$INERT/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["actuates"].append("Summon The Kraken")
json.dump(c,open(p,"w"),indent=2)
PY2
expect "an actuation naming an undeclared control does not clear" 1 "$INERT" \
  "actuating a control their surface never declared"
python3 - "$INERT/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["actuates"]=[n for n in c[0]["actuates"] if n != "Summon The Kraken"]
json.dump(c,open(p,"w"),indent=2)
PY2
expect "removing the stray actuation clears it again" 0 "$INERT"

# ── destinations of one shell that publish one image ────────────────────────
DEST="$WORK/dest"
python3 "$S/campaign.py" init "$DEST" --project Dest --lanes web >/dev/null
echo '[{"id":"REQ-001","class":"behaviour","text":"each destination shows its own screen"}]' >"$WORK/dr.json"
cat >"$WORK/ds.json" <<'JSON'
[{"id":"SURF-001","label":"Shell"},
 {"id":"SURF-002","label":"Mocks","destinationOf":"SURF-001","shot":"shots/mocks.png"},
 {"id":"SURF-003","label":"Storyboards","destinationOf":"SURF-001","shot":"shots/storyboards.png"}]
JSON
python3 "$S/campaign.py" add "$DEST" --kind requirement --file "$WORK/dr.json" >/dev/null
python3 "$S/campaign.py" add "$DEST" --kind surface --file "$WORK/ds.json" >/dev/null
png "$DEST/shots/mocks.png" 40 30 9 9 9
png "$DEST/shots/storyboards.png" 40 30 9 9 9    # byte-identical: the defect
png "$DEST/shots/shell.png" 40 30 1 1 1
cat >"$WORK/dc.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","lane":"web","oracle":"outcome"},
 {"surface":"SURF-002","req":"REQ-001","lane":"web","oracle":"outcome"},
 {"surface":"SURF-003","req":"REQ-001","lane":"web","oracle":"outcome"}]
JSON
python3 "$S/campaign.py" add "$DEST" --kind case --file "$WORK/dc.json" >/dev/null
for i in 1 2 3; do
  python3 "$S/campaign.py" set "$DEST" --case "CASE-000$i" --status pass \
    --evidence "shots/shell.png" --armed >/dev/null
done
expect "two destinations of one shell publishing one image do not clear" 1 "$DEST" \
  "publish one identical image"

# A declared share does not excuse it here, which is the one place this gate is
# stricter than the general duplicate rule.
mkdir -p "$DEST/evidence/shots"
cat >"$DEST/evidence/shots/captures.json" <<'JSON'
[{"path":"shots/mocks.png","subject":"SURF-002","target":"/mocks","channel":"cdp",
  "sharesWith":["SURF-003"],"sharesReason":"one address"},
 {"path":"shots/storyboards.png","subject":"SURF-003","target":"/mocks","channel":"cdp",
  "sharesWith":["SURF-002"],"sharesReason":"one address"}]
JSON
expect "a declared share does not excuse two destinations of one menu" 1 "$DEST" \
  "publish one identical image"

png "$DEST/shots/storyboards.png" 40 30 3 4 5     # each destination its own render
expect "distinct destination renders clear" 0 "$DEST"

# A destination no case reaches is a hole in the shell's denominator.
cat >"$WORK/ds2.json" <<'JSON'
[{"id":"SURF-004","label":"Proctor Runs","destinationOf":"SURF-001"}]
JSON
python3 "$S/campaign.py" add "$DEST" --kind surface --file "$WORK/ds2.json" >/dev/null
expect "a destination no case reaches does not clear" 1 "$DEST" \
  "with a destination no case reaches"

# ── the lane ledger is printed, and is an advisory rather than a gate ───────
LANE="$WORK/lane"
python3 "$S/campaign.py" init "$LANE" --project Lane --lanes web,api >/dev/null
echo '[{"id":"REQ-001","class":"behaviour","text":"the api answers"}]' >"$WORK/lr.json"
echo '[{"label":"Console"}]' >"$WORK/ls.json"
python3 "$S/campaign.py" add "$LANE" --kind requirement --file "$WORK/lr.json" >/dev/null
python3 "$S/campaign.py" add "$LANE" --kind surface --file "$WORK/ls.json" >/dev/null
png "$LANE/shots/a.png" 20 20 5 5 5
cat >"$WORK/lc.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","lane":"api","oracle":"outcome"},
 {"surface":"SURF-001","req":"REQ-001","lane":"web","oracle":"structural"}]
JSON
python3 "$S/campaign.py" add "$LANE" --kind case --file "$WORK/lc.json" >/dev/null
for i in 1 2; do
  python3 "$S/campaign.py" set "$LANE" --case "CASE-000$i" --status pass \
    --evidence "shots/a.png" --armed >/dev/null
done
out="$(python3 "$S/campaign.py" check "$LANE" 2>&1)"; rc=$?
if [ "$rc" = 0 ] \
   && grep -qF -- "Lane:       web — 1 case(s) · 1 pass · 0 at an effect rung" <<<"$out" \
   && grep -qF -- "Worth reading, not blocking" <<<"$out"; then
  say "ok    a lane with no effect-rung pass is reported on a clear run"; PASS=$((PASS+1))
else
  echo "FAIL  the lane ledger must print per lane and advise without blocking (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# ── the blind pass can see an arrow-style test block ────────────────────────
#
# Measured on two repositories: one monorepo held 224 declaration-style blocks
# and 2,179 arrow-style ones; a second held 4,741 arrow-style and zero
# declarations, so `blind=0` there was a statement about none of its tests.
ARROW="$WORK/arrow"
mkdir -p "$ARROW/camp" "$ARROW/tests" "$ARROW/src"
cat >"$ARROW/tests/config.spec.ts" <<'TS'
import { writeConfig, readConfig } from '../src/config';

it('writes the config and never looks again', async () => {
  await writeConfig({ a: 1 });
  expect(true).toBe(true);
});

test("writes the config and reads it back", async () => {
  await writeConfig({ a: 2 });
  const got = await readConfig();
  expect(got.a).toBe(2);
});
TS
echo 'export const writeConfig = async (x: any) => x;' >"$ARROW/src/config.ts"
cat >"$ARROW/camp/inventory.json" <<'JSON'
{"requirement":[{"id":"REQ-001","title":"config persists","effect":"filesystem-write",
  "evidence":"reported","provider":"src/config.ts writeConfig"}]}
JSON
echo '{"project":"Arrow","sourceRoot":"'"$ARROW/src"'","testRoot":"'"$ARROW/tests"'"}' \
  >"$ARROW/camp/campaign.json"
out="$(python3 "$S/vacuity-check.py" "$ARROW/camp" --mutator writeConfig --reader readConfig 2>&1)"
if grep -qF -- "arrow-style it/test 2" <<<"$out" \
   && grep -qF -- "examined=2" <<<"$out" \
   && grep -qF -- "no read after it" <<<"$out"; then
  say "ok    the blind pass sees arrow-style it/test blocks"; PASS=$((PASS+1))
else
  echo "FAIL  the blind pass reported nothing over an arrow-style corpus"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# The control: a corpus the pass cannot parse must say so rather than print a
# clean zero. `.mjs` is outside the scanned suffix list, so this file is a real
# file the pass will not read.
NOBLOCK="$WORK/noblock"
mkdir -p "$NOBLOCK/camp" "$NOBLOCK/tests"
printf 'const x = 1;\n' >"$NOBLOCK/tests/a.spec.ts"
cat >"$NOBLOCK/camp/inventory.json" <<'JSON'
{"requirement":[{"id":"REQ-001","title":"x","effect":"none","evidence":"reported"}]}
JSON
echo '{"project":"NoBlock","testRoot":"'"$NOBLOCK/tests"'"}' >"$NOBLOCK/camp/campaign.json"
out="$(python3 "$S/vacuity-check.py" "$NOBLOCK/camp" --gate 2>&1)"; rc=$?
if [ "$rc" = 1 ] && grep -qF -- "NOT MEASURED" <<<"$out"; then
  say "ok    zero recognised blocks reads as not measured, not as clean"; PASS=$((PASS+1))
else
  echo "FAIL  a blind pass over zero recognised blocks must not report clean (exit $rc)"
  echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# ── the journey gates: boundaries, differential manifest, denominators ─────
#
# A journey is a history, so no per-surface count can see it. The Android
# data-loss benchmark holds 110 reproducible faults of the interrupt-and-resume
# shape; RegDroid measured a 64% false-positive rate on previous-build diffs, 93%
# of them intended changes. references/sweeps.md sweeps O and P.

JRN="$WORK/journey"
python3 "$S/campaign.py" init "$JRN" --project Journey --lanes web >/dev/null
echo '[{"id":"REQ-001","class":"behaviour","text":"a draft survives interruption"}]' >"$WORK/jr.json"
echo '[{"label":"Checkout"}]' >"$WORK/js.json"
python3 "$S/campaign.py" add "$JRN" --kind requirement --file "$WORK/jr.json" >/dev/null
python3 "$S/campaign.py" add "$JRN" --kind surface --file "$WORK/js.json" >/dev/null
png "$JRN/shots/j.png" 20 20 4 4 4

# A critical journey cut at only two of the five durable boundaries.
cat >"$WORK/jj.json" <<'JSON'
[{"id":"JRN-001","label":"Place an order","critical":true,
  "boundariesCut":["request-issued","server-committed"]}]
JSON
python3 "$S/campaign.py" add "$JRN" --kind journey --file "$WORK/jj.json" >/dev/null
cat >"$WORK/jc.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","journey":"JRN-001","lane":"web","oracle":"outcome"}]
JSON
python3 "$S/campaign.py" add "$JRN" --kind case --file "$WORK/jc.json" >/dev/null
python3 "$S/campaign.py" set "$JRN" --case CASE-0001 --status pass \
  --evidence "shots/j.png" --armed >/dev/null
expect "a critical journey not cut at every boundary does not clear" 1 "$JRN" \
  "not cut at every durable boundary"

out="$(python3 "$S/campaign.py" check "$JRN" 2>&1)"
if grep -qF -- "boundaries 2/5 cut" <<<"$out"; then
  say "ok    the journey ledger prints its boundary denominator"; PASS=$((PASS+1))
else
  echo "FAIL  expected a printed boundary denominator"; echo "$out" | sed 's/^/      /'
  FAIL=$((FAIL+1))
fi

# Cutting at all five clears it.
python3 - "$JRN/inventory.json" <<'PY2'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
d["journey"][0]["boundariesCut"]=["request-issued","server-committed","provider-effect",
                                   "client-persisted","user-acknowledged"]
json.dump(d,open(p,"w"),indent=2)
PY2
expect "cutting at every boundary clears it" 0 "$JRN"

# A boundary name outside the closed list has no denominator to count against.
python3 - "$JRN/inventory.json" <<'PY2'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
d["journey"][0]["boundariesCut"].append("vibes-checked")
json.dump(d,open(p,"w"),indent=2)
PY2
expect "an unrecognised boundary name does not clear" 1 "$JRN" \
  "naming a boundary that is not one of the five"
python3 - "$JRN/inventory.json" <<'PY2'
import json,sys
p=sys.argv[1]; d=json.load(open(p))
d["journey"][0]["boundariesCut"]=[b for b in d["journey"][0]["boundariesCut"] if b!="vibes-checked"]
json.dump(d,open(p,"w"),indent=2)
PY2
expect "removing it clears again" 0 "$JRN"

# A previous-build comparison with no change-intent manifest.
python3 - "$JRN/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["comparedAgainstBuild"]="v2.3.1"
json.dump(c,open(p,"w"),indent=2)
PY2
expect "a differential claim with no change-intent manifest does not clear" 1 "$JRN" \
  "no change-intent manifest"
python3 - "$JRN/cases.json" <<'PY2'
import json,sys
p=sys.argv[1]; c=json.load(open(p))
c[0]["changeIntentManifest"]="docs/change-intent/v2.3.2.json"
json.dump(c,open(p,"w"),indent=2)
PY2
expect "declaring the manifest clears it" 0 "$JRN"

# A journey nothing drives.
cat >"$WORK/jj2.json" <<'JSON'
[{"id":"JRN-002","label":"Refund an order","critical":false,"boundariesCut":[]}]
JSON
python3 "$S/campaign.py" add "$JRN" --kind journey --file "$WORK/jj2.json" >/dev/null
expect "a journey no case drives does not clear" 1 "$JRN" "journey(s) with no case at all"

# ── the evidence-plane gate ────────────────────────────────────────────────
#
# Measured across seven projects in one week, each reporting its backlog
# implemented and verified: every one had retired stated intent on evidence from
# a weaker plane than the intent lived on. The oracle rung was honest each time —
# those cases really did assert an outcome, against a double.

PLN="$WORK/plane"
python3 "$S/campaign.py" init "$PLN" --project Plane --lanes api,macos-glass >/dev/null
cat >"$WORK/pr.json" <<'JSON'
[{"id":"REQ-001","class":"behaviour","text":"the desktop app opens a folder and compiles it",
  "planes":["in-tree","live-glass"]}]
JSON
echo '[{"label":"Workspace"}]' >"$WORK/ps.json"
python3 "$S/campaign.py" add "$PLN" --kind requirement --file "$WORK/pr.json" >/dev/null
python3 "$S/campaign.py" add "$PLN" --kind surface --file "$WORK/ps.json" >/dev/null
png "$PLN/shots/p.png" 20 20 7 7 7
# An outcome-rung case — an honest one — but against an in-process double.
cat >"$WORK/pc.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","lane":"api","oracle":"outcome","plane":"in-tree"}]
JSON
python3 "$S/campaign.py" add "$PLN" --kind case --file "$WORK/pc.json" >/dev/null
python3 "$S/campaign.py" set "$PLN" --case CASE-0001 --status pass \
  --evidence "shots/p.png" --armed >/dev/null
expect "an in-tree pass does not satisfy a live-glass requirement" 1 "$PLN" \
  "declaring a plane no passing case reaches"

out="$(python3 "$S/campaign.py" check "$PLN" 2>&1)"
if grep -qF -- "Planes:     in-tree 1" <<<"$out"; then
  say "ok    the plane census prints what evidence was checked against"; PASS=$((PASS+1))
else
  echo "FAIL  expected a printed plane census"; echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

# Adding the glass case clears it. Same rung, different plane.
cat >"$WORK/pc2.json" <<'JSON'
[{"surface":"SURF-001","req":"REQ-001","lane":"macos-glass","oracle":"outcome","plane":"live-glass"}]
JSON
python3 "$S/campaign.py" add "$PLN" --kind case --file "$WORK/pc2.json" >/dev/null
python3 "$S/campaign.py" set "$PLN" --case CASE-0002 --status pass \
  --evidence "shots/p.png" --armed >/dev/null
mkdir -p "$PLN/build/App.app" && printf 'x' >"$PLN/build/App.app/b"
python3 "$S/campaign.py" lane "$PLN" --lane macos-glass --artifact "$PLN/build/App.app" \
  --built-by "xcodebuild" --attached "pid 1 owns window" >/dev/null
expect "reaching the declared plane clears it" 0 "$PLN"

# A plane outside the closed list has no census to count against.
out="$(echo '[{"surface":"SURF-001","req":"REQ-001","lane":"api","oracle":"outcome","plane":"vibes"}]' \
  > "$WORK/pc3.json"; python3 "$S/campaign.py" add "$PLN" --kind case --file "$WORK/pc3.json" 2>&1)"
if grep -qF -- "is not a plane" <<<"$out"; then
  say "ok    an unrecognised plane is refused at add"; PASS=$((PASS+1))
else
  echo "FAIL  add should refuse an unknown plane"; echo "$out" | sed 's/^/      /'; FAIL=$((FAIL+1))
fi

echo "campaign gate tests: $PASS passed, $FAIL failed"
[ "$FAIL" = 0 ] || exit 1

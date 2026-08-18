#!/usr/bin/env bash
# Adversarial tests for mock_check.py.
#
# A check that cannot fail on plausible input is a finding about the checks, not a pass.
# Each case below is a mock built to defeat exactly one check, with the exit code it must
# produce. Run it after any edit to the gate.
#
#   bash scripts/gate_tests.sh
#
# Exit 0 means every check bites. Any FAIL line below is a hole in the gate.

set -u
GATE="$(cd "$(dirname "$0")" && pwd)/mock_check.py"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
pass=0; fail=0

# $1 name · $2 expected exit · $3 grep pattern that must appear in combined output · $4 body
case_() {
  local name="$1" want="$2" needle="$3" body="$4"
  printf '%s' "$body" > "$TMP/ledgerline-probe.html"
  local out; out="$(python3 "$GATE" "$TMP/ledgerline-probe.html" 2>&1)"; local got=$?
  if [ "$got" = "$want" ] && printf '%s' "$out" | grep -qi -- "$needle"; then
    printf 'ok    %-46s exit=%s\n' "$name" "$got"; pass=$((pass+1))
  else
    printf 'FAIL  %-46s exit=%s want=%s (needle: %s)\n' "$name" "$got" "$want" "$needle"
    printf '%s\n' "$out" | sed 's/^/        /' | head -12
    fail=$((fail+1))
  fi
}

STYLE_OK='<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
button:focus-visible{outline:2px solid #0071E3}</style>'
METRICS_OK='<!-- mac-craft:metrics
titlebar 33px kit
unified-toolbar 52px kit
control-regular 24px kit
body-type 13px kit
sidebar 256px kit
selection-radius 8px kit
-->'
BODY_OK='<div class="t"></div><div class="tb"></div><div class="c"></div><div class="s"></div><div class="r">Cleared balance</div><button>Reconcile</button><div class="empty-state">No transactions yet</div>'

# --- the control: a mock that should pass, so a later FAIL is about the case, not the harness
case_ "control: clean mock passes" 0 "PASS" \
  "<title>Ledgerline</title>$METRICS_OK$STYLE_OK$BODY_OK"

# --- [metrics] the novel check: declared, kit-correct, and absent from the stylesheet
case_ "metrics: declared value not built in CSS" 1 "appears nowhere in the CSS" \
  "<title>L</title><!-- mac-craft:metrics
titlebar 33px kit
--><style>:root{--bg:#FFF}body{background:var(--bg);color:rgba(0,0,0,.85);font-size:13px}
.t{height:48px}button:focus-visible{outline:2px solid #0071E3}</style><div class=\"t\">Balance</div><button>Go</button><div class=\"empty-state\">none</div>"

case_ "metrics: kit tag disagrees with published value" 1 "the kit specifies 33pt" \
  "<title>L</title><!-- mac-craft:metrics
titlebar 48px kit
--><style>:root{--bg:#FFF}body{background:var(--bg);color:rgba(0,0,0,.85);font-size:13px}
.t{height:48px}button:focus-visible{outline:2px solid #0071E3}</style><div class=\"t\">Balance</div><button>Go</button><div class=\"empty-state\">none</div>"

case_ "metrics: untagged row is a defect" 1 "no recognised tier" \
  "<title>L</title><!-- mac-craft:metrics
titlebar 33px
--><style>:root{--bg:#FFF}body{background:var(--bg);color:rgba(0,0,0,.85);font-size:13px}
.t{height:33px}button:focus-visible{outline:2px solid #0071E3}</style><div class=\"t\">Balance</div><button>Go</button><div class=\"empty-state\">none</div>"

case_ "metrics: direction tag on locked chrome metric" 1 "tagged \`direction\`" \
  "<title>L</title><!-- mac-craft:metrics
titlebar 33px direction
--><style>:root{--bg:#FFF}body{background:var(--bg);color:rgba(0,0,0,.85);font-size:13px}
.t{height:33px}button:focus-visible{outline:2px solid #0071E3}</style><div class=\"t\">Balance</div><button>Go</button><div class=\"empty-state\">none</div>"

case_ "metrics: empty block is unmeasured, never a pass" 2 "not a filled one" \
  "<title>L</title><!-- mac-craft:metrics
--><style>:root{--bg:#FFF}body{background:var(--bg);color:rgba(0,0,0,.85);font-size:13px}
button:focus-visible{outline:2px solid #0071E3}</style><div>Balance</div><button>Go</button><div class=\"empty-state\">none</div>"

# --- [contrast] the spine
case_ "contrast: 1.00:1 same-colour text" 1 "same colour as its own background" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
.g{background:#0088FF;color:#0088FF}button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<div class=\"g\">+</div>"

case_ "contrast: no text at all is unmeasured, not a pass" 2 "examined=0" \
  "<title>L</title>$METRICS_OK$STYLE_OK<div class=\"t\"></div><div class=\"tb\"></div><div class=\"c\"></div><div class=\"s\"></div><div class=\"r\"></div>"

case_ "contrast: unresolvable pair is not counted as passing" 0 "NOT counted as a pass" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
.grad{background:linear-gradient(#fff,#000);color:rgba(0,0,0,.85)}
button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<div class=\"grad\">Reconciled</div>"

case_ "contrast: system-hue failure gets its own message" 1 "platform's own published value" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
.p{background:#0088FF;color:#FFFFFF;font-size:13px}button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<button class=\"p\">Reconcile</button>"

case_ "contrast: disabled text is exempt, not a failure" 0 "disabled_exempt=1" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
button[disabled]{color:rgba(0,0,0,0.25)}button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<button disabled>Archived</button>"

# --- [keyboard]
case_ "keyboard: focus-visible inside a comment does not count" 1 "focus-visible\` 0 and" \
  "<title>L</title>$METRICS_OK<style>/* button:focus-visible{outline:2px solid red} */
:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}</style>$BODY_OK"

case_ "keyboard: clickable div with no role or tabindex" 1 "keyboard-dead" \
  "<title>L</title>$METRICS_OK$STYLE_OK$BODY_OK<div onclick=\"go()\">Match</div>"

# --- [self-contained], [casing], [cursor], [content], [naming]
case_ "self-contained: external web font" 1 "external reference" \
  "<title>L</title>$METRICS_OK<link rel=stylesheet href=\"https://fonts.googleapis.com/x\">$STYLE_OK$BODY_OK"

case_ "casing: tracked uppercase at heading size" 1 "loudest web tell" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
.h{text-transform:uppercase;letter-spacing:.09em;font-size:14px}button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<div class=\"h\">Ledgers</div>"

case_ "cursor: hand cursor on a button" 1 "web-content signal" \
  "<title>L</title>$METRICS_OK<style>:root{--bg:#FFFFFF;--fg:rgba(0,0,0,0.85)}body{background:var(--bg);color:var(--fg);font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
.btn{cursor:pointer}button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK<button class=\"btn\">Go</button>"

case_ "content: lorem ipsum" 1 "lorem ipsum" \
  "<title>L</title>$METRICS_OK$STYLE_OK$BODY_OK<p>Lorem ipsum dolor sit amet</p>"

case_ "content: unfilled prose placeholder is caught" 1 "unfilled template placeholder" \
  "<title>L</title>$METRICS_OK$STYLE_OK$BODY_OK<p>{{WHY_IT_SHIPS — the recommendation goes here}}</p>"

case_ "tokens: no token layer at all" 1 "no colour custom properties" \
  "<title>L</title>$METRICS_OK<style>body{background:#FFFFFF;color:#262626;font-size:13px}
.t{height:33px}.tb{height:52px}.c{height:24px}.s{width:256px}.r{border-radius:8px}
button:focus-visible{outline:2px solid #0071E3}</style>$BODY_OK"

echo
echo "----------------------------------------------------------------"
echo "$pass passed, $fail failed"
[ "$fail" = 0 ] || echo "A FAIL above is a check that did not bite — a hole in the gate, not in the fixture."
exit $([ "$fail" = 0 ] && echo 0 || echo 1)

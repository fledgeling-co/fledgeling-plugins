#!/usr/bin/env bash
# run-preflight.sh — serve a deck if needed, run deck-preflight.js against it,
# print the JSON, and return a deterministic exit code.
#
#   ./run-preflight.sh http://127.0.0.1:8000/deck.html
#   ./run-preflight.sh ./deck.html                     # serves it for you
#   ./run-preflight.sh ./deck.html --regulated         # adds the disclosure checks
#   ./run-preflight.sh ./deck.html --selector '.slide-wrap'
#   ./run-preflight.sh ./deck.html --source filings.md # cross-checks every figure
#   ./run-preflight.sh ./deck.html --wait 10           # a loaded machine, or a deck
#                                                      # that builds its slides at runtime
#
# Serve over HTTP, never file:// — module scripts and web fonts fail silently
# from the filesystem, and a deck measured with its fonts missing reports type
# and overflow numbers that belong to a different deck.
#
# Exit codes, and each one is a different claim:
#   0  the gate ran and found no blocker      1  the gate ran and found blockers
#   2  bad usage                              3  a dependency is missing
#   4  the probe returned nothing             5  the probe could not be configured
#   6  the config did not reach the probe     7  the probe reported it did not run
# Only 0 is a pass. 4, 5, 6 and 7 exist because a gate that did not run is
# otherwise indistinguishable from a clean deck, and that is this file's whole job.
set -euo pipefail

# `set -e` plus `pipefail` is the right posture for a gate, and it has one failure
# mode that defeats the gate's whole purpose: an unexpected non-zero anywhere
# kills the script with no output at all, and an exit with no message is
# indistinguishable from a clean deck to anything reading the exit code.
#
# Measured while building this file, 18 Aug 2026: the token guard below was
# written as `grep -o … | wc -l`, and on the case it exists to catch — the
# placeholder absent, so grep matches nothing and exits 1 — pipefail killed the
# script at that assignment, before the `if` could report. The guard against the
# silent gate exited silently. So there is a net under all of it.
trap 'rc=$?; if [ $rc -ne 0 ] && [ "${VERDICT_PRINTED:-0}" != "1" ]; then
        printf "\n[DECK-PREFLIGHT ABORTED] run-preflight.sh exited %s at line %s with no verdict.\n" "$rc" "$LINENO" >&2
        printf "This is NOT a pass: the gate stopped before it could report.\n" >&2
      fi' ERR

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROBE="$HERE/deck-preflight.js"
TARGET="${1:?usage: run-preflight.sh <url|file.html> [--regulated] [--selector SEL] [--canvas WxH] [--source FILE] [--wait N]}"
shift || true

CFG_REGULATED=false; CFG_SEL=null; CFG_W=1920; CFG_H=1080; SOURCES=(); WAIT=3
while [ $# -gt 0 ]; do
  case "$1" in
    --regulated) CFG_REGULATED=true; shift ;;
    --selector)  CFG_SEL="\"$2\""; shift 2 ;;
    --canvas)    CFG_W="${2%x*}"; CFG_H="${2#*x}"; shift 2 ;;
    --source)    SOURCES+=("$2"); shift 2 ;;
    --wait)      WAIT="$2"; shift 2 ;;
    *) echo "unknown option: $1" >&2; exit 2 ;;
  esac
done

SRV_PID=""
cleanup() { [ -n "$SRV_PID" ] && kill "$SRV_PID" 2>/dev/null || true; }
trap cleanup EXIT

URL="$TARGET"
SERVED_SHA="(not computed: gated a URL, not a file)"
if [[ "$TARGET" != http* ]]; then
  [ -f "$TARGET" ] || { echo "no such file: $TARGET" >&2; exit 2; }
  DIR="$(cd "$(dirname "$TARGET")" && pwd)"; FILE="$(basename "$TARGET")"
  # The served bytes are the delivered bytes only if nobody swaps the file. Print
  # the hash so the delivery can name what was actually gated: a gate run against
  # deck.html and a handover of deck-final.html is otherwise undetectable.
  SERVED_SHA="$(shasum -a 256 "$TARGET" | cut -c1-16)"
  PORT=$(( 8300 + RANDOM % 400 ))
  ( cd "$DIR" && python3 -m http.server "$PORT" >/dev/null 2>&1 ) &
  SRV_PID=$!
  sleep 1.5
  URL="http://127.0.0.1:$PORT/$FILE"
  echo "serving $TARGET at $URL" >&2
fi

command -v obscura >/dev/null || { echo "obscura not on PATH" >&2; exit 3; }
command -v python3 >/dev/null || { echo "python3 not on PATH" >&2; exit 3; }

# ── Configure the probe ──────────────────────────────────────────────────────
#
# The payload must be ONE expression, and the probe must stay the outermost one.
# Obscura's --eval returns the value of the first statement, so a
# `cfg = {…}; probe()` payload evaluates to null — a gate that reports nothing
# while looking like it ran. So the config is substituted into the probe's own
# final argument, replacing the string literal '__DECKCFG__'.
#
# That placeholder replaced a line-anchored `sed`, and the reason is measured.
# The old form was:
#   sed "s|^})(typeof __DECKCFG.*|})($CFG)|; s|^   : (typeof window.*||"
# anchored on the literal text and the three-space indentation of the file's last
# two lines. Reproduced 18 Aug 2026: reformatting that tail to the shape a
# standard formatter emits matches NEITHER anchor, so both substitutions no-op,
# the payload stays valid JavaScript, the config falls through to `{}`, and
# `regulated` reverts to false. A `--regulated` run then printed
# `[DECK-PREFLIGHT PASS] 0 blockers across 3 slides examined` with all four
# disclosure checks never having run — on an ASX results deck, the
# highest-stakes output this skill produces.
#
# A string literal is atomic, so no formatter can split it; only its quote style
# can change, and both are accepted. Two independent guards, because neither is
# sufficient alone: this one asserts the substitution CAN happen, and the one
# after the run asserts that it DID.
TOKENS="$( { grep -o -F -e "'__DECKCFG__'" -e '"__DECKCFG__"' "$PROBE" || true; } | wc -l | tr -d ' ')"
if [ "$TOKENS" != "1" ]; then
  echo "the probe's config placeholder appears $TOKENS time(s), expected exactly 1." >&2
  echo "$PROBE cannot be configured, so --regulated/--selector/--canvas would be" >&2
  echo "silently dropped and the probe would run on defaults. This is NOT a pass." >&2
  echo "Restore the literal '__DECKCFG__' in the probe's final argument." >&2
  exit 5
fi
# A CRLF checkout no longer breaks the substitution — a string literal is not
# line-anchored — but the payload still reaches a browser as JavaScript, so
# normalise line endings on the way through.
CFG="{slideSelector:$CFG_SEL,canvasW:$CFG_W,canvasH:$CFG_H,regulated:$CFG_REGULATED}"
PAYLOAD="$(CFG="$CFG" PROBE="$PROBE" python3 -c '
import os, sys
src = open(os.environ["PROBE"], "r", newline="").read().replace("\r\n", "\n").replace("\r", "\n")
hits = [t for t in ("\x27__DECKCFG__\x27", "\"__DECKCFG__\"") if t in src]
if len(hits) != 1 or src.count(hits[0]) != 1:
    sys.stderr.write("probe placeholder is not present exactly once\n"); sys.exit(5)
sys.stdout.write(src.replace(hits[0], os.environ["CFG"], 1))
')"

# ── Run it ───────────────────────────────────────────────────────────────────
#
# Obscura's stderr is relayed verbatim rather than discarded. Its real failures
# are things a guessed message cannot diagnose: an SSRF block on a private
# address (the exact failure --allow-private-network exists for, which fires
# anyway if the URL is a hostname), a CDP crash, an --eval syntax error in the
# payload. All three arrive as an empty stdout and one specific stderr line, and
# the previous `2>/dev/null` threw that line away and substituted a guess.
ERRF="$(mktemp)"; trap 'rm -f "$ERRF"; cleanup' EXIT
probe() { { obscura --allow-private-network fetch "$URL" --wait "$1" --eval "$PAYLOAD" 2>"$ERRF" \
            || true; } | sed -n '/^{/,$p'; }
OUT="$(probe "$WAIT")"
# One bounded retry on a zero denominator, and ONLY on a zero denominator.
# Measured 18 Aug 2026: one run in four against a four-slide deck came back with
# zero slides matched, because the probe reached the DOM before the page's own
# load handler had fitted the stage. That is a race, not a verdict — but the
# retry may never turn into a pass by attrition, so it happens once, with a
# longer settle, and a second zero is reported as a zero.
#
# The retry is not always enough. Measured on a machine running eleven concurrent
# jobs, a three-slide deck still came back with zero slides after the 8-second
# retry — and the gate refused, which is the correct outcome and not a false one.
# `--wait N` is the knob for that case rather than a larger hardcoded guess: an
# operator who knows the machine is loaded, or that the deck assembles its slides
# at runtime, can say so, and the retry then doubles whatever they set.
if printf '%s' "$OUT" | grep -q '"zeroDenominator": true'; then
  echo "0 slides matched on the first probe; retrying once with a longer settle" >&2
  OUT="$(probe $(( WAIT > 8 ? WAIT * 2 : 8 )))"
fi
ERR="$(cat "$ERRF")"

if [ -z "$OUT" ]; then
  [ -n "$ERR" ] && printf 'obscura said: %s\n' "$ERR" >&2
  echo "preflight returned nothing — this is NOT a pass. The probe did not run." >&2
  echo "Check that $URL serves over HTTP and that obscura can reach it." >&2
  exit 4
fi
printf '%s\n' "$OUT"
[ -n "$ERR" ] && printf '\nobscura stderr (relayed verbatim, the run still produced output):\n%s\n' "$ERR" >&2

# ── Evaluate ─────────────────────────────────────────────────────────────────
#
# python3 rather than node: this script already requires python3 for the fallback
# server, so using it here removes a second runtime dependency. A machine without
# node previously failed this block and reported the failure as a deck blocker —
# which is the one thing the script exists to prevent, a gate that did not run
# being indistinguishable from a clean deck.
#
# The key lists are NOT hardcoded here any more. They come from the probe's own
# `policy` object, because a split that lives only in the runner is a split
# nothing else can read — and six of the probe's 25 summary keys used to reach
# neither list, so the type floor could not fail a build and chart coverage had
# no denominator.
SRC_ARGS=()
for s in ${SOURCES+"${SOURCES[@]}"}; do SRC_ARGS+=("$s"); done
# From here on the evaluator reports for itself, and a non-zero exit from it is
# the intended signal rather than an abort — so the net comes down. Leaving it
# armed printed an ABORTED line above every legitimate FAIL.
trap - ERR
set +e
VERDICT="$(printf '%s' "$OUT" | python3 -c '
import json, sys, re

want_regulated = sys.argv[1] == "true"
want_selector  = sys.argv[2]
want_canvas    = sys.argv[3]
served_sha     = sys.argv[4]
sources        = sys.argv[5:]

try:
    d = json.load(sys.stdin)
except Exception as e:
    print("preflight ran, but its output could not be parsed (%s) — this is NOT a pass, "
          "because blockers were never evaluated." % e, file=sys.stderr)
    sys.exit(7)

# The probe refuses rather than running when it cannot trust its own inputs.
if d.get("error"):
    print("\n[DECK-PREFLIGHT DID NOT RUN] %s" % d["error"], file=sys.stderr)
    print(d.get("note", ""), file=sys.stderr)
    sys.exit(7)

s   = d.get("summary", {})
cfg = d.get("config", {})
pol = d.get("policy", {})
why = d.get("consequences", {})
notes = d.get("notes", [])

# ── Guard two: did the config actually arrive? ────────────────────────────────
# The probe echoes what it received. Nothing used to compare it, so a
# substitution that silently no-opped produced a clean PASS on default config
# with every --regulated check unrun. `configKeysReceived` is the direct signal.
received = cfg.get("configKeysReceived")
mismatch = []
if received is not None and len(received) == 0:
    mismatch.append("the probe received NO config keys at all — the substitution did not land")
if bool(cfg.get("regulated")) != want_regulated:
    mismatch.append("regulated: asked %s, probe ran with %s" % (want_regulated, cfg.get("regulated")))
if want_selector != "null" and cfg.get("slideSelector") != want_selector.strip("\""):
    mismatch.append("slideSelector: asked %s, probe ran with %r" % (want_selector, cfg.get("slideSelector")))
if cfg.get("canvas") != want_canvas:
    mismatch.append("canvas: asked %s, probe ran with %r" % (want_canvas, cfg.get("canvas")))
if mismatch:
    print("\n[DECK-PREFLIGHT CONFIG DID NOT REACH THE PROBE] — this is NOT a pass.", file=sys.stderr)
    for m in mismatch: print("  " + m, file=sys.stderr)
    print("  The probe ran, but on configuration you did not ask for, so the checks you", file=sys.stderr)
    print("  asked for did not run. Do not re-run until the cause is found: a retry", file=sys.stderr)
    print("  reproduces it exactly.", file=sys.stderr)
    sys.exit(6)

# ── Checks that threw did not run, and a null is not a zero ──────────────────
notrun = [n for n in notes if "treat as NOT RUN" in n]
if notrun:
    print("\n[DECK-PREFLIGHT NOT RUN] %d check(s) threw and did not run. A check that did"
          % len(notrun), file=sys.stderr)
    print("not run returns null, which reads as 0, which is indistinguishable from clean:",
          file=sys.stderr)
    for n in notrun: print("  " + n, file=sys.stderr)

blockers = pol.get("blockers") or []
warnings = pol.get("warnings") or []
if not blockers:
    print("\n[DECK-PREFLIGHT NO POLICY] the probe returned no policy object, so which keys "
          "gate is unknown — this is NOT a pass.", file=sys.stderr)
    sys.exit(7)

# A zero denominator before anything else, because every other count in the run
# is a zero over nothing and reads exactly like a clean deck. Measured on the
# previous version: one run in four of a four-slide deck came back with zero
# slides matched and printed `PASS ... across 0 slides examined`, exit 0.
if s.get("zeroDenominator") or s.get("slidesExamined", 0) == 0:
    print("\n[DECK-PREFLIGHT ZERO DENOMINATOR] 0 slides were examined — this is NOT a pass.",
          file=sys.stderr)
    if why.get("zeroDenominator"): print("  → %s" % why["zeroDenominator"], file=sys.stderr)
    for n in notes: print("  %s" % n, file=sys.stderr)
    sys.exit(7)

def val(k):
    v = s.get(k)
    return v if isinstance(v, (int, float)) else 0

found, warned = [], []
for k in blockers:
    if k == "hueFamilies":
        continue
    if val(k):
        line = "%s: %s" % (k, s[k])
        if k == "chartsNotZeroBased":
            line += " of %s charts checked" % s.get("chartsChecked", "?")
        found.append((k, line))
for k in warnings:
    if k == "hueFamilies":
        if val(k) > 1: warned.append((k, "hueFamilies: %s" % s[k]))
        continue
    if k == "noDisplayTier":
        if val(k): warned.append((k, "noDisplayTier: the largest type on the deck is below the cover floor"))
        continue
    if val(k):
        line = "%s: %s" % (k, s[k])
        if k == "chartGroupsUnverified":
            line += " (of %s group(s) found; %s judged)" % (
                val(k) + val("chartsChecked"), s.get("chartsChecked", "?"))
        warned.append((k, line))

# ── The source cross-check: figures the source does not contain ──────────────
# Fabrication does not arrive as an invented headline figure. It arrives as
# texture around a real one, and the sharpest case is the DERIVED ratio — a
# figure the deck computed from two real numbers and set as a chip. The
# arithmetic is right, which is why it survives review; a ratio you derived is
# your claim, not the issuer disclosure, and it is a figure no board approved.
# A derived figure is exactly the figure that appears nowhere in the source.
#
# This is a WARNING and not a blocker, deliberately. A legitimately disclosed
# figure can be phrased differently in the source, and a loose detector produces
# a gate people learn to ignore — which is worse than no gate. It names what to
# check; it does not claim a defect.
def norm_fig(x):
    x = x.strip().lower().replace(",", "").replace(" ", "")
    x = re.sub(r"(%|x|bn|m|k)$", "", x)
    return x.rstrip(".")

if sources:
    corpus = ""
    unread = []
    for p in sources:
        try:
            corpus += open(p, "r", errors="replace").read() + "\n"
        except Exception as e:
            unread.append("%s (%s)" % (p, e))
    if unread:
        print("\n[DECK-PREFLIGHT SOURCE UNREAD] %s — the figure cross-check did NOT run "
              "over these, so its silence is not a result." % "; ".join(unread), file=sys.stderr)
    if corpus:
        have = set()
        for raw in re.findall(r"\d[\d,]*(?:\.\d+)?", corpus):
            have.add(norm_fig(raw))
            have.add(norm_fig(raw).rstrip("0").rstrip("."))
        unsourced = []
        for row in d.get("numerals", []):
            f = norm_fig(row["figure"])
            if f in have or f.rstrip("0").rstrip(".") in have:
                continue
            if re.fullmatch(r"(19|20)\d\d", f):
                continue      # a year: the as-at-date check owns these
            unsourced.append(row)
        if unsourced:
            print("\n[DECK-PREFLIGHT FIGURES NOT IN SOURCE] %d figure(s) on the deck appear "
                  "nowhere in the supplied source. %s" % (len(unsourced), why.get("typeBelowFloor", "")[:0] or
                  "A derived ratio is the shape to look for: the arithmetic can be right and the "
                  "figure still be your claim rather than the issuer disclosure."), file=sys.stderr)
            for row in unsourced[:12]:
                print("  %s  %-12s in %r" % (row["slide"], row["figure"], row["context"]), file=sys.stderr)

        # A target is not an achievement, and the title is where that gets lost.
        # Measured: the source said the measures TARGET ~$8m; the title read
        # "Workshop Consolidation Delivers ~$8m Annual Benefit". One verb turned
        # a forward-looking target into a reported result.
        ACHIEVED = re.compile(r"\b(delivers?|delivered|achiev\w+|generated|returned|produced|realis\w+|realiz\w+|grew|cut|reduced)\b", re.I)
        FORWARD  = re.compile(r"\b(target\w*|expect\w*|forecast\w*|anticipat\w*|guidance|intend\w*|aim\w*|projected|estimate\w*)\b", re.I)
        risky = []
        for t in d.get("titles", []):
            if not ACHIEVED.search(t["text"]):
                continue
            figs = [norm_fig(x) for x in re.findall(r"\d[\d,]*(?:\.\d+)?", t["text"])]
            for f in figs:
                for m in re.finditer(re.escape(f), corpus.replace(",", "")):
                    window = corpus.replace(",", "")[max(0, m.start()-220):m.end()+220]
                    if FORWARD.search(window):
                        risky.append((t["slide"], t["text"], f))
                        break
                else:
                    continue
                break
        if risky:
            print("\n[DECK-PREFLIGHT TENSE] %d declarative title(s) state an achievement for a "
                  "figure the source discusses in forward-looking terms:" % len(risky), file=sys.stderr)
            for slide, text, f in risky[:8]:
                print("  %s  %r  (figure %s appears near target/expect/guidance language in the source)"
                      % (slide, text, f), file=sys.stderr)

n = s.get("slidesExamined", 0)

if warned:
    print("\n[DECK-PREFLIGHT WARN] %d warning(s) across %s slides. Warnings do not gate: each"
          % (len(warned), n), file=sys.stderr)
    print("has a legitimate exception, so they are reported for a human to rule on.", file=sys.stderr)
    for k, line in warned:
        print("  %s" % line, file=sys.stderr)
        if why.get(k): print("      → %s" % why[k], file=sys.stderr)

if found:
    print("\n[DECK-PREFLIGHT FAIL] %d blocker(s) across %s slides examined:" % (len(found), n),
          file=sys.stderr)
    for k, line in found:
        print("  %s" % line, file=sys.stderr)
        # Every consequence below was already written in the probe, ten lines
        # above its own check, in a comment nothing downstream ever saw. The
        # count says a rule fired; this says what happens to the deck.
        if why.get(k): print("      → %s" % why[k], file=sys.stderr)
    print("\ngated: %s · served sha256 %s" % (want_canvas, served_sha), file=sys.stderr)
    sys.exit(1)

print("\n[DECK-PREFLIGHT PASS] 0 blockers across %s slides examined%s."
      % (n, "" if not notrun else ", but %d check(s) did not run" % len(notrun)))
print("charts: %s judged, %s not zero-based, %s group(s) unverified."
      % (s.get("chartsChecked"), s.get("chartsNotZeroBased"), s.get("chartGroupsUnverified")))
print("gated: %s · served sha256 %s" % (want_canvas, served_sha))
print("A pass means no KNOWN defect is present. It does not mean verified — "
      "walk the deck per references/deck-review.md.")
if notrun:
    # A pass with an unrun check is not a clean pass, and the caller must not be
    # able to quote the PASS line without the caveat travelling with it.
    print("This pass is INCOMPLETE: %d check(s) threw. Treat those as unmeasured, not clean."
          % len(notrun))
    sys.exit(7)
' "$CFG_REGULATED" "$CFG_SEL" "${CFG_W}x${CFG_H}" "$SERVED_SHA" ${SRC_ARGS+"${SRC_ARGS[@]}"} 2>&1)"
RC=$?
set -e
VERDICT_PRINTED=1
printf '%s\n' "$VERDICT" >&2
exit $RC

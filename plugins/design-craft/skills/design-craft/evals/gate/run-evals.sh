#!/usr/bin/env bash
# Structural evals for the design-craft lint gate: the original and the rebuild,
# same fixtures, same invocations. Every assertion is an artifact check — did the
# run produce X — rather than a score, and each prints the evidence it judged on.
#
#   ./run-evals.sh          runs both versions and writes results/scorecard.md
#
# The comparison is built to be able to lose: A19-A22 are cases the ORIGINAL
# handles, and they are scored on both sides.
cd "$(dirname "$0")/../.."
OLD=evals/old/design-lint.py
NEW=scripts/design-lint.py
FX=evals/fixtures
OUT=evals/results
mkdir -p "$OUT"
SC="$OUT/scorecard.tsv"
: > "$SC"
rm -f "$OUT"/*missing-checks.txt

# The rebuild classifies anything under fixtures/ or references/ as non-source and
# refuses to lint it — which is assertion A22, and which also means the harness
# has to opt its own fixtures back in. --include-all is passed to the rebuild
# only; the original takes no flags and would read one as a filename.
run() {  # run <old|new> <fixture-path> [extra-flag]
  local side="$1" fx="$2" flag="${3:-}" tag
  tag="$side-$(basename "$fx" .html)"
  if [ "$side" = new ]; then
    python3 "$NEW" $flag "$fx" > "$OUT/$tag.out" 2> "$OUT/$tag.err"
  else
    python3 "$OLD" "$fx" > "$OUT/$tag.out" 2> "$OUT/$tag.err"
  fi
  echo $? > "$OUT/$tag.rc"
}

for f in "$FX"/*.html; do
  run old "$f"; run new "$f" --include-all
done
# A22 is the one case run WITHOUT the opt-in, because refusing it is the assertion.
run old "$FX/references/doc-example.html"
run new "$FX/references/doc-example.html"

# assert <id> <side> <PASS|FAIL> <evidence>
assert() { printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> "$SC"; }

# Search stdout+stderr together: the split is a feature of the new runner and
# an assertion about *whether a check fired* must not depend on which channel
# it landed on. Channel placement is asserted separately (A16, A17).
both() { cat "$OUT/$1.out" "$OUT/$1.err" 2>/dev/null; }
fired() { both "$1" | grep -qF "[$2]"; }
sev()   { both "$1" | grep -E "^$2 " | grep -qF "[$3]"; }
rc()    { [ "$(cat "$OUT/$1.rc")" = "$2" ]; }

j() { # j <id> <side> <condition-already-evaluated:0|1> <evidence>
  if [ "$3" = 0 ]; then assert "$1" "$2" PASS "$4"; else assert "$1" "$2" FAIL "$4"; fi
}

# ---------------------------------------------------------------------------
# A1-A4  Contrast: the defect this skill had the most evidence about and no gate
# ---------------------------------------------------------------------------
for s in old new; do
  fired "$s-pricing-tiers" contrast; j A1 "$s" $? "13px brand orange on paper (#E65400 on #FDFCFA, 3.66:1) is reported"
  sev "$s-pricing-tiers" CRITICAL contrast; j A2 "$s" $? "a contrast failure gates at critical"
  fired "$s-oklch-palette" contrast; j A3 "$s" $? "a failing pair written in oklch() is resolved and reported"
  fired "$s-hero-gradient" contrast-unmeasurable; j A4 "$s" $? "text on a gradient is reported UNMEASURABLE rather than skipped"
done

# ---------------------------------------------------------------------------
# A5-A7  The gate must not fire on the skill's own canonical snippets
# ---------------------------------------------------------------------------
for s in old new; do
  rc "$s-device-frame" 0; j A5 "$s" $? "the documented phone-bezel snippet passes (exit 0)"
  rc "$s-tweak-panel" 0; j A6 "$s" $? "the documented tweak-panel snippet passes (exit 0)"
  both "$s-webfont-and-cdn" | grep -qE "MAJOR.*external-resource\]"; j A7 "$s" $((1-$?)) "a Google Fonts <link> is not condemned as a blocker (it is the one origin the artifact CSP permits)"
done

# ---------------------------------------------------------------------------
# A8-A10  Rules that could not fire correctly
# ---------------------------------------------------------------------------
for s in old new; do
  fired "$s-lineno-and-img" unsized-img; j A8 "$s" $? "an <img> with no width/height attributes is caught even when its style string contains the words"
  both "$s-lineno-and-img" | grep -qE "lineno-and-img\.html:7.*external-resource"; j A9 "$s" $? "the external resource is reported at its own line, not at the first // in the file"
  both "$s-suppression-unjustified" | grep -qF "[pure-bw]"; j A10 "$s" $? "a suppression with no reason does not silence its check"
done

# ---------------------------------------------------------------------------
# A11-A13  Silent failure modes the prose named and nothing gated
# ---------------------------------------------------------------------------
for s in old new; do
  fired "$s-reveal-and-token" reveal-blank; j A11 "$s" $? "a resting opacity:0 on a page with reveal keyframes is reported (prints and captures blank)"
  fired "$s-reveal-and-token" unread-token; j A12 "$s" $? "a token defined and never referenced is reported"
  fired "$s-index" focus-ring-removed; j A13 "$s" $? "outline:none with no replacement is reported"
done

# ---------------------------------------------------------------------------
# A14-A15  The deliverable's name is content
# ---------------------------------------------------------------------------
for s in old new; do
  fired "$s-index" missing-title; j A14 "$s" $? "an HTML deliverable with no <title> is reported"
  fired "$s-index" generic-filename; j A15 "$s" $? "index.html is reported as naming the format, not the design"
done

# ---------------------------------------------------------------------------
# A16-A18  The gate's own honesty
# ---------------------------------------------------------------------------
for s in old new; do
  grep -qE "^(CRITICAL|MAJOR)" "$OUT/$s-regress.out" && ! grep -qE "^MINOR" "$OUT/$s-regress.out"
  j A16 "$s" $? "gating findings go to stdout and warnings do not (fail/warn split)"
  grep -q "not checked" "$OUT/$s-regress.out"; j A17 "$s" $? "the run prints its own not-checked line, so a clean result cannot be read as verified"
  both "$s-regress" | grep -qE "\-> .+" ; j A18 "$s" $? "every finding names the downstream consequence, not just the rule"
done

# ---------------------------------------------------------------------------
# A19-A22  REGRESSION GUARDS — everything the original already caught
# ---------------------------------------------------------------------------
for s in old new; do
  for c in placeholder-text pure-bw gradient-stops unresolved-var default-card \
           default-font untracked-caps over-tight-tracking three-dots 100vh \
           zindex-arms-race div-as-button decorative-emoji leaked-verification; do
    both "$s-regress" | grep -qF "[$c]" || { echo "$c" >> "$OUT/$s-missing-checks.txt"; }
  done
  [ ! -s "$OUT/$s-missing-checks.txt" ]
  j A19 "$s" $? "all 14 checks the original carried still fire on the regression fixture"
  rc "$s-regress" 1; j A20 "$s" $? "a file full of defects exits non-zero"
  rc "$s-pricing-tiers" 1; j A21 "$s" $? "a contrast failure alone is enough to fail the build"
  [ ! -s "$OUT/$s-references-doc-example.out" ] || ! grep -qE "^(CRITICAL|MAJOR)" "$OUT/$s-references-doc-example.out"
  j A22 "$s" $? "the gate does not lint a file under references/ as source"
done

# ---------------------------------------------------------------------------
# A23-A25  COST ASSERTIONS — where the rebuild is deliberately weaker
# ---------------------------------------------------------------------------
# A scorecard that only shows wins convinces nobody. These three are real costs
# of the rebuild's design decisions, and the original passes all three.
for s in old new; do
  rc "$s-slop-only" 1
  j A23 "$s" $? "a file whose ONLY defects are aesthetic cues (pure b/w, Inter, the border-left card, Tailwind indigo) fails the build"
  ! ( both "$s-hero-gradient" | grep -qF "[contrast-unmeasurable]" )
  j A24 "$s" $? "a hero with text over a gradient produces no finding at all"
  rc "$s-tokens-for-consumers" 0
  j A25 "$s" $? "a specimen file publishing tokens for downstream consumers passes (exit 0)"
done

# ---------------------------------------------------------------------------
# Render the scorecard
# ---------------------------------------------------------------------------
python3 - "$SC" "$OUT/scorecard.md" <<'PY'
import collections, sys
rows = [l.rstrip("\n").split("\t") for l in open(sys.argv[1]) if l.strip()]
by = collections.OrderedDict()
for aid, side, verdict, ev in rows:
    by.setdefault(aid, {"ev": ev})[side] = verdict
old = sum(1 for a in by.values() if a.get("old") == "PASS")
new = sum(1 for a in by.values() if a.get("new") == "PASS")
out = [
 "# design-craft lint gate — structural evals, original vs rebuild", "",
 f"**original {old}/{len(by)} · rebuild {new}/{len(by)}**  ",
 "Artifact checks, not scores. Both versions run the same fixtures with the same",
 "invocations. A19-A22 are regression guards over what the original already did;",
 "A23-A25 are cost assertions the ORIGINAL passes and the rebuild deliberately",
 "does not — each one is a trade named in evidence.md rather than an oversight.", "",
 "| # | assertion | original | rebuild |", "|---|---|---|---|",
]
for aid, a in by.items():
    out.append(f"| {aid} | {a['ev']} | {a.get('old','-')} | {a.get('new','-')} |")
out += ["", "## Where the original wins or draws", ""]
lost = [f"- **{aid}** — {a['ev']}" for aid, a in by.items()
        if a.get("old") == "PASS" and a.get("new") != "PASS"]
drew = [f"- **{aid}** — {a['ev']}" for aid, a in by.items()
        if a.get("old") == "PASS" and a.get("new") == "PASS"]
out += (lost or ["_No assertion where the original passes and the rebuild does not._"])
out += ["", "Drawn (both pass) — these are the regression guards doing their job:", ""]
out += (drew or ["_none_"])
open(sys.argv[2], "w").write("\n".join(out) + "\n")
print("\n".join(out[:6]))
PY
echo "scorecard: $OUT/scorecard.md"

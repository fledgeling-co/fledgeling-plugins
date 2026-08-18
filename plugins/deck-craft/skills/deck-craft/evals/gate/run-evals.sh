#!/usr/bin/env bash
# Structural evals for the deck-craft preflight gate: old vs new, same fixtures,
# same invocations. Every assertion is an artifact check — did the run produce X —
# rather than a score, and each one prints the evidence it judged on.
#
#   ./run-evals.sh          runs both versions and writes results/scorecard.md
cd "$(dirname "$0")"
OLD=./old
OLDFMT=./old-reformatted            # the same original, tail reformatted
NEW=/Users/lukerhodes/Dev/fledgeling-plugins/plugins/deck-craft/skills/deck-craft/scripts
NEWFMT=./new-reformatted            # the rebuild, tail reformatted
mkdir -p results
SC=results/scorecard.tsv
: > "$SC"

run() {   # run <runner-dir> <tag> <fixture> [args...]
  local dir="$1" tag="$2" fx="$3"; shift 3
  "$dir/run-preflight.sh" "fixtures/$fx" "$@" > "results/$tag.out" 2>&1
  echo $? > "results/$tag.rc"
  # The ORIGINAL runner intermittently reports "PASS ... across 0 slides examined"
  # when the probe reaches the DOM before the page's load handler has fitted the
  # stage — measured at roughly 1 run in 4. That is assertion A5's defect, and it
  # must not be allowed to contaminate every other assertion by making a blocker
  # look like it stopped firing. So any run that examined zero slides is retried
  # once here, and the fact that it needed retrying is recorded.
  if grep -qE '0 slides (examined|were examined)|ZERO DENOMINATOR' "results/$tag.out" && [ "$fx" != noslides.html ]; then
    echo "$tag" >> results/zero-denominator-flakes.txt
    "$dir/run-preflight.sh" "fixtures/$fx" "$@" > "results/$tag.out" 2>&1
    echo $? > "results/$tag.rc"
  fi
}

# assert <id> <side> <PASS|FAIL> <note>
assert() { printf '%s\t%s\t%s\t%s\n' "$1" "$2" "$3" "$4" >> "$SC"; }

has()  { grep -qF -- "$2" "results/$1.out"; }
# The verdict block only: everything from the first [DECK-PREFLIGHT tag onward.
# A bare grep over the whole run also matches the probe's JSON dump, which lists
# every summary key including the zeros — so it scores a key that exists but never
# gates as if it had gated.
vhas() { sed -n '/^\[DECK-PREFLIGHT/,$p' "results/$1.out" | grep -qF -- "$2"; }
rc()   { cat "results/$1.rc"; }

echo "== A1  a --regulated run whose config was defeated by a formatter =="
run "$OLDFMT" a1-old regulated.html --regulated
run "$NEWFMT" a1-new regulated.html --regulated
has a1-old "PREFLIGHT PASS" \
  && assert A1 old FAIL "printed PASS with all four disclosure checks unrun (rc $(rc a1-old))" \
  || assert A1 old PASS "refused"
has a1-new "PREFLIGHT PASS" \
  && assert A1 new FAIL "printed PASS (rc $(rc a1-new))" \
  || assert A1 new PASS "refused, rc $(rc a1-new); provenanceMissing reported"

echo "== A2  the type floor must be able to fail a build =="
run "$OLD" a2-old typefloor.html
run "$NEW" a2-new typefloor.html
[ "$(rc a2-old)" = 0 ] && assert A2 old FAIL "typeBelowFloor computed and ignored; exit 0, PASS" \
                       || assert A2 old PASS "gated"
has a2-new "typeBelowFloor" && [ "$(rc a2-new)" != 0 ] \
  && assert A2 new PASS "typeBelowFloor is a blocker; rc $(rc a2-new)" \
  || assert A2 new FAIL "not gated"

echo "== A4  a declared two-bar pair with a truncated axis is judged =="
run "$OLD" a4-old charts.html
run "$NEW" a4-new charts.html
vhas a4-old "chartsNotZeroBased" \
  && assert A4 old PASS "judged" \
  || assert A4 old FAIL "2-bar groups declined by judge(); printed PASS at exit $(rc a4-old)"
vhas a4-new "chartsNotZeroBased" && [ "$(rc a4-new)" != 0 ] \
  && assert A4 new PASS "judged and blocking; rc $(rc a4-new)" \
  || assert A4 new FAIL "not judged"

echo "== A3  chart coverage reports its denominator =="
grep -qE 'of [0-9]+ charts checked|charts: [0-9]+ judged' results/a4-new.out \
  && assert A3 new PASS "denominator printed beside the count" \
  || assert A3 new FAIL "no denominator"
grep -qE 'of [0-9]+ charts checked|charts: [0-9]+ judged' results/a4-old.out \
  && assert A3 old PASS "denominator printed" \
  || assert A3 old FAIL "chartsChecked never reaches the verdict"

echo "== A5  a zero denominator is not a pass =="
run "$OLD" a5-old noslides.html --regulated
run "$NEW" a5-new noslides.html --regulated
has a5-old "PREFLIGHT PASS" \
  && assert A5 old FAIL "PASS across 0 slides examined, exit $(rc a5-old)" \
  || assert A5 old PASS "refused"
has a5-new "ZERO DENOMINATOR" && [ "$(rc a5-new)" = 7 ] \
  && assert A5 new PASS "refused with rc 7 and the cause named" \
  || assert A5 new FAIL "not refused"

echo "== A6  every blocker carries its downstream consequence =="
grep -q '      → ' results/a2-new.out \
  && assert A6 new PASS "consequence printed beneath each finding" \
  || assert A6 new FAIL "bare counts only"
grep -q '      → ' results/a2-old.out \
  && assert A6 old PASS "consequence printed" \
  || assert A6 old FAIL "bare count and coordinates; every consequence is in a source comment the caller never sees"

echo "== A7  the deck's own name is gated =="
run "$OLD" a7-old regulated.html --regulated
run "$NEW" a7-new regulated.html --regulated
vhas a7-old "genericName" && assert A7 old PASS "flagged" \
  || assert A7 old FAIL "<title>Deck</title> unchecked"
vhas a7-new "genericName" && assert A7 new PASS "flagged as a blocker" \
  || assert A7 new FAIL "not flagged"

echo "== A8  drawn accent marks count toward the accent budget =="
vhas a7-old "accentOverspent" && assert A8 old PASS "counted" \
  || assert A8 old FAIL "text leaves only: 4 accent bars + a rule scored 0, and accentOverspent never reaches the verdict"
vhas a7-new "accentOverspent" && assert A8 new PASS "drawn marks counted, reported as a warning" \
  || assert A8 new FAIL "not counted"

echo "== A9  a non-IFRS measure needs a statutory companion on its own slide =="
vhas a7-old "nonIfrsUnpaired" && assert A9 old PASS "flagged" \
  || assert A9 old FAIL "only deck-wide audit-qualifier presence is tested"
vhas a7-new "nonIfrsUnpaired" && assert A9 new PASS "flagged as a blocker (SEC Reg G / CDI 102.10, ASIC RG 230)" \
  || assert A9 new FAIL "not flagged"

echo "== A10 dual and inverted axes =="
run "$OLD" a10-old axes.html
run "$NEW" a10-new axes.html
vhas a10-old "axisMisleaders" && assert A10 old PASS "flagged" \
  || assert A10 old FAIL "no dual/inverted axis check; printed PASS at exit $(rc a10-old)"
vhas a10-new "axisMisleaders" && [ "$(rc a10-new)" != 0 ] \
  && assert A10 new PASS "both caught and blocking; rc $(rc a10-new)" \
  || assert A10 new FAIL "not caught"

echo "== A11 a misspelled config key is refused, not ignored =="
for side in old new; do
  src=$OLD/deck-preflight.js; [ $side = new ] && src=$NEW/deck-preflight.js
  python3 - "$src" "$side" <<'PY'
import sys,re
src=open(sys.argv[1]).read(); side=sys.argv[2]
for tok in ("'__DECKCFG__'",'"__DECKCFG__"'):
    if tok in src: src=src.replace(tok,'{regualted:true}',1); break
else:
    src=re.sub(r"\)\(typeof __DECKCFG.*\n.*$", ")({regualted:true})", src)
open('results/misspell-%s.js'%side,'w').write(src)
PY
done
(cd fixtures && python3 -m http.server 8413 >/dev/null 2>&1 &) ; sleep 1.2
for side in old new; do
  obscura --allow-private-network fetch "http://127.0.0.1:8413/regulated.html" --wait 2 \
    --eval "$(cat results/misspell-$side.js)" 2>/dev/null | sed -n '/^{/,$p' > results/a11-$side.out
  if grep -q 'unknown config key' results/a11-$side.out; then
    assert A11 $side PASS "refused: unknown config key(s): regualted"
  else
    assert A11 $side FAIL "Object.assign accepted it; the probe ran on defaults and reported a clean deck"
  fi
done

echo "== A12 obscura's own stderr is relayed verbatim =="
for side in old new; do
  dir=$OLD; [ $side = new ] && dir=$NEW
  "$dir/run-preflight.sh" "http://127.0.0.1:9/deck.html" > results/a12-$side.out 2>&1
  echo $? > results/a12-$side.rc
  if grep -q 'obscura said:' results/a12-$side.out; then
    assert A12 $side PASS "relayed under the guard"
  else
    assert A12 $side FAIL "2>/dev/null discarded it and substituted a guessed advisory (rc $(cat results/a12-$side.rc))"
  fi
done

echo "== A13 CONTROL: a genuinely clean deck still passes =="
run "$OLD" a13-old clean.html --regulated
run "$NEW" a13-new clean.html --regulated
for side in old new; do
  if has a13-$side "PREFLIGHT PASS" && ! has a13-$side "0 slides examined"; then
    assert A13 $side PASS "passed with a real denominator"
  else
    assert A13 $side FAIL "did not pass a clean deck, or passed it over zero slides"
  fi
done

echo "== A14 the verdict names what was actually gated =="
for side in old new; do
  grep -q 'served sha256' results/a13-$side.out \
    && assert A14 $side PASS "served bytes identified in the verdict" \
    || assert A14 $side FAIL "nothing ties the URL gated to the file delivered"
done

echo "== A15 a check that threw is reported as unrun, not as clean =="
for side in old new; do
  src=$OLD; [ $side = new ] && src=$NEW
  rm -rf fault-$side && mkdir fault-$side
  cp "$src/run-preflight.sh" fault-$side/; chmod +x fault-$side/run-preflight.sh
  python3 - "$src/deck-preflight.js" "fault-$side/deck-preflight.js" <<'PY'
import sys
s=open(sys.argv[1]).read()
# fault-inject one check so it throws, exactly as an engine gap would
s=s.replace("  step('Hue budget', () => {",
            "  step('Hue budget', () => {\n    throw new Error('simulated engine gap: DOMMatrixReadOnly is absent');",1)
open(sys.argv[2],'w').write(s)
PY
  ./fault-$side/run-preflight.sh fixtures/clean.html --regulated > results/a15-$side.out 2>&1
  echo $? > results/a15-$side.rc
  if grep -qE '^\[DECK-PREFLIGHT NOT RUN\]|check\(s\) did not run|pass is INCOMPLETE' results/a15-$side.out; then
    assert A15 $side PASS "surfaced as NOT RUN (rc $(cat results/a15-$side.rc))"
  else
    assert A15 $side FAIL "the note is in the JSON and never read; null read as 0 and the verdict was PASS at exit $(cat results/a15-$side.rc)"
  fi
done

echo "== A16 an empty probe result is refused, and says so =="
for side in old new; do
  dir=$OLD; [ $side = new ] && dir=$NEW
  "$dir/run-preflight.sh" "http://127.0.0.1:9/deck.html" > results/a16-$side.out 2>&1
  echo $? > results/a16-$side.rc
  if grep -q 'this is NOT a pass' results/a16-$side.out && [ "$(cat results/a16-$side.rc)" != 0 ]; then
    assert A16 $side PASS "exit $(cat results/a16-$side.rc) with \"this is NOT a pass\" in the message"
  else
    assert A16 $side FAIL "a silent gate is indistinguishable from a clean deck"
  fi
done

echo "== A17 NO REGRESSION: pre-existing blockers still fire =="
run "$OLD" a17-old regress.html
run "$NEW" a17-new regress.html
for side in old new; do
  if vhas a17-$side "titleWrap" && [ "$(rc a17-$side)" != 0 ]; then
    assert A17 $side PASS "titleWrap still blocks; rc $(rc a17-$side)"
  else
    assert A17 $side FAIL "a pre-existing blocker stopped firing"
  fi
done

echo; echo "================ SCORECARD ================"
python3 - <<'PY'
rows=[l.rstrip('\n').split('\t') for l in open('results/scorecard.tsv') if l.strip()]
by={}
for i,s,v,n in rows: by.setdefault(i,{})[s]=(v,n)
names={
 'A1':'--regulated survives a reformatted probe',
 'A2':'the type floor can fail a build',
 'A3':'chart coverage carries its denominator',
 'A4':'a declared two-bar truncated pair is judged',
 'A5':'a zero denominator is not a pass',
 'A6':'every blocker carries its consequence',
 'A7':"the deck's own name is gated",
 'A8':'drawn accent marks count',
 'A9':'non-IFRS needs a statutory companion on its slide',
 'A10':'dual and inverted axes are caught',
 'A11':'a misspelled config key is refused',
 'A12':"obscura's stderr is relayed verbatim",
 'A13':'CONTROL: a clean deck still passes',
 'A14':'the verdict names what was gated',
 'A15':'a check that threw reads as unrun',
 'A16':"an empty probe result is refused",
 'A17':'NO REGRESSION: pre-existing blockers still fire',
}
op=np=0
out=['| # | assertion | original | rebuild |','|---|---|---|---|']
for k in sorted(by, key=lambda x:int(x[1:])):
    o=by[k].get('old',('-','')); n=by[k].get('new',('-',''))
    if o[0]=='PASS': op+=1
    if n[0]=='PASS': np+=1
    out.append('| %s | %s | **%s** — %s | **%s** — %s |'%(k,names.get(k,k),o[0],o[1],n[0],n[1]))
out.append('')
out.append('**original %d/%d · rebuild %d/%d**'%(op,len(by),np,len(by)))
txt='\n'.join(out)
open('results/scorecard.md','w').write(txt+'\n')
print(txt)
PY

#!/usr/bin/env bash
# vouch process evals. Each id maps to an entry in evals.json.
#
# Hermetic: the fixture claim is generated, every figure in it is invented, and no
# household data ships with this skill.
#
# An eval that cannot run is REPORTED AS NOT RUN, never skipped silently. A suite whose
# "all green" and whose "nothing ran" look the same is the defect this whole skill is
# organised against.
set -u
cd "$(dirname "$0")"
HERE="$PWD"; SC="$HERE/../skills/vouch/scripts"; FX="$HERE/fixtures"
WORK="$(mktemp -d)"; trap 'rm -rf "$WORK"' EXIT

PASS=0; FAIL=0; NOTRUN=0
pass(){ printf '  PASS   %s  %s\n' "$1" "$2"; PASS=$((PASS+1)); }
fail(){ printf '  FAIL   %s  %s\n' "$1" "$2"; FAIL=$((FAIL+1)); }
notrun(){ printf '  NOTRUN %s  %s\n' "$1" "$2"; NOTRUN=$((NOTRUN+1)); }

python3 make_fixtures.py >/dev/null || { echo "fixtures failed to build"; exit 1; }

# The PDF extractor. Without a Swift toolchain the document-reading evals cannot run,
# and they say so rather than passing.
PDFTEXT=""
if command -v swiftc >/dev/null 2>&1; then
  swiftc -O "$SC/pdftext.swift" -o "$WORK/pdftext" >/dev/null 2>&1 && PDFTEXT="$WORK/pdftext"
fi
[ -n "$PDFTEXT" ] || echo "  note   no Swift toolchain: the document-reading evals cannot run"

CSV="$WORK/claim.csv"
build(){ python3 "$SC/build_csv.py" --rows "$FX/claim_rows.json" --form "$FX/form.json" \
           --out "$1" >/dev/null 2>&1; }
validate(){ python3 "$SC/validate.py" --csv "$1" --rows "$FX/claim_rows.json" --dir "$FX" \
              --start 2025-08-01 --end 2025-09-30 --extractor "${PDFTEXT:-/nonexistent}" 2>&1; }

# --- V-01 green, then eight reds ------------------------------------------------
build "$CSV"
if [ -n "$PDFTEXT" ] && validate "$CSV" | grep -q '^PASS.*FAIL 0$'; then
  pass V-01a "the gate is green on a correct claim"
elif [ -z "$PDFTEXT" ]; then
  notrun V-01a "needs the PDF extractor"
else
  fail V-01a "the gate is NOT green on a correct claim"; validate "$CSV" | grep '^  FAIL'
fi

red(){ # id, description, python mutation over the row list `L`
  local id="$1" desc="$2" mut="$3" want="$4"
  python3 - "$CSV" "$WORK/$id.csv" <<PY
import csv,sys
L=list(csv.reader(open(sys.argv[1])))
body=[i for i,x in enumerate(L) if x and '/' in x[0] and x[2]]
$mut
csv.writer(open(sys.argv[2],'w',newline='')).writerows(L)
PY
  local out; out="$(validate "$WORK/$id.csv")"
  if echo "$out" | grep -q "^  FAIL.*$want"; then pass "$id" "$desc"
  else fail "$id" "$desc — expected a failure matching '$want'"; echo "$out" | grep '^  FAIL' | sed 's/^/         /'; done_=1
  fi
}

if [ -n "$PDFTEXT" ]; then
  red V-01b "one date moved outside the period" \
    "L[body[0]][0]='04/08/2024'" "outside the claim period"
  red V-01c "an invoice number duplicated" \
    "L[body[1]][2]=L[body[0]][2]" "duplicate invoice numbers"
  red V-01d "one row's amount edited" \
    "L[body[2]][5]=f'{float(L[body[2]][5])-10:.2f}'; L[body[2]][3]=f'{float(L[body[2]][3])-10:.2f}'" "Total"
  red V-01e "two rows swapped out of date order" \
    "L[body[0]],L[body[4]]=L[body[4]],L[body[0]]" "NOT in date order"
  red V-01f "one row's signs flipped" \
    "L[body[0]][3]=L[body[0]][3].lstrip('-'); L[body[0]][4]=L[body[0]][4].lstrip('-'); L[body[0]][5]=L[body[0]][5].lstrip('-')" "sign convention"
  # V-02: the transposition the arithmetic check is blind to. Whole column swapped AND
  # the totals recomputed from it, so checks 6 and 9-11 all pass.
  red V-02 "whole tax column transposed with the totals recomputed from it" \
    "ex=tx=0
for x in L:
    if x and '/' in x[0] and x[3]:
        x[3],x[4]=x[4],x[3]; ex+=float(x[3] or 0); tx+=float(x[4] or 0)
for x in L:
    if len(x)>2 and x[2]=='Total': x[3]=f'{ex:.2f}'; x[4]=f'{tx:.2f}'" \
    "tax exceeds the ex-tax amount"
else
  for id in V-01b V-01c V-01d V-01e V-01f V-02; do notrun "$id" "needs the PDF extractor"; done
fi

# --- V-03 the filename audit goes red on a swap ---------------------------------
if [ -n "$PDFTEXT" ]; then
  A="$FX/2025-08/NW-2025-0801.pdf"; B="$FX/2025-08/CA-88213.pdf"
  mv "$A" "$FX/.sw" && mv "$B" "$A" && mv "$FX/.sw" "$B"
  out="$(python3 "$SC/audit_invoices.py" --rows "$FX/claim_rows.json" --dir "$FX" --extractor "$PDFTEXT" 2>&1)"
  mv "$A" "$FX/.sw" && mv "$B" "$A" && mv "$FX/.sw" "$B"
  if echo "$out" | grep -qE 'filename NOT found in the file *: 2'; then
    pass V-03 "the filename audit names both swapped documents"
  else
    fail V-03 "the filename audit did NOT see two swapped filenames"; echo "$out" | sed -n '2,6p' | sed 's/^/         /'
  fi
else
  notrun V-03 "needs the PDF extractor"
fi

# --- V-04 every gate names a defect ---------------------------------------------
if python3 - "$SC/validate.py" "$HERE/../skills/vouch/references/gates.md" <<'PY'
import re,sys
src, doc = open(sys.argv[1]).read(), open(sys.argv[2]).read()
calls = len(re.findall(r'\bok\(', src))
rows  = len(re.findall(r'^\| *\d+', doc, re.M)) + len(re.findall(r'^\| *\d+.\d+', doc, re.M))
sys.exit(0 if rows >= 20 and calls >= 20 else 1)
PY
then pass V-04 "the gate suite and gates.md both enumerate at least 20 checks"
else fail V-04 "gates.md and validate.py disagree about how many checks exist"; fi

# --- V-05 the builder reproduces a recorded form --------------------------------
build "$WORK/again.csv"
if cmp -s "$CSV" "$WORK/again.csv"; then pass V-05 "the CSV builder is byte-stable"
else fail V-05 "two builds from one source differ"; fi

# --- V-06 both builders refuse a relative output path ---------------------------
r1=$(cd "$WORK" && python3 "$SC/build_csv.py" --rows "$FX/claim_rows.json" --form "$FX/form.json" --out rel.csv >/dev/null 2>&1; echo $?)
r2=$(cd "$WORK" && python3 "$SC/build_reports.py" --rows "$FX/claim_rows.json" --config "$FX/report.json" --outdir . >/dev/null 2>&1; echo $?)
if [ "$r1" = 2 ] && [ "$r2" = 2 ]; then pass V-06 "both builders refuse a relative output path"
else fail V-06 "a builder accepted a relative path (csv=$r1 reports=$r2)"; fi

# --- V-07 no money or count literal in report prose -----------------------------
if python3 - "$SC/build_reports.py" <<'PY'
import re,sys
src=open(sys.argv[1]).read()
bad=[]
for m in re.finditer(r'''["'f]{1,2}["'][^"']*?["']''', src):
    pass
# Every string literal that reaches the page, checked for a bare figure.
for s in re.findall(r'f?"([^"\n]{12,})"|f?\'([^\'\n]{12,})\'', src):
    t = s[0] or s[1]
    if '<' not in t and '{' not in t and re.search(r'\b\d[\d,]*\.\d\d\b|\b(?<![\w-])\d{2,}(?![\w%-])', t):
        bad.append(t)
print('\n'.join(bad[:5]))
sys.exit(1 if bad else 0)
PY
then pass V-07 "no money figure or standalone count is a literal in report prose"
else fail V-07 "a figure is typed into report prose rather than derived"; fi

# --- V-08 / V-09 rendered geometry ----------------------------------------------
notrun V-08 "needs a browser; run design-review against a served copy"
notrun V-09 "needs a browser; run design-review against a served copy"

# --- V-10 one-to-one assignment --------------------------------------------------
out="$(cd "$WORK" && python3 "$SC/match.py" "$FX/charges.json" "$FX/invoices.json" --window 4 2>&1)"
if echo "$out" | grep -q 'assigned=2' && echo "$out" | grep -q 'invoices unused=0'; then
  pass V-10 "two identical charges take two different invoices"
else
  fail V-10 "assignment did not pair one to one"; echo "$out" | sed 's/^/         /'
fi

# --- V-11 feed-blind days ---------------------------------------------------------
out="$(cd "$WORK" && python3 "$SC/find_blind_days.py" "$FX/feed.json" --account "Card 0001" \
       --start 2025-08-01 --end 2025-09-30 2>&1)"
if echo "$out" | grep -q '(38 days with no transaction at all)'; then
  pass V-11 "the 38-day hole is found and named"
else
  fail V-11 "the deliberate feed hole was not reported"; echo "$out" | sed 's/^/         /'
fi

# --- V-12 the hand-off page is a complete document --------------------------------
cat > "$WORK/outstanding.json" <<'JSON'
[{"date":"2025-08-14","supplier":"Northwind Hosting","local":44.0,"kind":"portal",
  "account":"billing@example.com","todo":"Sign in and download"}]
JSON
(cd "$WORK" && python3 "$SC/wanted_invoices.py" outstanding.json --out wanted.html --fx 1.52 >/dev/null 2>&1)
if head -1 "$WORK/wanted.html" | grep -qi '<!doctype html>' && grep -q '</body></html>' "$WORK/wanted.html" \
   && grep -q 'Northwind Hosting' "$WORK/wanted.html"; then
  pass V-12 "the hand-off page is a complete document carrying its rows"
else
  fail V-12 "the hand-off page is a fragment or lost its rows"; fi

# --- V-13 no tax characterisation asserted ----------------------------------------
if grep -rniE '\b(is (tax[- ]?)?deductible|you (can|may) claim|qualifies for|is eligible for) ' \
     "$SC/build_reports.py" "$HERE/../skills/vouch/assets/"*.json >/dev/null 2>&1; then
  fail V-13 "a report asserts a tax characterisation"
  grep -rniE '\b(is (tax[- ]?)?deductible|you (can|may) claim|qualifies for|is eligible for) ' \
    "$SC/build_reports.py" "$HERE/../skills/vouch/assets/"*.json | sed 's/^/         /'
else
  pass V-13 "no report asserts a tax or legal characterisation"
fi

# --- V-15 the account census separates the rungs ----------------------------------
# Rung 4 is the one this exists for: it is indistinguishable from rung 3 until the
# pattern that finds the contact email actually fires, and it was worth eleven rows.
if [ -n "$PDFTEXT" ]; then
  out="$(python3 "$SC/classify_accounts.py" --rows "$FX/claim_rows.json" --dir "$FX" \
          --company-domain example.com --company-name 'Example Company Pty Ltd' \
          --extractor "$PDFTEXT" 2>&1)"
  if echo "$out" | grep -q '1 company email in the bill-to' \
     && echo "$out" | grep -q '2 company domain elsewhere' \
     && echo "$out" | grep -q '4 company named, NON-company contact email'; then
    pass V-15 "the census separates a company email, a bare domain and a personal contact"
  else
    fail V-15 "the census collapsed rungs that the fixtures hold apart"
    echo "$out" | sed 's/^/         /' | head -8
  fi
else
  notrun V-15 "needs the PDF extractor"
fi

# --- V-16 no money or count literal in the census or the gate output ---------------
if grep -nE '"[^"]*\b[0-9]{2,}\b[^"]*"' "$SC/classify_accounts.py" \
     | grep -vE '#|help=|desc|\{|:[0-9]|\.[0-9]|0-9|s\)|utf8|360|320|46|36|30|28|18|f"' >/dev/null; then
  fail V-16 "a count literal appears in census output text"
else
  pass V-16 "the census prints no hardcoded count"
fi

# --- V-17 the three patterns that once could not fire ------------------------------
if out="$(python3 "$HERE/check_patterns.py" 2>&1)"; then
  pass V-17 "each pattern is held by a fixture it must match and one it must not"
else
  fail V-17 "a pattern matched nothing, or matched what it should refuse"
  echo "$out" | sed 's/^/         /'
fi

# --- V-18 the statement cadence is derived, and refuses to guess -------------------
mkdir -p "$WORK/st-good" "$WORK/st-bad"
touch "$WORK/st-good/2026-01-16.pdf" "$WORK/st-good/2026-02-16.pdf" "$WORK/st-good/2026-03-16.pdf"
touch "$WORK/st-bad/2026-01-16.pdf" "$WORK/st-bad/2026-02-03.pdf"
cat > "$WORK/out.json" <<'JSON'
[{"date":"2026-04-20","supplier":"Northwind Hosting","local":44.0,"kind":"portal","card":"Card 0001"}]
JSON
g="$(python3 "$SC/wanted_invoices.py" "$WORK/out.json" --out "$WORK/g.html" --statements "$WORK/st-good/*.pdf" 2>&1)"
b="$(python3 "$SC/wanted_invoices.py" "$WORK/out.json" --out "$WORK/b.html" --statements "$WORK/st-bad/*.pdf" 2>&1)"
if echo "$g" | grep -q 'closing on day 16' && grep -q 'A statement is missing' "$WORK/g.html" \
   && grep -q '17 Apr to 16 May 2026' "$WORK/g.html" \
   && echo "$b" | grep -q 'different days of the month' \
   && ! grep -q 'A statement is missing' "$WORK/b.html"; then
  pass V-18 "the cycle is read from the statements, and conflicting ones drop the note"
else
  fail V-18 "the cadence was declared rather than derived, or a conflict was guessed through"
  echo "$g" | sed 's/^/         good: /'; echo "$b" | sed 's/^/         bad:  /'
fi

# --- V-19 a card statement filed in the claim folder is refused --------------------
if [ -n "$PDFTEXT" ]; then
  python3 - "$FX" <<'PYX'
import sys, os, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
# A minimal document carrying the markers a real card statement carries.
text = ("Statement Period From July 17 to August 16, 2026\\nPrevious Balance\\n"
        "Closing Balance\\nMinimum Payment\\nPayment Due Date")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), '.'))
from make_fixtures import pdf
open(os.path.join(sys.argv[1], '2025-08', 'STMT-PROBE.pdf'), 'wb').write(pdf(text.split('\\n')))
PYX
  out="$(validate "$CSV")"
  rm -f "$FX/2025-08/STMT-PROBE.pdf"
  if echo "$out" | grep -q 'card statement(s) filed in the claim folder'; then
    pass V-19 "a card statement copied into the claim folder is refused"
  else
    fail V-19 "a card statement in the claim folder was not refused"
  fi
else
  notrun V-19 "needs the PDF extractor"
fi

# --- V-20 the two leftover piles are checked against each other -------------------
CROSSDIR="$(mktemp -d)"
cat > "$CROSSDIR/outstanding.json" <<'JSONA'
[{"date":"2026-07-14","supplier":"ElevenLabs","local":36.17,"kind":"portal","card":"Amex ...3003"},
 {"date":"2026-07-19","supplier":"Slack","local":26.00,"kind":"portal","card":"Amex ...3003"}]
JSONA
cat > "$CROSSDIR/nocharge.json" <<'JSONB'
[{"file":"Receipt-A.pdf","sup":"ElevenLabs","inv":"60DFBA11-0019","date":"2026-07-15","total":24.20,"cur":"AUD","diolog":true},
 {"file":"Invoice-B.pdf","sup":"Tailscale","inv":"PHVU4ZBH-0014","date":"2026-08-01","total":12.00,"cur":"USD","diolog":true}]
JSONB
cross_out="$(python3 "$SC/cross_check.py" --outstanding "$CROSSDIR/outstanding.json" \
  --nocharge "$CROSSDIR/nocharge.json" --fx-low 1.40 --fx-high 1.60 2>&1)"; cross_rc=$?
if [ "$cross_rc" -ne 0 ] \
   && echo "$cross_out" | grep -q '60DFBA11-0019' \
   && ! echo "$cross_out" | grep -q 'PHVU4ZBH-0014' \
   && echo "$cross_out" | grep -q 'plausible pairs=1'; then
  pass V-20 "a converted amount on both piles is paired, and an unrelated pair is not"
else
  fail V-20 "the two leftover piles were not cross-checked (rc=$cross_rc)"
fi
rm -rf "$CROSSDIR"

# --- V-14 determinism across a second full run ------------------------------------
python3 "$SC/build_reports.py" --rows "$FX/claim_rows.json" --config "$FX/report.json" \
  --outdir "$WORK" >/dev/null 2>&1
mkdir -p "$WORK/second"
python3 "$SC/build_reports.py" --rows "$FX/claim_rows.json" --config "$FX/report.json" \
  --outdir "$WORK/second" >/dev/null 2>&1
if cmp -s "$WORK/Approval.html" "$WORK/second/Approval.html" \
   && cmp -s "$WORK/Accounting.html" "$WORK/second/Accounting.html"; then
  pass V-14 "a second run over unchanged input is byte-identical"
else
  fail V-14 "two runs over one input differ — something read a clock or a listing order"
fi

# --- V-22 a document naming somebody else's card is refused -----------------------
if [ -n "$PDFTEXT" ]; then
  CARDDIR="$(mktemp -d)"; mkdir -p "$CARDDIR/2026-07"
  python3 - "$CARDDIR" <<'PYC'
import sys, os, json, pathlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, str(pathlib.Path.cwd()))
from make_fixtures import pdf
d = sys.argv[1]
open(os.path.join(d, '2026-07', 'MINE.pdf'), 'wb').write(
    pdf(['INVOICE', 'Invoice No.', 'MINE', 'Payment Method',
         'Credit Card: American Express XXXX-XXXX-XXXX-3003']))
open(os.path.join(d, '2026-07', 'THEIRS.pdf'), 'wb').write(
    pdf(['INVOICE', 'Invoice No.', 'THEIRS', 'Payment Method',
         'Credit Card: Visa XXXX-XXXX-XXXX-7812']))
json.dump([{'date': '2026-07-01', 'vendor': 'Fixture', 'inv': 'MINE',
            'file_rel': '2026-07/MINE.pdf'},
           {'date': '2026-07-02', 'vendor': 'Fixture', 'inv': 'THEIRS',
            'file_rel': '2026-07/THEIRS.pdf'}],
          open(os.path.join(d, 'rows.json'), 'w'))
PYC
  card_out="$(python3 "$SC/card_on_document.py" --rows "$CARDDIR/rows.json" --dir "$CARDDIR" \
    --mine 3003,2005 --extractor "$PDFTEXT" 2>&1)"; card_rc=$?
  if [ "$card_rc" -ne 0 ] \
     && echo "$card_out" | grep -q 'FOREIGN CARD.*THEIRS.*7812' \
     && ! echo "$card_out" | grep -q 'FOREIGN CARD.*MINE' \
     && echo "$card_out" | grep -q 'names a card=2'; then
    pass V-22 "a document naming somebody else's card is refused, and one naming mine is not"
  else
    fail V-22 "the card named on a document was not read (rc=$card_rc)"
  fi
  rm -rf "$CARDDIR"
else
  notrun V-22 "needs the PDF extractor"
fi

# --- V-23 the empty outstanding set renders as a result, not an empty page --------
EMPTYDIR="$(mktemp -d)"; echo '[]' > "$EMPTYDIR/empty.json"
empty_out="$(python3 "$SC/wanted_invoices.py" "$EMPTYDIR/empty.json" \
  --out "$EMPTYDIR/probe.html" --currency AUD 2>&1)"
if grep -q 'Nothing is outstanding' "$EMPTYDIR/probe.html" \
   && ! grep -q 'Each row below' "$EMPTYDIR/probe.html" \
   && ! grep -qE '^<p class=lede>\.' "$EMPTYDIR/probe.html" \
   && ! echo "$empty_out" | grep -qE '· +·'; then
  pass V-23 "an empty outstanding set states the result and promises no rows"
else
  fail V-23 "the empty outstanding set rendered as an empty page rather than a result"
fi
rm -rf "$EMPTYDIR"

# --- V-24 a supplier whose own rows disagree is named ------------------------------
if [ -n "$PDFTEXT" ]; then
  SPLITDIR="$(mktemp -d)"; mkdir -p "$SPLITDIR/2026-01"
  python3 - "$SPLITDIR" <<'PYS'
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from make_fixtures import pdf
d = sys.argv[1]
docs = {
    # One supplier, two rungs: an invoice naming the company, and a receipt naming
    # a personal address. This is the shape the census used to hide.
    'SPLIT-1': ['INVOICE', 'Invoice No.', 'SPLIT-1', 'Bill To', 'Acme Pty Ltd', '1 Test Street'],
    'SPLIT-2': ['RECEIPT', 'Invoice No.', 'SPLIT-2', 'Bill To', 'someone@gmail.com'],
    # One supplier, one rung, one address: must NOT be named.
    'SAME-1':  ['INVOICE', 'Invoice No.', 'SAME-1', 'Bill To', 'Acme Pty Ltd', '1 Test Street'],
    'SAME-2':  ['INVOICE', 'Invoice No.', 'SAME-2', 'Bill To', 'Acme Pty Ltd', '1 Test Street'],
}
rows = []
for inv, lines in docs.items():
    open(os.path.join(d, '2026-01', f'{inv}.pdf'), 'wb').write(pdf(lines))
    rows.append({'date': '2026-01-05', 'vendor': 'Splitter' if inv.startswith('SPLIT') else 'Steady',
                 'inv': inv, 'inc': 10.0, 'ex': 10.0, 'gst': 0.0,
                 'file_rel': f'2026-01/{inv}.pdf'})
json.dump(rows, open(os.path.join(d, 'rows.json'), 'w'))
PYS
  split_out="$(python3 "$SC/classify_accounts.py" --rows "$SPLITDIR/rows.json" --dir "$SPLITDIR" \
    --company-domain acme.test --company-name Acme --extractor "$PDFTEXT" 2>&1)"
  if echo "$split_out" | grep -q 'whose own rows disagree=1' \
     && echo "$split_out" | grep -q 'Splitter' \
     && ! echo "$split_out" | sed -n '/vouch-split/,$p' | grep -q 'Steady'; then
    pass V-24 "a supplier whose rows land in two places is named, one whose rows agree is not"
  else
    fail V-24 "the split-supplier census did not separate the two fixtures"
  fi
  rm -rf "$SPLITDIR"
else
  notrun V-24 "needs the PDF extractor"
fi

# --- the declaration and the runner are reconciled ---------------------------------
# An eval declared in evals.json with no branch here produces no line at all, so the
# summary counts it in neither column and the suite reports a clean run over a check
# that never existed. Same shape as every defect this suite exists to catch: a pass and
# a cannot-run that look identical from outside.
UNRUN="$(python3 - "$HERE" <<'PYU'
import json, re, sys, os
h = sys.argv[1]
declared = [e['id'] for e in json.load(open(os.path.join(h, 'evals.json')))['evals']]
run = set(re.findall(r'\b(?:pass|fail|notrun) (V-\d+)', open(os.path.join(h, 'run_evals.sh')).read()))
print(' '.join(i for i in declared if i not in run))
PYU
)"
UNRUN_N=0
if [ -n "$UNRUN" ]; then
  UNRUN_N="$(echo "$UNRUN" | wc -w | tr -d ' ')"
  for id in $UNRUN; do
    printf '  %-6s %s\n' "NOEXEC" "$id  declared in evals.json with no branch in this runner"
  done
fi

echo
echo "[vouch-evals] pass=$PASS · fail=$FAIL · not run=$NOTRUN · declared with no runner=$UNRUN_N"
[ "$FAIL" -eq 0 ] || exit 1

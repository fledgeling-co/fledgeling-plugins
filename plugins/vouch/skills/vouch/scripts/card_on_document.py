#!/usr/bin/env python3
"""Where a document names the card that paid it, that beats every other kind of evidence.

Most invoices are silent about the card, which is why the pipeline matches on supplier,
date and amount instead. A minority state it outright, and on those rows there is nothing
left to infer: the document says whose money it was.

It earns its place because it goes red. One supplier stated `American Express ...3003` for
ten consecutive months and then `Visa ...7812` -- the company's own card -- from the
eleventh. Nothing else in the run could see that: same supplier, same amount, same
subscription ids, same monthly cadence, and the charge simply stopped appearing on any
personal card. Read as a feed gap, it would have been claimed. Read on the document, it is
the company paying its own bill.

The mask formats are the whole difficulty, so they are listed rather than generalised. A
pattern that misses a form reports a smaller denominator and looks identical to a clean
run: this file's own first version missed `3*** ****** *3003` and under-counted by one.
Every form here was measured on a real document; add to the list rather than loosening a
pattern, and keep the census printing so a silent narrowing is visible.

Usage:
    python3 card_on_document.py --rows claim_rows.json --dir out/ \
        --mine 3003,2005,7328,4055 [--extractor /tmp/pdftext]
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys

BANNER = re.compile(r'^=== .* ===$', re.M)

# (pattern, the form it catches). Each was seen on a real invoice or receipt.
FORMS = [
    (r'Charged to\s+[A-Za-z ]{4,20}\s*\(\s*[\dX\*x•·\s]{4,}?(\d{4})\s*\)', 'charged-to + interleaved mask'),
    (r'(?:Payment Method|Payment method)[^\n]{0,60}?[X\*x•·\-\s]{4,}(\d{4})\b', 'payment-method + mask'),
    (r'(?:Visa|Mastercard|American Express|Amex)\s*[X\*x•·\-\s]{4,}(\d{4})\b', 'brand + mask'),
    (r'(?:Visa|Mastercard|American Express|Amex)\s*[-–]\s*(\d{4})\b', 'brand + bare dash'),
    (r'Payment method\s*\n?\s*[-–]\s*(\d{4})\b', 'stripe bare "- NNNN"'),
    (r'(?:ending in|ending)\s*(\d{4})\b', '"ending in NNNN"'),
]


def card_in(text: str):
    for pat, form in FORMS:
        m = re.search(pat, text, re.I)
        if m:
            return m.group(1), form
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--mine', required=True,
                    help='comma-separated last-4s of every card the claimant pays personally')
    ap.add_argument('--extractor', default='/tmp/pdftext')
    a = ap.parse_args()

    mine = {x.strip() for x in a.mine.split(',') if x.strip()}
    rows = json.load(open(a.rows))
    stated, silent, foreign, forms = [], 0, [], {}
    for r in rows:
        path = os.path.join(a.dir, r['file_rel'])
        if not os.path.exists(path):
            silent += 1
            continue
        if path.lower().endswith('.pdf'):
            text = BANNER.sub('', subprocess.run([a.extractor, path],
                                                 capture_output=True, text=True).stdout)
        else:
            text = open(path, encoding='utf8', errors='replace').read()
        last4, form = card_in(text)
        if not last4:
            silent += 1
            continue
        stated.append((r, last4, form))
        forms[form] = forms.get(form, 0) + 1
        if last4 not in mine:
            foreign.append((r, last4))

    print(f"[card-on-document] rows={len(rows)} · names a card={len(stated)} · "
          f"silent={silent} · not a card of the claimant's={len(foreign)}")
    for form, n in sorted(forms.items(), key=lambda x: -x[1]):
        print(f"    {n:3d}  {form}")

    # A supplier whose documents SPLIT is the signal that a mask form is being missed.
    # One vendor's paperwork comes off one template, so "some name a card and some do not"
    # is either a real change in their billing or a gap in the list above -- and the two
    # look identical in the totals. Measured twice on one run: adding `Mastercard - 7328`
    # (brand, bare dash, no mask) took the census from 11 documents to 26. Both misses
    # reported a smaller denominator and a clean result.
    named_by, silent_by = {}, {}
    for r, _l, _f in stated:
        named_by[r.get('vendor', '?')] = named_by.get(r.get('vendor', '?'), 0) + 1
    for r in rows:
        v = r.get('vendor', '?')
        if v not in silent_by:
            silent_by[v] = 0
    for v in list(silent_by):
        silent_by[v] = sum(1 for r in rows if r.get('vendor', '?') == v) - named_by.get(v, 0)
    split = sorted((v, named_by[v], silent_by[v]) for v in named_by if silent_by.get(v, 0) > 0)
    if split:
        print(f"    split suppliers (some documents name a card, some do not): {len(split)}")
        for v, n, si in split:
            print(f"      {v}: {n} name one, {si} do not — a real change in their billing, "
                  "or a mask form this list does not read")
    for r, last4 in foreign:
        print(f"  FOREIGN CARD  {r['date']}  {r.get('vendor','')}  {r['inv']}  ...{last4}")
    if foreign:
        print(f"\n{len(foreign)} row(s) carry a document naming a card the claimant does not pay. "
              "The document outranks the feed match: these are somebody else's expense.")
    return 1 if foreign else 0


if __name__ == '__main__':
    raise SystemExit(main())

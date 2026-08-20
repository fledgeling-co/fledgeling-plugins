#!/usr/bin/env python3
"""The bill-to census: where every claimed row sits on the evidence ladder.

This is the instrument the operator sets the bar with. It does not decide anything.

The account test reads as one question — "is this the company's account?" — and it is
really six answers of different strength. On a real run the claim was reviewed four
times and each pass moved the bar, because each pass saw a different one of these for
the first time. Printing all six at once, per supplier, with counts and values, turns
four rounds into one.

  1 company email address in the bill-to        strongest
  2 company domain elsewhere on the page        (a hosting invoice names the domain)
  3 company named as addressee, no email        (the supplier prints no contact)
  4 company named AND a non-company email       (a company account, personal contact)
  5 a non-company email only                    weak
  6 neither a name nor an address               weakest; a blank or personal bill-to

Rule 4 is the one nobody predicts. It looks like rule 3 until the pattern that finds
the email actually fires, and it was worth 11 rows on a real claim.

Usage:
    python3 classify_accounts.py --rows claim_rows.json --dir out/ \
        --company-domain example.com --company-name "Example Pty Ltd" \
        [--company-name "Example"] [--extractor /tmp/pdftext] [--json census.json]
"""
from __future__ import annotations
import argparse, collections, json, os, re, subprocess, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from patterns import BANNER, EMAIL, BILLTO   # noqa: E402  one definition, proved once

LADDER = [
    ('1 company email in the bill-to',            'strongest'),
    ('2 company domain elsewhere on the page',    'strong'),
    ('3 company named, no email either way',      'moderate'),
    ('4 company named, NON-company contact email', 'weak'),
    ('5 a non-company email only',                'weaker'),
    ('6 neither a company name nor an address',   'weakest'),
]


def read(path: str, extractor: str) -> str:
    if path.lower().endswith('.pdf'):
        t = subprocess.run([extractor, path], capture_output=True, text=True).stdout
        return BANNER.sub('', t)
    return open(path, encoding='utf8', errors='replace').read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--company-domain', required=True,
                    help='e.g. example.com; matched as @example.com and as a bare domain')
    ap.add_argument('--company-name', action='append', default=[],
                    help='repeatable; the legal name and any trading name')
    ap.add_argument('--vendor-domain', action='append', default=[],
                    help='repeatable; a supplier domain to ignore, e.g. stripe.com')
    ap.add_argument('--extractor', default='/tmp/pdftext')
    ap.add_argument('--json', help='write the census as JSON as well')
    a = ap.parse_args()

    rows = json.load(open(a.rows))
    dom = a.company_domain.lower().lstrip('@')
    names = [n for n in a.company_name if n.strip()] or [dom.split('.')[0]]
    namere = re.compile('|'.join(re.escape(n) for n in names), re.I)
    vend = re.compile('|'.join(re.escape(v) for v in a.vendor_domain), re.I) if a.vendor_domain else None

    census = collections.defaultdict(list)
    for r in rows:
        path = os.path.join(a.dir, r['file_rel'])
        if not os.path.exists(path):
            census['file missing'].append((r, '', ''))
            continue
        text = read(path, a.extractor)
        m = BILLTO.search(text)
        blk = ' '.join((m.group(1) if m else text[:360]).split())
        found = [e.lower().rstrip('.,') for e in EMAIL.findall(blk)]
        if vend:
            found = [e for e in found if not vend.search(e)]
        company = [e for e in found if e.endswith('@' + dom)]
        other = [e for e in found if not e.endswith('@' + dom)]
        named = bool(namere.search(blk))
        page_dom = dom in text.lower()

        if company:            k = LADDER[0][0]
        elif page_dom:         k = LADDER[1][0]
        elif named and other:  k = LADDER[3][0]
        elif named:            k = LADDER[2][0]
        elif other:            k = LADDER[4][0]
        else:                  k = LADDER[5][0]
        census[k].append((r, ', '.join(company or other) or '(no email line)',
                          blk.split(' Ship to')[0][:46]))

    total = sum(x[0]['inc'] for v in census.values() for x in v)
    print(f"[vouch-accounts] rows={len(rows)} · total={total:,.2f} · "
          f"steps occupied={len([k for k in census if census[k]])}/6")
    print()
    for k, strength in LADDER:
        v = census.get(k, [])
        if not v:
            continue
        print(f"{len(v):4d} rows  {sum(x[0]['inc'] for x in v):>10,.2f}   {k}  ({strength})")
        # Grouped by supplier and address, not by the addressee string: a supplier
        # that prints the amount inside the bill-to block yields a different string
        # per invoice and would list every row separately.
        agg = collections.defaultdict(lambda: [0, 0.0, ''])
        for r, em, who in v:
            g = agg[(r.get('vendor', '?'), em)]
            g[0] += 1; g[1] += r['inc']
            if not g[2]:
                g[2] = who
        for (ven, em), (n, val, who) in sorted(agg.items(), key=lambda kv: -kv[1][1]):
            print(f"        {n:3d}  {val:>9,.2f}  {ven[:18]:18} {em[:30]:30} {who[:36]}")
        print()

    if census.get('file missing'):
        print(f"    {len(census['file missing'])} rows have no document on disk")

    # ── suppliers whose own rows disagree ─────────────────────────────────────
    #
    # The census above is grouped by RUNG, so a supplier whose rows land on two
    # different rungs appears in two separate blocks and nothing says they are the
    # same supplier. That is the reading a person does not do: they see a supplier
    # under "a company address appears" and take the whole supplier as settled.
    #
    # It is the same defect a merchant-level decision has in a ledger — one value
    # written across rows that are not all the same thing — and it is ordinary
    # rather than rare. Measured on a real claim: one supplier's rows split between
    # invoices naming the company and receipts naming a personal address, and
    # another sold a metered developer API and a consumer subscription under one
    # payee. A supplier is a folder, not an answer.
    #
    # A DESCRIPTION, NOT A QUEUE: it has no target, nothing clears it, and a
    # supplier legitimately split stays listed forever.
    by_supplier = collections.defaultdict(lambda: {'rungs': collections.Counter(),
                                                   'addrs': set(), 'rows': 0, 'val': 0.0})
    for k, _strength in LADDER:
        for r, em, _who in census.get(k, []):
            g = by_supplier[r.get('vendor', '?')]
            g['rungs'][k] += 1
            g['addrs'].add(em)
            g['rows'] += 1
            g['val'] += r['inc']
    split = {v: g for v, g in by_supplier.items()
             if len(g['rungs']) > 1 or len(g['addrs']) > 1}
    print(f"\n[vouch-split] suppliers examined={len(by_supplier)} · "
          f"whose own rows disagree={len(split)}")
    for ven, g in sorted(split.items(), key=lambda kv: -kv[1]['val']):
        print(f"    {ven[:22]:22} {g['rows']:3d} rows  {g['val']:>9,.2f}")
        for k, n in g['rungs'].most_common():
            print(f"         {n:3d} on rung  {k}")
        if len(g['addrs']) > 1:
            for em in sorted(g['addrs']):
                print(f"         addressed to  {em or '(no address on the document)'}")
    if split:
        print("    A supplier's rows landing in more than one place is normal — two accounts,"
              "\n    two products, or a billing contact that changed. It is worth a look because"
              "\n    a decision taken at the supplier level would be right for some of these"
              "\n    rows and wrong for the rest.")

    # Two denominators the operator should see whatever bar they set.
    strict = sum(len(census.get(LADDER[i][0], [])) for i in (0, 1))
    print(f"[vouch-accounts] a company address appears on {strict} of {len(rows)} documents; "
          f"the remaining {len(rows) - strict} rest on a company NAME or on nothing")
    print("This is a census, not a verdict. The bar is the operator's to set, and it is "
          "the same bar for every supplier or it is not a bar.")

    if a.json:
        json.dump({k: [x[0]['inv'] for x in v] for k, v in census.items()},
                  open(a.json, 'w'), indent=1)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

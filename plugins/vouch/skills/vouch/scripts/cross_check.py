#!/usr/bin/env python3
"""Check the two leftover piles against each other before either is published.

A run ends with two populations that are described as opposites: charges with no
document, and documents with no charge. They are only opposites if nothing belongs to
both, and on a real run three rows did. ElevenLabs prints its receipts as `$24.20` with
an Australian GST line beside them; the extractor read the currency as AUD, the amount
therefore never matched the A$36.17 that actually left the card, and the same
transaction was reported twice -- once as a missing invoice and once as a missing
charge. Both pages looked right. Both were wrong, in opposite directions, which is why
neither reading caught it.

The pairing test is deliberately loose, because it produces a QUESTION rather than a
row: same supplier, within a few days, and a ratio inside the observed conversion band.
A hit is never written into the claim automatically -- it is printed for a human to open
the document and read, since the whole point is that one of the two figures was
misparsed and only the document says which.

Usage:
    python3 cross_check.py --outstanding outstanding.json --nocharge nocharge.json \
        [--fx-low 1.40 --fx-high 1.60] [--days 8]
"""
from __future__ import annotations
import argparse, datetime as dt, json, re, sys


def norm(s: str) -> str:
    return re.sub(r'[^a-z0-9]', '', (s or '').lower())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--outstanding', required=True, help='charges with no invoice')
    ap.add_argument('--nocharge', required=True, help='documents with no charge')
    ap.add_argument('--fx-low', type=float, default=1.0)
    ap.add_argument('--fx-high', type=float, default=1.0)
    ap.add_argument('--days', type=int, default=8)
    a = ap.parse_args()

    charges = json.load(open(a.outstanding))
    docs = json.load(open(a.nocharge))
    hits = []
    for c in charges:
        amt = c.get('local')
        if amt is None or not c.get('date'):
            continue
        cd = dt.date.fromisoformat(c['date'][:10])
        for d in docs:
            if not d.get('date') or d.get('total') is None:
                continue
            if norm(d.get('sup', '')) != norm(c.get('supplier', '')):
                continue
            if abs((dt.date.fromisoformat(d['date'][:10]) - cd).days) > a.days:
                continue
            tot = float(d['total'])
            if not tot:
                continue
            ratio = amt / tot
            # Either the two figures are the same money, or one is the other converted.
            if abs(ratio - 1) < 0.005 or a.fx_low <= ratio <= a.fx_high:
                hits.append((c, d, ratio))

    print(f"[vouch-cross] charges-without-a-document={len(charges)} · "
          f"documents-without-a-charge={len(docs)} · plausible pairs={len(hits)}")
    for c, d, ratio in hits:
        how = "same amount" if abs(ratio - 1) < 0.005 else f"ratio {ratio:.4f}, inside the band"
        print(f"  {c['date']}  {c.get('supplier')}  {c['local']:,.2f} charged")
        print(f"     <-> {d['date']}  {d.get('inv')}  {d.get('cur')} {float(d['total']):,.2f}  ({how})")
        print(f"     open {d.get('file')} and read its currency; if they are one transaction, "
              "the row belongs in the claim rather than on either page")
    if hits:
        print(f"\n{len(hits)} transaction(s) may be double-counted as two different absences. "
              "A charge and its document reported as separate gaps is one row missing from the "
              "claim, not two problems.")
    return 1 if hits else 0


if __name__ == '__main__':
    raise SystemExit(main())

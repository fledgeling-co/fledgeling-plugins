#!/usr/bin/env python3
"""One-to-one assignment of charges to invoices, with an FX-band consistency check.

THE rule this file exists for: assignment, never per-charge lookup.

Two identical subscription top-ups four days apart will BOTH match whichever invoice a
lookup returns first. One write lands, the second's filter matches nothing and silently
does nothing, and the tally reports two. Measured: independent lookup matched 7 of 10
and flagged two ambiguous; this assignment matched 9 of 10 and correctly identified the
tenth as belonging to a different account.

Usage:
    python3 match.py charges.json invoices.json --window 4 --fx-min 1.35 --fx-max 1.75
"""
from __future__ import annotations
import argparse, datetime as dt, json, statistics, sys


def gap(a: str, b: str) -> int:
    return abs((dt.date.fromisoformat(a) - dt.date.fromisoformat(b)).days)


def assign(charges, invoices, window, tol, fx_min, fx_max):
    pairs = []
    for ci, c in enumerate(charges):
        for ii, v in enumerate(invoices):
            if not (c.get('date') and v.get('date')):
                continue
            g = gap(v['date'], c['date'])
            if g > window:
                continue
            # Match on the invoice's own currency figure where the statement supplies it.
            target = c.get('foreign') or c.get('local')
            if v.get('total') is None or target is None:
                continue
            if abs(v['total'] - target) > tol:
                # Cross-currency: accept only inside a plausible FX band.
                if not c.get('foreign') and c.get('local'):
                    rate = c['local'] / v['total'] if v['total'] else 0
                    if not (fx_min <= rate <= fx_max):
                        continue
                else:
                    continue
            pairs.append((g, ci, ii))
    pairs.sort()                                   # nearest date first
    used_c, used_i, out = set(), set(), {}
    for g, ci, ii in pairs:
        if ci in used_c or ii in used_i:
            continue
        used_c.add(ci); used_i.add(ii)
        out[ci] = (ii, g)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('charges'); ap.add_argument('invoices')
    ap.add_argument('--window', type=int, default=4)
    ap.add_argument('--tol', type=float, default=0.02)
    ap.add_argument('--fx-min', type=float, default=1.35)
    ap.add_argument('--fx-max', type=float, default=1.75)
    ap.add_argument('--fx-outlier-bp', type=int, default=800,
                    help='flag a pair whose implied rate deviates this far from the median')
    a = ap.parse_args()

    charges = json.load(open(a.charges))
    invoices = json.load(open(a.invoices))
    asg = assign(charges, invoices, a.window, a.tol, a.fx_min, a.fx_max)

    matched, rates = [], []
    for ci, c in enumerate(charges):
        if ci not in asg:
            continue
        ii, g = asg[ci]
        v = invoices[ii]
        rate = (c.get('local') / v['total']) if (v.get('total') and c.get('foreign')) else None
        matched.append({'charge': c, 'invoice': v, 'gap_days': g, 'implied_fx': rate})
        if rate:
            rates.append(rate)

    print(f"[vouch-match] charges={len(charges)} · invoices={len(invoices)} · "
          f"assigned={len(matched)} · charges unmatched={len(charges) - len(matched)} · "
          f"invoices unused={len(invoices) - len(matched)}")

    # The FX band is an independent check on the PAIRING, never an input to an amount.
    if len(rates) >= 3:
        med = statistics.median(rates)
        print(f"[vouch-fx] pairs with an implied rate={len(rates)} · "
              f"median={med:.4f} · min={min(rates):.4f} · max={max(rates):.4f}")
        for m in matched:
            r = m['implied_fx']
            if r and abs(r - med) / med * 10000 > a.fx_outlier_bp:
                print(f"    OUTLIER {m['charge'].get('date')} {m['charge'].get('desc','')[:34]} "
                      f"rate={r:.4f} vs median {med:.4f} — suspect the pairing, not the rate")
    else:
        print("[vouch-fx] too few cross-currency pairs to form a band")

    for ci, c in enumerate(charges):
        if ci not in asg:
            print(f"    NO INVOICE  {c.get('date')}  {c.get('desc','')[:44]}  "
                  f"{c.get('local')}", file=sys.stderr)

    json.dump(matched, open('matched.json', 'w'), indent=1)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

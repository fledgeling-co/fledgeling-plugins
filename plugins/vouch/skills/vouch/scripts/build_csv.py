#!/usr/bin/env python3
"""Emit the claim form as CSV, in the employer's own layout.

The layout is DATA, not code. An employer's form carries a preamble (claimant, period),
a header row, the rows, and a footer (totals, banking, signature) — and every one of
those varies. They live in a form spec so a new employer is a new JSON file rather than
a new script, and so the shape the run validates against is the shape it wrote.

Two rules this file exists to hold:

  Every figure is DERIVED at the moment of writing. A total typed into the spec is a
  total that rots: on a real run five hardcoded counts survived a move from 66 rows to
  68, and then "sixty-eight" survived the move to 88.

  The output path is ABSOLUTE. A builder that writes a relative path writes wherever the
  harness happened to leave the working directory, and on a real run two rebuilds landed
  in /tmp while the delivered folder kept stale copies, silently.

Usage:
    python3 build_csv.py --rows claim_rows.json --form form.json \
        --out "/abs/path/Expense Claim Form - Name (period).csv" \
        [--classify rd_classification.json]

form.json:
{
  "claimant": "A. Person",
  "period": "8/2025 - 6/2026",
  "preamble": [["Expense Claim Form"], ["Applicant Name: ", "{claimant}"], [],
               ["Expense Period :", "{period}"], []],
  "columns": ["Date", "Description", "Invoice No.",
              "Amount    (excl. GST)", "GST", "Amount      (incl. GST)"],
  "classify_columns": ["R&D", "R&D reason"],
  "date_format": "%d/%m/%Y",
  "negative": true,
  "zero_literal": "0",
  "total_label_col": 2,
  "footer": [[], [], [], "", "Bank Account"],
  "footer_blocks": [
    ["", "", "", "", "Bank Account"],
    ["", "", "", "", "Account Name:", "{claimant}"],
    ["", "", "", "", "BSB: ", "000 000"],
    ["", "", "", "", "Account No: ", "000 000"],
    [],
    ["", "", "", "", "Applicant Signature"],
    ["", "", "", "", "Date:"]
  ]
}

The column HEADINGS are copied verbatim from the employer's own form, whitespace and
all. A prior-year form on a real run had its ex-tax and tax values transposed relative
to its own headers; the fix is to write in header order and say so, never to reproduce
the error for consistency.
"""
from __future__ import annotations
import argparse, csv, json, os, sys


def dmy(iso: str, fmt: str) -> str:
    import datetime as dt
    return dt.date.fromisoformat(iso[:10]).strftime(fmt)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--form', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--classify', help='JSON map: supplier -> {verdict, reason}')
    a = ap.parse_args()

    if not os.path.isabs(a.out):
        print("--out must be an absolute path: a relative one writes wherever the "
              "harness left the working directory, and the stale copy stays delivered.",
              file=sys.stderr)
        return 2

    rows = json.load(open(a.rows))
    form = json.load(open(a.form))
    cls = json.load(open(a.classify)) if a.classify else {}

    fmt = form.get('date_format', '%d/%m/%Y')
    neg = form.get('negative', True)
    zero = form.get('zero_literal', '0')
    cols = list(form['columns'])
    ccols = list(form.get('classify_columns', [])) if cls else []
    width = len(cols) + len(ccols)

    def money(v: float) -> str:
        if not v:
            return zero
        return f"-{v:.2f}" if neg else f"{v:.2f}"

    def pad(r):
        r = list(r) + [''] * (width - len(r))
        return [str(c).replace('{claimant}', form.get('claimant', ''))
                      .replace('{period}', form.get('period', '')) for c in r[:width]]

    def classify(r):
        if not ccols:
            return []
        e = cls.get(r.get('vendor', ''))
        if not e:
            return [''] * len(ccols)
        verdict = e.get('verdict')
        if verdict is None:
            verdict = 'TRUE' if e.get('rd') else 'FALSE'
        return ([verdict, e.get('reason', '')] + [''] * len(ccols))[:len(ccols)]

    body = [[dmy(r['date'], fmt), r['desc'], r['inv'],
             money(r['ex']), money(r['gst']), money(r['inc'])] + classify(r)
            for r in sorted(rows, key=lambda x: (x['date'], x.get('vendor', '')))]

    ex = sum(r['ex'] for r in rows)
    tax = sum(r['gst'] for r in rows)
    inc = sum(r['inc'] for r in rows)

    tcol = form.get('total_label_col', 2)
    total = [''] * width
    total[tcol] = 'Total'
    total[3], total[4], total[5] = money(ex), money(tax), money(inc)

    out = [pad(r) for r in form.get('preamble', [])]
    out.append(pad(cols + ccols))
    out += [pad(r) for r in body]
    out.append(total)

    # A classification subtotal is derived here or not written at all.
    if ccols:
        sel = [r for r in rows
               if (cls.get(r.get('vendor', ''), {}).get('verdict', '')
                   or ('TRUE' if cls.get(r.get('vendor', ''), {}).get('rd') else '')) == 'TRUE']
        sub = [''] * width
        sub[1] = f"{len(sel)} of {len(rows)} charges"
        sub[tcol] = f"{ccols[0]}-eligible total"
        # Each figure sits under its OWN header. A subtotal written into a neighbouring
        # money column is the transposition of check 21 committed by the writer instead
        # of by the operator, and it lands on the column an assessor reads first: on a
        # real run the tax-inclusive R&D subtotal sat under the ex-tax heading, where a
        # notional deduction has to be tax-exclusive.
        sub[3] = money(sum(r['ex'] for r in sel))
        sub[4] = money(sum(r['gst'] for r in sel))
        sub[5] = money(sum(r['inc'] for r in sel))
        out.append(pad([]))
        out.append(sub)

    for blk in form.get('footer_blocks', []):
        out.append(pad(blk))

    with open(a.out, 'w', newline='') as f:
        w = csv.writer(f)
        for r in out:
            w.writerow(r)

    print(f"[vouch-csv] rows={len(body)} · columns={width} · "
          f"excl={ex:,.2f} · tax={tax:,.2f} · incl={inc:,.2f}")
    print(f"wrote {a.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

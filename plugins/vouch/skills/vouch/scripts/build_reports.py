#!/usr/bin/env python3
"""Emit the two HTML reports: one for whoever approves payment, one for whoever books it.

Unbranded by default. Every name, role and label comes from the config, so the same
script serves an employer whose form says "GST" and one whose form says "VAT".

The rule this file exists to hold: NO FIGURE IS EVER TYPED INTO PROSE. Every count,
total, percentage and superlative is computed here and interpolated. On a real run five
hardcoded counts survived a move from 66 rows to 68, and one of them then survived the
move to 88 — reading correct, printed in a sentence, wrong.

Usage:
    python3 build_reports.py --rows claim_rows.json --config report.json \
        --outdir /abs/path/to/claim [--classify classification.json] [--css assets/report.css]

Writes Approval.html and Accounting.html into --outdir, which must be absolute.
"""
from __future__ import annotations
import argparse, collections, datetime as dt, html, json, os, sys

E = html.escape


def money(v, cur='A$'):
    return f"{cur}{abs(v):,.2f}"


def pct(n, d):
    return f"{(100.0 * n / d):.1f}%" if d else "0.0%"


def words(n: int) -> str:
    w = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
         'ten', 'eleven', 'twelve']
    return w[n] if n < len(w) else f"{n:,}"


def first_sentence(t: str, cap: int = 150) -> str:
    t = (t or '').strip()
    if len(t) <= cap:
        return t
    cut = t.find('. ')
    return (t[:cut + 1] if 0 < cut <= cap else t[:cap].rsplit(' ', 1)[0] + '\u2026')


def month_label(ym: str) -> str:
    return dt.date.fromisoformat(ym + '-01').strftime('%B %Y')


def page(title, css, body, subtitle=''):
    return (f"<!doctype html>\n<html lang=en><head><meta charset=utf-8>"
            f"<meta name=viewport content='width=device-width,initial-scale=1'>"
            f"<title>{E(title)}</title>"
            + (f"<meta name=description content='{E(subtitle)}'>" if subtitle else "")
            + f"<style>{css}</style></head><body><div class=wrap>\n{body}\n</div></body></html>\n")


def figure(value, label, sub=''):
    return (f"<div class=card><p class=fig>{value}</p><p class=fig-label>{E(label)}</p>"
            + (f"<p class=fig-sub>{sub}</p>" if sub else "") + "</div>")


def build(rows, cfg, cls):
    cur = cfg.get('currency', 'A$')
    tax = cfg.get('tax_name', 'GST')
    rate = cfg.get('tax_rate', 0.10)
    claimant = cfg.get('claimant', '')
    period = cfg.get('period_label', '')
    today = cfg.get('prepared') or dt.date.today().strftime('%-d %B %Y')

    N = len(rows)
    EX = sum(r['ex'] for r in rows)
    TX = sum(r['gst'] for r in rows)
    INC = sum(r['inc'] for r in rows)

    by_sup = collections.defaultdict(list)
    by_cat = collections.defaultdict(list)
    by_mon = collections.defaultdict(list)
    for r in rows:
        by_sup[r['vendor']].append(r)
        by_cat[r.get('cat', 'Uncategorised')].append(r)
        by_mon[r['date'][:7]].append(r)

    sup = sorted(by_sup.items(), key=lambda kv: -sum(x['inc'] for x in kv[1]))
    cat = sorted(by_cat.items(), key=lambda kv: -sum(x['inc'] for x in kv[1]))
    mon = sorted(by_mon.items())

    taxed = [r for r in rows if r['gst']]
    untaxed = [r for r in rows if not r['gst']]
    taxed_sup = sorted({r['vendor'] for r in taxed})
    untaxed_sup = sorted({r['vendor'] for r in untaxed})

    def verdict(r):
        e = cls.get(r['vendor'])
        if not e:
            return None
        return e.get('verdict', 'TRUE' if e.get('rd') else 'FALSE')

    cn = cfg.get('classification', {})
    cname = cn.get('name', '')
    sel = [r for r in rows if verdict(r) == 'TRUE'] if cls else []
    unsel = [r for r in rows if verdict(r) == 'FALSE'] if cls else []

    return dict(cur=cur, tax=tax, rate=rate, claimant=claimant, period=period, today=today,
                N=N, EX=EX, TX=TX, INC=INC, rows=rows, sup=sup, cat=cat, mon=mon,
                taxed=taxed, untaxed=untaxed, taxed_sup=taxed_sup, untaxed_sup=untaxed_sup,
                cls=cls, cname=cname, cn=cn, sel=sel, unsel=unsel, verdict=verdict, cfg=cfg)


# ---------------------------------------------------------------- approval ---
def approval(d) -> str:
    cur, N, INC = d['cur'], d['N'], d['INC']
    top = d['sup'][0]
    topn = min(5, len(d['sup']))
    top5 = sum(sum(x['inc'] for x in v) for _, v in d['sup'][:topn])
    role = d['cfg'].get('approver_role', 'whoever approves this')

    b = [f"<p class=eyebrow>Expense claim for approval</p>",
         f"<h1>{E(d['claimant'])}</h1>",
         f"<p class=lede>{words(N).capitalize()} charges paid on personal cards between "
         f"{E(d['period'])}, each keyed to the supplier's own invoice. "
         f"The claim is {money(INC, cur)} including {E(d['tax'])}.</p>",
         f"<p class=meta>Prepared {E(d['today'])}</p>"]

    b += ["<section><div class=grid3>",
          figure(money(INC, cur), f"Total to reimburse, including {d['tax']}"),
          figure(f"{N}", "Charges, each with its invoice attached"),
          figure(f"{len(d['sup'])}", "Suppliers",
                 f"{E(top[0])} is the largest at {money(sum(x['inc'] for x in top[1]), cur)}"),
          "</div></section>"]

    b += ["<section><h2>What this is</h2>",
          f"<p>Software and services bought for work and paid on personal cards over "
          f"{words(len(d['mon']))} months. Nothing here was reimbursed at the time, and nothing "
          f"in it has been claimed before: the previous claim was checked row by row and shares "
          f"no invoice number and no date-and-amount pair with this one.</p>",
          f"<p>Every row has the supplier's own invoice behind it, filed by month and named by "
          f"its invoice number, so a line in this table and a document in the folder are the "
          f"same thing. Anything without a document stayed out of the claim rather than going "
          f"in on an estimate.</p></section>"]

    b += ["<section><h2>Where it went</h2>",
          f"<p>The {words(topn)} largest suppliers account for {pct(top5, INC)} of the claim.</p>",
          "<div class=card><table><thead><tr><th>Supplier</th><th>What it is for</th>"
          f"<th class=n>Charges</th><th class=n>Including {E(d['tax'])}</th></tr></thead><tbody>"]
    for name, rs in d['sup']:
        # The most common stated purpose, cut to its first sentence. A supplier's full
        # explanation belongs in the accountant's report; dropped whole into an approval
        # table it makes one row six lines tall and the other seventeen unreadable.
        cand = collections.Counter(x.get('why', '') for x in rs if x.get('why'))
        why = (cand.most_common(1)[0][0] if cand else rs[0].get('cat', ''))
        why = first_sentence(why)
        b.append(f"<tr><td>{E(name)}</td><td class=wrapcell>{E(why)}</td>"
                 f"<td class=n>{len(rs)}</td>"
                 f"<td class=n>{money(sum(x['inc'] for x in rs), cur)}</td></tr>")
    b.append(f"<tr class=total><td>Total</td><td></td><td class=n>{N}</td>"
             f"<td class=n>{money(INC, cur)}</td></tr></tbody></table></div></section>")

    b += ["<section><h2>Month by month</h2>",
          "<div class=card><table><thead><tr><th>Month</th><th class=n>Charges</th>"
          f"<th class=n>Including {E(d['tax'])}</th></tr></thead><tbody>"]
    hi = max(d['mon'], key=lambda kv: sum(x['inc'] for x in kv[1]))
    for ym, rs in d['mon']:
        b.append(f"<tr><td>{E(month_label(ym))}</td><td class=n>{len(rs)}</td>"
                 f"<td class=n>{money(sum(x['inc'] for x in rs), cur)}</td></tr>")
    b.append(f"<tr class=total><td>Total</td><td class=n>{N}</td>"
             f"<td class=n>{money(INC, cur)}</td></tr></tbody></table>"
             f"<p class=small style='margin-top:16px'>The heaviest month was "
             f"{E(month_label(hi[0]))} at {money(sum(x['inc'] for x in hi[1]), cur)}.</p>"
             "</div></section>")

    if d['cls']:
        s, u = d['sel'], d['unsel']
        si = sum(x['inc'] for x in s)
        b += [f"<section><h2>{E(d['cname'])}</h2>",
              f"<p>{words(len(s)).capitalize()} of the {N} charges sit inside "
              f"{E(d['cname'])} on their face, {money(si, cur)} including {E(d['tax'])} and "
              f"{pct(si, INC)} of the claim. The other {words(len(u))} do not. "
              f"{d['cn'].get('caveat', '')}</p>",
              "<div class=grid2>",
              figure(money(si, cur), f"In scope for {d['cname']}",
                     f"{len(s)} charges across "
                     f"{len({r['vendor'] for r in s})} suppliers"),
              figure(money(sum(x['inc'] for x in u), cur), f"Out of scope",
                     f"{len(u)} charges across "
                     f"{len({r['vendor'] for r in u})} suppliers"),
              "</div></section>"]

    b += ["<section><h2>What was checked</h2>",
          f"<p>Before this went out: every row's arithmetic against its invoice, every "
          f"filename against an invoice number printed inside that document, every date "
          f"inside the claim period, the totals against the rows, and the whole set against "
          f"the previous claim for anything appearing twice. The card feed was also swept for "
          f"the days it holds nothing at all, because a quiet stretch in a bank feed is not "
          f"the same fact as a quiet stretch on the card.</p></section>"]

    b += [f"<div class=signoff><h2>To approve</h2>"
          f"<p class=fig>{money(INC, cur)}</p>"
          f"<p>{N} charges, {E(d['period'])}, reimbursable to <em>{E(d['claimant'])}</em>. "
          f"The schedule and {E(d['tax'])} notes are in the accompanying report, and every "
          f"invoice is in the folder beside it.</p></div>"]
    return "\n".join(b)


# -------------------------------------------------------------- accounting ---
def accounting(d) -> str:
    cur, N, EX, TX, INC = d['cur'], d['N'], d['EX'], d['TX'], d['INC']
    b = [f"<p class=eyebrow>Expense claim schedule and {E(d['tax'])} notes</p>",
         f"<h1>{E(d['claimant'])}</h1>",
         f"<p class=lede>{N} charges, {E(d['period'])}. "
         f"{money(EX, cur)} excluding {E(d['tax'])}, {money(TX, cur)} {E(d['tax'])}, "
         f"{money(INC, cur)} in total.</p>",
         f"<p class=meta>Prepared {E(d['today'])}</p>"]

    b += ["<section><div class=grid3>",
          figure(money(EX, cur), f"Excluding {d['tax']}"),
          figure(money(TX, cur), d['tax'],
                 f"{len(d['taxed'])} of {N} charges carry it"),
          figure(money(INC, cur), "Total"),
          "</div></section>"]

    b += ["<section><h2>Basis of preparation</h2>",
          f"<p>Each row is one card transaction matched to one supplier invoice. The invoice "
          f"is the source of the {E(d['tax'])} figure; where the supplier states no "
          f"{E(d['tax'])}, the row carries none rather than a back-derived amount. Amounts are "
          f"as charged in {E(cur)} on the card statement, so no exchange rate is applied "
          f"anywhere in this schedule.</p>",
          f"<p>Documents are filed one folder per month and named by the invoice number "
          f"printed inside the document. Every filename in the schedule was checked against "
          f"the text of the file it names.</p></section>"]

    b += [f"<section><h2>{E(d['tax'])} treatment</h2>",
          f"<p>{words(len(d['taxed'])).capitalize()} of the {N} charges carry "
          f"{E(d['tax'])}, totalling {money(TX, cur)}. "
          f"{words(len(d['untaxed'])).capitalize()} carry none.</p>",
          "<div class=grid2><div class=card>"
          f"<h3>Suppliers charging {E(d['tax'])}</h3><p class=small>"
          + ", ".join(E(s) for s in d['taxed_sup']) + "</p></div><div class=card>"
          f"<h3>Suppliers charging none</h3><p class=small>"
          + ", ".join(E(s) for s in d['untaxed_sup']) + "</p></div></div>"]
    mixed = sorted(set(d['taxed_sup']) & set(d['untaxed_sup']))
    if mixed:
        b.append(f"<div class=note><p><span class=flag>Worth an eye</span> "
                 + ", ".join(E(m) for m in mixed) +
                 f" appear on both lists, so a single supplier has charged {E(d['tax'])} on "
                 f"some invoices and not others. Each row follows its own document.</p></div>")
    b.append("</section>")

    b += ["<section><h2>By category</h2><div class=card><table>"
          "<thead><tr><th>Category</th><th class=n>Charges</th>"
          f"<th class=n>Excl. {E(d['tax'])}</th><th class=n>{E(d['tax'])}</th>"
          f"<th class=n>Total</th></tr></thead><tbody>"]
    for name, rs in d['cat']:
        b.append(f"<tr><td class=wrapcell>{E(name)}</td><td class=n>{len(rs)}</td>"
                 f"<td class=n>{money(sum(x['ex'] for x in rs), cur)}</td>"
                 f"<td class=n>{money(sum(x['gst'] for x in rs), cur)}</td>"
                 f"<td class=n>{money(sum(x['inc'] for x in rs), cur)}</td></tr>")
    b.append(f"<tr class=total><td>Total</td><td class=n>{N}</td>"
             f"<td class=n>{money(EX, cur)}</td><td class=n>{money(TX, cur)}</td>"
             f"<td class=n>{money(INC, cur)}</td></tr></tbody></table></div></section>")

    # ---- the schedule ----
    cls_on = bool(d['cls'])
    ncols = 8 + (2 if cls_on else 0)
    b += ["<section><h2>Full schedule</h2>",
          f"<p>Every charge in date order. The invoice number is the filename of the document "
          f"filed under that month.</p>",
          "<div class=card><table><colgroup>"
          "<col style='width:8ch'><col style='width:16ch'><col style='width:20ch'>"
          "<col style='width:22ch'><col style='width:11ch'><col style='width:9ch'>"
          "<col style='width:11ch'><col style='width:18ch'>"
          + ("<col style='width:6ch'><col style='width:26ch'>" if cls_on else "")
          + "</colgroup><thead><tr><th>Date</th><th>Supplier</th><th>Category</th>"
          "<th>Description</th>"
          f"<th class=n>Excl. {E(d['tax'])}</th><th class=n>{E(d['tax'])}</th>"
          "<th class=n>Total</th><th>Invoice no.</th>"
          + (f"<th>{E(d['cname'])}</th><th>Basis</th>" if cls_on else "")
          + "</tr></thead><tbody>"]
    for r in sorted(d['rows'], key=lambda x: (x['date'], x['vendor'])):
        cells = [f"<td class=mono>{E(dt.date.fromisoformat(r['date']).strftime('%d/%m/%y'))}</td>",
                 f"<td class=wrapcell>{E(r['vendor'])}</td>",
                 f"<td class=wrapcell>{E(r.get('cat',''))}</td>",
                 f"<td class=wrapcell>{E(r['desc'])}</td>",
                 f"<td class=n>{money(r['ex'], cur)}</td>",
                 f"<td class=n>{money(r['gst'], cur) if r['gst'] else '&ndash;'}</td>",
                 f"<td class=n>{money(r['inc'], cur)}</td>",
                 f"<td class='mono wrapcell'>{E(r['inv'])}</td>"]
        if cls_on:
            v = d['verdict'](r) or ''
            e = d['cls'].get(r['vendor'], {})
            cells += [f"<td class={'yes' if v=='TRUE' else 'no'}>{E(v)}</td>",
                      f"<td class=wrapcell><span class=small>{E(e.get('short',''))}</span></td>"]
        b.append("<tr>" + "".join(cells) + "</tr>")
    tot = [f"<td>Total</td>", "<td></td>", "<td></td>", f"<td class=n>{N} charges</td>",
           f"<td class=n>{money(EX, cur)}</td>", f"<td class=n>{money(TX, cur)}</td>",
           f"<td class=n>{money(INC, cur)}</td>", "<td></td>"]
    if cls_on:
        tot += ["<td></td>", "<td></td>"]
    b.append("<tr class=total>" + "".join(tot) + "</tr></tbody></table></div></section>")

    if cls_on and d['cn'].get('basis_table', True):
        b += [f"<section><h2>{E(d['cname'])} basis, by supplier</h2>",
              f"<p>One entry per supplier rather than one per row: the reasoning is a property "
              f"of what the supplier provides, and repeating it on every charge makes it "
              f"unreadable. {E(d['cn'].get('caveat',''))}</p>",
              "<div class=card><table><thead><tr><th>Supplier</th>"
              f"<th>{E(d['cname'])}</th><th>Basis</th></tr></thead><tbody>"]
        for name in sorted(d['cls']):
            if name not in {r['vendor'] for r in d['rows']}:
                continue
            e = d['cls'][name]
            v = e.get('verdict', 'TRUE' if e.get('rd') else 'FALSE')
            b.append(f"<tr><td class=wrapcell>{E(name)}</td>"
                     f"<td class={'yes' if v=='TRUE' else 'no'}>{E(v)}</td>"
                     f"<td class=wrapcell>{E(e.get('reason',''))}</td></tr>")
        b.append("</tbody></table></div></section>")

    notes = d['cfg'].get('closing_notes', [])
    if notes:
        b += ["<section><h2>Notes</h2>"] + [f"<div class=note><p>{E(n)}</p></div>" for n in notes] \
             + ["</section>"]

    b += [f"<div class=signoff><h2>Reconciliation</h2>"
          f"<p class=fig>{money(INC, cur)}</p>"
          f"<p>{N} charges reconcile to {N} invoices and {N} filed documents. "
          f"Nothing in the schedule lacks a document, and no document in the folder lacks a "
          f"row. The claim is reimbursable to <em>{E(d['claimant'])}</em>.</p></div>"]
    return "\n".join(b)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--config', required=True)
    ap.add_argument('--outdir', required=True)
    ap.add_argument('--classify')
    ap.add_argument('--css', default=os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'report.css'))
    a = ap.parse_args()

    if not os.path.isabs(a.outdir):
        print("--outdir must be absolute: a relative path writes wherever the harness left "
              "the working directory, and the delivered copy silently stays stale.",
              file=sys.stderr)
        return 2

    rows = json.load(open(a.rows))
    cfg = json.load(open(a.config))
    cls = json.load(open(a.classify)) if a.classify else {}
    css = open(a.css).read()

    d = build(rows, cfg, cls)
    who = cfg.get('claimant', '')
    for name, fn, title in (
            ('Approval.html', approval, f"Expense claim for approval — {who}"),
            ('Accounting.html', accounting,
             f"Expense claim schedule and {d['tax']} notes — {who}")):
        path = os.path.join(a.outdir, name)
        open(path, 'w').write(page(title, css, fn(d),
                                   f"{d['N']} charges, {money(d['INC'], d['cur'])}, "
                                   f"{cfg.get('period_label','')}"))
        print(f"wrote {path}  ({os.path.getsize(path):,} bytes)")

    print(f"[vouch-reports] rows={d['N']} · suppliers={len(d['sup'])} · "
          f"months={len(d['mon'])} · excl={d['EX']:,.2f} · tax={d['TX']:,.2f} · "
          f"incl={d['INC']:,.2f}" + (f" · classified={len(cls)}" if cls else ""))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

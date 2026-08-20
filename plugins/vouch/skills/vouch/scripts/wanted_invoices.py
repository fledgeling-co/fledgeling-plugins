#!/usr/bin/env python3
"""The wanted-invoices hand-off page.

When a portal blocks automation, or Mail never downloaded an attachment, stop and emit
this rather than retrying. On a real run the page came back with nineteen invoices
attached within minutes: a named hand-off beats an hour of automation.

Per outstanding charge: date, supplier, amount as charged, estimated original amount
(back-derived from the implied FX band and MARKED AS AN ESTIMATE), the account address
the invoice is expected to name, a deep link to the portal's billing history, and what
the operator needs to do.

Usage:
    python3 wanted_invoices.py outstanding.json --out wanted.html \
        --portals portals.json --fx 1.52 --currency AUD
"""
from __future__ import annotations
import argparse, datetime as dt, glob, html, json, os, re, subprocess, sys

CSS = """
:root{--ink:#12151c;--ink2:#4a5163;--muted:#6b7385;--line:rgba(18,21,28,.10);
 --bg:#fff;--soft:#f5f6f9;--accent:#1f3fa6;--warn-bg:#fbf1de;--warn:#8a5a1b}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
 --ink:#e9ecf3;--ink2:#b3bacb;--muted:#8b93a7;--line:rgba(255,255,255,.12);
 --bg:#12151c;--soft:#1a1e27;--accent:#8fa6f0;--warn-bg:#2b2416;--warn:#e0b872}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
 font:400 16px/1.6 -apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;
 font-variant-numeric:tabular-nums}
.wrap{max-width:1100px;margin:0 auto;padding:48px 24px 96px}
h1{font-size:clamp(26px,4vw,38px);line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}
.lede{color:var(--ink2);max-width:64ch;margin:0 0 8px}
.meta{color:var(--muted);font-size:14px;margin:0 0 32px}
.group{margin:40px 0 0}
.group h2{font-size:19px;margin:0 0 6px}
.group p{color:var(--ink2);font-size:14.5px;margin:0 0 16px;max-width:70ch}
.card{border:1px solid var(--line);border-radius:12px;overflow-x:auto;background:var(--bg)}
table{width:100%;border-collapse:collapse;font-size:14px;min-width:860px}
th{text-align:left;font-size:11.5px;letter-spacing:.06em;text-transform:uppercase;
 color:var(--muted);font-weight:600;padding:14px 16px;border-bottom:1px solid var(--line)}
td{padding:14px 16px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
td.n{text-align:right;white-space:nowrap}
.d{white-space:nowrap;color:var(--ink2)}
.sup{font-weight:600}
.est{color:var(--muted);font-size:13px}
.small{font-size:12.5px;color:var(--ink2);white-space:nowrap}
.acct{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:12.5px;color:var(--ink2)}
a{color:var(--accent)}
.todo{background:var(--warn-bg);color:var(--warn);border-radius:6px;padding:4px 8px;
 font-size:12px;display:inline-block;white-space:nowrap}
.note{background:var(--soft);border-radius:12px;padding:20px 24px;margin:32px 0 0;
 color:var(--ink2);font-size:14.5px;max-width:76ch}
.total{color:var(--muted);font-size:14px;margin-top:10px}
"""

KIND_TEXT = {
    'portal': ('Sign in and download',
               'The supplier portal refused automation, so these need your own browser. '
               'Each link goes to the billing-history page rather than the vendor home page.'),
    'mail': ('Open the message in Mail',
             'The invoice is attached to an email, but Mail never downloaded the attachment bytes. '
             'Opening each message makes Mail fetch it, and it then lands where the run can read it.'),
    'unknown': ('Source unknown',
                'No invoice was found in the mail index, on disk, or at a known portal for these. '
                'They stay out of the claim until a document exists.'),
    'account': ('The invoice names the wrong contact',
                'The charge and the invoice both exist, and the invoice names the company as the billed party '
                'while carrying a personal contact address. That is a third reason a row stays out, and the '
                'repair is to change the billing contact on the account and ask the supplier to re-issue.'),
    'statement': ('The invoice exists; the charge does not',
                  'These run the other way. The supplier issued an invoice and no matching charge has '
                  'reached the bank feed, so there is nothing to claim against it yet. That is a gap in '
                  'the feed rather than a missing document, and a card statement closes it.'),
}


def lede(rows) -> str:
    """Two populations, counted apart. A charge with no invoice and an invoice with no
    charge are opposite problems, and summing them into one number makes the sentence
    state something untrue about both."""
    nc = sum(1 for r in rows if r.get('kind') not in ('statement', 'account'))
    na = sum(1 for r in rows if r.get('kind') == 'account')
    ni = sum(1 for r in rows if r.get('kind') == 'statement')
    bits = []
    if nc:
        bits.append(f"{nc} charge{'s' if nc != 1 else ''} ha{'ve' if nc != 1 else 's'} "
                    "no invoice yet, so they are not in the claim")
    if na:
        bits.append(f"{na} more have an invoice that names the wrong contact")
    if ni:
        bits.append(f"{ni} invoice{'s' if ni != 1 else ''} ha{'ve' if ni != 1 else 's'} "
                    "no matching charge in the bank feed")
    if not bits:
        # An empty set is a RESULT, not an empty page. Rendered naively the lede opened on a
        # full stop and promised "each row below" over a table with no rows -- a finished
        # artefact stating something untrue, which is the defect class this whole skill is
        # about. Say plainly that nothing is outstanding, and keep the page: the reports link
        # to it, and a page asserting the zero is better evidence than a dangling link.
        return ("<p class=lede>Nothing is outstanding. Every charge in the period that belongs "
                "on the claim has its supplier document, and every document on hand has its "
                "matching charge.</p>")
    return ("<p class=lede>" + ", and ".join(bits).capitalize()
            + ". Each row below says what is needed and where to get it.</p>")


def statement_cadence(paths: list[str], extractor: str | None = None):
    """Work the statement cycle out FROM the statements, rather than being told it.

    The operator has statements; their closing day is a fact those files already
    carry, so asking for it as a flag invites a typo that silently sends every row
    to the wrong document. Two sources, in order: an ISO date in the filename, then
    a closing date inside the text. Where the observed days DISAGREE the cadence is
    reported as unknown and the column is dropped, because a cycle guessed from
    conflicting evidence is worse than no cycle at all.

    A cycle is a fact about ONE card, so the endings the statements name are read at the
    same time and returned beside it. Applying a cycle read off an Amex to a Mastercard
    invents a period no document supports, and the note that results reads exactly like a
    measured one -- caught on a real run, where a day-16 Amex cadence was printed against
    a Mastercard whose statements were never supplied.

    Returns (closing_day | None, held ISO dates, card endings seen, a sentence).
    """
    import collections
    seen = {}
    endings = set()
    for path in paths:
        stem = os.path.basename(path)
        txt = ''
        if extractor and path.lower().endswith('.pdf'):
            txt = subprocess.run([extractor, path], capture_output=True, text=True).stdout
            for m in re.finditer(r'[X\*x]{2,}[-\s]?[X\*x]{2,}[-\s]?(\d{4,6})', txt):
                endings.add(m.group(1)[-4:])
        m = re.match(r'(\d{4})-(\d{2})-(\d{2})', stem)
        if m:
            seen[path] = '-'.join(m.groups())
            continue
        if txt:
            m = re.search(r'(?:closing|statement)\s+date[^\n]*?(\d{1,2})\s+([A-Za-z]{3,9})\s+(\d{4})',
                          txt, re.I)
            if m:
                try:
                    seen[path] = dt.datetime.strptime(
                        f"{m.group(1)} {m.group(2)[:3]} {m.group(3)}", "%d %b %Y").date().isoformat()
                except ValueError:
                    pass
    if len(seen) < 2:
        return None, set(), endings, (
            f"{len(seen)} statement date(s) read from {len(paths)} file(s) — "
            "at least two are needed to infer a cycle")
    days = collections.Counter(int(d[8:10]) for d in seen.values())
    if len(days) != 1:
        return None, set(seen.values()), endings, (
            f"{len(seen)} statements close on {len(days)} different days of the month "
            f"({', '.join(str(d) for d in sorted(days))}) — no single cycle to infer")
    day = next(iter(days))
    return day, set(seen.values()), endings, (
        f"{len(seen)} statements read, all closing on day {day} of the month"
        + (f" · card{'s' if len(endings) != 1 else ''} {', '.join(sorted(endings))}"
           if endings else " · no card ending readable, so the note is withheld"))


def statement_note(rows, closing: int, held: set[str], endings: set[str], cur: str) -> str:
    """One line naming the card and the statement periods that would cover these charges.

    This was a per-row column and it should not have been: the same period repeated
    down eight rows is eight copies of one fact, and the fact is about the CARD, not
    about any charge. What the operator needs is "the Amex statement for this window
    is missing", once, at the top.

    A row is named only when its card is one the statements THEMSELVES identify. The
    cycle was read off particular documents and says nothing about a card those
    documents do not cover, so a row on any other card is left out of the note rather
    than given a period derived from somebody else's billing cycle.
    """
    import collections
    want = collections.defaultdict(set)
    skipped = set()
    for r in rows:
        if not r.get('date'):
            continue
        card = r.get('card') or ''
        if endings and not any(e in card for e in endings):
            if card:
                skipped.add(card)
            continue
        d = dt.date.fromisoformat(r['date'][:10])
        close = d.replace(day=closing)
        if d > close:
            close = (close.replace(day=28) + dt.timedelta(days=8)).replace(day=closing)
        if close.isoformat() not in held:
            want[r.get('card') or 'the card'].add(close)
    if not want:
        return ""
    bits = []
    aside = ''
    if skipped:
        aside = (' No statement in the folder covers '
                 + (', '.join(sorted(skipped)[:-1]) + ' or ' + sorted(skipped)[-1]
                    if len(skipped) > 1 else sorted(skipped)[0])
                 + ', so no period is named for '
                 + ('those cards.' if len(skipped) > 1 else 'that card.'))
    for card, closes in sorted(want.items()):
        spans = []
        for c in sorted(closes):
            start = (c.replace(day=1) - dt.timedelta(days=1)).replace(day=closing) + dt.timedelta(days=1)
            spans.append(f"{start.strftime('%-d %b')} to {c.strftime('%-d %b %Y')}")
        bits.append(f"<strong>{html.escape(card)}</strong>: "
                    + (", ".join(spans[:-1]) + " and " + spans[-1] if len(spans) > 1 else spans[0]))
    return ('<div class=note><strong>A statement is missing.</strong> These charges are on a card '
            'whose statement for the period named here is not in the folder, so there is nothing to '
            'check the amounts against beyond the feed. ' + "; ".join(bits) + '.' + aside + '</div>')


def money(v, cur):
    return f"{cur}&nbsp;{v:,.2f}" if v is not None else "&ndash;"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('outstanding', help='JSON array of charges with no invoice')
    ap.add_argument('--out', default='wanted-invoices.html')
    ap.add_argument('--portals', help='JSON map of supplier -> billing-history URL')
    ap.add_argument('--fx', type=float, help='median implied rate, for the estimate column')
    ap.add_argument('--currency', default='AUD')
    ap.add_argument('--foreign-currency', default='USD')
    ap.add_argument('--title', default='Invoices still needed')
    ap.add_argument('--statements', action='append', default=[],
                    help='repeatable path or glob of card statements already held. The '
                         'closing day and the periods covered are READ from them; adds a '
                         'column naming the period each charge falls in and whether it is held')
    ap.add_argument('--extractor', help='PDF text extractor, for statements whose filename '
                                        'is not a date')
    a = ap.parse_args()

    rows = json.load(open(a.outstanding))
    paths = sorted({p for pat in a.statements for p in glob.glob(os.path.expanduser(pat))})
    closing, held, endings, cadence = (statement_cadence(paths, a.extractor)
                                       if paths else (None, set(), set(), ''))
    if paths:
        print(f"[vouch-cadence] {cadence}"
              + (f" \u00b7 periods held={len(held)}" if closing else " \u00b7 no missing-statement note"))
    portals = json.load(open(a.portals)) if a.portals else {}

    # Biggest first: the operator's first five minutes should recover the most value.
    rows.sort(key=lambda r: -(r.get('local') or 0))

    groups: dict[str, list] = {}
    for r in rows:
        groups.setdefault(r.get('kind', 'unknown'), []).append(r)

    parts = ["<!doctype html>", "<html lang=en><head><meta charset=utf-8>",
             "<meta name=viewport content='width=device-width,initial-scale=1'>",
             f"<title>{html.escape(a.title)}</title><style>{CSS}</style></head><body>",
             "<div class=wrap>",
             f"<h1>{html.escape(a.title)}</h1>",
             lede(rows),
             f"<p class=meta>Prepared {dt.date.today().strftime('%-d %B %Y')}"
             + (f" &middot; estimates use an implied rate of {a.fx:.4f}" if a.fx else "")
             + "</p>",
             (statement_note(rows, closing, held, endings, a.currency) if closing else "")]

    for kind in ('portal', 'mail', 'account', 'statement', 'unknown'):
        g = groups.get(kind)
        if not g:
            continue
        heading, blurb = KIND_TEXT[kind]
        total = sum(r.get('local') or 0 for r in g)
        parts.append(f"<div class=group><h2>{heading}</h2><p>{blurb}</p><div class=card><table>")
        parts.append("<thead><tr><th>Charge date</th><th>Supplier</th>"
                     f"<th class=n>As charged</th><th class=n>Estimated {a.foreign_currency}</th>"
                     f"<th>Account it should name</th><th>Where</th><th>What is needed</th>"
                     "</tr></thead><tbody>")
        for r in g:
            local = r.get('local')
            est = r.get('foreign')
            est_html = money(est, a.foreign_currency) if est else (
                f"<span class=est>~{money(local / a.fx, a.foreign_currency)}</span>"
                if (a.fx and local) else "&ndash;")
            sup = html.escape(r.get('supplier') or r.get('desc', '')[:34])
            url = r.get('url') or portals.get(r.get('supplier', ''), '')
            where = (f"<a href='{html.escape(url)}'>billing history</a>" if url
                     else (html.escape(r.get('subject', '')[:44]) if kind == 'mail' else '&ndash;'))
            parts.append(
                f"<tr><td class=d>{html.escape(r.get('date',''))}</td>"
                f"<td class=sup>{sup}</td>"
                f"<td class=n>{money(local, a.currency)}</td>"
                f"<td class=n>{est_html}</td>"
                f"<td class=acct>{html.escape(r['account']) if r.get('account') else '&mdash;'}</td>"
                f"<td>{where}</td>"
                f"<td><span class=todo>{html.escape(r.get('todo') or heading)}</span></td></tr>")
        parts.append("</tbody></table></div>"
                     f"<p class=total>{len(g)} charges &middot; {money(total, a.currency)}</p></div>")

    parts.append(
        "<div class=note><strong>Why these are not in the claim.</strong> Every claimed row is keyed to the "
        "supplier's own invoice, and the invoice is read for the account it was issued to. Without the document "
        "there is nothing to key to, so the row stays out rather than going in on a guess. The estimated column "
        "is derived from the rate implied by charges that <em>do</em> have invoices; it is there to help you "
        "recognise the right line in a billing history, and it is never used as a claimed amount.</div>")
    parts.append("</div></body></html>")

    open(a.out, 'w').write("\n".join(parts))
    # Join only the groups that exist: an empty middle segment printed `charges=0 ·  · total`,
    # which reads as a census that failed rather than one that found nothing.
    census = [f"charges={len(rows)}"] + [f"{k}={len(v)}" for k, v in groups.items()]
    census.append(f"total={sum(r.get('local') or 0 for r in rows):,.2f} {a.currency}")
    print("[vouch-wanted] " + " · ".join(census))
    print(f"wrote {a.out}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

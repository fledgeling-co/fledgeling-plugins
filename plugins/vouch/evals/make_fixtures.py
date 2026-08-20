#!/usr/bin/env python3
"""Build the hermetic fixture claim: six charges, three suppliers, two months.

Every figure is invented. No household data ships with this skill, which is also why
the fixture PDFs are generated rather than copied: a real invoice carries a real
account, a real address and a real amount.

The PDFs are written by hand rather than by a library, so the evals have no dependency
to install. Each is a single Helvetica page whose text a PDF text extractor can read.
"""
from __future__ import annotations
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'fixtures')

ROWS = [
    dict(date='2025-08-04', vendor='Northwind Hosting', cat='Development & Infrastructure',
         desc='Application hosting, August', why='Hosting for the product.',
         inv='NW-2025-0801', ex=40.00, gst=4.00, inc=44.00),
    dict(date='2025-08-11', vendor='Cobalt Analytics', cat='Development & Infrastructure',
         desc='Log ingestion, August', why='Log ingestion and observability.',
         inv='CA-88213', ex=25.00, gst=0.00, inc=25.00),
    dict(date='2025-08-27', vendor='Pelham Office Suite', cat='Productivity & Business Tools',
         desc='Office suite, six seats', why='Company email and calendar.',
         inv='PEL-0000442', ex=90.00, gst=9.00, inc=99.00),
    dict(date='2025-09-04', vendor='Northwind Hosting', cat='Development & Infrastructure',
         desc='Application hosting, September', why='Hosting for the product.',
         inv='NW-2025-0901', ex=40.00, gst=4.00, inc=44.00),
    dict(date='2025-09-19', vendor='Cobalt Analytics', cat='Development & Infrastructure',
         desc='Log ingestion, September', why='Log ingestion and observability.',
         inv='CA-89007', ex=25.00, gst=0.00, inc=25.00),
    dict(date='2025-09-27', vendor='Pelham Office Suite', cat='Productivity & Business Tools',
         desc='Office suite, six seats', why='Company email and calendar.',
         inv='PEL-0000517', ex=90.00, gst=9.00, inc=99.00),
]


def pdf(lines: list[str]) -> bytes:
    """A one-page PDF carrying `lines` as Helvetica text. No dependencies."""
    text = "BT /F1 11 Tf 54 760 Td 15 TL\n"
    for ln in lines:
        esc = ln.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')
        text += f"({esc}) Tj T*\n"
    text += "ET"
    stream = text.encode('latin-1', 'replace')
    objs = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        b"/Resources << /Font << /F1 5 0 R >> >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out = bytearray(b"%PDF-1.4\n")
    offsets = []
    for i, o in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode() + o + b"\nendobj\n"
    xref = len(out)
    out += f"xref\n0 {len(objs)+1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {len(objs)+1} /Root 1 0 R >>\nstartxref\n{xref}\n"
            "%%EOF\n").encode()
    return bytes(out)


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    rows = []
    for r in ROWS:
        month = r['date'][:7]
        os.makedirs(os.path.join(OUT, month), exist_ok=True)
        rel = f"{month}/{r['inv']}.pdf"
        # Each supplier bills in a different shape, so the account census has one
        # document on each rung of the evidence ladder rather than six on the top one.
        billto = {
            'Northwind Hosting': ["Bill to", "Example Company Pty Ltd", "1 Sample Street",
                                  "ops@example.com"],                       # rung 1
            'Cobalt Analytics':  ["Bill to", "Example Company Pty Ltd", "1 Sample Street",
                                  "someone@personalmail.test"],             # rung 4
            'Pelham Office Suite': ["Bill to", "A. Person", "1 Sample Street",
                                    "Domain name example.com"],             # rung 2
        }[r['vendor']]
        open(os.path.join(OUT, rel), 'wb').write(pdf([
            r['vendor'],
            "Tax invoice",
            f"Invoice number {r['inv']}",
            f"Date of issue {r['date']}",
        ] + billto + [
            "",
            r['desc'],
            f"Subtotal {r['ex']:.2f}",
            f"GST {r['gst']:.2f}",
            f"Total {r['inc']:.2f}",
        ]))
        rows.append({**r, 'file': os.path.basename(rel), 'file_rel': rel})
    json.dump(rows, open(os.path.join(OUT, 'claim_rows.json'), 'w'), indent=1)

    json.dump({
        "claimant": "A. Person", "period": "8/2025 - 9/2025",
        "preamble": [["Expense Claim Form"], ["Applicant Name: ", "{claimant}"], [],
                     ["Expense Period :", "{period}"], []],
        "columns": ["Date", "Description", "Invoice No.",
                    "Amount    (excl. GST)", "GST", "Amount      (incl. GST)"],
        "date_format": "%d/%m/%Y", "negative": True, "zero_literal": "0",
        "total_label_col": 2,
        "footer_blocks": [[], ["", "", "", "", "Bank Account"],
                          ["", "", "", "", "Account Name:", "{claimant}"], [],
                          ["", "", "", "", "Applicant Signature"], ["", "", "", "", "Date:"]],
    }, open(os.path.join(OUT, 'form.json'), 'w'), indent=1)

    json.dump({
        "claimant": "A. Person", "period_label": "4 August 2025 and 30 September 2025",
        "currency": "A$", "tax_name": "GST", "tax_rate": 0.10,
        "approver_role": "the approver", "prepared": "1 October 2025",
    }, open(os.path.join(OUT, 'report.json'), 'w'), indent=1)

    # Charges and invoices for the assignment eval: two identical charges four days
    # apart, which an independent lookup pairs with whichever invoice returns first.
    json.dump([
        {"date": "2025-08-04", "desc": "Northwind top-up", "local": 44.00, "foreign": 20.00},
        {"date": "2025-08-08", "desc": "Northwind top-up", "local": 44.00, "foreign": 20.00},
    ], open(os.path.join(OUT, 'charges.json'), 'w'), indent=1)
    json.dump([
        {"date": "2025-08-04", "id": "NW-A", "total": 20.00},
        {"date": "2025-08-08", "id": "NW-B", "total": 20.00},
    ], open(os.path.join(OUT, 'invoices.json'), 'w'), indent=1)

    # A feed with a deliberate 38-day hole, for the coverage eval.
    import datetime as dt
    feed, d = [], dt.date(2025, 8, 1)
    while d <= dt.date(2025, 9, 30):
        if not (dt.date(2025, 8, 12) <= d <= dt.date(2025, 9, 18)):
            feed.append({"day": d.isoformat(), "acct": "Card 0001"})
        d += dt.timedelta(days=1)
    json.dump(feed, open(os.path.join(OUT, 'feed.json'), 'w'), indent=1)

    print(f"[vouch-fixtures] rows={len(rows)} · documents={len(rows)} · "
          f"excl={sum(r['ex'] for r in rows):.2f} · tax={sum(r['gst'] for r in rows):.2f} · "
          f"incl={sum(r['inc'] for r in rows):.2f} · feed days={len(feed)}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

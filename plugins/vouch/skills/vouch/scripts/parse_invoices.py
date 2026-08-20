#!/usr/bin/env python3
"""Parse a folder of extracted invoice text into structured records.

Input:  a directory of .txt files produced by pdftext.swift --out
Output: JSON array of {file, supplier, date, inv, total, currency, billed[], billto, cards[], tax}

Every pattern here exists because a real invoice needed it. Notes:
  - Vendors break the line after a label, hence `\\s*\\n?\\s*` throughout.
  - One supplier changed its id label mid-series (Invoice number -> Invoice reference);
    both are tried, always.
  - Month abbreviations can be 4 letters ("Sept"), hence [A-Za-z]{3,}.
  - A single amount pattern silently returned nothing on 6 of 13 invoices; layer them.

Usage:
    python3 parse_invoices.py /tmp/pdftext --config vouch.json > invoices.json
"""
from __future__ import annotations
import argparse, datetime as dt, glob, json, os, re, sys

MONTH = "January|February|March|April|May|June|July|August|September|October|November|December"

INV_PATTERNS = [
    r'Invoice number:?\s*\n?\s*([A-Za-z0-9][A-Za-z0-9\-\._]{2,40})',
    r'Invoice reference:?\s*\n?\s*([A-Z0-9\-]{4,40})',
    r'Invoice #\s*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice no\.?\s*:?\s*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice ID[:\s]*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice:\s*\n?\s*(?:Date:\s*\n?\s*Status:\s*\n?\s*)?([0-9a-f]{32})',
    r'Receipt number\s*\n?\s*([0-9\-]{4,40})',
    r'Order number[:\s]*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Billing Number\s*\n?\s*(\S+)',
    r'Transaction ID\s*\n?\s*(\S+)',
]

DATE_PATTERNS = [
    r'Date paid\s*\n?\s*([A-Za-z]{3,} \d{1,2}, \d{4})',
    r'Date paid\s*\n?\s*(\d{1,2} [A-Za-z]{3,} \d{4})',
    r'Date of issue\s*\n?\s*(\d{1,2} [A-Za-z]{3,} \d{4})',
    r'Date of issue\s*\n?\s*([A-Za-z]{3,} \d{1,2}, \d{4})',
    r'Issue Date\s*\n?\s*([A-Za-z]{3,} \d{1,2}, \d{4})',
    r'Issue Date\s*\n?\s*(\d{1,2} [A-Za-z]{3,} \d{4})',
    r'Invoice date\s*\n?[\.\s]*\n?\s*(\d{1,2} [A-Za-z]{3,} \d{4})',
    r'Invoice date\s*\n?[\.\s]*\n?\s*([A-Za-z]{3,} \d{1,2}, \d{4})',
    r'Document Date\s*\n?\s*(\d{2}/\d{2}/\d{4})',
    r'\b(\d{4}-\d{2}-\d{2})\b',
]
DATE_FORMATS = ('%B %d, %Y', '%d %B %Y', '%b %d, %Y', '%d %b %Y', '%Y-%m-%d', '%d/%m/%Y')

TOTAL_PATTERNS = [
    r'Amount paid\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)',
    r'Amount due\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)',
    r'\bTotal\s*\n?\s*(?:US|AU|A)?\$?\s*([\d,]+\.\d\d)',
    r'Total \(including Tax\)\s*(?:AUD|USD)?\s*([\d,]+\.\d\d)',
    r'Total (?:in )?(?:AUD|USD)\s*\n?\s*\$?\s*([\d,]+\.\d\d)',
    r'TOTAL\s*\$\s*([\d,]+\.\d\d)',
    r'Total amount\s*\n?\s*(?:AU|US)?\$?\s*([\d,]+\.\d\d)',
    r'INVOICE TOTAL:?\s*\$?\s*([\d,]+\.\d\d)',
]

CARD_RE = re.compile(r'(American Express|Visa|Mastercard|MasterCard)[^\n]{0,30}?(\d{4})\b')
EMAIL_RE = re.compile(r'[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}')
# Local-currency equivalent printed beside a foreign tax line: "(A$0.73)"
TAX_LOCAL_RE = re.compile(r'\((A?\$[\d,]+\.\d\d)\)')


def norm(t: str) -> str:
    """NFKC and dash/quote normalisation. Vendors emit en dashes and curly quotes."""
    import unicodedata
    t = unicodedata.normalize('NFKC', t)
    for a, b in (('–', '-'), ('—', '-'), ('’', "'"), ('−', '-')):
        t = t.replace(a, b)
    return t


def first(patterns, text, flags=0):
    for p in patterns:
        m = re.search(p, text, flags)
        if m:
            return m.group(1)
    return None


def parse_date(text):
    raw = first(DATE_PATTERNS, text)
    if not raw:
        return None
    raw = re.sub(r'\s+', ' ', raw).strip()
    for f in DATE_FORMATS:
        try:
            return dt.datetime.strptime(raw, f).date().isoformat()
        except ValueError:
            pass
    return None


def parse_total(text):
    v = first(TOTAL_PATTERNS, text)
    return float(v.replace(',', '')) if v else None


def resolve_supplier(text, filename, prefix_map, issuer_map, filename_rules):
    """Three stages, in order of authority. See references/extraction.md."""
    head = text[:400]
    for prefix, name in prefix_map.items():          # 1. invoice-number prefix
        if prefix in filename or prefix in head:
            return name, prefix
    low = text.lower()
    for name, marker in issuer_map:                  # 2. issuer text marker
        if marker in low:
            return name, None
    for pattern, name in filename_rules:             # 3. filename shape
        if re.match(pattern, filename):
            return name, None
    return None, None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('textdir')
    ap.add_argument('--config', help='JSON with prefix_map, issuer_map, filename_rules, vendor_domains')
    ap.add_argument('--skip-statements', action='store_true', default=True)
    a = ap.parse_args()

    cfg = json.load(open(a.config)) if a.config else {}
    prefix_map = cfg.get('prefix_map', {})
    issuer_map = [tuple(x) for x in cfg.get('issuer_map', [])]
    filename_rules = [tuple(x) for x in cfg.get('filename_rules', [])]
    vendor_domains = tuple(cfg.get('vendor_domains', []))
    statement_markers = cfg.get('statement_markers', ['Statement of Account'])

    out, skipped = [], 0
    for f in sorted(glob.glob(os.path.join(a.textdir, '*.txt'))):
        text = norm(open(f, encoding='utf8', errors='replace').read())
        fn = os.path.basename(f)[:-4]
        # A statement contains every amount in the corpus; never parse one as an invoice.
        if a.skip_statements and any(m in text[:600] for m in statement_markers):
            skipped += 1
            continue
        supplier, prefix = resolve_supplier(text, fn, prefix_map, issuer_map, filename_rules)
        bt = re.search(r'Bill [Tt]o\s*\n(.{0,220})', text, re.S)
        emails = [e.lower() for e in EMAIL_RE.findall(text)
                  if not any(d in e.lower() for d in vendor_domains)]
        tax_local = TAX_LOCAL_RE.search(text)
        out.append({
            'file': fn,
            'supplier': supplier,
            'prefix': prefix,
            'date': parse_date(text),
            'inv': first(INV_PATTERNS, text),
            'total': parse_total(text),
            'billed': sorted(set(emails))[:3],
            'billto': re.sub(r'\s+', ' ', bt.group(1))[:160] if bt else '',
            'cards': [f'{b} {c}' for b, c in CARD_RE.findall(text)],
            'tax_local': tax_local.group(1) if tax_local else None,
        })

    json.dump(out, sys.stdout, indent=1)
    ok = [r for r in out if r['supplier'] and r['date']]
    # Denominators, on stderr so stdout stays parseable.
    print(f"\n[vouch-invoices] parsed={len(out)} · statements skipped={skipped} · "
          f"supplier+date={len(ok)} · no supplier={sum(1 for r in out if not r['supplier'])} · "
          f"no date={sum(1 for r in out if r['supplier'] and not r['date'])} · "
          f"no total={sum(1 for r in out if r['supplier'] and not r['total'])}", file=sys.stderr)
    for r in out:
        if r['supplier'] and not (r['date'] and r['total'] and r['inv']):
            miss = [k for k in ('date', 'total', 'inv') if not r[k]]
            print(f"  incomplete: {r['file']}  missing {','.join(miss)}", file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

#!/usr/bin/env python3
"""Audit every filed document: does its filename match an invoice id printed inside it?

This is the check that makes "name every attachment by its invoice number" a safe
convention rather than a hopeful one. An earlier pass on a real run keyed rows to
billing emails instead of invoices and put FOURTEEN rows on the wrong month; a vendor's
monthly emails look alike, and nothing else would have caught it.

Reports four buckets plus orphans, so a clean result has a denominator.

Usage:
    python3 audit_invoices.py --rows claim_rows.json --dir out/ [--extractor /tmp/pdftext]
"""
from __future__ import annotations
import argparse, json, os, re, subprocess, sys

ID_PATTERNS = [
    r'Invoice number:?\s*\n?\s*([A-Za-z0-9][A-Za-z0-9\-\._]{2,40})',
    r'Invoice reference:?\s*\n?\s*([A-Z0-9\-]{4,40})',
    r'Invoice #\s*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice no\.?\s*:?\s*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice ID[:\s]*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Invoice:\s*\n?\s*([0-9a-f]{32})',
    r'Receipt number\s*\n?\s*([0-9\-]{4,40})',
    r'Order number[:\s]*\n?\s*([A-Za-z0-9\-\._]{2,40})',
    r'Billing Number\s*\n?\s*(\S+)',
    r'Transaction ID\s*\n?\s*(\S+)',
]


def ids_in(text: str) -> set[str]:
    out = set()
    for p in ID_PATTERNS:
        for m in re.finditer(p, text):
            out.add(m.group(1).strip().rstrip('.,'))
    return out


BANNER = re.compile(r'^=== .* ===$', re.M)


def read(path: str, extractor: str) -> str:
    """Document text with the extractor's own filename banner REMOVED.

    pdftext.swift prints `=== <path> ===` ahead of each document so a batch can be
    split. Left in, it makes this whole audit vacuous: the fallback match looks for the
    filename anywhere in the text, and the banner IS the filename, so every file matches
    its own name whatever is inside it. Measured — two documents' filenames were swapped
    so each held the other's invoice number, and the audit still reported 88 of 88.
    A check whose pass is indistinguishable from its cannot-run is worse than no check.
    """
    if path.lower().endswith('.pdf'):
        text = subprocess.run([extractor, path], capture_output=True, text=True).stdout
        return BANNER.sub('', text)
    # A non-PDF read through the PDF extractor reports absent while sitting on disk.
    return open(path, encoding='utf8', errors='replace').read()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--rows', required=True)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--extractor', default='/tmp/pdftext')
    a = ap.parse_args()

    rows = json.load(open(a.rows))
    matched, mismatch, missing, unreadable = [], [], [], []

    for r in rows:
        path = os.path.join(a.dir, r['file_rel'])
        if not os.path.exists(path):
            missing.append(r); continue
        stem = os.path.splitext(os.path.basename(path))[0]
        text = read(path, a.extractor)
        if not text.strip():
            unreadable.append((r, stem)); continue
        ids = ids_in(text)
        flat = re.sub(r'\s+', '', text)
        if stem in ids or re.sub(r'\s+', '', stem) in flat:
            matched.append(r)
        else:
            mismatch.append((r, stem, sorted(ids)[:5]))

    cited = [r['file_rel'] for r in rows]
    on_disk = {os.path.relpath(os.path.join(d, f), a.dir)
               for d, _, fs in os.walk(a.dir) for f in fs
               if f.lower().endswith(('.pdf', '.eml', '.png', '.jpg'))}
    orphans = sorted(on_disk - set(cited))

    print(f"rows: {len(rows)}")
    print(f"  filename matches an invoice id inside the file : {len(matched)}")
    print(f"  filename NOT found in the file                 : {len(mismatch)}")
    print(f"  file missing                                   : {len(missing)}")
    print(f"  file unreadable                                : {len(unreadable)}")
    print(f"  files on disk cited by no row                  : {len(orphans)}")

    for r in missing:
        print(f"    MISSING   {r['date']}  {r.get('vendor','')}  {r['inv']} -> {r['file_rel']}")
    for r, stem, ids in mismatch:
        print(f"    MISMATCH  {r['date']}  {r.get('vendor','')}  file={stem}")
        print(f"              ids inside: {ids or '(none matched a known pattern)'}")
    for r, stem in unreadable:
        print(f"    NO TEXT   {r['date']}  {stem}")
    for o in orphans:
        print(f"    ORPHAN    {o}")

    bad = len(mismatch) + len(missing) + len(orphans)
    if bad:
        print(f"\n{bad} problems. A filename that disagrees with its document is the defect "
              "that puts rows on the wrong month.")
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())

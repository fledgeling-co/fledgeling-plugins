#!/usr/bin/env python3
"""The gate suite. Exits non-zero on any blocking failure.

This is the run's exit condition, not advice. Every check names the defect that
motivated it in references/gates.md; the two that have caught the most are #6
(excl + tax == incl, which found a real column transposition) and #15 (filename
matches an id printed inside the document, which found 14 rows on the wrong month).

Usage:
    python3 validate.py --csv claim.csv --rows claim_rows.json --dir out/ \
        --start 2025-08-07 --end 2026-06-30 --extractor /tmp/pdftext
"""
from __future__ import annotations
import argparse, csv, datetime as dt, json, os, re, subprocess, sys

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

BANNER = re.compile(r'^=== .* ===$', re.M)

FAIL, WARN, OK = [], [], []
def fail(m): FAIL.append(m)
def warn(m): WARN.append(m)
def ok(m):   OK.append(m)


def money(s: str) -> float:
    s = s.strip().replace(',', '').replace('$', '')
    return 0.0 if s in ('', '-', 'NA', 'N/A') else float(s)


def ids_in(text: str) -> set[str]:
    out = set()
    for p in ID_PATTERNS:
        for m in re.finditer(p, text):
            out.add(m.group(1).strip().rstrip('.,'))
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--csv', required=True)
    ap.add_argument('--rows', required=True)
    ap.add_argument('--dir', required=True)
    ap.add_argument('--start', required=True)
    ap.add_argument('--end', required=True)
    ap.add_argument('--extractor', default='/tmp/pdftext')
    ap.add_argument('--date-format', default='%d/%m/%Y')
    ap.add_argument('--negative', action='store_true', default=True,
                    help='the form uses negative amounts')
    ap.add_argument('--tax-rate', type=float, default=0.10,
                    help='headline consumption-tax rate; 0 disables the magnitude checks')
    ap.add_argument('--tax-tol', type=float, default=0.02,
                    help='relative tolerance on the tax-share check')
    ap.add_argument('--classify-col', type=int, default=6,
                    help='0-based index of the optional classification column, -1 to skip')
    a = ap.parse_args()

    rows_src = json.load(open(a.rows))
    lines = list(csv.reader(open(a.csv)))

    # ---- 1-3 structure ------------------------------------------------------
    try:
        hi = next(i for i, r in enumerate(lines) if r and r[0].strip() == 'Date')
    except StopIteration:
        fail("no header row: no line begins with 'Date'")
        print_report(); return 1
    hdr = lines[hi]
    width = len(hdr)
    ok(f"header at line {hi+1}, {width} columns")
    bad = [i + 1 for i, r in enumerate(lines) if len(r) != width]
    fail(f"{len(bad)} lines are not {width} columns wide: {bad[:8]}") if bad else \
        ok(f"all {len(lines)} lines are {width} columns wide")

    body = [r for r in lines[hi+1:] if r and r[0].strip() and '/' in r[0]]
    ok(f"{len(body)} data rows") if len(body) == len(rows_src) else \
        fail(f"data rows {len(body)} != source rows {len(rows_src)}")

    # ---- 4-5 dates ----------------------------------------------------------
    lo, hi_d = dt.date.fromisoformat(a.start), dt.date.fromisoformat(a.end)
    parsed, bad_d = [], []
    for r in body:
        try:
            d = dt.datetime.strptime(r[0].strip(), a.date_format).date()
            parsed.append(d)
            if not (lo <= d <= hi_d):
                bad_d.append((r[0], 'outside the claim period'))
        except ValueError:
            bad_d.append((r[0], f'unparseable as {a.date_format}'))
    fail(f"{len(bad_d)} bad dates: {bad_d[:5]}") if bad_d else \
        ok(f"all {len(body)} dates parse and sit inside {a.start}..{a.end}")
    ok("rows are in date order") if parsed == sorted(parsed) else fail("rows are NOT in date order")

    # ---- 6-8 money ----------------------------------------------------------
    arith, signs, fmt = [], [], []
    for r in body:
        ex, tax, inc = money(r[3]), money(r[4]), money(r[5])
        if abs((ex + tax) - inc) > 0.005:
            arith.append((r[0], r[2], ex, tax, inc))
        if a.negative and any(v > 0 for v in (ex, tax, inc)):
            signs.append((r[0], r[2]))
        if not all(re.fullmatch(r'-?\d+\.\d\d|0', r[i].strip()) for i in (3, 4, 5)):
            fmt.append(r[0])
    fail(f"{len(arith)} rows where excl + tax != incl: {arith[:4]}") if arith else \
        ok("every row: excl + tax == incl")
    fail(f"{len(signs)} rows break the sign convention: {signs[:4]}") if signs else \
        ok("sign convention holds on every amount")
    fail(f"{len(fmt)} rows not 2-decimal or literal 0: {fmt[:5]}") if fmt else \
        ok("all money fields are 2-decimal or literal 0")

    # Transposition is invisible to check #6: swapping two values preserves their sum.
    # What catches it is magnitude — on a tax-bearing row the tax is the SMALLER part,
    # and for a rate r it is incl * r/(1+r). A real prior-year form held the tax figure
    # under the ex-tax header on every row, and this is the shape that found it.
    if a.tax_rate > 0:
        share = a.tax_rate / (1 + a.tax_rate)
        swapped, offrate = [], []
        for r in body:
            ex, tax, inc = abs(money(r[3])), abs(money(r[4])), abs(money(r[5]))
            if tax == 0 or inc == 0:
                continue
            if tax > ex:
                swapped.append((r[0], r[2], ex, tax))
            elif abs(tax - inc * share) > max(0.02, inc * share * a.tax_tol):
                offrate.append((r[0], r[2], tax, round(inc * share, 2)))
        fail(f"{len(swapped)} tax-bearing rows where tax exceeds the ex-tax amount "
             f"(columns transposed?): {swapped[:4]}") if swapped else \
            ok("on every tax-bearing row the tax is the smaller component")
        warn(f"{len(offrate)} rows whose tax is not ~{a.tax_rate:.0%} of the inclusive amount "
             f"(fine for a mixed or exempt supply, worth an eye): {offrate[:4]}") if offrate else \
            ok(f"every tax-bearing row's tax is ~{a.tax_rate:.0%} of its inclusive amount")

    # ---- 9-11 totals --------------------------------------------------------
    tot = next((r for r in lines if len(r) > 2 and r[2].strip() == 'Total'), None)
    if not tot:
        fail("no Total row")
    else:
        for idx, label in ((3, 'excl.'), (4, 'tax'), (5, 'incl.')):
            s, t = round(sum(money(r[idx]) for r in body), 2), round(money(tot[idx]), 2)
            ok(f"Total {label} {t:,.2f} equals the sum of the rows") if abs(s - t) < 0.005 else \
                fail(f"Total {label}: row says {t}, rows sum to {s}")

    # ---- 12-14 invoices and files ------------------------------------------
    seen: dict[str, list[str]] = {}
    for r in body:
        seen.setdefault(r[2].strip(), []).append(r[0])
    dups = {k: v for k, v in seen.items() if len(v) > 1}
    fail(f"duplicate invoice numbers: {dups}") if dups else \
        ok(f"all {len(seen)} invoice numbers are unique")

    by_inv = {r['inv']: r for r in rows_src}
    orphan_nums = [r[2] for r in body if r[2].strip() not in by_inv]
    fail(f"{len(orphan_nums)} CSV invoice numbers absent from the source: {orphan_nums[:5]}") \
        if orphan_nums else ok("every CSV invoice number exists in the source rows")

    missing_file = [s['inv'] for s in rows_src
                    if not os.path.exists(os.path.join(a.dir, s['file_rel']))]
    fail(f"{len(missing_file)} rows whose file is absent: {missing_file[:5]}") if missing_file else \
        ok("every row's invoice file exists")

    # ---- 15 filename vs document content -----------------------------------
    mism, unreadable, checked = [], [], 0
    for s in rows_src:
        p = os.path.join(a.dir, s['file_rel'])
        if not os.path.exists(p):
            continue
        stem = os.path.splitext(os.path.basename(p))[0]
        if p.lower().endswith('.pdf'):
            text = subprocess.run([a.extractor, p], capture_output=True, text=True).stdout
            # Strip the extractor's own `=== <path> ===` banner FIRST. Left in, the
            # fallback below finds the filename in the banner rather than in the
            # document, so every file matches its own name whatever is inside it —
            # measured, with two documents' filenames swapped and 88 of 88 still green.
            text = BANNER.sub('', text)
        else:
            # Read a non-PDF as text, or a .eml reports absent while sitting on disk.
            text = open(p, encoding='utf8', errors='replace').read()
        if not text.strip():
            unreadable.append(stem); continue
        checked += 1
        if stem not in ids_in(text) and re.sub(r'\s+', '', stem) not in re.sub(r'\s+', '', text):
            mism.append(stem)
    fail(f"{len(mism)} filenames not found inside their own document: {mism[:5]}") if mism else \
        ok(f"all {checked} filenames match an invoice id printed inside the document")
    warn(f"{len(unreadable)} files produced no text: {unreadable[:5]}") if unreadable else None

    # ---- 15b no card statement filed in the claim folder --------------------
    # A statement is EVIDENCE, not a claimed document. It is read where it lies to
    # confirm a charge was paid personally when the card's last four digits cannot be
    # found any other way, and it carries every other transaction on that card for the
    # month — including ones that are nobody's business but the cardholder's. Copying
    # one into a folder that goes to an approver and an accountant discloses all of them.
    STATEMENT_MARKERS = re.compile(
        r'statement period|closing balance|minimum payment|previous balance|payment due date',
        re.I)
    filed = []
    for d, _, fs in os.walk(a.dir):
        for f in fs:
            if not f.lower().endswith('.pdf'):
                continue
            p_ = os.path.join(d, f)
            txt = BANNER.sub('', subprocess.run([a.extractor, p_], capture_output=True,
                                                text=True).stdout)
            if STATEMENT_MARKERS.search(txt):
                filed.append(os.path.relpath(p_, a.dir))
    fail(f"{len(filed)} card statement(s) filed in the claim folder: {filed[:4]} — a statement "
         f"is read where it lies, never copied in; it carries the cardholder's other "
         f"transactions") if filed else \
        ok("no card statement is filed in the claim folder")

    # ---- 16 orphans and shared files ---------------------------------------
    cited = [s['file_rel'] for s in rows_src]
    on_disk = {os.path.relpath(os.path.join(d, f), a.dir)
               for d, _, fs in os.walk(a.dir) for f in fs
               if f.lower().endswith(('.pdf', '.eml', '.png', '.jpg'))}
    orphans = sorted(on_disk - set(cited))
    fail(f"{len(orphans)} files on disk cited by no row: {orphans[:5]}") if orphans else \
        ok("no orphan files")
    shared = {k for k in cited if cited.count(k) > 1}
    fail(f"{len(shared)} files cited by more than one row: {sorted(shared)[:4]}") if shared else \
        ok("no file is cited by two rows")

    # ---- 17 CSV vs source, field by field ----------------------------------
    def dmy(iso):
        y, m, d = iso.split('-'); return f"{d}/{m}/{y}"
    mism2 = []
    for r, s in zip(body, sorted(rows_src, key=lambda x: (x['date'], x['vendor']))):
        if r[0].strip() != dmy(s['date']): mism2.append((r[2], 'date'))
        if r[2].strip() != s['inv']:       mism2.append((r[2], 'inv'))
        if abs(abs(money(r[5])) - s['inc']) > 0.005: mism2.append((r[2], 'incl'))
    fail(f"{len(mism2)} CSV/source field mismatches: {mism2[:4]}") if mism2 else \
        ok("every CSV field matches its source row")

    # ---- 18-20 hygiene and the optional classification ----------------------
    raw = open(a.csv, 'rb').read()
    try:
        raw.decode('utf8'); ok("file is valid UTF-8")
    except UnicodeDecodeError:
        fail("file is not valid UTF-8")
    warn("file has a BOM") if raw[:3] == b'\xef\xbb\xbf' else ok("no BOM")
    warn("CRLF line endings (Excel-friendly, not a defect)") if b'\r\n' in raw else ok("LF line endings")

    c = a.classify_col
    if c >= 0 and width > c:
        vals = {r[c].strip() for r in body}
        if vals <= {''}:
            warn("classification column is empty on every row")
        else:
            badv = sorted(v for v in vals if v not in ('TRUE', 'FALSE', ''))
            fail(f"classification column holds {badv}") if badv else \
                ok("classification column is TRUE/FALSE only")
            nore = [r[2] for r in body if r[c].strip() and not r[c+1].strip()]
            fail(f"{len(nore)} classified rows carry no reason") if nore else \
                ok("every classified row carries a reason")

    print_report()
    return 1 if FAIL else 0


def print_report():
    print("=" * 74)
    print(f"PASS {len(OK)}   WARN {len(WARN)}   FAIL {len(FAIL)}")
    print("=" * 74)
    for m in OK:   print("  ok    ", m)
    for m in WARN: print("  WARN  ", m)
    for m in FAIL: print("  FAIL  ", m)
    if FAIL:
        print("\nThe claim is not ready. Every FAIL above is blocking.")


if __name__ == '__main__':
    raise SystemExit(main())

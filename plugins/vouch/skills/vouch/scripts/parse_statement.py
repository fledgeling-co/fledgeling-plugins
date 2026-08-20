#!/usr/bin/env python3
"""Parse card statement PDFs into dated transaction rows.

A statement is the authority for what was actually charged, and the only source that
states the foreign amount and the conversion commission alongside the local one:

    October 19 SLACK T05TTDDSUAG DUBLIN
    13.13 21.00
    UNITED STATES DOLLAR
    AUD 21.00 includes conversion commission of AUD .61

Handles: the statement-period header, the year rollover (a January line on a statement
ending in February belongs to the prior year), the one-line amount form, the two-line
foreign form, and the CR credit marker on the following line.

Usage:
    python3 parse_statement.py --extractor /tmp/pdftext stmt1.pdf stmt2.pdf > rows.json
"""
from __future__ import annotations
import argparse, json, re, subprocess, sys

MONTHS = ["January", "February", "March", "April", "May", "June",
          "July", "August", "September", "October", "November", "December"]
M = {m: i + 1 for i, m in enumerate(MONTHS)}
MONTH_RE = "|".join(MONTHS)

PERIOD_RE = re.compile(
    r'Statement Period From (\w+) (\d+) to (\w+) (\d+), (\d{4})')
LINE_RE = re.compile(rf'^({MONTH_RE}) (\d{{1,2}}) (.+)$')
TAIL_AMOUNT_RE = re.compile(r'(-?[\d,]+\.\d\d)$')
PAIR_RE = re.compile(r'^([\d,]+\.\d\d) ([\d,]+\.\d\d)$')     # foreign, local
LONE_RE = re.compile(r'^([\d,]+\.\d\d)$')
ACCOUNT_RE = re.compile(r'([X\*x]{3,}[-\s]?[X\*x]*[-\s]?(\d{4,5}))')


def extract(path: str, extractor: str) -> str:
    return subprocess.run([extractor, path], capture_output=True, text=True).stdout


def parse(path: str, extractor: str):
    txt = extract(path, extractor)
    per = PERIOD_RE.search(txt)
    if not per:
        print(f"  !! no statement period found in {path}", file=sys.stderr)
        return None, []
    end_year, end_month = int(per.group(5)), M[per.group(3)]
    acct = ACCOUNT_RE.search(txt)
    lines = [l.rstrip() for l in txt.splitlines()]
    rows, i = [], 0
    while i < len(lines):
        m = LINE_RE.match(lines[i])
        if not m:
            i += 1
            continue
        mo, day, rest = M[m.group(1)], int(m.group(2)), m.group(3)
        # A month later than the statement's end month belongs to the previous year.
        year = end_year if mo <= end_month else end_year - 1
        if end_month < 3 and mo > 10:
            year = end_year - 1

        local = foreign = None
        tail = TAIL_AMOUNT_RE.search(rest)
        if tail:
            local = float(tail.group(1).replace(',', ''))
            desc = rest[:tail.start()].strip()
        else:
            desc = rest.strip()
            for j in range(i + 1, min(i + 4, len(lines))):
                p = PAIR_RE.match(lines[j].strip())
                if p:
                    foreign = float(p.group(1).replace(',', ''))
                    local = float(p.group(2).replace(',', ''))
                    break
                s = LONE_RE.match(lines[j].strip())
                if s and local is None:
                    local = float(s.group(1).replace(',', ''))
        credit = 'CR' in (lines[i + 1] if i + 1 < len(lines) else '')
        if local is not None:
            rows.append({'date': f'{year:04d}-{mo:02d}-{day:02d}', 'desc': desc,
                         'local': local, 'foreign': foreign, 'credit': credit,
                         'statement': path})
        i += 1
    return (per.group(0), acct.group(1) if acct else None), rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('pdfs', nargs='+')
    ap.add_argument('--extractor', default='/tmp/pdftext',
                    help='compiled pdftext binary (swiftc -O pdftext.swift -o /tmp/pdftext)')
    a = ap.parse_args()

    all_rows = []
    for p in a.pdfs:
        meta, rows = parse(p, a.extractor)
        if meta:
            print(f"=== {p}\n    {meta[0]} · account {meta[1] or '?'} · {len(rows)} lines",
                  file=sys.stderr)
        all_rows += rows
    json.dump(all_rows, sys.stdout, indent=1)
    charges = [r for r in all_rows if not r['credit']]
    print(f"\n[vouch-statement] statements={len(a.pdfs)} · lines={len(all_rows)} · "
          f"charges={len(charges)} · credits={len(all_rows) - len(charges)} · "
          f"with a foreign amount={sum(1 for r in charges if r['foreign'])}", file=sys.stderr)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

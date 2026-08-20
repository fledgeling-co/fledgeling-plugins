#!/usr/bin/env python3
"""The extraction patterns, defined once.

They lived in four scripts as four copies, which is how one of them drifted into a shape
that could not fire while the others were fine. A pattern with one definition has one
place to prove it, and `evals/check_patterns.py` proves each against a string it must
match and a string it must refuse.

Currency is deliberately not spelled as `$`. This skill claims to work outside one
jurisdiction, and a pattern hardcoding a dollar sign quietly makes that untrue: it was
caught by an eval fixture in pounds, not by review.
"""
from __future__ import annotations
import re

# The extractor prints `=== <path> ===` ahead of each document so a batch can be split.
# Strip it before matching anything: it contains the filename, so any check that looks
# for the filename in the text finds it there and passes on every file.
BANNER = re.compile(r'^=== .* ===$', re.M)

EMAIL = re.compile(r'[\w\.\-\+]+@[\w\.\-]+\.\w+')

# Case-insensitive, and every label a real supplier has been observed printing. A
# case-sensitive `Bill To` misses `BILL TO` silently and falls through to the page
# header, which then reads as the addressee.
BILLTO = re.compile(
    r'(?:bill(?:ed)?\s*to|sold\s*to|invoice\s*to|account\s+billed|issued\s*to|ship\s*to)\b(.{0,320})',
    re.I | re.S)

# Any currency symbol or code, or none. `[^\d\n]{0,6}` covers $, A$, US$, £, €, AUD, USD
# and a bare number, without naming any of them.
MONEY = r'[^\d\n]{0,6}([\d,]+\.\d\d)'

# The TAX line, capturing the tax and never the base it is computed on. A supplier writes
# `GST - Australia (10% on A$309.09) A$30.91`, and a greedy pattern returns 309.09 — the
# net amount wearing the tax label, which then fails the magnitude gate rather than the
# extraction. Anchor on the closing bracket of the rate clause first.
TAX_WITH_RATE = re.compile(r'(?:GST|VAT|Tax|Sales tax)[^\n]*?\)\s*' + MONEY, re.I)
TAX_PLAIN = re.compile(r'^\s*(?:GST|VAT|Tax|Sales tax)\b[^\n]{0,24}?' + MONEY + r'\s*$', re.I | re.M)

TOTAL = re.compile(r'(?:Total|Amount due|Amount paid)\b[^\n]{0,24}?' + MONEY, re.I)

INVOICE_ID = [
    re.compile(r'Invoice number:?\s*\.*\s*\n?\s*([A-Za-z0-9][A-Za-z0-9\-\._]{2,40})', re.I),
    re.compile(r'Invoice reference:?\s*\n?\s*([A-Z0-9\-]{4,40})', re.I),
    re.compile(r'Invoice #\s*\n?\s*([A-Za-z0-9\-\._]{2,40})', re.I),
    re.compile(r'Invoice no\.?\s*:?\s*\n?\s*([A-Za-z0-9\-\._]{2,40})', re.I),
    re.compile(r'Invoice ID[:\s]*\n?\s*([A-Za-z0-9\-\._]{2,40})', re.I),
    re.compile(r'Billing Number\s*\n?\s*(\S+)', re.I),
    re.compile(r'Receipt number\s*\n?\s*([0-9\-]{4,40})', re.I),
    re.compile(r'Transaction ID\s*\n?\s*(\S+)', re.I),
]


def tax_amount(text: str, net_hint: float | None = None) -> float | None:
    """The tax stated on the document, or None.

    `net_hint` is the ex-tax figure where it is known. A tax larger than its own net is
    the transposition gate 21 exists for, and returning None is better than returning a
    number that will fail a gate two stages later with no clue where it came from.
    """
    for pat in (TAX_WITH_RATE, TAX_PLAIN):
        m = pat.search(text)
        if not m:
            continue
        v = float(m.group(1).replace(',', ''))
        if net_hint is not None and v > net_hint:
            continue
        return round(v, 2)
    return None


def invoice_ids(text: str) -> set[str]:
    out = set()
    for pat in INVOICE_ID:
        for m in pat.finditer(text):
            out.add(m.group(1).strip().rstrip('.,'))
    return out

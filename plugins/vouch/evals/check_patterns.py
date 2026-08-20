#!/usr/bin/env python3
"""Every extraction pattern is held by a fixture it must match AND one it must not.

Three real defects sit behind this file, and all three would have passed a suite of
positive fixtures alone: a domain pattern that required a trailing character so a bare
address never matched, a case-sensitive bill-to label that fell through to the page
header, and a tax pattern that returned the base the tax was computed on.

Usage:  python3 check_patterns.py ../skills/vouch/scripts/classify_accounts.py
"""
from __future__ import annotations
import importlib.util, os, re, sys


def load(path):
    spec = importlib.util.spec_from_file_location('subject', path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    m = load(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          '..', 'skills', 'vouch', 'scripts', 'patterns.py'))
    bad, checked = [], 0

    # (a) an address whose domain ends the string must still match.
    for good in ('someone@personalmail.test', 'a.b+c@sub.example.co.uk', 'x@y.gg'):
        checked += 1
        if not m.EMAIL.search(good):
            bad.append(f'EMAIL misses {good!r}')
    for nope in ('no address here', 'at sign @ alone', 'trailing@'):
        checked += 1
        if m.EMAIL.search(nope):
            bad.append(f'EMAIL matched {nope!r}')

    # (b) the label must match whatever case and wording a supplier prints.
    for good in ('Bill to', 'BILL TO', 'Billed To', 'bill  to', 'Sold To',
                 'ISSUED TO', 'Invoice to', 'Account billed'):
        checked += 1
        if not m.BILLTO.search(good + ' Someone Ltd'):
            bad.append(f'BILLTO misses {good!r}')
    for nope in ('Total due on receipt', 'Payable to the order of'):
        checked += 1
        if m.BILLTO.search(nope):
            bad.append(f'BILLTO matched {nope!r}')

    # (c) a tax line quoting both the rate and its base must yield the TAX, in any
    # currency. A pattern hardcoding a dollar sign makes the skill's claim to work
    # outside one jurisdiction quietly untrue, and only a non-dollar fixture finds it.
    for line, want in (('GST - Australia (10% on A$309.09) A$30.91', 30.91),
                       ('VAT (20% on \u00a3100.00) \u00a320.00', 20.00),
                       ('Sales tax (8.875% on US$1,000.00) US$88.75', 88.75),
                       ('Tax (19% on \u20ac210.00) \u20ac39.90', 39.90)):
        checked += 1
        got = m.tax_amount(line)
        if got is None or abs(got - want) > 0.005:
            bad.append(f'tax_amount returned {got} for {line!r}, wanted {want}')
    # and it must refuse a figure larger than the net it is told about
    checked += 1
    if m.tax_amount('GST - Australia (10% on A$309.09) A$30.91', net_hint=10.0) is not None:
        bad.append('tax_amount returned a tax larger than the net it was given')

    print(f"[vouch-patterns] assertions={checked} · failures={len(bad)}")
    for b in bad:
        print('   ', b)
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())

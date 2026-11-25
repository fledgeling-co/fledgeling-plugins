#!/usr/bin/env python3
"""Source a real US-listed client's figures, filing dates and holders from SEC EDGAR, so nothing on screen is invented.

    edgar.py cik ACME                                  # ticker to CIK, from SEC's company_tickers.json
    edgar.py filings ACME --forms 8-K,10-Q --limit 12  # newest filings: date, form, accession, document, 8-K items
    edgar.py release ACME <accession> -o q2-release.txt   # an 8-K's Exhibit 99.1 as plain text
    edgar.py holders ACME                              # Schedule 13G / 13G/A filings: holder, shares, percent, dates
    edgar.py --self-test

SEC asks every automated client to identify itself. The User-Agent comes from SEC_USER_AGENT; set it to a name and
a contact address the project is happy to send, never a person's private email without their say-so. Requests are
spaced 0.15 s apart, under SEC's 10-a-second limit.

`holders` reads the XML cover page of each Schedule 13G and 13G/A filed since SEC's 2024 format change, which names
the reporting person, the shares and the percent of class. Older text filings are listed with their dates and left
for you to read, because their layouts vary too much to parse reliably. A holder whose newest filing reports 0 shares
has usually moved its reporting to an affiliate (an index-fund manager to an affiliated adviser in 2026, for one), and
that is exactly the stale-ownership case a demo can show from real filings.
"""
import argparse
import html
import json
import os
import re
import sys
import time
import urllib.request

UA = os.environ.get('SEC_USER_AGENT', '')


def _ua():
    """SEC asks automated clients to name themselves with a contact; it answers 403 without one."""
    if '@' not in UA and 'http' not in UA:
        sys.exit('Set SEC_USER_AGENT to a name and a contact, e.g. "Example Research research@example.com". '
                 'SEC answers 403 without one. Use a generic contact rather than the user\'s own address unless they say so.')
    return UA
_last = [0.0]


def get(url):
    wait = 0.15 - (time.time() - _last[0])
    if wait > 0:
        time.sleep(wait)
    req = urllib.request.Request(url, headers={'User-Agent': _ua(), 'Accept-Encoding': 'identity'})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            _last[0] = time.time()
            return r.read().decode('utf-8', errors='replace')
    except urllib.error.HTTPError as e:
        sys.exit(f'SEC answered {e.code} for {url}' + (' (set SEC_USER_AGENT)' if e.code == 403 else ''))


def cik_of(t):
    if t.isdigit():
        return int(t)
    d = json.loads(get('https://www.sec.gov/files/company_tickers.json'))
    for row in d.values():
        if row['ticker'].upper() == t.upper():
            return int(row['cik_str'])
    sys.exit(f'no CIK for ticker {t}')


def recent(cik):
    d = json.loads(get(f'https://data.sec.gov/submissions/CIK{cik:010d}.json'))
    r = d['filings']['recent']
    rows = [{k: r[k][i] for k in ('filingDate', 'form', 'accessionNumber', 'primaryDocument', 'items')} for i in range(len(r['form']))]
    return d['name'], rows


def to_text(page):
    t = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', page, flags=re.S | re.I)
    t = re.sub(r'<br\s*/?>|</p>|</div>|</tr>', '\n', t, flags=re.I)
    t = html.unescape(re.sub(r'<[^>]+>', ' ', t))
    t = re.sub(r'[ \t\xa0]+', ' ', t)
    t = re.sub(r' *\n *', '\n', t)
    return re.sub(r'\n\s*\n+', '\n', t).strip()


def tag(xml, name):
    m = re.search(rf'<(?:\w+:)?{name}>(.*?)</(?:\w+:)?{name}>', xml, re.S)
    return m.group(1).strip() if m else ''


def parse_13g(xml):
    """(holder, shares, percent, event date) from a Schedule 13G XML cover page."""
    names = re.findall(r'<(?:\w+:)?reportingPersonName>(.*?)</', xml, re.S)
    shares = tag(xml, 'aggregateAmountOwned') or tag(xml, 'reportingPersonBeneficiallyOwnedAggregateNumberOfShares')
    pct = tag(xml, 'classPercent') or tag(xml, 'percentOfClass')
    event = tag(xml, 'dateOfEvent') or tag(xml, 'eventDateRequiresFilingThisStatement')
    return (html.unescape(names[0]).strip() if names else '?', shares, pct, event)


def cmd_holders(cik):
    name, rows = recent(cik)
    print(f'{name}: Schedule 13G filings, newest first')
    for r in rows:
        if '13G' not in r['form']:
            continue
        acc = r['accessionNumber'].replace('-', '')
        base = f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/'
        if r['primaryDocument'].endswith('.xml'):
            holder, shares, pct, event = parse_13g(get(base + 'primary_doc.xml'))
            print(f"  {r['filingDate']}  {r['form']:<15} {holder:<34} {shares:>14} shares  {pct:>6}%  event {event}  {r['accessionNumber']}")
        else:
            print(f"  {r['filingDate']}  {r['form']:<15} (text filing, read {base}{r['primaryDocument']})")


def cmd_release(cik, accession, out):
    acc = accession.replace('-', '')
    idx = json.loads(get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/index.json'))
    docs = [i['name'] for i in idx['directory']['item'] if re.search(r'ex-?99', i['name'], re.I) and i['name'].endswith(('.htm', '.html', '.txt'))]
    if not docs:
        sys.exit(f'no Exhibit 99 in {accession}: {[i["name"] for i in idx["directory"]["item"]]}')
    text = to_text(get(f'https://www.sec.gov/Archives/edgar/data/{cik}/{acc}/{docs[0]}'))
    if out:
        open(out, 'w').write(text)
    print(f'{docs[0]}: {len(text):,} characters' + (f' written to {out}' if out else ''))
    if not out:
        print(text[:3000])


def self_test():
    xml = ('<edgarSubmission><coverPageHeader><dateOfEvent>09/30/2026</dateOfEvent></coverPageHeader>'
           '<coverPageHeaderReportingPersonDetails><reportingPersonName>Example Advisers LLC</reportingPersonName>'
           '<reportingPersonBeneficiallyOwnedAggregateNumberOfShares>6122306</reportingPersonBeneficiallyOwnedAggregateNumberOfShares>'
           '<classPercent>5.8</classPercent></coverPageHeaderReportingPersonDetails></edgarSubmission>')
    page = '<html><style>x{}</style><p>Net revenue increased 6% to $1.2&nbsp;billion</p><div>Gross margin was 41.2%</div></html>'
    cases = [
        ('13G cover page parsed', parse_13g(xml), ('Example Advisers LLC', '6122306', '5.8', '09/30/2026')),
        ('release text unescaped and split', to_text(page), 'Net revenue increased 6% to $1.2 billion\nGross margin was 41.2%'),
        ('a missing tag is empty, not an error', tag(xml, 'nothingHere'), ''),
    ]
    failed = [n for n, got, want in cases if got != want]
    print(f'self-test: {len(cases) - len(failed)}/{len(cases)} passed' + (f'; failed: {", ".join(failed)}' if failed else ''))
    sys.exit(1 if failed else 0)


def main():
    if '--self-test' in sys.argv:
        self_test()
    ap = argparse.ArgumentParser(description=__doc__.split('\n\n')[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    sub.add_parser('cik').add_argument('ticker')
    p = sub.add_parser('filings')
    p.add_argument('ticker')
    p.add_argument('--forms', default='')
    p.add_argument('--limit', type=int, default=20)
    sub.add_parser('holders').add_argument('ticker')
    p = sub.add_parser('release')
    p.add_argument('ticker')
    p.add_argument('accession')
    p.add_argument('-o', '--out')
    a = ap.parse_args()
    cik = cik_of(a.ticker)
    if a.cmd == 'cik':
        print(cik)
    elif a.cmd == 'filings':
        name, rows = recent(cik)
        forms = {f.strip() for f in a.forms.split(',') if f.strip()}
        print(name)
        for r in [r for r in rows if not forms or r['form'] in forms][:a.limit]:
            print(f"  {r['filingDate']}  {r['form']:<10} {r['accessionNumber']}  {r['primaryDocument']}  {r['items']}")
    elif a.cmd == 'holders':
        cmd_holders(cik)
    else:
        cmd_release(cik, a.accession, a.out)


if __name__ == '__main__':
    main()

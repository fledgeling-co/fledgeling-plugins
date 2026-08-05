#!/usr/bin/env python3
"""Score a compaction summary against the transcript it replaced.

Exact string match only -- no model judgment -- so the number is reproducible,
free, and cannot flatter the summary that produced it.

Two modes:
  --transcript X --summary Y   score one summary
  --scan-history               measure real /compact events under ~/.claude/projects

The correction list is the output that matters. Bulk retention percentages are
context: pushing file-path retention toward 100% would mean pasting the transcript
back in, which is the failure this whole exercise exists to avoid.
"""
import argparse, glob, io, json, os, re, statistics, sys

PATH_RE = re.compile(r'(?:/[\w.\-]+){2,}\.\w{1,6}\b')
IDENT_RE = re.compile(r'`([A-Za-z_][\w./\-]{2,60})`')
# Keyword heuristic. Misses politely-phrased corrections, flags some non-corrections.
# A candidate list to read, never a count to report.
CORRECTION_RE = re.compile(
    r"\b(no,|not that|actually|wrong|incorrect|don'?t |stop |instead|i said|"
    r"that's not|revert|undo|you (?:mis|missed|forgot))", re.I)


def text_of(o):
    m = o.get('message') or {}
    c = m.get('content')
    if isinstance(c, str):
        return c
    out = []
    if isinstance(c, list):
        for b in c:
            if not isinstance(b, dict):
                continue
            t = b.get('type')
            if t == 'text':
                out.append(b.get('text') or '')
            elif t == 'tool_use':
                out.append(json.dumps(b.get('input') or {})[:4000])
            elif t == 'tool_result':
                cc = b.get('content')
                out.append(cc if isinstance(cc, str) else json.dumps(cc)[:4000])
    return '\n'.join(out)


def load(path):
    rows = []
    with io.open(path, encoding='utf-8', errors='replace') as fh:
        for line in fh:
            if len(line) > 4_000_000:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows


def extract(rows):
    """Pull the four retention classes out of a run of transcript rows."""
    paths, idents, umsgs, corrections = set(), set(), [], []
    for p in rows:
        if p.get('isCompactSummary'):
            continue          # never credit a prior summary's content as source material
        t = text_of(p)
        if not t:
            continue
        for m in PATH_RE.findall(t):
            if len(m) < 90:
                paths.add(m)
        idents.update(IDENT_RE.findall(t))
        if p.get('type') == 'user':
            c = (p.get('message') or {}).get('content')
            if isinstance(c, str) and c.strip() and not c.startswith('[{'):
                s = c.strip()
                umsgs.append(s)
                if CORRECTION_RE.search(s[:600]):
                    corrections.append(s)
    return paths, idents, umsgs, corrections


def retention(items, summary):
    items = list(items)
    if not items:
        return None, 0, []
    missing = [x for x in items if x not in summary]
    return (len(items) - len(missing)) / len(items), len(items), missing


def score_one(transcript, summary_text, show_missing=True):
    rows = load(transcript)
    cut = next((i for i, o in enumerate(rows) if o.get('isCompactSummary')), len(rows))
    paths, idents, umsgs, corrections = extract(rows[:cut])
    um_keys = [u[:60] for u in umsgs if len(u) > 25]
    cr_keys = [u[:60] for u in corrections if len(u) > 25]

    print(f'transcript rows before compaction: {cut:,}')
    print(f'summary: {len(summary_text):,} chars (~{len(summary_text)//3.6:,.0f} tokens)\n')

    out = {}
    for label, items in (('file paths', paths), ('identifiers', idents),
                         ('user messages', um_keys), ('CORRECTIONS', cr_keys)):
        r, n, missing = retention(items, summary_text)
        out[label] = dict(retention=r, n=n, missing=len(missing))
        if r is None:
            print(f'  {label:<16} none found in transcript')
        else:
            print(f'  {label:<16} {r*100:5.1f}%   ({n - len(missing)} of {n} kept)')

    _, _, missed_corr = retention(cr_keys, summary_text)
    if show_missing and missed_corr:
        print(f'\nCORRECTIONS NOT IN THE SUMMARY ({len(missed_corr)}):')
        print('Read these. Each one is something the next session may now repeat.\n')
        for m in missed_corr:
            print(f'  - {m.strip()[:160]}')
    elif not missed_corr and cr_keys:
        print('\nEvery detected correction appears in the summary.')
    return out


def scan_history(limit=None):
    files = glob.glob(os.path.expanduser('~/.claude/projects/*/*.jsonl'))
    sys.stderr.write(f'scanning {len(files)} transcripts\n')
    acc = {k: [] for k in ('file paths', 'identifiers', 'user messages', 'CORRECTIONS')}
    n_events = 0
    for f in files:
        try:
            rows = load(f)
        except Exception:
            continue
        for i, o in enumerate(rows):
            if not o.get('isCompactSummary'):
                continue
            summary = text_of(o)
            if len(summary) < 500 or i < 20:
                continue
            paths, idents, umsgs, corrections = extract(rows[:i])
            pairs = (('file paths', paths), ('identifiers', idents),
                     ('user messages', [u[:60] for u in umsgs if len(u) > 25]),
                     ('CORRECTIONS', [u[:60] for u in corrections if len(u) > 25]))
            for label, items in pairs:
                r, n, _ = retention(items, summary)
                if r is not None:
                    acc[label].append((r, n))
            n_events += 1
            if limit and n_events >= limit:
                break
        if limit and n_events >= limit:
            break

    print(f'\ncompaction events measured: {n_events}\n')
    print('RETENTION — fraction of pre-compaction items appearing verbatim in the summary')
    for label, vals in acc.items():
        if not vals:
            print(f'  {label:<16} no data'); continue
        r = [v for v, _ in vals]; n = [c for _, c in vals]
        print(f'  {label:<16} median {statistics.median(r)*100:5.1f}%   '
              f'mean {statistics.mean(r)*100:5.1f}%   '
              f'(n={len(r)}, median {statistics.median(n):,.0f} items each)')
    print('\nBulk classes are context. The CORRECTIONS row is the one that costs real work'
          '\nwhen it is low: a dropped correction is a mistake the next session repeats.')


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--transcript', help='session .jsonl the summary replaced')
    ap.add_argument('--summary', help='file holding the summary text')
    ap.add_argument('--scan-history', action='store_true',
                    help='measure real /compact events under ~/.claude/projects')
    ap.add_argument('--limit', type=int, help='stop after N events (with --scan-history)')
    a = ap.parse_args()

    if a.scan_history:
        scan_history(a.limit); return
    if not (a.transcript and a.summary):
        ap.error('need --transcript and --summary, or --scan-history')
    if not os.path.exists(a.transcript):
        ap.error(f'no such transcript: {a.transcript}')
    if not os.path.exists(a.summary):
        ap.error(f'no such summary: {a.summary}')
    score_one(a.transcript, io.open(a.summary, encoding='utf-8', errors='replace').read())


if __name__ == '__main__':
    main()

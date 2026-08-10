#!/usr/bin/env python3
"""Score a compaction summary against the transcript it replaced.

Exact string match only -- no model judgment -- so the number is reproducible,
free, and cannot flatter the summary that produced it.

Three modes:
  --transcript X --summary Y            score one summary
  --transcript X --summary Y --against Z  score two summaries of the same window,
                                        and print what each one pinned that the
                                        other dropped
  --scan-history                        measure real /compact events under
                                        ~/.claude/projects

The correction list is the output that matters. Bulk retention percentages are
context: pushing file-path retention toward 100% would mean pasting the transcript
back in, which is the failure this whole exercise exists to avoid.

TWO MATCHERS, BOTH REPORTED. `exact` is substring identity, which is the right test
for a path, an error string or an id -- a nearly-right one is worthless. `soft` is
distinctive-token overlap, which is the right test for a constraint or a rejected
approach, because a summary legitimately restates those in its own words while
keeping the reason intact.

Reporting exact alone understates the semantic classes badly enough to invert a
comparison. Measured on one paired case (`references/case-study-paired.md`): two
summaries that each carried 7-8 correctly-reasoned rejected approaches both scored
exact 0.0% over 49 detected spans. An instrument that scores a full pinned block
the same as an empty one cannot show whether pinning works.
"""
import argparse, glob, io, json, os, re, statistics, sys

PATH_RE = re.compile(r'(?:/[\w.\-]+){2,}\.\w{1,6}\b')
IDENT_RE = re.compile(r'`([A-Za-z_][\w./\-]{2,60})`')
# Keyword heuristic. Misses politely-phrased corrections, flags some non-corrections.
# A candidate list to read, never a count to report.
CORRECTION_RE = re.compile(
    r"\b(no,|not that|actually|wrong|incorrect|don'?t |stop |instead|i said|"
    r"that's not|revert|undo|you (?:mis|missed|forgot))", re.I)

# A correction does not have to come from the user. In a fleet or subagent run the
# most consequential one often arrives from a peer agent reporting that the parent
# got something wrong -- measured in the paired case study, where the single
# correction both summaries chose to pin was a runner's, and this scorer scored the
# whole class `n/a (0 of 0)` because it only read `type == "user"` rows.
# Tighter wording than CORRECTION_RE, because assistant text is voluminous and the
# loose pattern matches ordinary prose.
PEER_CORRECTION_RE = re.compile(
    r"(one correction|correction worth|that isn'?t right|that's not right|"
    r"i was wrong|you were wrong|to correct the record|retract|superseded by|"
    r"is not accurate|isn'?t accurate)", re.I)

# Harness furniture wrapped around user turns. Left in place, these dominate the
# leading characters of a message and collapse distinct instructions onto one key.
WRAPPER_RE = re.compile(
    r'<(command-message|command-name|command-args|command-stdout|command-contents|'
    r'local-command-caveat|system-reminder|user-prompt-submit-hook)>.*?'
    r'</\1>|<[^>]{1,40}/>', re.S)

STOPWORDS = frozenset(
    'a an and are as at be but by for from had has have if in into is it its of on '
    'or that the their then there these this to was were what when which who will '
    'with you your i we they them he she do does did not no so than too very can '
    'could would should may might must been being over under about after before '
    'again once here now also just only own same such other more most any each'.split())


def strip_wrappers(s):
    """Remove harness furniture so a user turn keys on what the user actually said."""
    return re.sub(r'\s+', ' ', WRAPPER_RE.sub(' ', s)).strip()


def user_key(s, n=60):
    """A distinctive key for a user message.

    Keying on the first n characters silently merges every message sharing a
    preamble. Measured: 26 user turns in one window collapsed onto 4 keys, 5 of them
    identical cron-heartbeat prefixes, and the one instruction both summaries quoted
    verbatim keyed as `<command-message>goal-harness:goal-harness</command-message>`
    and scored as dropped by both.

    So strip the furniture first, then key on the longest line, which is where the
    instruction lives when a wrapper or a preamble comes first.
    """
    stripped = strip_wrappers(s)
    lines = [ln.strip() for ln in re.split(r'[\n.]', stripped) if len(ln.strip()) > 25]
    return (max(lines, key=len) if lines else stripped)[:n]


def distinctive(span):
    """Content tokens of a span: what a faithful restatement has to keep."""
    toks = re.findall(r"[\w./\-']{2,}", span.lower())
    return [t for t in toks if t not in STOPWORDS and (len(t) > 3 or any(c.isdigit() for c in t))]


def soft_hit(span, summary_norm):
    """Did this span survive in substance -- same distinctive tokens, reason intact?

    Requires most content tokens present AND at least one long or non-alphabetic
    token, so a span made only of common words cannot match on stopword residue.
    """
    toks = distinctive(span)
    if len(toks) < 3:
        return span.lower() in summary_norm
    present = [t for t in toks if t in summary_norm]
    if len(present) / len(toks) < 0.6:
        return False
    return any(len(t) >= 6 or not t.isalpha() for t in present)


def normalise(s):
    return re.sub(r'\s+', ' ', re.sub(r'[`*_#>|]', ' ', s.lower()))


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
                if CORRECTION_RE.search(strip_wrappers(s)[:600]):
                    corrections.append(s)
        elif PEER_CORRECTION_RE.search(t[:3000]):
            # A peer agent or subagent correcting the record. Kept to the sentence
            # that carries it, so one long report does not become one giant span.
            for sent in re.split(r'(?<=[.!?])\s+', t[:3000]):
                if PEER_CORRECTION_RE.search(sent) and 25 < len(sent) < 400:
                    corrections.append(sent.strip())
    return paths, idents, umsgs, corrections


def retention(items, summary, soft=False):
    """Fraction of items the summary kept, plus the ones it did not.

    `soft=True` counts a span as kept when its distinctive tokens survive, which is
    what a faithful restatement of a constraint or a rejected approach looks like.
    Exact stays the default, and stays correct, for paths, ids and error strings.
    """
    items = list(dict.fromkeys(items))
    if not items:
        return None, 0, []
    if soft:
        norm = normalise(summary)
        missing = [x for x in items if not soft_hit(x, norm)]
    else:
        missing = [x for x in items if x not in summary]
    return (len(items) - len(missing)) / len(items), len(items), missing


def classes(rows, cut):
    """The four classes, keyed for scoring. One place, so compare mode agrees."""
    paths, idents, umsgs, corrections = extract(rows[:cut])
    return {
        'file paths': (sorted(paths), False),
        'identifiers': (sorted(idents), False),
        'user messages': ([user_key(u) for u in umsgs if len(u) > 25], True),
        'CORRECTIONS': ([user_key(u, 90) for u in corrections if len(u) > 25], True),
    }


def score_one(transcript, summary_text, show_missing=True):
    rows = load(transcript)
    cut = next((i for i, o in enumerate(rows) if o.get('isCompactSummary')), len(rows))
    cls = classes(rows, cut)

    print(f'transcript rows before compaction: {cut:,}')
    print(f'summary: {len(summary_text):,} chars (~{len(summary_text)//3.6:,.0f} tokens)\n')
    print(f'  {"class":<16} {"exact":>7}  {"soft":>7}   items')

    out = {}
    for label, (items, semantic) in cls.items():
        r, n, missing = retention(items, summary_text)
        rs = retention(items, summary_text, soft=True)[0] if semantic else None
        out[label] = dict(retention=r, soft=rs, n=n, missing=len(missing))
        if r is None:
            print(f'  {label:<16} none found in transcript')
        else:
            soft_col = f'{rs*100:6.1f}%' if rs is not None else '      -'
            print(f'  {label:<16} {r*100:6.1f}%  {soft_col}   ({n} found)')

    corr_items = cls['CORRECTIONS'][0]
    _, _, missed_corr = retention(corr_items, summary_text, soft=True)
    if show_missing and missed_corr:
        print(f'\nCORRECTIONS NOT IN THE SUMMARY ({len(missed_corr)} of {len(corr_items)}):')
        print('Read these. Each one is something the next session may now repeat.\n')
        for m in missed_corr:
            print(f'  - {m.strip()[:160]}')
    elif not missed_corr and corr_items:
        print('\nEvery detected correction appears in the summary.')
    return out


def compare(transcript, a_text, b_text, a_name, b_name):
    """Score two summaries of the same window and print what each one dropped.

    The disjoint sets are the output. Two summaries can score alike on every
    percentage and still pin almost non-overlapping material -- which is exactly
    what the paired case study found, and no per-summary score would have shown it.
    """
    rows = load(transcript)
    cut = len(rows)
    cls = classes(rows, cut)

    print(f'window: {cut:,} rows')
    print(f'  {a_name}: {len(a_text):,} chars')
    print(f'  {b_name}: {len(b_text):,} chars '
          f'({len(b_text)/max(1,len(a_text)):.2f}x)\n')
    print(f'  {"class":<16} {a_name[:11]:>11} {b_name[:11]:>11}   items')
    for label, (items, semantic) in cls.items():
        ra = retention(items, a_text, soft=semantic)
        rb = retention(items, b_text, soft=semantic)
        if ra[0] is None:
            continue
        print(f'  {label:<16} {ra[0]*100:10.1f}% {rb[0]*100:10.1f}%   ({ra[1]} found)')

    for label, (items, semantic) in cls.items():
        if not items:
            continue
        miss_a = set(retention(items, a_text, soft=semantic)[2])
        miss_b = set(retention(items, b_text, soft=semantic)[2])
        only_a = miss_b - miss_a          # a kept it, b dropped it
        only_b = miss_a - miss_b
        for owner, other, spans in ((a_name, b_name, only_a), (b_name, a_name, only_b)):
            if not spans:
                continue
            print(f'\n{label}: kept by {owner}, dropped by {other} ({len(spans)}):')
            for s in sorted(spans)[:12]:
                print(f'  - {s.strip()[:150]}')
            if len(spans) > 12:
                print(f'  ... and {len(spans) - 12} more')


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
            pairs = (('file paths', paths, False), ('identifiers', idents, False),
                     ('user messages', [user_key(u) for u in umsgs if len(u) > 25], True),
                     ('CORRECTIONS',
                      [user_key(u, 90) for u in corrections if len(u) > 25], True))
            for label, items, semantic in pairs:
                r, n, _ = retention(items, summary, soft=semantic)
                if r is not None:
                    acc[label].append((r, n))
            n_events += 1
            if limit and n_events >= limit:
                break
        if limit and n_events >= limit:
            break

    print(f'\ncompaction events measured: {n_events}\n')
    print('RETENTION — fraction of pre-compaction items the summary kept')
    print('(paths and identifiers by exact match; user messages and corrections by')
    print(' distinctive-token overlap, which credits a faithful restatement)')
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
    ap.add_argument('--against',
                    help='a second summary of the SAME window; switches to compare '
                         'mode and prints what each one pinned that the other dropped')
    ap.add_argument('--scan-history', action='store_true',
                    help='measure real /compact events under ~/.claude/projects')
    ap.add_argument('--limit', type=int, help='stop after N events (with --scan-history)')
    a = ap.parse_args()

    if a.scan_history:
        scan_history(a.limit); return
    if not (a.transcript and a.summary):
        ap.error('need --transcript and --summary, or --scan-history')
    for p in (a.transcript, a.summary, a.against):
        if p and not os.path.exists(p):
            ap.error(f'no such file: {p}')
    read = lambda p: io.open(p, encoding='utf-8', errors='replace').read()
    if a.against:
        compare(a.transcript, read(a.summary), read(a.against),
                os.path.basename(a.summary), os.path.basename(a.against))
    else:
        score_one(a.transcript, read(a.summary))


if __name__ == '__main__':
    main()

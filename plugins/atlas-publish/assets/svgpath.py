"""A minimal SVG path reader, used only by make_glyph.py.

potrace emits absolute M with relative m/c/l and z, and the Atlas mark comes
back as one connected outline plus its counters. To cut the letterform at the
A/t handover and normalise it back into the 1024 space, the path has to be
parsed rather than string-edited: subpaths after the first start with a
RELATIVE moveto, so their absolute position depends on every command before
them, and a naive split on "m" silently relocates them.

Handles M/m, C/c, L/l, H/h, V/v and Z/z, which is everything potrace produces.
Arcs and quadratics are not implemented, because nothing here emits them.
"""

import re
NUM = re.compile(r'[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?')

def parse(d):
    """Return list of subpaths; each is dict(start=(x,y), segs=[('C',p1,p2,p3)|('L',p)], closed=bool)."""
    toks = re.findall(r'[MmCcLlZzHhVv]|[-+]?(?:\d*\.\d+|\d+\.?)(?:[eE][-+]?\d+)?', d)
    i = 0; cur = (0.0, 0.0); start = (0.0, 0.0); subs = []; sub = None; cmd = None
    def num():
        nonlocal i
        v = float(toks[i]); i += 1; return v
    while i < len(toks):
        t = toks[i]
        if re.match(r'[A-Za-z]', t):
            cmd = t; i += 1
        if cmd in 'Mm':
            x, y = num(), num()
            if cmd == 'm': x, y = cur[0]+x, cur[1]+y
            cur = (x, y); start = cur
            sub = {'start': cur, 'segs': [], 'closed': False}; subs.append(sub)
            cmd = 'L' if cmd == 'M' else 'l'
        elif cmd in 'Cc':
            pts = [(num(), num()) for _ in range(3)]
            if cmd == 'c': pts = [(cur[0]+p[0], cur[1]+p[1]) for p in pts]
            sub['segs'].append(('C',)+tuple(pts)); cur = pts[2]
        elif cmd in 'Ll':
            x, y = num(), num()
            if cmd == 'l': x, y = cur[0]+x, cur[1]+y
            sub['segs'].append(('L', (x, y))); cur = (x, y)
        elif cmd in 'Hh':
            x = num()
            if cmd == 'h': x = cur[0]+x
            sub['segs'].append(('L', (x, cur[1]))); cur = (x, cur[1])
        elif cmd in 'Vv':
            y = num()
            if cmd == 'v': y = cur[1]+y
            sub['segs'].append(('L', (cur[0], y))); cur = (cur[0], y)
        elif cmd in 'Zz':
            sub['closed'] = True; cur = start; i += 0
        else:
            raise ValueError('cmd %r' % cmd)
    return subs

def xf(subs, a, b, c, dd, e, f):
    """affine (a,b,c,d,e,f) as in SVG matrix."""
    def T(p): return (a*p[0]+c*p[1]+e, b*p[0]+dd*p[1]+f)
    out = []
    for s in subs:
        out.append({'start': T(s['start']),
                    'segs': [(g[0],)+tuple(T(p) for p in g[1:]) for g in s['segs']],
                    'closed': s['closed']})
    return out

def emit(subs, prec=2):
    def n(v): return f'{v:.{prec}f}'.rstrip('0').rstrip('.')
    out = []
    for s in subs:
        out.append('M' + n(s['start'][0]) + ' ' + n(s['start'][1]))
        for g in s['segs']:
            if g[0] == 'C':
                out.append('C' + ' '.join(n(p[0])+' '+n(p[1]) for p in g[1:]))
            else:
                out.append('L' + n(g[1][0]) + ' ' + n(g[1][1]))
        if s['closed']: out.append('Z')
    return ''.join(out)

def bbox(subs, samples=24):
    xs = []; ys = []
    for s in subs:
        cur = s['start']; xs.append(cur[0]); ys.append(cur[1])
        for g in s['segs']:
            if g[0] == 'L':
                cur = g[1]; xs.append(cur[0]); ys.append(cur[1])
            else:
                p0, p1, p2, p3 = cur, g[1], g[2], g[3]
                for k in range(samples+1):
                    t = k/samples; u = 1-t
                    x = u*u*u*p0[0]+3*u*u*t*p1[0]+3*u*t*t*p2[0]+t*t*t*p3[0]
                    y = u*u*u*p0[1]+3*u*u*t*p1[1]+3*u*t*t*p2[1]+t*t*t*p3[1]
                    xs.append(x); ys.append(y)
                cur = p3
    return min(xs), min(ys), max(xs), max(ys)

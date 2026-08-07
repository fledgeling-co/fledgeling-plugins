"""Which geometry does C2's un-planed field actually have?

Three hypotheses, scored the same way: bin the plane's pixels by the candidate
coordinate, take the mean per bin, and report the residual sd of the pixels
about their own bin mean.  The coordinate that explains the field best wins.

  (a) linear ramp at angle theta      s = x cos(theta) + y sin(theta)
  (b) radial about a free centre      s = |(x,y) - (cx,cy)|
  (c) what we currently build         s = (x + y) / sqrt2      [= (a) at 45 deg]

Texture (grain, mottle, pitting) inflates every residual equally, so only the
differences between hypotheses carry information.
"""
import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2], a[..., 3]


def dil(m, r):
    o = m.copy()
    for dy in range(-r, r + 1, max(1, r // 6)):
        for dx in range(-r, r + 1, max(1, r // 6)):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


H = W = 1024
Y, X = np.mgrid[0:H, 0:W]


def rough_mask(g, a, fline):
    blk = dil(g < 0.45, 55)
    inner = (a > 0.95) & (X > 26) & (X < 998) & (Y > 26) & (Y < 998)
    return inner & (~blk) & (fline < -45)


def resid(mask, g, s, nb=40):
    lo, hi = s[mask].min(), s[mask].max()
    edges = np.linspace(lo, hi, nb + 1)
    idx = np.clip(np.digitize(s[mask], edges) - 1, 0, nb - 1)
    vals = g[mask]
    tot, n = 0.0, 0
    for b in range(nb):
        sel = idx == b
        if sel.sum() < 400:
            continue
        tot += ((vals[sel] - vals[sel].mean()) ** 2).sum()
        n += sel.sum()
    return math.sqrt(tot / n), n


for name, path, fline in (
        ('C2 reference', 'loop-runs/r07/reference-1024.png', Y - (-0.8026 * X + 991.2)),
        ('our master  ', 'loop-runs/r07/candidate-1024.png',
         Y - (604 - math.tan(math.radians(33.0)) * (X - 543)))):
    g, a = load(path)
    m = rough_mask(g, a, fline)
    print('== %s ==  n=%d' % (name, m.sum()))
    best = None
    for th in range(20, 76, 5):
        t = math.radians(th)
        r, n = resid(m, g, X * math.cos(t) + Y * math.sin(t))
        if best is None or r < best[0]:
            best = (r, th)
        print('   linear theta %2d deg   resid sd %.5f' % (th, r))
    print('   -> best linear: %d deg, sd %.5f' % (best[1], best[0]))
    bestr = None
    for cx in range(-700, 701, 100):
        for cy in range(-700, 301, 100):
            s = np.sqrt((X - cx) ** 2.0 + (Y - cy) ** 2.0)
            r, n = resid(m, g, s)
            if bestr is None or r < bestr[0]:
                bestr = (r, cx, cy)
    print('   -> best radial: centre (%d,%d), sd %.5f' % (bestr[1], bestr[2], bestr[0]))
    print()

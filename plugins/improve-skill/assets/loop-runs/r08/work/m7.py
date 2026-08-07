"""Does C2's TRUED plane sit on the same source, or is its geometry different?

Same residual-sd test as m5.py, on the trued side of each icon.  The finish gain
is out of reach this round (every reduction breaks the contrast floor), but the
plane's falloff GEOMETRY is a separate question and costs no contrast.
"""
import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]


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


def resid(mask, g, s, nb=30):
    lo, hi = s[mask].min(), s[mask].max()
    edges = np.linspace(lo, hi, nb + 1)
    idx = np.clip(np.digitize(s[mask], edges) - 1, 0, nb - 1)
    v = g[mask]
    tot = n = 0
    for b in range(nb):
        sel = idx == b
        if sel.sum() < 400:
            continue
        tot += ((v[sel] - v[sel].mean()) ** 2).sum()
        n += sel.sum()
    return math.sqrt(tot / n)


for name, path, fline in (
        ('C2 reference', 'loop-runs/r07/reference-1024.png', Y - (-0.8026 * X + 991.2)),
        ('our master  ', 'loop-runs/r07/candidate-1024.png',
         Y - (604 - math.tan(math.radians(33.0)) * (X - 543)))):
    g, a = load(path)
    m = (a > 0.95) & (X > 26) & (X < 998) & (Y > 26) & (Y < 998) & (~dil(g < 0.45, 55)) & (fline > 45)
    print('== %s trued ==  n=%d' % (name, m.sum()))
    for th in (30, 40, 45, 50, 60, 70, 80, 90):
        t = math.radians(th)
        print('   linear theta %2d  sd %.5f' % (th, resid(m, g, X * math.cos(t) + Y * math.sin(t))))
    b = None
    for cx in range(-300, 501, 50):
        for cy in range(-300, 301, 50):
            r = resid(m, g, np.sqrt((X - cx) ** 2.0 + (Y - cy) ** 2.0))
            if b is None or r < b[0]:
                b = (r, cx, cy)
    print('   radial about (%d,%d) sd %.5f' % (b[1], b[2], b[0]))
    R75 = np.sqrt((X - 75.0) ** 2 + (Y + 25.0) ** 2)
    print('   radial about the ROUGH source (75,-25) sd %.5f' % resid(m, g, R75))
    print('   profile about (75,-25):')
    for r0 in range(600, 1500, 100):
        s = m & (R75 >= r0) & (R75 < r0 + 100)
        if s.sum() < 400:
            continue
        print('      r %4d  L %.4f  n %6d' % (r0 + 50, g[s].mean(), s.sum()))
    print()

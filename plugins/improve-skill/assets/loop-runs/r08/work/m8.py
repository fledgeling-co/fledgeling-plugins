"""C2's un-planed field, with its translucent curl excluded.

The curl reads 0.85-0.95 against ground of 0.70-0.80 and sits at radii 150-500
from the fitted source, i.e. squarely inside the bins this round is authored
from.  Left in, it biases the near field UP and would have been copied into the
master's key bloom as if it were light.  Box taken off a 1.2x crop of the
reference (work/ref-curl-crop.png), not assumed.
"""
import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
CURLBOX = (X >= 178) & (X <= 492) & (Y >= 50) & (Y <= 414)


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA')).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2], a[..., 3], rgb


def dil(m, r):
    o = m.copy()
    for dy in range(-r, r + 1, max(1, r // 6)):
        for dx in range(-r, r + 1, max(1, r // 6)):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


def resid(mask, g, s, nb=40):
    lo, hi = s[mask].min(), s[mask].max()
    e = np.linspace(lo, hi, nb + 1)
    idx = np.clip(np.digitize(s[mask], e) - 1, 0, nb - 1)
    v = g[mask]
    tot = n = 0
    for b in range(nb):
        sel = idx == b
        if sel.sum() < 300:
            continue
        tot += ((v[sel] - v[sel].mean()) ** 2).sum()
        n += sel.sum()
    return math.sqrt(tot / n)


g, a, rgb = load('loop-runs/r07/reference-1024.png')
fline = Y - (-0.8026 * X + 991.2)
m = ((a > 0.95) & (X > 22) & (X < 1002) & (Y > 22) & (Y < 1002)
     & (~dil(g < 0.45, 55)) & (fline < -45) & (~CURLBOX))
print('n = %d  (was 187677 with the curl in)' % m.sum())

best = None
for th in range(25, 76, 5):
    t = math.radians(th)
    r = resid(m, g, X * math.cos(t) + Y * math.sin(t))
    if best is None or r < best[0]:
        best = (r, th)
print('best linear ramp: %d deg, sd %.5f' % (best[1], best[0]))
print('   our authored 45 deg:      sd %.5f' % resid(m, g, (X + Y) / math.sqrt(2)))
b = None
for cx in range(-200, 401, 25):
    for cy in range(-350, 201, 25):
        r = resid(m, g, np.sqrt((X - cx) ** 2.0 + (Y - cy) ** 2.0))
        if b is None or r < b[0]:
            b = (r, cx, cy)
print('best radial: centre (%d,%d), sd %.5f' % (b[1], b[2], b[0]))
CX, CY = b[1], b[2]
R = np.sqrt((X - CX) ** 2.0 + (Y - CY) ** 2.0)
print('\nC2 rough profile f(r) about (%d,%d), curl excluded:' % (CX, CY))
print('%6s %8s %8s   %s' % ('r', 'L', 'n', 'r,g,b'))
for r0 in list(range(20, 200, 30)) + list(range(200, 1120, 60)):
    w = 30 if r0 < 200 else 60
    s = m & (R >= r0) & (R < r0 + w)
    if s.sum() < 300:
        continue
    print('%6d %8.4f %8d   %.3f,%.3f,%.3f'
          % (r0 + w / 2, g[s].mean(), s.sum(),
             rgb[..., 0][s].mean(), rgb[..., 1][s].mean(), rgb[..., 2][s].mean()))

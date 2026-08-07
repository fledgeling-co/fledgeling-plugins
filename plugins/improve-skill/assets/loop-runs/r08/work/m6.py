"""Refine the source centre for C2's un-planed field and read off its f(r)."""
import math, numpy as np
from PIL import Image
NEUTRAL = 128 / 255.0
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]


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


g, a, rgb = load('loop-runs/r07/reference-1024.png')
fline = Y - (-0.8026 * X + 991.2)
m = (a > 0.95) & (X > 26) & (X < 998) & (Y > 26) & (Y < 998) & (~dil(g < 0.45, 55)) & (fline < -45)

best = None
for cx in range(-200, 401, 25):
    for cy in range(-300, 201, 25):
        r = resid(m, g, np.sqrt((X - cx) ** 2.0 + (Y - cy) ** 2.0))
        if best is None or r < best[0]:
            best = (r, cx, cy)
print('C2 rough field: best radial centre (%d,%d) sd %.5f' % (best[1], best[2], best[0]))
CX, CY = best[1], best[2]
R = np.sqrt((X - CX) ** 2.0 + (Y - CY) ** 2.0)
print('\nC2 rough profile f(r), radial about (%d,%d):' % (CX, CY))
print('%6s %8s %8s %10s %s' % ('r', 'L', 'n', 'sd', 'rgb'))
prof = []
for r0 in range(0, 1500, 60):
    sel = m & (R >= r0) & (R < r0 + 60)
    if sel.sum() < 400:
        continue
    L = g[sel].mean()
    prof.append((r0 + 30, L))
    print('%6d %8.4f %8d %10.4f  %.3f,%.3f,%.3f'
          % (r0 + 30, L, sel.sum(), g[sel].std(),
             rgb[..., 0][sel].mean(), rgb[..., 1][sel].mean(), rgb[..., 2][sel].mean()))
np.save('loop-runs/r08/work/ref_rough_profile.npy', np.array(prof))
print('\ncentre in normalised tile units: cx=%.4f cy=%.4f' % (CX / 1024.0, CY / 1024.0))

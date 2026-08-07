"""Shadow profile, with the cut boundary fitted in each image so the un-planed
plane cannot contaminate the trued-side bins, and with the profile split by
azimuth (down-right = shadow side, up-left = key side) as a control."""
import subprocess
import tempfile
import pathlib
import sys
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    c = a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size=1024):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


def shift(m, dy, dx):
    return np.roll(np.roll(m, dy, 0), dx, 1)


def mass_of(g):
    dark = g < 0.42
    er = dark.copy()
    for dy in (-2, 0, 2):
        for dx in (-2, 0, 2):
            er &= shift(dark, dy, dx)
    out = er.copy()
    for _ in range(2):
        d = out.copy()
        for dy in (-2, 0, 2):
            for dx in (-2, 0, 2):
                d |= shift(out, dy, dx)
        out = d & dark
    return out


def chamfer(mask):
    INF = 1e6
    d = np.where(mask, 0.0, INF)
    h, w = d.shape
    for rng, off in ((range(1, h), -1), (range(h - 2, -1, -1), +1)):
        for y in rng:
            row, nb = d[y], d[y + off]
            cand = np.minimum(nb + 3, np.minimum(
                np.concatenate(([INF], nb[:-1] + 4)),
                np.concatenate((nb[1:] + 4, [INF]))))
            np.minimum(row, cand, out=row)
            for x in range(1, w):
                if row[x - 1] + 3 < row[x]:
                    row[x] = row[x - 1] + 3
            for x in range(w - 2, -1, -1):
                if row[x + 1] + 3 < row[x]:
                    row[x] = row[x + 1] + 3
    return d / 3.0


def fit_cut(g, mass):
    """Line y = a + b x maximising the mean luminance step across it, ignoring the
    block. Coarse grid on slope and intercept; the cut is the only long straight
    step in either image."""
    h, w = g.shape
    y, x = np.mgrid[0:h, 0:w]
    ok = ~mass
    best = None
    for b in np.arange(-1.10, -0.40, 0.02):
        for a in np.arange(400, 1200, 8):
            resid = y - (a + b * x)
            up = ok & (resid > -80) & (resid < -20)
            dn = ok & (resid > 20) & (resid < 80)
            if up.sum() < 5000 or dn.sum() < 5000:
                continue
            step = abs(g[dn].mean() - g[up].mean())
            if best is None or step > best[0]:
                best = (step, a, b)
    return best


def run(name, im):
    g = lum(im)
    mass = mass_of(g)
    step, a, b = fit_cut(g, mass)
    d = chamfer(mass)
    h, w = g.shape
    y, x = np.mgrid[0:h, 0:w]
    trued = (y - (a + b * x)) > 12          # strictly below the fitted cut
    ys, xs = np.nonzero(mass)
    cy, cx = ys.mean(), xs.mean()
    az = np.arctan2(y - cy, x - cx)         # 0 = right, +pi/2 = down
    down_right = (az > -0.2) & (az < 1.9)
    band = (~mass) & trued & down_right & (d > 0)
    bins = [(0, 6), (6, 12), (12, 20), (20, 30), (30, 45), (45, 65),
            (65, 90), (90, 120), (120, 150), (150, 180), (180, 220)]
    vals, ns = [], []
    for lo, hi in bins:
        m = band & (d >= lo) & (d < hi)
        ns.append(int(m.sum()))
        vals.append(float(np.median(g[m])) if m.sum() > 60 else np.nan)
    far = vals[-1]
    print(f'--- {name}: mass {mass.sum()}px  cut y = {a:.0f} {b:+.2f}x (step {step:.3f}, '
          f'{np.degrees(np.arctan(-b)):.1f} deg)  far L {far:.3f}')
    print('    d px      ' + ' '.join(f'{lo:>3d}-{hi:<3d}' for lo, hi in bins))
    print('    n         ' + ' '.join(f'{v:7d}' for v in ns))
    print('    L         ' + ' '.join(f'{v:7.3f}' for v in vals))
    print('    / far     ' + ' '.join(f'{v/far:7.3f}' for v in vals))
    return vals


ref = Image.open('icon-engineC-f5665d-2.png').resize((1024, 1024), Image.LANCZOS)
for arg in (sys.argv[1:] or ['icon.svg']):
    run(arg, rsvg(arg))
run('reference', ref)

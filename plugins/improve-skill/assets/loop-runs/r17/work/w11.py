"""Shadow profile done cleanly: march perpendicular to each image's OWN hone line.

The hone is the contact line where the solid meets the ground, it is trivially
findable in both images (the only saturated red thing in either), and everything
perpendicular-and-down-right of it is trued plane in both images for 250px. So
this reads the shadow with no cut-fitting and no un-planed contamination.
Each profile is normalised by its own far field, which is what makes it survive
our trued plane running 0.22 brighter than C2's.
"""
import subprocess
import tempfile
import pathlib
import sys
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def comp(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    return a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])


def lum(c):
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size=1024):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


BINS = [(0, 8), (8, 16), (16, 26), (26, 40), (40, 60), (60, 85),
        (85, 115), (115, 150), (150, 190), (190, 235), (235, 285)]


def fit_hone(c):
    red = c[..., 0] - c[..., 1]
    m = red > 0.20
    ys, xs = np.nonzero(m)
    wt = red[m]
    mx, my = np.average(xs, weights=wt), np.average(ys, weights=wt)
    dx, dy = xs - mx, ys - my
    cov = np.array([[np.average(dx * dx, weights=wt), np.average(dx * dy, weights=wt)],
                    [np.average(dx * dy, weights=wt), np.average(dy * dy, weights=wt)]])
    w, v = np.linalg.eigh(cov)
    u = v[:, np.argmax(w)]                       # along the hone
    if u[0] < 0:
        u = -u
    n = np.array([-u[1], u[0]])                  # perpendicular
    if n[1] < 0:
        n = -n                                   # point DOWN, into the trued plane
    return (mx, my), u, n, m.sum(), float(np.hypot(dx, dy).max())


def run(name, im):
    c = comp(im)
    g = lum(c)
    (mx, my), u, n, npix, half = fit_hone(c)
    h, w = g.shape
    yy, xx = np.mgrid[0:h, 0:w]
    s = (xx - mx) * u[0] + (yy - my) * u[1]      # along the hone, 0 at its centre
    t = (xx - mx) * n[0] + (yy - my) * n[1]      # perpendicular, + into the trued plane
    inside = (np.abs(s) < half * 0.75) & (t > 0)
    print(f'--- {name}: hone {npix}px through ({mx:.0f},{my:.0f}) '
          f'bearing {np.degrees(np.arctan2(-u[1], u[0])):.1f} deg, half-length {half:.0f}')
    vals, ns = [], []
    for lo, hi in BINS:
        m = inside & (t >= lo) & (t < hi)
        ns.append(int(m.sum()))
        vals.append(float(np.median(g[m])) if m.sum() > 200 else np.nan)
    far = vals[-1]
    print('    t px      ' + ' '.join(f'{lo:>3d}-{hi:<3d}' for lo, hi in BINS))
    print('    n         ' + ' '.join(f'{v:7d}' for v in ns))
    print('    L         ' + ' '.join(f'{v:7.3f}' for v in vals))
    print('    / far     ' + ' '.join(f'{v/far:7.3f}' for v in vals))
    return [v / far for v in vals]


ref = Image.open('icon-engineC-f5665d-2.png').resize((1024, 1024), Image.LANCZOS)
out = {}
for arg in (sys.argv[1:] or ['icon.svg']):
    out[arg] = run(arg, rsvg(arg))
out['reference'] = run('reference', ref)
print('\n    normalised profiles, candidate(s) then reference:')
for k, v in out.items():
    print(f'    {k:34s} ' + ' '.join('  nan  ' if np.isnan(x) else f'{x:7.3f}' for x in v))

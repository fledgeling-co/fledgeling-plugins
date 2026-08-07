"""Palette-free view of the small-size error.

The trued plane runs ~+0.20 too bright and the block silhouette sits 1-2 cells
off: both are other edit classes and both dominate the raw residual. Subtract
each region's own median error and what remains is FEATURE error - the part a
small-size-repair round can actually own.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
B_LEFT, B_RIGHT, W = 957.0, 292.0, 1024.0


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    c = a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


ref = Image.open('icon-engineC-f5665d-2.png')

for s in (16, 32):
    lc, lr = lum(rsvg('icon.svg', s)), lum(ref.resize((s, s), Image.LANCZOS))
    d = lc - lr
    y, x = np.mgrid[0:s, 0:s]
    # canvas coords of cell centres
    cx, cy = (x + 0.5) * W / s, (y + 0.5) * W / s
    bnd = B_LEFT + (B_RIGHT - B_LEFT) * cx / W
    trued = cy > bnd
    dark = lc < 0.45          # the block, by value: it owns every dark pixel
    rim = (np.abs((x - (s - 1) / 2) / ((s - 1) / 2)) ** 5
           + np.abs((y - (s - 1) / 2) / ((s - 1) / 2)) ** 5) ** 0.2 > 0.86
    regions = {'trued ground': trued & ~dark & ~rim,
               'rough ground': ~trued & ~dark & ~rim,
               'block/dark': dark & ~rim,
               'rim band': rim}
    print(f'=== {s}px')
    for k, m in regions.items():
        print(f'    {k:14s} n={m.sum():4d} median err {np.median(d[m]):+.3f} '
              f'mean {d[m].mean():+.3f} sd {d[m].std():.3f} '
              f'p10 {np.percentile(d[m],10):+.3f} p90 {np.percentile(d[m],90):+.3f}')
    corr = d.copy()
    for m in regions.values():
        corr[m] -= np.median(d[m])
    print(f'    raw mean|d| {np.abs(d).mean():.4f} -> region-detrended {np.abs(corr).mean():.4f}')
    print('    detrended err x100 (feature error only):')
    for yy in range(s):
        print('    ' + ' '.join(f'{v*100:+4.0f}' for v in corr[yy]))

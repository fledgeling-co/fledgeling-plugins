"""The block's shadow, measured palette-invariantly in each image's own frame.

Each image's block is found by value (the dark mass), then ground luminance is
binned by chamfer distance from that mask on the trued side and normalised by the
same image's far field (d 170-200px). Normalising each image by its own far field
is what makes the comparison survive our trued plane running 0.22 brighter than
C2's: it reads the SHADOW, not the palette.
"""
import subprocess
import tempfile
import pathlib
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


def chamfer(mask, maxd=240):
    """Distance (in px, 3-4 chamfer / 3) from mask, two passes."""
    INF = 1e6
    d = np.where(mask, 0.0, INF)
    h, w = d.shape
    for y in range(1, h):
        row, prev = d[y], d[y - 1]
        cand = np.minimum(prev + 3, np.minimum(
            np.concatenate(([INF], prev[:-1] + 4)),
            np.concatenate((prev[1:] + 4, [INF]))))
        row[:] = np.minimum(row, cand)
        for x in range(1, w):  # left-to-right horizontal pass
            if row[x - 1] + 3 < row[x]:
                row[x] = row[x - 1] + 3
        for x in range(w - 2, -1, -1):
            if row[x + 1] + 3 < row[x]:
                row[x] = row[x + 1] + 3
    for y in range(h - 2, -1, -1):
        row, nxt = d[y], d[y + 1]
        cand = np.minimum(nxt + 3, np.minimum(
            np.concatenate(([INF], nxt[:-1] + 4)),
            np.concatenate((nxt[1:] + 4, [INF]))))
        row[:] = np.minimum(row, cand)
        for x in range(1, w):
            if row[x - 1] + 3 < row[x]:
                row[x] = row[x - 1] + 3
        for x in range(w - 2, -1, -1):
            if row[x + 1] + 3 < row[x]:
                row[x] = row[x + 1] + 3
    return d / 3.0


def profile(name, im):
    g = lum(im)
    dark = g < 0.42
    # keep only the big mass: drop stray dark pixels by a 3x3 majority erode/dilate
    def shift(m, dy, dx):
        return np.roll(np.roll(m, dy, 0), dx, 1)
    er = dark.copy()
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            er &= shift(dark, dy, dx)
    mass = er
    for _ in range(3):
        g2 = mass.copy()
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                g2 |= shift(mass, dy, dx)
        mass = g2 & dilate_ok(dark)
    d = chamfer(mass)
    ys, xs = np.nonzero(mass)
    # trued side = below-right of the block: use pixels whose nearest mass pixel
    # lies up-left, approximated by y greater than the mass centroid row
    cy = ys.mean()
    band = (~mass) & (d > 0) & (d < 210)
    lower = band & (np.mgrid[0:g.shape[0], 0:g.shape[1]][0] > cy)
    bins = [(0, 6), (6, 12), (12, 20), (20, 30), (30, 45), (45, 65),
            (65, 90), (90, 120), (120, 150), (150, 170), (170, 200)]
    vals = []
    for lo, hi in bins:
        m = lower & (d >= lo) & (d < hi)
        vals.append(np.median(g[m]) if m.sum() > 40 else np.nan)
    far = vals[-1]
    print(f'--- {name}: block mass {mass.sum()} px, centroid row {cy:.0f}, far field L {far:.3f}')
    print('    d px      ' + ' '.join(f'{lo:>3d}-{hi:<3d}' for lo, hi in bins))
    print('    L         ' + ' '.join(f'{v:7.3f}' for v in vals))
    print('    / far     ' + ' '.join(f'{v/far:7.3f}' for v in vals))
    return vals


def dilate_ok(m):
    return m | True


ref = Image.open('icon-engineC-f5665d-2.png').resize((1024, 1024), Image.LANCZOS)
profile('candidate', rsvg('icon.svg'))
profile('reference', ref)

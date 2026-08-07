"""Where do the 256px and 128px edge disagreements live? Density of FP and FN per
32x32 block of the 256px grid (i.e. eighths of the tile), so the region that owns
the loop's worst structural number is named rather than guessed."""
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


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


def sobel(g):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy)


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def blocks(m, k):
    s = m.shape[0] // k
    return m.reshape(k, s, k, s).sum((1, 3))


ref = Image.open('icon-engineC-f5665d-2.png')
for s in (256, 128):
    gc, gr = lum(rsvg('icon.svg', s)), lum(ref.resize((s, s), Image.LANCZOS))
    keep = ~rim_mask(s)
    ec, er = (sobel(gc) > 0.4) & keep, (sobel(gr) > 0.4) & keep
    fp, fn = ec & ~dilate(er), er & ~dilate(ec)
    k = 8
    print(f'=== {s}px  cand {ec.sum()} ref {er.sum()} FP {fp.sum()} FN {fn.sum()}')
    for name, m in (('cand edges', ec), ('ref edges', er), ('FP', fp), ('FN', fn)):
        b = blocks(m, k)
        print(f'  {name} per {s//k}x{s//k} block:')
        for row in b:
            print('    ' + ' '.join(f'{v:4d}' for v in row))

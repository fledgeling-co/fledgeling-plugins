"""The hone line at small size: does it stay red, or wash pale?

Fit each image's own hone independently (ridge of max R-G), then read its
cross-section at 1024 and at the natively-rendered small sizes. The hone is the
icon's signature and the only feature the rubric checks by name at 16px, so it
is the first thing to audit in a small-size-repair round.
"""
import subprocess
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def rgba(im):
    return np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0


def comp(im):
    a = rgba(im)
    return a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])


def lum(c):
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def sat(c):
    mx, mn = c.max(-1), c.min(-1)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


def report(name, im):
    c = comp(im)
    n = c.shape[0]
    redness = c[..., 0] - c[..., 1]
    print(f'--- {name} {n}px  redness max {redness.max():.4f} '
          f'mean {redness.mean():+.4f}  n>0.10 {(redness > 0.10).sum()}')
    # the hot core: pixels in the top decile of redness
    m = redness > max(0.10, np.percentile(redness, 99.5))
    if m.sum() == 0:
        print('    no hone pixels found')
        return
    ys, xs = np.nonzero(m)
    L, S = lum(c)[m], sat(c)[m]
    print(f'    core n={m.sum()} bbox x{xs.min()}-{xs.max()} y{ys.min()}-{ys.max()}  '
          f'L mean {L.mean():.3f} max {L.max():.3f}   sat mean {S.mean():.3f} max {S.max():.3f}')
    # brightest-redness pixel and its neighbours' colour
    y0, x0 = np.unravel_index(np.argmax(redness), redness.shape)
    print(f'    peak at ({y0},{x0}) rgb {c[y0,x0].round(3)} L {lum(c)[y0,x0]:.3f} sat {sat(c)[y0,x0]:.3f}')
    # how much of the icon is "warm and bright" (the hone read) vs "warm"
    print(f'    pixels redness>0.06: {(redness>0.06).sum()}   >0.15: {(redness>0.15).sum()}'
          f'   >0.25: {(redness>0.25).sum()}')


big_ref = Image.open('icon-engineC-f5665d-2.png')
for s in (1024, 32, 16):
    report('candidate', rsvg('icon.svg', s))
    report('reference', big_ref.resize((s, s), Image.LANCZOS))

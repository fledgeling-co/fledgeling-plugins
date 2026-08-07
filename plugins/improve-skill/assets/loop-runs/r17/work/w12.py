"""Which 32px cells does the shadow broadening ADD, and are they at the shadow?

w7 says the probes add 23 edge cells and 8 FPs at 32px with recall untouched, so
something is crossing the sobel threshold that did not before. This names the
cells, gives their canvas boxes, and reports each image's |grad| there, so the new
edges are attributed to a region rather than assumed to be the penumbra.
"""
import subprocess
import sys
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


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


S = 32
ref = Image.open('icon-engineC-f5665d-2.png')
gr = lum(ref.resize((S, S), Image.LANCZOS))
mr = sobel(gr)
keep = ~rim_mask(S)
base, probe = sys.argv[1], sys.argv[2]
ga, gb = lum(rsvg(base, S)), lum(rsvg(probe, S))
ma, mb = sobel(ga), sobel(gb)
ea, eb = (ma > 0.4) & keep, (mb > 0.4) & keep
new = eb & ~ea
lost = ea & ~eb
print(f'base {ea.sum()} probe {eb.sum()}  new {new.sum()} lost {lost.sum()}')
for label, m in (('NEW', new), ('LOST', lost)):
    ys, xs = np.nonzero(m)
    print(f'  {label} cells: cell(y,x) canvas box | base|g| probe|g| ref|g| | baseL probeL refL')
    for y, x in zip(ys, xs):
        print(f'    ({y:2d},{x:2d}) x{x*1024//S:4d}-{(x+1)*1024//S:4d} y{y*1024//S:4d}-{(y+1)*1024//S:4d} |'
              f' {ma[y,x]:5.2f} {mb[y,x]:5.2f} {mr[y,x]:5.2f} |'
              f' {ga[y,x]:5.3f} {gb[y,x]:5.3f} {gr[y,x]:5.3f}')

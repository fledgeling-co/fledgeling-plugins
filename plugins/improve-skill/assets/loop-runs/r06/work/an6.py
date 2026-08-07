"""Redo the reference's split line properly.

The first attempt fitted 'warm and bright' and caught the timber, which is also
warm and bright, and produced a line on the wrong diagonal. The hone is the only
strongly CHROMATIC thing in either image, so fit it on chroma alone.
"""
import numpy as np, pathlib, math
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


gr, cr = load(B / 'reference-1024.png')
gc, cc = load(B / 'candidate-1024.png')
chroma = cr[..., 0] - (cr[..., 1] + cr[..., 2]) / 2
print('ref chroma percentiles', {q: round(float(np.percentile(chroma, q)), 3)
                                 for q in (50, 90, 99, 99.5, 99.9)})
thr = np.percentile(chroma, 99.5)
m = chroma >= thr
ys, xs = np.nonzero(m)
print(f'hone pixels {m.sum()}  bbox x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}]')
k, b = np.polyfit(xs, ys, 1)
res = ys - (k * xs + b)
keep = np.abs(res) < 2.5 * res.std()
k, b = np.polyfit(xs[keep], ys[keep], 1)
print(f'ref hone: y = {k:.4f}x + {b:.1f}   angle {math.degrees(math.atan2(-k,1)):.2f} deg'
      f'   endpoints ({xs.min()},{k*xs.min()+b:.0f}) -> ({xs.max()},{k*xs.max()+b:.0f})'
      f'   residual sd {np.std(ys[keep]-(k*xs[keep]+b)):.1f}px')
np.save(B / 'honeline.npy', np.array([k, b]))

# the same for the candidate, as a check that the method agrees with known truth
chc = cc[..., 0] - (cc[..., 1] + cc[..., 2]) / 2
mc = chc >= np.percentile(chc, 99.5)
ys2, xs2 = np.nonzero(mc)
k2, b2 = np.polyfit(xs2, ys2, 1)
print(f'cand hone (same method): angle {math.degrees(math.atan2(-k2,1)):.2f} deg  '
      f'(build says 33.00) -- method check')

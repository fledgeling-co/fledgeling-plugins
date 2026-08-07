"""Where does the 32/16px error live? Per-cell signed and abs dL between candidate and
reference downsamples, printed as ASCII maps, plus the top offending cells."""
import numpy as np
from PIL import Image


def lum(im):
    a = np.asarray(im.convert('RGB'), dtype=np.float64) / 255.0
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


c = Image.open('loop-runs/r16/candidate-1024.png')
r = Image.open('loop-runs/r16/reference-1024.png')

for s in (16, 32):
    cl = lum(c.resize((s, s), Image.LANCZOS))
    rl = lum(r.resize((s, s), Image.LANCZOS))
    d = cl - rl
    print(f'=== {s}px  mean|dL| {np.abs(d).mean():.4f}  signed {d.mean():+.4f}  worst {np.abs(d).max():.4f}')
    print('signed dL x100 (positive = we are brighter):')
    for y in range(s):
        print(' '.join(f'{v*100:+4.0f}' for v in d[y]))
    idx = np.dstack(np.unravel_index(np.argsort(-np.abs(d).ravel()), d.shape))[0][:14]
    print('top cells (y,x, cand, ref, d):')
    for y, x in idx:
        print(f'  ({y:2d},{x:2d}) {cl[y,x]:.3f} {rl[y,x]:.3f} {d[y,x]:+.3f}')

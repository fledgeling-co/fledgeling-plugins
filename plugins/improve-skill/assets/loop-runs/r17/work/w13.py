"""Mask discipline check for the halo layer (rubric #1, non-negotiable).

A 105px blur pushed 58/66px down-right could pool against the squircle's lower
right rim and read as a baked corner shadow. This walks the rim band inward and
reports the luminance profile in each octant, before and after, so any new dark
crescent at the mask edge shows up as an octant that dropped much more than the
tile as a whole.
"""
import subprocess
import sys
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
N = 1024


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    c = a[..., :3] * a[..., 3:4] + NEUTRAL * (1 - a[..., 3:4])
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2], a[..., 3]


def rsvg(svg, size=N):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


y, x = np.mgrid[0:N, 0:N]
u = (x - (N - 1) / 2) / ((N - 1) / 2)
v = (y - (N - 1) / 2) / ((N - 1) / 2)
r = (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2          # 1.0 at the squircle edge
az = np.degrees(np.arctan2(v, u)) % 360
OCT = [('E', 337.5, 22.5), ('SE', 22.5, 67.5), ('S', 67.5, 112.5), ('SW', 112.5, 157.5),
       ('W', 157.5, 202.5), ('NW', 202.5, 247.5), ('N', 247.5, 292.5), ('NE', 292.5, 337.5)]
BANDS = [(0.97, 1.00), (0.93, 0.97), (0.88, 0.93), (0.80, 0.88), (0.60, 0.80)]

prof = {}
for svg in sys.argv[1:]:
    g, a = lum(rsvg(svg))
    inside = a > 0.5
    prof[svg] = {}
    for name, lo, hi in OCT:
        sect = ((az >= lo) | (az < hi)) if lo > hi else ((az >= lo) & (az < hi))
        prof[svg][name] = [float(np.median(g[inside & sect & (r >= b0) & (r < b1)]))
                           for b0, b1 in BANDS]
    prof[svg]['ALL'] = float(np.median(g[inside]))

names = list(prof)
print('band r:      ' + ' '.join(f'{b0:.2f}-{b1:.2f}' for b0, b1 in BANDS))
for svg in names:
    print(f'--- {pathlib.Path(svg).name}   whole-tile median {prof[svg]["ALL"]:.4f}')
    for name, _, _ in OCT:
        print(f'    {name:>3} ' + ' '.join(f'{v:9.4f}' for v in prof[svg][name]))
if len(names) == 2:
    a0, b0 = prof[names[0]], prof[names[1]]
    dall = b0['ALL'] - a0['ALL']
    print(f'\n--- delta (2nd minus 1st); whole-tile median {dall:+.4f}. A rim crescent would be'
          f'\n    an octant whose outermost band drops well past that, and past its own inner bands.')
    for name, _, _ in OCT:
        d = [b0[name][i] - a0[name][i] for i in range(len(BANDS))]
        flag = '  <-- rim-heavy' if d[0] < min(d[1:]) - 0.004 else ''
        print(f'    {name:>3} ' + ' '.join(f'{v:+9.4f}' for v in d) + flag)

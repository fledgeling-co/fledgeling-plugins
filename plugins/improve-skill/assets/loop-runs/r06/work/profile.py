"""r06: the trued ground's PROFILE in both images, not just its mean.

faces.py found our trued field 0.159 too bright over 39% of the canvas - the single
largest material error in the icon. It cannot be answered by darkening the field,
because our p90 lives there and the 32/16px self_contrast floor (the term that
rejected r05) is p90 - p10 on the candidate alone. So the question is which end is
wrong. If C2's trued plane runs from dark near the block to bright toward its key
and ours is a flat bright slab, the fix is RANGE - deepen the near end, hold the
peak - which lowers the mean, protects p90, and is a gradient/AO edit either way.

C2's cut is found by its own step rather than assumed, then both fields are read
along their own key axis so "near" and "far" mean the same thing in each image.
"""
import importlib.util
import math
import pathlib
import sys

import numpy as np
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
R = A / 'loop-runs/r04'
NEUTRAL = 128 / 255.


def load(p):
    a = np.asarray(Image.open(p).convert('RGBA'), dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


gc, gr = load(R / 'candidate-1024.png'), load(R / 'reference-1024.png')
y, x = np.mgrid[0:1024, 0:1024]

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)


def polymask(pts, n=1024):
    im = Image.new('L', (n, n), 0)
    ImageDraw.Draw(im).polygon([(float(px), float(py)) for px, py in pts], fill=255)
    return np.asarray(im) > 127


SOLID = polymask(bi.SILHOUETTE)
CURL = polymask(bi.SHAVING_SIL) if bi.SHAVING else np.zeros_like(SOLID)
GND_C = ~SOLID & ~CURL
BOUND_C = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * x / 1024.

# ---- C2's own cut: the offset that maximises the luminance step across a 38.93 deg line
SLOPE_R = -math.tan(math.radians(38.93))
DARK_R = gr < 0.45                       # C2's block and its shadow, by its own darkness
GND_R = ~DARK_R
best = None
for c0 in range(200, 1200, 2):
    line = SLOPE_R * x + c0
    band_a = GND_R & (line - y > 6) & (line - y < 40)
    band_b = GND_R & (y - line > 6) & (y - line < 40)
    if band_a.sum() < 4000 or band_b.sum() < 4000:
        continue
    step = gr[band_b].mean() - gr[band_a].mean()
    if best is None or step > best[0]:
        best = (step, c0)
step, C0 = best
BOUND_R = SLOPE_R * x + C0
print(f"C2's cut found at y = {SLOPE_R:.4f}x + {C0}  (step across it {step:+.3f})")

FIELDS = {
    'cand trued': (gc, GND_C & (y > BOUND_C)),
    'ref  trued': (gr, GND_R & (y > BOUND_R)),
    'cand rough': (gc, GND_C & (y <= BOUND_C)),
    'ref  rough': (gr, GND_R & (y <= BOUND_R)),
}
print(f'\n{"field":<12}{"area%":>7}{"mean":>7}{"p2":>7}{"p10":>7}{"p50":>7}{"p90":>7}{"p98":>7}{"range":>8}')
for nm, (g, m) in FIELDS.items():
    q = [np.percentile(g[m], p) for p in (2, 10, 50, 90, 98)]
    print(f'{nm:<12}{100*m.mean():7.2f}{g[m].mean():7.3f}' + ''.join(f'{v:7.3f}' for v in q)
          + f'{q[4]-q[0]:8.3f}')

# ---- along each image's own key axis. The key sits toward the upper right in both;
# distance is measured perpendicular to the cut, positive away from the blade.
print('\ntrued plane, perpendicular distance from its own cut (px), median L')
print(f'{"band":<12}{"cand":>8}{"ref":>8}{"c-r":>8}')
dc = (y - BOUND_C) / math.hypot(1, (bi.B_RIGHT - bi.B_LEFT) / 1024.)
dr = (y - BOUND_R) / math.hypot(1, SLOPE_R)
for a, b in ((0, 30), (30, 70), (70, 120), (120, 180), (180, 260), (260, 360), (360, 500)):
    mc = GND_C & (dc >= a) & (dc < b)
    mr = GND_R & (dr >= a) & (dr < b)
    if mc.sum() < 300 or mr.sum() < 300:
        continue
    vc, vr = np.median(gc[mc]), np.median(gr[mr])
    print(f'{f"{a}-{b}":<12}{vc:8.3f}{vr:8.3f}{vc-vr:+8.3f}')

# ---- and along the cut, to see whether the falloff toward the key is being carried
print('\ntrued plane, position ALONG the cut (0 = leading/left end), median L')
print(f'{"band":<12}{"cand":>8}{"ref":>8}{"c-r":>8}')
for a, b in ((0, 128), (128, 256), (256, 384), (384, 512), (512, 640), (640, 768), (768, 1024)):
    mc = GND_C & (y > BOUND_C) & (x >= a) & (x < b)
    mr = GND_R & (y > BOUND_R) & (x >= a) & (x < b)
    if mc.sum() < 300 or mr.sum() < 300:
        continue
    vc, vr = np.median(gc[mc]), np.median(gr[mr])
    print(f'{f"{a}-{b}":<12}{vc:8.3f}{vr:8.3f}{vc-vr:+8.3f}')

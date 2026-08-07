import math
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def load(p):
    im = Image.open(p).convert('RGBA')
    a = np.asarray(im).astype(np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    rgb = rgb * al + NEUTRAL * (1 - al)
    g = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    return rgb, g


crgb, gc = load('loop-runs/r06/candidate-1024.png')
rrgb, gr = load('loop-runs/r06/reference-1024.png')
H, W = gc.shape
Y, X = np.mgrid[0:H, 0:W]

# trued side = below each icon's own hone line, and outside its own block
ang = math.radians(33.0)
f_ours = Y - (604 - math.tan(ang) * (X - 543))
f_ref = Y - (-0.8026 * X + 991.2)

# block masks dilated a little so cast shadow near the block is excluded
blk_c = gc < 0.45
blk_r = gr < 0.45


def dilate(m, r):
    out = m.copy()
    for dy in range(-r, r + 1, max(1, r // 4)):
        for dx in range(-r, r + 1, max(1, r // 4)):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


bc = dilate(blk_c, 40)
br = dilate(blk_r, 40)

# alpha (the squircle) — use candidate alpha for both since ref is opaque square
alp = np.asarray(Image.open('loop-runs/r06/candidate-1024.png').convert('RGBA'))[..., 3] > 250
inner = alp & (X > 30) & (X < 994) & (Y > 30) & (Y < 994)

tru_c = inner & (f_ours > 30) & (~bc)
tru_r = inner & (f_ref > 30) & (~br)
rgh_c = inner & (f_ours < -30) & (~bc)
rgh_r = inner & (f_ref < -30) & (~br)

print('trued  ours %.3f  ref %.3f   |  rough ours %.3f ref %.3f'
      % (gc[tru_c].mean(), gr[tru_r].mean(), gc[rgh_c].mean(), gr[rgh_r].mean()))

# ---- spatial profile along distance from top-left corner (key light) ----
dist = np.sqrt(X ** 2 + Y ** 2)
print()
print('TRUED ground vs distance-from-top-left-corner (px)')
print('%8s %10s %10s %8s %8s' % ('bin', 'ours', 'ref', 'n_ours', 'n_ref'))
for lo in range(400, 1500, 100):
    hi = lo + 100
    mo = tru_c & (dist >= lo) & (dist < hi)
    mr = tru_r & (dist >= lo) & (dist < hi)
    if mo.sum() < 400 or mr.sum() < 400:
        continue
    print('%8d %10.3f %10.3f %8d %8d' % (lo, gc[mo].mean(), gr[mr].mean(), mo.sum(), mr.sum()))

print()
print('ROUGH ground vs distance-from-top-left-corner (px)')
for lo in range(0, 1200, 100):
    hi = lo + 100
    mo = rgh_c & (dist >= lo) & (dist < hi)
    mr = rgh_r & (dist >= lo) & (dist < hi)
    if mo.sum() < 400 or mr.sum() < 400:
        continue
    print('%8d %10.3f %10.3f %8d %8d' % (lo, gc[mo].mean(), gr[mr].mean(), mo.sum(), mr.sum()))

# ---- perpendicular distance below each hone line ----
n = 1.0 / math.sqrt(1 + math.tan(ang) ** 2)
perp_o = f_ours * n
nr = 1.0 / math.sqrt(1 + 0.8026 ** 2)
perp_r = f_ref * nr
print()
print('TRUED ground vs perpendicular depth below own hone line')
for lo in range(0, 700, 50):
    hi = lo + 50
    mo = tru_c & (perp_o >= lo) & (perp_o < hi)
    mr = tru_r & (perp_r >= lo) & (perp_r < hi)
    if mo.sum() < 400 or mr.sum() < 400:
        continue
    print('%8d %10.3f %10.3f %8d %8d' % (lo, gc[mo].mean(), gr[mr].mean(), mo.sum(), mr.sum()))

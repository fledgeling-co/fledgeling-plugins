"""Rubric checks on the real render: the single-light ordering predicate,
figure-ground against each plane, and the 16px read.
"""
import numpy as np
from PIL import Image
import sim3 as S

new = Image.open(S.A / 'icon.png').convert('RGBA')
gn = S.F.to_gray(new)
go = S.g0
gr = S.F.to_gray(Image.open(S.B / 'reference-1024.png').convert('RGBA'))
alpha = S.alpha

# ---- ordering predicate: brightest ground nearest the key ----
P, I = 110, 60
W = 1024
corners = {'TL': (I, I), 'TR': (W - I - P, I), 'BL': (I, W - I - P), 'BR': (W - I - P, W - I - P)}
print('corner patch L, as a multiple of each icon\'s own ground mean')
gmn = gn[alpha & (gn > 0.45)].mean()
gmo = go[alpha & (go > 0.45)].mean()
gmr = gr[gr > 0.45].mean()
print('ground mean: was %.3f  now %.3f  ref %.3f' % (gmo, gmn, gmr))
rows = {}
for k, (x, y) in corners.items():
    al = alpha[y:y + P, x:x + P]
    a_o = go[y:y + P, x:x + P][al].mean()
    a_n = gn[y:y + P, x:x + P][al].mean()
    b = gr[y:y + P, x:x + P].mean()
    rows[k] = a_n
    print('  %s  was %.3f (%.2fx)   now %.3f (%.2fx)   ref %.3f (%.2fx)'
          % (k, a_o, a_o / gmo, a_n, a_n / gmn, b, b / gmr))
print('  brightest corner now: %s   (key is TL)' % max(rows, key=rows.get))

# ---- figure-ground: the block against the ground it sits on ----
BLK = S.BLOCK & alpha
RING = (~S.BLOCK) & alpha
from numpy import roll  # noqa: E402
near = np.zeros_like(S.BLOCK)
for d in range(6, 90, 6):
    for ax in (0, 1):
        near |= roll(S.BLOCK, d, ax) | roll(S.BLOCK, -d, ax)
near &= RING


def lin(v):
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def ratio(gimg, blk, gnd):
    a, b = lin(gimg[blk]).mean(), lin(gimg[gnd]).mean()
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


for lbl, m in (('rough side', near & (S.LY > 0)), ('trued side', near & (S.LY <= 0))):
    print('figure-ground %s: was %.2f:1  now %.2f:1   (block L was %.3f now %.3f, '
          'local ground was %.3f now %.3f)'
          % (lbl, ratio(go, BLK, m), ratio(gn, BLK, m),
             go[BLK].mean(), gn[BLK].mean(), go[m].mean(), gn[m].mean()))

# ---- the 16px read ----
for size in (16, 32):
    a = S.F.to_gray(new.resize((size, size), Image.LANCZOS))
    b = S.F.to_gray(S.cand.resize((size, size), Image.LANCZOS))
    print('%2dpx  spread was %.3f now %.3f   dark-half mean was %.3f now %.3f   '
          'bright-half mean was %.3f now %.3f'
          % (size, b.max() - b.min(), a.max() - a.min(),
             b[b < np.median(b)].mean(), a[a < np.median(a)].mean(),
             b[b >= np.median(b)].mean(), a[a >= np.median(a)].mean()))

# vermilion footprint at 16px
for lbl, img in (('was', S.cand), ('now', new)):
    s = np.asarray(img.resize((16, 16), Image.LANCZOS).convert('RGB'), float)
    warm = (s[..., 0] - s[..., 2] > 40) & (s[..., 0] > 120)
    print('vermilion 16px footprint %s: %.2f%% of tile' % (lbl, 100 * warm.mean()))

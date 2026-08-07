import numpy as np, math
from PIL import Image

W = 1024
R = 'loop-runs/r04/'


def rgb(p):
    return np.asarray(Image.open(p).convert('RGB'), dtype=np.float64) / 255.0


def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def Lstar(a):
    y = 0.2126 * lin(a[..., 0]) + 0.7152 * lin(a[..., 1]) + 0.0722 * lin(a[..., 2])
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100, 903.3 * y / 100)


ra, ca = rgb(R + 'reference-1024.png'), rgb(R + 'candidate-1024.png')
RL, CL = Lstar(ra), Lstar(ca)
Y, X = np.mgrid[0:W, 0:W]
alpha = np.asarray(Image.open(R + 'candidate-1024.png').convert('RGBA'))[..., 3]
inside = alpha > 250


def frame(angle_deg, y0):
    a = math.radians(angle_deg)
    return -math.sin(a) * X - math.cos(a) * (Y - y0)


RV, CV = frame(39.59, 1007.85), frame(33.0, 956.6)
cand_obj = (X >= 120) & (X <= 830) & (Y >= 60) & (Y <= 800)
ref_obj = (X >= 100) & (X <= 830) & (Y >= 30) & (Y <= 700)


def hue(name, a, L, V, obj):
    print('===', name)
    for lo, hi, side in ((60, 340, 'un-planed near'), (340, 900, 'un-planed far'),
                         (-340, -60, 'trued near'), (-900, -340, 'trued far')):
        m = inside & (~obj) & (V >= min(lo, hi)) & (V < max(lo, hi))
        if m.sum() < 400:
            continue
        r, g, b = a[..., 0][m].mean(), a[..., 1][m].mean(), a[..., 2][m].mean()
        mx, mn = max(r, g, b), min(r, g, b)
        print('  %-16s rgb %.3f %.3f %.3f  hex #%02X%02X%02X  sat %.3f  L* %.3f'
              % (side, r, g, b, round(r * 255), round(g * 255), round(b * 255),
                 (mx - mn) / mx, L[m].mean()))


hue('REFERENCE', ra, RL, RV, ref_obj)
hue('CANDIDATE', ca, CL, CV, cand_obj)

# block body luminance (dark solid), both images
for nm, a, L in (('REF', ra, RL), ('CAND', ca, CL)):
    m = inside & (L < 0.45) & (X > 150) & (X < 830) & (Y > 100) & (Y < 720)
    print(nm, 'block px %d  median L* %.3f  mean rgb %.3f %.3f %.3f'
          % (m.sum(), np.median(L[m]), a[..., 0][m].mean(), a[..., 1][m].mean(), a[..., 2][m].mean()))

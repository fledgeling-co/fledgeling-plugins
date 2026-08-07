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


RL = Lstar(rgb(R + 'reference-1024.png'))
CL = Lstar(rgb(R + 'candidate-1024.png'))
gr = np.asarray(Image.open(R + 'reference-1024.png').convert('L'), float) / 255
gc = np.asarray(Image.open(R + 'candidate-1024.png').convert('L'), float) / 255
Y, X = np.mgrid[0:W, 0:W]
alpha = np.asarray(Image.open(R + 'candidate-1024.png').convert('RGBA'))[..., 3]
inside = alpha > 250
print('squircle interior = %.1f%% of tile' % (100 * inside.mean()))


def frame(angle_deg, y0):
    a = math.radians(angle_deg)
    nx, ny = -math.sin(a), -math.cos(a)
    return nx * X + ny * (Y - y0)


RV = frame(39.59, 1007.85)
CV = frame(33.0, 956.6)
cand_obj = (X >= 120) & (X <= 830) & (Y >= 60) & (Y <= 800)
ref_obj = (X >= 100) & (X <= 830) & (Y >= 30) & (Y <= 700)

d = np.abs(gc - gr)
print('lum_delta(1024) total %.4f' % d.mean())
regions = [
    ('outside squircle (corners)', ~inside),
    ('trued ground', inside & (CV < -60) & (~cand_obj)),
    ('un-planed ground', inside & (CV > 60) & (~cand_obj)),
    ('boundary band', inside & (np.abs(CV) <= 60) & (~cand_obj)),
    ('object box', inside & cand_obj),
]
for k, m in regions:
    print('  %-28s share %5.1f%%  mean|d| %.4f  contribution %.4f'
          % (k, 100 * m.mean(), d[m].mean(), (d * m).sum() / d.size))
print()

bands = [(60, 180, 'un-planed 60-180'), (180, 340, 'un-planed 180-340'),
         (340, 560, 'un-planed 340-560'), (560, 900, 'un-planed 560+'),
         (-180, -60, 'trued 60-180'), (-340, -180, 'trued 180-340'),
         (-560, -340, 'trued 340-560'), (-900, -560, 'trued 560+')]
for nm, L, V, obj in (('REF', RL, RV, ref_obj), ('CAND', CL, CV, cand_obj)):
    print('===', nm)
    for lo, hi, side in bands:
        m = inside & (~obj) & (V >= min(lo, hi)) & (V < max(lo, hi))
        if m.sum() < 400:
            print('  %-20s n=%d' % (side, m.sum()))
            continue
        print('  %-20s L* %.3f   n=%d' % (side, L[m].mean(), m.sum()))

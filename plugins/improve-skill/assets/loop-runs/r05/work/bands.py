import numpy as np, math, sys
from PIL import Image

W = 1024
cand = sys.argv[1] if len(sys.argv) > 1 else 'icon.png'


def rgb(p):
    im = Image.open(p).convert('RGBA').resize((W, W), Image.LANCZOS)
    a = np.asarray(im, float) / 255
    return a[..., :3], a[..., 3]


def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def Lstar(a):
    y = 0.2126 * lin(a[..., 0]) + 0.7152 * lin(a[..., 1]) + 0.0722 * lin(a[..., 2])
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100, 903.3 * y / 100)


ca, al = rgb(cand)
CL = Lstar(ca)
Y, X = np.mgrid[0:W, 0:W]
inside = al > 0.98
a = math.radians(33.0)
V = -math.sin(a) * X - math.cos(a) * (Y - 956.6)
obj = (X >= 120) & (X <= 830) & (Y >= 60) & (Y <= 800)

TARGET = {'un-planed 60-180': 0.620, 'un-planed 180-340': 0.678, 'un-planed 340-560': 0.750,
          'un-planed 560+': 0.855, 'trued 60-180': 0.855, 'trued 180-340': 0.840,
          'trued 340-560': 0.812}
REF = {'un-planed 60-180': 0.570, 'un-planed 180-340': 0.577, 'un-planed 340-560': 0.690,
       'un-planed 560+': 0.838, 'trued 60-180': 0.664, 'trued 180-340': 0.666,
       'trued 340-560': 0.626}
bands = [(60, 180, 'un-planed 60-180'), (180, 340, 'un-planed 180-340'),
         (340, 560, 'un-planed 340-560'), (560, 900, 'un-planed 560+'),
         (-180, -60, 'trued 60-180'), (-340, -180, 'trued 180-340'),
         (-560, -340, 'trued 340-560')]
print('band                  now    target   miss    ref    sat')
for lo, hi, nm in bands:
    m = inside & (~obj) & (V >= min(lo, hi)) & (V < max(lo, hi))
    r, g, b = ca[..., 0][m].mean(), ca[..., 1][m].mean(), ca[..., 2][m].mean()
    sat = (max(r, g, b) - min(r, g, b)) / max(r, g, b)
    L = CL[m].mean()
    print('%-20s %.3f  %.3f  %+.3f  %.3f  %.3f  #%02X%02X%02X'
          % (nm, L, TARGET[nm], L - TARGET[nm], REF[nm], sat, round(r*255), round(g*255), round(b*255)))

# ordering predicate: brightest ground vs the key corner
grd = inside & (~obj) & (np.abs(V) > 60)
tr = grd & (V < 0)
up = grd & (V > 0)
print()
print('brightest trued patch  L* %.3f' % np.percentile(CL[tr], 99.5))
print('brightest un-planed    L* %.3f' % np.percentile(CL[up], 99.5))
corner = inside & (X < 130) & (Y < 130)
print('top-left corner 130px  L* %.3f   (C2 corner 0.946)' % CL[corner].mean())

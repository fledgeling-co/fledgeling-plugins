import numpy as np, math
from PIL import Image

W = 1024
R = 'loop-runs/r04/'
ra = np.asarray(Image.open(R + 'reference-1024.png').convert('RGB'), float) / 255
Y, X = np.mgrid[0:W, 0:W]


def lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def Lstar(a):
    y = 0.2126 * lin(a[..., 0]) + 0.7152 * lin(a[..., 1]) + 0.0722 * lin(a[..., 2])
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100, 903.3 * y / 100)


RL = Lstar(ra)
a = math.radians(39.59)
V = -math.sin(a) * X - math.cos(a) * (Y - 1007.85)   # + = un-planed
U = math.cos(a) * X - math.sin(a) * (Y - 1007.85)    # along the split, up-right
obj = (X >= 100) & (X <= 830) & (Y >= 30) & (Y <= 700)

print('REFERENCE ground, banded by distance from the cut (+ = un-planed):')
edges = [-620, -500, -400, -300, -200, -100, -60, 60, 150, 250, 350, 450, 550, 650, 760]
for lo, hi in zip(edges[:-1], edges[1:]):
    if lo == -60:
        continue
    m = (~obj) & (V >= lo) & (V < hi)
    if m.sum() < 800:
        continue
    r, g, b = ra[..., 0][m].mean(), ra[..., 1][m].mean(), ra[..., 2][m].mean()
    print('  v %5d..%5d  L* %.3f  #%02X%02X%02X  sat %.3f  n=%6d'
          % (lo, hi, RL[m].mean(), round(r*255), round(g*255), round(b*255), (max(r,g,b)-min(r,g,b))/max(r,g,b), m.sum()))

print()
print('REFERENCE corner patches (60x60):')
for nm, x0, y0 in (('top-left', 10, 10), ('top-left+', 90, 90), ('top-right', 950, 10),
                   ('bottom-left', 10, 950), ('bottom-right', 950, 950), ('mid-right', 950, 500)):
    m = (X >= x0) & (X < x0+60) & (Y >= y0) & (Y < y0+60)
    r, g, b = ra[..., 0][m].mean(), ra[..., 1][m].mean(), ra[..., 2][m].mean()
    print('  %-12s L* %.3f  #%02X%02X%02X  sat %.3f' % (nm, RL[m].mean(), round(r*255), round(g*255), round(b*255), (max(r,g,b)-min(r,g,b))/max(r,g,b)))

"""r08 budget harness.

Same shape as loop-runs/r07/work/sim3.py: apply a proposed field transform to the
rendered 1024 PNG, recompute fidelity.py's own metrics at all five sizes plus
measure.py's polarity, and print the p90/p10 the gate's contrast floor reads.

Two transforms, both multiplicative so every hue survives untouched:

  rough_radial  swap the un-planed field's coordinate from u=(x+y)/sqrt2 to
                r=|(x,y)-(75,25)|, C2's own fitted source, carrying C2's own
                measured f(r).  Ratio is (new authored profile at r) / (current
                authored profile at u), i.e. exactly what changing the gradient
                element does to the base field, with every overlay riding on top.
  trued_gain    scale the trued plane by gnew/1.34.  The measured ours/C2 ratio
                is a flat 1.31-1.39 at every station along u, so the whole
                remaining trued error IS this one scalar.
"""
import math, sys, json, pathlib, importlib.util
import numpy as np
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r07'
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F  # noqa: E402

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec)
sys.modules['bi'] = bi
spec.loader.exec_module(bi)

H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
U = (X + Y) / math.sqrt(2.0)

CX, CY = 75.0, 25.0
R = np.sqrt((X - CX) ** 2.0 + (Y - CY) ** 2.0)

# the roughField stops as built today: (u, target L), from build_icon.py's own comments
OLD_U = np.array([0, 100, 180, 260, 340, 420, 500, 580, 680, 800, 940, 1500], float)
OLD_L = np.array([.888, .860, .791, .736, .677, .641, .601, .569, .571, .568, .568, .568])

# C2's measured f(r) about (75,25), curl excluded, from work/m8.py
REF_R = np.array([0, 35, 65, 95, 125, 155, 185, 230, 290, 350, 410, 470, 530,
                  590, 650, 710, 770, 830, 890, 1500], float)
REF_L = np.array([.940, .9166, .8915, .8651, .8412, .8152, .7845, .7521, .7179, .6813,
                  .6523, .6500, .6250, .6016, .5778, .5655, .5655, .5643, .5483, .5483])

# the truedField stops as built today: (u, target L), from build_icon.py's own comments
OLD_T_U = np.array([0, 660, 760, 860, 960, 1060, 1160, 1260, 1360, 1448, 2100], float)
OLD_T_L = np.array([.863, .863, .871, .869, .852, .848, .809, .747, .700, .683, .683])


def polymask(pts, grow=0):
    im = Image.new('L', (W, H), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255,
                               outline=255, width=max(1, grow))
    a = np.asarray(im) > 127
    if grow:
        out = a.copy()
        for dy in range(-grow, grow + 1, max(1, grow // 3)):
            for dx in range(-grow, grow + 1, max(1, grow // 3)):
                out |= np.roll(np.roll(a, dy, 0), dx, 1)
        a = out
    return a


cand = Image.open(B / 'candidate-1024.png').convert('RGBA')
arr0 = np.asarray(cand, dtype=np.float64) / 255.0

ang = math.radians(33.0)
UXa, UYa = math.cos(ang), -math.sin(ang)
NX, NY = -math.sin(ang), -math.cos(ang)
AX, AY = 543.0 - UXa * 320.0, 604.0 - UYa * 320.0
LY = NX * (X - AX) + NY * (Y - AY)          # >0 rough, <0 trued (measure.py sign)

BLOCK = polymask(bi.SILHOUETTE, grow=6)
CURL = polymask(bi.SHAVING_SIL, grow=14) if bi.SHAVING else np.zeros((H, W), bool)
HONE = np.abs(LY) < 34
alpha = np.asarray(cand)[..., 3] > 240
PAINTABLE = alpha & ~BLOCK & ~CURL & ~HONE
ROUGH = PAINTABLE & (LY > 0)
TRUED = PAINTABLE & (LY <= 0)


def apply(rough_radial=False, trued_gain=None, rough_gain=1.0, trued_radial=False):
    a = arr0.copy()
    ratio = np.ones((H, W))
    if rough_radial:
        rr = np.interp(R, REF_R, REF_L) / np.interp(U, OLD_U, OLD_L)
        ratio = np.where(ROUGH, rr * rough_gain, ratio)
    elif rough_gain != 1.0:
        ratio = np.where(ROUGH, rough_gain, ratio)
    tg = 1.0 if trued_gain is None else trued_gain / 1.34
    if trued_radial:
        tr = np.interp(R, OLD_T_U, OLD_T_L) / np.interp(U, OLD_T_U, OLD_T_L)
        ratio = np.where(TRUED, tr * tg, ratio)
    elif trued_gain is not None:
        ratio = np.where(TRUED, tg, ratio)
    for c in range(3):
        a[..., c] = np.clip(a[..., c] * ratio, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8))


def srgb_to_lin(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def lstar_img(img):
    a = np.asarray(img.convert('RGB'), float) / 255.0
    y = (0.2126 * srgb_to_lin(a[..., 0]) + 0.7152 * srgb_to_lin(a[..., 1])
         + 0.0722 * srgb_to_lin(a[..., 2]))
    return np.where(y > 0.008856, (116 * np.cbrt(y) - 16) / 100.0, 903.3 * y / 100.0)


BAND = np.abs(LY) >= 60


def polarity(img):
    L = lstar_img(img)
    rg = BAND & (LY > 0) & (L > 0.50)
    tr = BAND & (LY <= 0) & (L > 0.50)
    return L[tr].mean() - L[rg].mean(), L[rg].mean(), L[tr].mean()


def metrics(img):
    out = {}
    for size in F.SIZES:
        ci = img.resize((size, size), Image.LANCZOS) if size != 1024 else img
        ri = F.normalise_reference(B / 'reference-1024.png', size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': float(np.abs(gc - gr).mean()), 'ssim': F.ssim(gc, gr),
             'edge_f1': F.edge_f1(gc, gr), 'mask_iou': F.mask_iou(ci, ri),
             'p90': float(np.percentile(gc, 90)), 'p10': float(np.percentile(gc, 10))}
        m['self_contrast'] = m['p90'] - m['p10']
        m['composite'] = F.composite_for(size, m)
        out[size] = m
    return out


BASE = metrics(cand)
REAL = json.loads((B / 'score.json').read_text())['sizes']
FLOOR = {s: REAL[str(s)]['self_contrast'] * 0.94 for s in (32, 16)}
BIAS = {s: BASE[s]['self_contrast'] - REAL[str(s)]['self_contrast'] for s in (32, 16)}


def report(name, img):
    m = metrics(img)
    net = sum(m[s]['composite'] - BASE[s]['composite'] for s in F.SIZES)
    d, rg, tr = polarity(img)
    sc32 = m[32]['self_contrast'] - BIAS[32]
    sc16 = m[16]['self_contrast'] - BIAS[16]
    ok = sc32 >= FLOOR[32] and sc16 >= FLOOR[16]
    print('%-30s net %+.4f  ' % (name, net)
          + ' '.join('%d:%.4f' % (s, m[s]['composite']) for s in F.SIZES)
          + '  sc32 %.3f sc16 %.3f %s pol %+.3f lum %.4f ssim %.4f'
          % (sc32, sc16, 'ok   ' if ok else 'FLOOR', d, m[1024]['lum_delta'], m[1024]['ssim']))
    return m


if __name__ == '__main__':
    print('calibration: sim vs real')
    for s in F.SIZES:
        print('  %4d  composite %.4f / %.4f    self_contrast %.4f / %.4f'
              % (s, BASE[s]['composite'], REAL[str(s)]['composite'],
                 BASE[s]['self_contrast'], REAL[str(s)]['self_contrast']))
    print('floors (6%% below baseline): 32 %.3f  16 %.3f' % (FLOOR[32], FLOOR[16]))
    d, rg, tr = polarity(cand)
    print('baseline polarity %+.3f (rough %.3f trued %.3f)\n' % (d, rg, tr))

    report('rough -> radial only', apply(rough_radial=True))
    report('trued -> radial only', apply(trued_radial=True))
    report('both -> radial', apply(rough_radial=True, trued_radial=True))
    print()
    for g in (1.34, 1.28, 1.22, 1.16, 1.10, 1.04, 1.00):
        report('trued gain %.2f' % g, apply(trued_gain=g))
    print()
    for g in (1.28, 1.22, 1.16, 1.10, 1.04):
        report('radial + trued gain %.2f' % g, apply(rough_radial=True, trued_gain=g))

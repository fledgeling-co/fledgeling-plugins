"""Build a patched variant of build_icon.py in a temp dir and score it at all 5 sizes.

Mirrors fidelity.py's metric stack exactly (numpy tier) so ablations can be compared
against the r01 baseline without re-running the full harness for every probe.
"""
import pathlib, shutil, subprocess, sys, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
NEUTRAL = 128


def build(patches, name):
    d = pathlib.Path(tempfile.mkdtemp(prefix='var_'))
    shutil.copy(A / 'squircle-path.txt', d / 'squircle-path.txt')
    src = (A / 'build_icon.py').read_text()
    for old, new in patches:
        if old not in src:
            raise SystemExit('PATCH NOT FOUND: ' + repr(old[:90]))
        src = src.replace(old, new, 1)
    (d / 'build_icon.py').write_text(src)
    subprocess.run([sys.executable, str(d / 'build_icon.py')], check=True, capture_output=True)
    out = A / 'loop-runs/r03' / (name + '.svg')
    shutil.copy(d / 'icon.svg', out)
    shutil.rmtree(d)
    return out


def rend(p, s):
    p = pathlib.Path(p)
    if p.suffix.lower() == '.svg':
        t = pathlib.Path(tempfile.mktemp(suffix='.png'))
        subprocess.run(['rsvg-convert', '-w', str(s), '-h', str(s), str(p), '-o', str(t)], check=True)
        im = Image.open(t).convert('RGBA')
        t.unlink()
        return im
    return Image.open(p).convert('RGBA').resize((s, s), Image.LANCZOS)


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def box_mean(x, w):
    pad = w // 2
    xp = np.pad(x, pad, mode='edge')
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[:x.shape[0], :x.shape[1]]


def ssim(a, b):
    w = max(3, min(11, a.shape[0] // 4) | 1)
    c1, c2 = 0.01 ** 2, 0.03 ** 2
    ma, mb = box_mean(a, w), box_mean(b, w)
    va = box_mean(a * a, w) - ma ** 2
    vb = box_mean(b * b, w) - mb ** 2
    cov = box_mean(a * b, w) - ma * mb
    s = ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma ** 2 + mb ** 2 + c1) * (va + vb + c2))
    return float(np.clip(s, -1, 1).mean())


def sob(g, th=0.10):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) > th * 4


def dil(m, r=1):
    o = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            o |= np.roll(np.roll(m, dy, 0), dx, 1)
    return o


def ef1(a, b):
    ea, eb = sob(a), sob(b)
    if not ea.any() and not eb.any():
        return 1.0
    prec = (ea & dil(eb)).sum() / max(ea.sum(), 1)
    rec = (eb & dil(ea)).sum() / max(eb.sum(), 1)
    return float(2 * prec * rec / max(prec + rec, 1e-9))


def miou(ca, cb):
    aa = np.asarray(ca)[..., 3] > 16
    ab = np.asarray(cb)[..., 3] > 16
    if ab.mean() > 0.99 and aa.mean() > 0.99:
        return None
    return float((aa & ab).sum() / max((aa | ab).sum(), 1))


REF = A / 'icon-engineC-f5665d-2.png'
_refcache = {}


def refi(s):
    if s not in _refcache:
        _refcache[s] = Image.open(REF).convert('RGBA').resize((s, s), Image.LANCZOS)
    return _refcache[s]


def comp(size, m):
    lum = 1 - min(m['lum_delta'] * 4, 1.0)
    if size >= 128:
        parts = [(0.40, m['ssim']), (0.35, lum), (0.25, m['edge_f1'])]
    else:
        parts = [(0.35, m['edge_f1']), (0.25, m['mask_iou']), (0.25, m['ssim']), (0.15, lum)]
    return round(sum(w * v for w, v in parts), 4)


def score(svg, sizes=(1024, 256, 128, 32, 16)):
    out = {}
    for s in sizes:
        ci, ri = rend(svg, s), refi(s)
        gc, gr = gray(ci), gray(ri)
        m = {'lum_delta': round(float(np.abs(gc - gr).mean()), 4),
             'ssim': round(ssim(gc, gr), 4),
             'edge_f1': round(ef1(gc, gr), 4),
             'mask_iou': miou(ci, ri),
             'self_contrast': round(float(np.percentile(gc, 90) - np.percentile(gc, 10)), 4)}
        if m['mask_iou'] is not None:
            m['mask_iou'] = round(m['mask_iou'], 4)
        m['composite'] = comp(s, m)
        out[s] = m
    return out


BASE = {1024: 0.3950, 256: 0.3869, 128: 0.3940, 32: 0.7098, 16: 0.7748}
BASE_SC = {32: 0.5415, 16: 0.5358}


def report(name, sc):
    net = 0.0
    print('--- ' + name)
    for s, m in sc.items():
        d = m['composite'] - BASE[s]
        net += d
        print('  %4d: comp %.4f (%+.4f)  ssim %.4f  ef1 %.4f  lum %.4f  sc %.4f'
              % (s, m['composite'], d, m['ssim'], m['edge_f1'], m['lum_delta'], m['self_contrast']))
    print('  net %+.4f' % net)
    for s in (32, 16):
        if s in sc and sc[s]['self_contrast'] < BASE_SC[s] * 0.94:
            print('  !! %dpx self_contrast floor breach' % s)
    return net

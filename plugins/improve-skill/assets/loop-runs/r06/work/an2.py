"""Where the contrast budget actually lives, and what the reference's trued
plane is doing that ours is not.

(a) 16px/32px p90 and p10 provenance, mapped back to the 1024 regions.
(b) The trued plane's profile in both images, measured perpendicular to the cut
    and as a function of distance from the block's contact line.
"""
import numpy as np, sys, pathlib, importlib.util
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
NEUTRAL = 128 / 255.


def load(p, n=1024):
    im = Image.open(p).convert('RGBA')
    if n != im.width:
        im = im.resize((n, n), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    comp = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * comp[..., 0] + 0.7152 * comp[..., 1] + 0.0722 * comp[..., 2], comp


spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, n=1024):
    im = Image.new('L', (n, n), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im) > 127


TOPM, FRONTM = polymask(bi.TOP), polymask(bi.FRONT_FACE)
SOLID, CURL = polymask(bi.SILHOUETTE), polymask(bi.SHAVING_SIL)
y, x = np.mgrid[0:1024, 0:1024]
BOUND = bi.B_LEFT + (bi.B_RIGHT - bi.B_LEFT) * x / 1024.
TRUED = (y > BOUND) & ~SOLID & ~CURL
ROUGH = (y <= BOUND) & ~SOLID & ~CURL
LABEL = np.zeros((1024, 1024), int)
for i, m in enumerate([TOPM & ~CURL, FRONTM & ~TOPM & ~CURL, CURL, TRUED, ROUGH], 1):
    LABEL[m & (LABEL == 0)] = i
NAMES = {0: 'other', 1: 'top face', 2: 'front face', 3: 'curl', 4: 'trued', 5: 'rough'}

print('=== (a) contrast-budget provenance ===')
for n in (16, 32):
    g, _ = load(B / 'candidate-1024.png', n)
    lab = np.asarray(Image.fromarray(LABEL.astype(np.uint8)).resize((n, n), Image.NEAREST))
    p90, p10 = np.percentile(g, 90), np.percentile(g, 10)
    hi, lo = g >= p90, g <= p10
    def brk(m):
        return ', '.join(f'{NAMES[k]} {100*(lab[m]==k).mean():.0f}%'
                         for k in sorted(set(lab[m].tolist())) if (lab[m] == k).mean() > 0.08)
    print(f'{n}px  self_contrast {p90-p10:.4f}  p90 {p90:.3f} [{brk(hi)}]  p10 {p10:.3f} [{brk(lo)}]')
    print(f'      floor {0.5534*0.94 if n==16 else 0.553*0.94:.4f};  p99 {np.percentile(g,99):.3f}'
          f'  p1 {np.percentile(g,1):.3f}')

print('\n=== (b) the trued plane, both images ===')
gc, cc = load(B / 'candidate-1024.png')
gr, cr = load(B / 'reference-1024.png')
for nm, g in (('cand', gc), ('ref ', gr)):
    v = g[TRUED]
    print(f'{nm} trued: mean {v.mean():.3f}  p5 {np.percentile(v,5):.3f}  p50 {np.percentile(v,50):.3f}'
          f'  p95 {np.percentile(v,95):.3f}  max {v.max():.3f}  spread(p95-p5) {np.percentile(v,95)-np.percentile(v,5):.3f}')
    v = g[ROUGH]
    print(f'{nm} rough: mean {v.mean():.3f}  p5 {np.percentile(v,5):.3f}  p50 {np.percentile(v,50):.3f}'
          f'  p95 {np.percentile(v,95):.3f}  spread {np.percentile(v,95)-np.percentile(v,5):.3f}')

# distance from the block's contact chain, on the trued side only
foot = np.array(bi.FOOT_LOWER)
print('\ndistance-from-contact profile on the trued ground (L, and ratio to the far field)')
yy, xx = np.mgrid[0:1024, 0:1024]
d = np.full((1024, 1024), 1e9)
for px, py in foot[::4]:
    d = np.minimum(d, np.hypot(xx - px, yy - py))
bins = [(0, 20), (20, 45), (45, 80), (80, 130), (130, 200), (200, 300), (300, 450)]
print(f'{"band":<12}{"cand":>8}{"ref":>8}{"c/far":>8}{"r/far":>8}')
cfar = np.median(gc[TRUED & (d > 400)]); rfar = np.median(gr[TRUED & (d > 400)])
for a, b in bins:
    m = TRUED & (d >= a) & (d < b)
    if m.sum() < 200:
        continue
    print(f'{f"{a}-{b}px":<12}{np.median(gc[m]):8.3f}{np.median(gr[m]):8.3f}'
          f'{np.median(gc[m])/cfar:8.3f}{np.median(gr[m])/rfar:8.3f}')
print(f'far field (>400px): cand {cfar:.3f}  ref {rfar:.3f}')
np.save(B / 'dist.npy', d)

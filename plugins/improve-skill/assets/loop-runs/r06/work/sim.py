"""Budget the edit before building it.

Applies the proposed top-face transform to the rendered 1024 candidate and
recomputes every gate metric, so the p90-p10 spread and the composite are known
before a constant moves. Uses fidelity.py's own metric functions; the only
approximation is that small sizes come from a LANCZOS downsample of the 1024
render rather than a native rsvg render, so the baseline row is printed both
ways as the calibration.
"""
import numpy as np, pathlib, sys, importlib.util, json
from PIL import Image, ImageDraw

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
B = A / 'loop-runs/r06/work/base'
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F

spec = importlib.util.spec_from_file_location('bi', A / 'build_icon.py')
bi = importlib.util.module_from_spec(spec); sys.modules['bi'] = bi; spec.loader.exec_module(bi)


def polymask(pts, nn=1024):
    im = Image.new('L', (nn, nn), 0)
    ImageDraw.Draw(im).polygon([(float(x), float(y)) for x, y in pts], fill=255)
    return np.asarray(im).astype(np.float64) / 255.


TOP = polymask(bi.TOP) * (1 - polymask(bi.SHAVING_SIL))
cand = Image.open(B / 'candidate-1024.png').convert('RGBA')
ref = Image.open(B / 'reference-1024.png').convert('RGBA')
arr0 = np.asarray(cand, dtype=np.float64) / 255.


def transform(target_mean, squash):
    """Scale the top face's RGB toward a target mean L, compressing its spread
    about that mean by `squash`. Multiplicative, so hue is preserved."""
    a = arr0.copy()
    g = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    m = TOP > 0.5
    cur = g[m].mean()
    newg = target_mean + (g - cur) * squash
    ratio = np.where(g > 1e-6, newg / np.maximum(g, 1e-6), 1.0)
    ratio = 1.0 + (ratio - 1.0) * TOP           # feather by the mask's coverage
    for c in range(3):
        a[..., c] = np.clip(a[..., c] * ratio, 0, 1)
    return Image.fromarray((a * 255).round().astype(np.uint8))


def metrics(img):
    out = {}
    for size in F.SIZES:
        ci = img.resize((size, size), Image.LANCZOS) if size != 1024 else img
        ri = F.normalise_reference(B / 'reference-1024.png', size)
        gc, gr = F.to_gray(ci), F.to_gray(ri)
        m = {'lum_delta': float(np.abs(gc - gr).mean()), 'ssim': F.ssim(gc, gr),
             'edge_f1': F.edge_f1(gc, gr), 'mask_iou': F.mask_iou(ci, ri),
             'self_contrast': float(np.percentile(gc, 90) - np.percentile(gc, 10))}
        m['composite'] = F.composite_for(size, m)
        out[size] = m
    return out


real = json.loads((B / 'score.json').read_text())['sizes']
print('calibration -- simulated baseline vs the harness\'s real render')
b = metrics(cand)
print(f'{"size":>6}{"sim comp":>10}{"real comp":>10}{"sim sc":>9}{"real sc":>9}')
for s in F.SIZES:
    print(f'{s:>6}{b[s]["composite"]:10.4f}{real[str(s)]["composite"]:10.4f}'
          f'{b[s]["self_contrast"]:9.4f}{real[str(s)]["self_contrast"]:9.4f}')

print('\nproposed top-face transforms (target mean L, spread squash)')
for tgt, sq in [(0.338, 1.0), (0.300, 0.85), (0.280, 0.80), (0.260, 0.75), (0.245, 0.70), (0.225, 0.70)]:
    m = metrics(transform(tgt, sq))
    net = sum(m[s]['composite'] - b[s]['composite'] for s in F.SIZES)
    sc = [m[s]['self_contrast'] for s in (32, 16)]
    floor = [real['32']['self_contrast'] * 0.94, real['16']['self_contrast'] * 0.94]
    ok = all(x >= f - (b[s]['self_contrast'] - real[str(s)]['self_contrast'])
             for x, f, s in zip(sc, floor, (32, 16)))
    print(f'  mean {tgt:.3f} squash {sq:.2f}: net {net:+.4f}  '
          + ' '.join(f'{s}:{m[s]["composite"]:.4f}' for s in F.SIZES)
          + f'   sc32 {sc[0]:.3f} sc16 {sc[1]:.3f}  lum1024 {m[1024]["lum_delta"]:.4f}'
          + f'  ssim1024 {m[1024]["ssim"]:.4f}')

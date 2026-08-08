"""Calibrate CURL_TRANSMIT against two measured targets, not against the composite.

Target A (material): the shaded outer face lands where C2's does -- curl-box
percentiles p5/p10/p25 against C2's 0.579 / 0.605 / 0.647.
Target B (small-size guard): the curl's silhouette must still clear the sobel
threshold at 16px, where its edges are what edge_f1 is reading.
"""
import subprocess, pathlib, re, shutil, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def render(svg, size, tag):
    t = OUT / f'.cal-{tag}-{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def ref(size):
    return Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA').resize((size, size), Image.LANCZOS)


def sobel_mag(g):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def build(tau):
    src = (A / 'build_icon.py').read_text()
    src = re.sub(r'CURL_TRANSMIT = [0-9.]+', f'CURL_TRANSMIT = {tau}', src, count=1)
    tmp = A / '_cal_build.py'
    tmp.write_text(src)
    subprocess.run(['python3', str(tmp)], cwd=str(A), check=True, stdout=subprocess.DEVNULL)
    dst = OUT / f'.cal-{tau}.svg'
    shutil.copy(A / 'icon.svg', dst)
    tmp.unlink()
    return dst


BOX = (150, 160, 430, 420)
REF_P = {'p5': 0.579, 'p10': 0.605, 'p25': 0.647, 'p50': 0.707, 'p90': 0.817}

gr16 = to_gray(ref(16))
mr16 = sobel_mag(gr16)
gr32 = to_gray(ref(32))
mr32 = sobel_mag(gr32)

print('C2 target percentiles: ' + ' '.join(f'{k} {v:.3f}' for k, v in REF_P.items()))
print('tau  |  p5    p10   p25   p50   p90  | 32px curl edges (ref 22) | 16px curl cells >0.10 (ref 14)')
for tau in (0.0, 0.25, 0.32, 0.38, 0.45):
    svg = build(tau)
    g = to_gray(render(svg, 1024, str(tau)))
    x0, y0, x1, y1 = BOX
    p = g[y0:y1, x0:x1]
    qs = [np.percentile(p, q) for q in (5, 10, 25, 50, 90)]
    g32 = to_gray(render(svg, 32, str(tau)))
    m32 = sobel_mag(g32)
    n32 = int((m32[4:13, 4:13] > 0.10).sum())
    g16 = to_gray(render(svg, 16, str(tau)))
    m16 = sobel_mag(g16)
    n16 = int((m16[2:6, 2:6] > 0.10).sum())
    print(f'{tau:4.2f} | ' + ' '.join(f'{v:.3f}' for v in qs) +
          f' | {n32:3d} | {n16:2d}   min-in-box {m16[2:6, 2:6].max():.3f}')

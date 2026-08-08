"""Calibrate CURL_BOUNCE against the measured targets.

Material target: the interior lands on C2's own interior, p5 0.579 / p10 0.605.
Small-size guard: the curl must keep enough silhouette gradient at 16px to hold
the edges that make edge_f1 1.0000 there (12 cells over 0.10 today, ref 14).
"""
import subprocess, pathlib, re, shutil, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128
BOX = (150, 160, 430, 420)


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def render(svg, size, tag):
    t = OUT / f'.b-{tag}-{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def sobel_mag(g):
    p = np.pad(g, 1, mode='edge')
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def build(b, tau=0.38):
    src = (A / 'build_icon.py').read_text()
    src = re.sub(r'CURL_BOUNCE = [0-9.]+', f'CURL_BOUNCE = {b}', src, count=1)
    src = re.sub(r'CURL_TRANSMIT = [0-9.]+', f'CURL_TRANSMIT = {tau}', src, count=1)
    tmp = A / '_cal2_build.py'
    tmp.write_text(src)
    subprocess.run(['python3', str(tmp)], cwd=str(A), check=True, stdout=subprocess.DEVNULL)
    dst = OUT / f'.b-{b}-{tau}.svg'
    shutil.copy(A / 'icon.svg', dst)
    tmp.unlink()
    return dst


print('C2 interior: p5 0.579  p10 0.605  p25 0.647  p50 0.707  p90 0.817')
print('bnce tau  |  p5    p10   p25   p50   p90  | 32px curl edges (ref 22) | 16px cells>0.10 (12 now) max|g|')
for b, tau in ((1.0, 0.0), (1.0, 0.38), (1.5, 0.38), (1.9, 0.38), (2.2, 0.38), (2.6, 0.38)):
    svg = build(b, tau)
    g = to_gray(render(svg, 1024, f'{b}-{tau}'))
    x0, y0, x1, y1 = BOX
    p = g[y0:y1, x0:x1]
    qs = [np.percentile(p, q) for q in (5, 10, 25, 50, 90)]
    m32 = sobel_mag(to_gray(render(svg, 32, f'{b}-{tau}')))
    m16 = sobel_mag(to_gray(render(svg, 16, f'{b}-{tau}')))
    n32 = int((m32[4:13, 4:13] > 0.10).sum())
    n16 = int((m16[2:6, 2:6] > 0.10).sum())
    print(f'{b:4.2f} {tau:4.2f} | ' + ' '.join(f'{v:.3f}' for v in qs) +
          f' | {n32:3d} | {n16:2d}  {m16[2:6, 2:6].max():.3f}')

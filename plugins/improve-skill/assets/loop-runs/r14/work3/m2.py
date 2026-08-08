"""Crop the curl region out of both images at 1024 and 256, and locate the
reference's ribbon by luminance so the comparison is on measured pixels."""
import subprocess, pathlib, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def render(svg, size, tag='c'):
    t = OUT / f'.{tag}{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def ref(size):
    return Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA').resize((size, size), Image.LANCZOS)


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


BOX = (120, 60, 640, 500)   # 1024 coords, covers both curls

if __name__ == '__main__':
    c = render(A / 'icon.svg', 1024)
    r = ref(1024)
    x0, y0, x1, y1 = BOX
    c.convert('RGB').crop(BOX).save(OUT / 'crop-cand-curl.png')
    r.convert('RGB').crop(BOX).save(OUT / 'crop-ref-curl.png')

    gc, gr = to_gray(c), to_gray(r)
    # column/row profile of the curl region for both
    print('--- row means (1024 coords), curl band x 200..430 ---')
    for y in range(120, 460, 20):
        print(f'y={y:4d}  cand {gc[y, 200:430].mean():.4f}  ref {gr[y, 200:430].mean():.4f} '
              f'| cand min {gc[y, 200:430].min():.4f} max {gc[y, 200:430].max():.4f} '
              f'| ref min {gr[y, 200:430].min():.4f} max {gr[y, 200:430].max():.4f}')

"""Horizontal transects across both curls at 1024, printed as numbers.

The question a transect answers that a crop cannot: how much of each ribbon's
contrast is carried by its rim and how much by its body, and how dark each
material actually gets against the ground right beside it.
"""
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


def transect(g, y, x0, x1, step=8):
    return ' '.join(f'{g[y, x]:.2f}' for x in range(x0, x1, step))


if __name__ == '__main__':
    gc = to_gray(render(A / 'icon.svg', 1024))
    gr = to_gray(ref(1024))
    print('x from 140 to 460 step 8')
    for y in (180, 220, 260, 300, 340):
        print(f'\ny={y}')
        print('  cand', transect(gc, y, 140, 460))
        print('  ref ', transect(gr, y, 140, 460))

    # saturation in shadow: darkest pixel of each curl region and its RGB
    ca = np.asarray(render(A / 'icon.svg', 1024).convert('RGB'), dtype=np.float64)
    ra = np.asarray(ref(1024).convert('RGB'), dtype=np.float64)
    for name, arr, g, box in (('cand', ca, gc, (150, 150, 450, 440)), ('ref', ra, gr, (170, 80, 470, 400))):
        x0, y0, x1, y1 = box
        sub = g[y0:y1, x0:x1]
        i = np.unravel_index(np.argmin(sub), sub.shape)
        px = arr[y0 + i[0], x0 + i[1]]
        mx = np.unravel_index(np.argmax(sub), sub.shape)
        pxm = arr[y0 + mx[0], x0 + mx[1]]
        print(f'\n{name} curl box darkest L {sub.min():.4f} rgb {px} at {(x0+i[1], y0+i[0])}'
              f' | brightest L {sub.max():.4f} rgb {pxm} at {(x0+mx[1], y0+mx[0])}')
        print(f'  {name} local ground (a clean patch): ', end='')
        if name == 'cand':
            print(f'{g[120:170, 600:700].mean():.4f}')
        else:
            print(f'{g[120:170, 600:700].mean():.4f}')

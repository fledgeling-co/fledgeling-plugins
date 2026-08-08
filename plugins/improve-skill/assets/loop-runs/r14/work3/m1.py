"""Measure the shaving curl's small-size behaviour in both images.

Q1: what does the curl cost / earn at each size? (control render, SHAVING=0)
Q2: what contrast does each image's curl carry against its own local ground,
    at 1024 down to 16?
"""
import subprocess, pathlib, os, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128
SIZES = (1024, 256, 128, 32, 16)


def render(svg, size, tag):
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


def stats(g, box, size):
    """box in 1024 coords -> scaled"""
    s = size / 1024.0
    x0, y0, x1, y1 = [int(round(v * s)) for v in box]
    p = g[y0:y1, x0:x1]
    return p


if __name__ == '__main__':
    # --- build the control (no shaving)
    env = dict(os.environ, SHAVING='0')
    subprocess.run(['python3', str(A / 'build_icon.py')], env=env, cwd=str(A), check=True,
                   stdout=subprocess.DEVNULL)
    (OUT / 'icon-noshaving.svg').write_bytes((A / 'icon.svg').read_bytes())
    subprocess.run(['python3', str(A / 'build_icon.py')], cwd=str(A), check=True, stdout=subprocess.DEVNULL)

    CURL = (200, 160, 430, 400)      # generous box round our curl, 1024 coords
    REFCURL = (230, 100, 560, 450)   # the reference ribbon, 1024 coords

    print('size | cand curl-box mean/sd | ref curl-box mean/sd | cand MAE-in-box')
    for s in SIZES:
        c = to_gray(render(A / 'icon.svg', s, 'c'))
        n = to_gray(render(OUT / 'icon-noshaving.svg', s, 'n'))
        r = to_gray(ref(s))
        pc, pn, pr = stats(c, CURL, s), stats(n, CURL, s), stats(r, REFCURL, s)
        d_with = np.abs(stats(c, CURL, s) - stats(r, CURL, s)).mean()
        d_without = np.abs(stats(n, CURL, s) - stats(r, CURL, s)).mean()
        print(f'{s:5d} | cand {pc.mean():.4f}/{pc.std():.4f} | noshav {pn.mean():.4f}/{pn.std():.4f} '
              f'| ref(its own curl) {pr.mean():.4f}/{pr.std():.4f} | MAE box with {d_with:.4f} without {d_without:.4f}')

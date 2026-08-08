import subprocess, pathlib, numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')
OUT = pathlib.Path(__file__).resolve().parent
NEUTRAL = 128


def render_cand(svg, size):
    t = OUT / f'.tmp{size}.png'
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), str(svg), '-o', str(t)], check=True)
    return Image.open(t).convert('RGBA')


def ref(size):
    im = Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGBA')
    return im.resize((size, size), Image.LANCZOS)


def to_gray(im):
    a = np.asarray(im, dtype=np.float64)
    al = a[..., 3:4] / 255.0
    rgb = a[..., :3] * al + NEUTRAL * (1 - al)
    return (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]) / 255.0


def up(im, f, name):
    im.convert('RGB').resize((im.width * f, im.height * f), Image.NEAREST).save(OUT / name)


if __name__ == '__main__':
    for s in (32, 16):
        c = render_cand(A / 'icon.svg', s)
        r = ref(s)
        up(c, 16, f'cand-{s}-x16.png')
        up(r, 16, f'ref-{s}-x16.png')
        gc, gr = to_gray(c), to_gray(r)
        d = np.abs(gc - gr)
        print(s, 'MAE', round(float(d.mean()), 4), 'max', round(float(d.max()), 3))
        Image.fromarray((d / max(d.max(), 1e-6) * 255).astype(np.uint8)).resize((s * 16, s * 16), Image.NEAREST).save(OUT / f'diff-{s}-x16.png')
    for s in (128, 256):
        c = render_cand(A / 'icon.svg', s)
        r = ref(s)
        c.convert('RGB').save(OUT / f'cand-{s}.png')
        r.convert('RGB').save(OUT / f'ref-{s}.png')

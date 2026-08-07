"""Print the 32px and 16px luminance field as a number grid, candidate beside reference."""
import subprocess, tempfile, pathlib, sys
import numpy as np
from PIL import Image

NEUTRAL = 128


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


def grid(g, x0, y0, x1, y1, label):
    print(label)
    print('     ' + ' '.join('%4d' % x for x in range(x0, x1)))
    for y in range(y0, y1):
        print('%3d: ' % y + ' '.join('%4.0f' % (g[y, x] * 100) for x in range(x0, x1)))


if __name__ == '__main__':
    cand = sys.argv[1] if len(sys.argv) > 1 else 'icon.svg'
    ref = 'icon-engineC-f5665d-2.png'
    s = 32
    gc, gr = gray(rend(cand, s)), gray(rend(ref, s))
    grid(gc, 2, 3, 18, 20, 'CANDIDATE 32px (L*100) curl+upper-left region')
    grid(gr, 2, 3, 18, 20, 'REFERENCE 32px (L*100) same window')

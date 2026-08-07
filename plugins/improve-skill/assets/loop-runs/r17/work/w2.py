"""Is the small-size render aliasing, or just small?

rsvg-convert renders the candidate natively at 16/32px (fidelity.py does not
downsample from 1024), so any per-shape AA / seam-leakage artifact shows up in
the scored pixels but NOT in a supersampled 1024->N downsample. Difference
between the two IS the aliasing, isolated.
"""
import subprocess
import sys
import tempfile
import pathlib
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0


def lum(im):
    a = np.asarray(im.convert('RGBA'), dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def rsvg(svg, size):
    t = pathlib.Path(tempfile.mkstemp(suffix='.png')[1])
    subprocess.run(['rsvg-convert', '-w', str(size), '-h', str(size), svg, '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA').copy()
    t.unlink()
    return im


svg = sys.argv[1] if len(sys.argv) > 1 else 'icon.svg'
big = rsvg(svg, 1024)
for s in (16, 32, 128):
    native = rsvg(svg, s)
    supers = big.resize((s, s), Image.LANCZOS)
    ln, ls = lum(native), lum(supers)
    d = ln - ls
    print(f'=== {s}px native rsvg vs 1024->{s} LANCZOS: mean|d| {np.abs(d).mean():.4f} '
          f'signed {d.mean():+.4f} worst {np.abs(d).max():.4f}')
    print(f'    native  p10 {np.percentile(ln,10):.4f} p90 {np.percentile(ln,90):.4f} spread {np.percentile(ln,90)-np.percentile(ln,10):.4f}')
    print(f'    supers  p10 {np.percentile(ls,10):.4f} p90 {np.percentile(ls,90):.4f} spread {np.percentile(ls,90)-np.percentile(ls,10):.4f}')
    if s <= 32:
        print('    signed d x100:')
        for y in range(s):
            print('    ' + ' '.join(f'{v*100:+4.0f}' for v in d[y]))

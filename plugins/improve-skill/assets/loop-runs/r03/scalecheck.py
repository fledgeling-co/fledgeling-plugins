"""Does the SVG render the same at 32px as the 1024 render does when downsampled?

rsvg-convert applies filters in user space at the requested raster scale; a filter
that behaves differently at 1/32 scale is a small-size defect the 1024 view cannot show.
"""
import subprocess, tempfile, pathlib, sys
import numpy as np
from PIL import Image


def rend(p, s):
    t = pathlib.Path(tempfile.mktemp(suffix='.png'))
    subprocess.run(['rsvg-convert', '-w', str(s), '-h', str(s), str(p), '-o', str(t)], check=True)
    im = Image.open(t).convert('RGBA')
    t.unlink()
    return im


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + 0.501961 * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


svg = sys.argv[1] if len(sys.argv) > 1 else 'icon.svg'
big = rend(svg, 1024)
for s in (256, 128, 32, 16):
    direct = gray(rend(svg, s))
    down = gray(big.resize((s, s), Image.LANCZOS))
    d = np.abs(direct - down)
    print('%4dpx  direct-vs-downsampled  meanΔ %.4f  maxΔ %.4f  mean L %.4f vs %.4f'
          % (s, d.mean(), d.max(), direct.mean(), down.mean()))
    if s == 32:
        print('   worst cells (y,x,direct,down):',
              ', '.join('(%d,%d,%.2f,%.2f)' % (y, x, direct[y, x], down[y, x])
                        for y, x in np.dstack(np.unravel_index(
                            np.argsort(d.ravel())[::-1][:8], d.shape))[0]))

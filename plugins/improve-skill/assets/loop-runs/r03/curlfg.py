"""The curl's own figure-ground ratio, measured rather than assumed.

Rendering with and without SHAVING gives the curl's exact footprint (the changed
pixels) and, in the no-curl render, the ground it covers. Compare the master's
curl-vs-its-own-ground ratio with the reference's curl-vs-its-own-ground ratio.
"""
import os, subprocess, sys, tempfile, pathlib, shutil
import numpy as np
from PIL import Image

A = pathlib.Path('/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets')


def build_variant(shaving, tag):
    d = pathlib.Path(tempfile.mkdtemp(prefix='sh_'))
    shutil.copy(A / 'squircle-path.txt', d / 'squircle-path.txt')
    shutil.copy(A / 'build_icon.py', d / 'build_icon.py')
    env = dict(os.environ, SHAVING=shaving)
    subprocess.run([sys.executable, str(d / 'build_icon.py')], check=True, capture_output=True, env=env)
    out = A / 'loop-runs/r03' / (tag + '.svg')
    shutil.copy(d / 'icon.svg', out)
    shutil.rmtree(d)
    return out


def rend(p, s):
    t = pathlib.Path(tempfile.mktemp(suffix='.png'))
    subprocess.run(['rsvg-convert', '-w', str(s), '-h', str(s), str(p), '-o', str(t)], check=True)
    im = np.asarray(Image.open(t).convert('RGBA'), dtype=np.float64) / 255.
    t.unlink()
    rgb, al = im[..., :3], im[..., 3:4]
    return rgb * al + 0.501961 * (1 - al)


def L(c):
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


with_curl = build_variant('1', 'with-curl')
no_curl = build_variant('0', 'no-curl')
a, b = rend(with_curl, 1024), rend(no_curl, 1024)
la, lb = L(a), L(b)
mask = np.abs(la - lb) > 0.02
print('curl footprint: %d px (%.2f%% of canvas)' % (mask.sum(), 100 * mask.mean()))
print('  curl mean L        %.3f  (min %.3f, p10 %.3f, p90 %.3f, max %.3f)'
      % (la[mask].mean(), la[mask].min(), np.percentile(la[mask], 10),
         np.percentile(la[mask], 90), la[mask].max()))
print('  ground it covers L %.3f' % lb[mask].mean())
print('  ratio ground:curl  %.2f:1' % (lb[mask].mean() / la[mask].mean()))
print('  internal range     %.2f:1' % (np.percentile(la[mask], 97) / max(np.percentile(la[mask], 3), 1e-6)))

ys, xs = np.where(mask)
print('  bbox x %d-%d y %d-%d' % (xs.min(), xs.max(), ys.min(), ys.max()))

# the reference's curl, sampled by hand-placed box inside its ribbon, and the
# ground immediately beside it
ref = np.asarray(Image.open(A / 'icon-engineC-f5665d-2.png').convert('RGB'), dtype=np.float64) / 255.
ref = np.asarray(Image.fromarray((ref * 255).astype(np.uint8)).resize((1024, 1024), Image.LANCZOS),
                 dtype=np.float64) / 255.
lr = L(ref)
for tag, x0, y0, x1, y1 in [('ref ribbon upper arc', 250, 100, 340, 150),
                            ('ref ribbon right band', 350, 180, 400, 260),
                            ('ref ribbon lower-left', 195, 230, 240, 300),
                            ('ref loop interior (ground)', 255, 200, 320, 260),
                            ('ref ground left of curl', 100, 200, 160, 280),
                            ('ref ground above curl', 250, 40, 330, 80),
                            ('ref ground below curl', 200, 400, 300, 450)]:
    p = lr[y0:y1, x0:x1]
    print('  %-28s L %.3f  sd %.3f' % (tag, p.mean(), p.std()))

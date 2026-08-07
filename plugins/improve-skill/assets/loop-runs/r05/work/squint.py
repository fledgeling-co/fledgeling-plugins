import numpy as np
from PIL import Image

# squint check: does the r05 ground actually read worse small, or is the
# self_contrast drop purely the trued field's own p90 coming down?
# before = r04 candidate, after = r05 candidate, ref = engineC-f5665d-2.

PAIRS = [('before', 'loop-runs/r04/candidate-1024.png'),
         ('after', 'loop-runs/r05/candidate-1024.png'),
         ('ref', 'loop-runs/r05/reference-1024.png')]
SIZES = (32, 16)
Z = 8

rows = []
for size in SIZES:
    strip = []
    for nm, p in PAIRS:
        im = Image.open(p).convert('RGBA').resize((size, size), Image.LANCZOS)
        strip.append(np.asarray(im.resize((size * Z, size * Z), Image.NEAREST)))
    h = max(s.shape[0] for s in strip)
    padded = [np.pad(s, ((0, h - s.shape[0]), (8, 8), (0, 0))) for s in strip]
    rows.append(np.concatenate(padded, axis=1))
w = max(r.shape[1] for r in rows)
rows = [np.pad(r, ((8, 8), (0, w - r.shape[1]), (0, 0))) for r in rows]
Image.fromarray(np.concatenate(rows, axis=0)).save('loop-runs/r05/work/squint.png')

# where does self_contrast live? p10 and p90 of each image's own gray, inside the tile.
print('        p10     p90    spread   (self_contrast is p90-p10)')
for nm, p in PAIRS:
    for size in SIZES:
        a = np.asarray(Image.open(p).convert('RGBA').resize((size, size), Image.LANCZOS), float) / 255
        g = np.asarray(Image.open(p).convert('L').resize((size, size), Image.LANCZOS), float) / 255
        lo, hi = np.percentile(g, 10), np.percentile(g, 90)
        print('%-7s %3dpx  %.3f  %.3f  %.3f' % (nm, size, lo, hi, hi - lo))

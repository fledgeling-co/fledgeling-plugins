"""Coarse luminance map of a region of the reference (or any 1024 image), in blocks."""
import sys
import numpy as np
from PIL import Image

p = sys.argv[1]
x0, y0, x1, y1, step = (int(v) for v in sys.argv[2:7])
im = Image.open(p).convert('RGB')
if im.size != (1024, 1024):
    im = im.resize((1024, 1024), Image.LANCZOS)
a = np.asarray(im, dtype=np.float64) / 255.
L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
print('     ' + ' '.join('%4d' % x for x in range(x0, x1, step)))
for y in range(y0, y1, step):
    print('%4d ' % y + ' '.join('%4.0f' % (L[y:y + step, x:x + step].mean() * 100)
                                for x in range(x0, x1, step)))

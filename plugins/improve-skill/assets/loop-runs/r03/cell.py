"""Map 32px cells back to 1024 canvas blocks and report the mean colour of each,
so a value seen in the small render can be traced to the geometry that made it."""
import sys
import numpy as np
from PIL import Image

img = np.asarray(Image.open(sys.argv[1]).convert('RGBA'), dtype=np.float64) / 255.
rgb, al = img[..., :3], img[..., 3:4]
c = rgb * al + 0.501961 * (1 - al)
Lm = 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]

for cell in sys.argv[2:]:
    r, col = (int(v) for v in cell.split(','))
    y0, y1, x0, x1 = r * 32, (r + 1) * 32, col * 32, (col + 1) * 32
    blk = c[y0:y1, x0:x1].reshape(-1, 3)
    lb = Lm[y0:y1, x0:x1]
    print('cell r%-3d c%-3d  canvas x%4d-%4d y%4d-%4d  L %.3f (min %.3f max %.3f)  rgb %.3f %.3f %.3f'
          % (r, col, x0, x1, y0, y1, lb.mean(), lb.min(), lb.max(),
             blk[:, 0].mean(), blk[:, 1].mean(), blk[:, 2].mean()))

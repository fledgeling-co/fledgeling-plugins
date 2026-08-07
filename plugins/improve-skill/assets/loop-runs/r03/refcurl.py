"""Reference curl percentiles and dark-end hue, over the ribbon's own area."""
import numpy as np
from PIL import Image

im = Image.open('icon-engineC-f5665d-2.png').convert('RGB')
if im.size != (1024, 1024):
    im = im.resize((1024, 1024), Image.LANCZOS)
a = np.asarray(im, dtype=np.float64) / 255.
L = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

# the curl's area, block excluded by staying left of / above the iron's silhouette
reg = np.zeros(L.shape, bool)
reg[80:330, 180:395] = True
yy, xx = np.mgrid[0:1024, 0:1024]
reg &= ~((xx > 340) & (yy > 270))          # keep clear of the block's corner
sub = L[reg]
print('reference curl area: n=%d' % sub.size)
for q in (1, 3, 10, 25, 50, 75, 90, 97, 99):
    print('  p%-3d %.3f' % (q, np.percentile(sub, q)))
print('  mean %.3f  min %.3f  max %.3f' % (sub.mean(), sub.min(), sub.max()))

dark = sub <= np.percentile(sub, 2)
px = a[reg][dark]
print('  darkest 2%% rgb %.3f %.3f %.3f  (R>G>B warm)' % tuple(px.mean(0)))

# the ground it sits on, immediately outside that area
gnd = np.zeros(L.shape, bool)
gnd[80:330, 60:170] = True
print('  ground beside it   L %.3f' % L[gnd].mean())

import math
import numpy as np
from PIL import Image
import sys
sys.path.insert(0, '/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts')
import fidelity as F  # noqa: E402

cand = Image.open('loop-runs/r06/candidate-1024.png').convert('RGBA')
ref = Image.open('loop-runs/r06/reference-1024.png').convert('RGBA')
gc, gr = F.to_gray(cand), F.to_gray(ref)
H = W = 1024
Y, X = np.mgrid[0:H, 0:W]
alpha = np.asarray(cand)[..., 3] > 240

# corner patches, inset far enough to clear the squircle
P = 110
corners = {'TL': (60, 60), 'TR': (W - 60 - P, 60), 'BL': (60, W - 60 - P), 'BR': (W - 60 - P, W - 60 - P)}
print('corner patch means (110px), and each as a fraction of its own icon\'s ground mean')
gm_c = gc[alpha & (gc > 0.45)].mean()
gm_r = gr[gr > 0.45].mean()
print('ground mean: ours %.3f  ref %.3f' % (gm_c, gm_r))
for k, (x, y) in corners.items():
    a = gc[y:y + P, x:x + P]
    b = gr[y:y + P, x:x + P]
    al = alpha[y:y + P, x:x + P]
    ov = a[al].mean() if al.sum() > 100 else float('nan')
    print('  %s  ours %.3f (%.2fx)   ref %.3f (%.2fx)   alpha-cover %.2f'
          % (k, ov, ov / gm_c, b.mean(), b.mean() / gm_r, al.mean()))

# how each corner compares with the same plane sampled mid-tile at the same side
print()
print('vignette check: corner value vs the same plane 250px inboard along the diagonal')
for k, (x, y) in corners.items():
    sx = 1 if x < 500 else -1
    sy = 1 if y < 500 else -1
    x2, y2 = x + sx * 230, y + sy * 230
    a1 = gc[y:y + P, x:x + P][alpha[y:y + P, x:x + P]].mean()
    a2 = gc[y2:y2 + P, x2:x2 + P].mean()
    b1 = gr[y:y + P, x:x + P].mean()
    b2 = gr[y2:y2 + P, x2:x2 + P].mean()
    print('  %s  ours %.3f/%.3f = %.3f    ref %.3f/%.3f = %.3f' % (k, a1, a2, a1 / a2, b1, b2, b1 / b2))

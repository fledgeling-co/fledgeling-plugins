import numpy as np, math
from PIL import Image

W = 1024
R = 'loop-runs/r04/'
gr = np.asarray(Image.open(R + 'reference-1024.png').convert('L'), float) / 255
gc = np.asarray(Image.open(R + 'candidate-1024.png').convert('L'), float) / 255
alpha = np.asarray(Image.open(R + 'candidate-1024.png').convert('RGBA'))[..., 3]
inside = alpha > 250
d = np.abs(gc - gr)
# block masks: dark pixels in each image
bc = inside & (gc < 0.42)
br = inside & (gr < 0.42)
both = bc & br
only_c = bc & ~br
only_r = br & ~bc
neither = inside & ~bc & ~br
print('block-in-both      share %5.1f%%  mean|d| %.4f  contrib %.4f' % (100*both.mean(), d[both].mean(), (d*both).sum()/d.size))
print('block only in cand share %5.1f%%  mean|d| %.4f  contrib %.4f' % (100*only_c.mean(), d[only_c].mean(), (d*only_c).sum()/d.size))
print('block only in ref  share %5.1f%%  mean|d| %.4f  contrib %.4f' % (100*only_r.mean(), d[only_r].mean(), (d*only_r).sum()/d.size))
print('ground in both     share %5.1f%%  mean|d| %.4f  contrib %.4f' % (100*neither.mean(), d[neither].mean(), (d*neither).sum()/d.size))
print('outside squircle   share %5.1f%%  mean|d| %.4f  contrib %.4f' % (100*(~inside).mean(), d[~inside].mean(), (d*~inside).sum()/d.size))
print()
print('mean gray on block-in-both: cand %.3f ref %.3f  (signed %+.3f)' % (gc[both].mean(), gr[both].mean(), (gc-gr)[both].mean()))
print('mean gray on ground-in-both: cand %.3f ref %.3f  (signed %+.3f)' % (gc[neither].mean(), gr[neither].mean(), (gc-gr)[neither].mean()))

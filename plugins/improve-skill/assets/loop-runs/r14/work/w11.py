import math
import numpy as np
from PIL import Image

lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
rd = lambda p, n=1024: np.asarray(Image.open(p).convert("RGB").resize((n, n), Image.LANCZOS)
                                  ).astype(np.float32) / 255.
new, old = rd("icon.png"), rd("loop-runs/r13/candidate-1024.png")

ANGLE = math.radians(33.0)
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)
AX = 543.0 - UX * 320.0
AY = 604.0 - UY * 320.0
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)
LY = NX * (X - AX) + NY * (Y - AY)

for nm, im in (("r13", old), ("r14", new)):
    L = lum(im)
    on = L > .02
    blk = on & (L < .40)                       # the block reads dark
    up = on & (LY > 60) & (L >= .40)
    tr = on & (LY < -60) & (L >= .40)
    chr_ = (im.max(-1) - im.min(-1)) / np.maximum(im.max(-1), 1e-6)
    verm = on & (chr_ > .20)
    print(f"{nm}: block med {np.median(L[blk]):.3f}  un-planed {L[up].mean():.3f} "
          f"trued {L[tr].mean():.3f}   f/g un-planed {L[up].mean()/np.median(L[blk]):.2f}:1 "
          f"trued {L[tr].mean()/np.median(L[blk]):.2f}:1   vermilion {100*verm.mean():.2f}%")

for n in (32, 16):
    a = rd("icon.png", n)
    b = rd("loop-runs/r13/candidate-1024.png", n)
    La, Lb = lum(a), lum(b)
    d = np.abs(La - Lb)
    print(f"{n}px: max |dL| {d.max():.4f}  mean {d.mean():.5f}  "
          f"spread r13 {Lb[Lb>.02].max()-Lb[Lb>.02].min():.3f} r14 {La[La>.02].max()-La[La>.02].min():.3f}")

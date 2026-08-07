import math
import numpy as np
from PIL import Image

ANGLE = math.radians(33.0)
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)
EDGE_MID = (543.0, 604.0)
BLADE_LEN = 640.0
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2

lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
rd = lambda p: np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255.
new, old = rd("icon.png"), rd("loop-runs/r13/candidate-1024.png")
Ln, Lo = lum(new), lum(old)
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)
LY = NX * (X - AX) + NY * (Y - AY)      # exact local y: >0 un-planed, <0 trued
LXc = UX * (X - AX) + UY * (Y - AY)

# block-free stations, in canvas x, left of the block's tip (x=179)
wins = [(15, 75), (75, 135), (135, 179)]
print("EXACT local-frame cross-profile.  d = -local y, so + is into the trued side.")
print("   d " + "".join(f"     x{a}-{b}" for a, b in wins))
for d in range(-8, 17):
    row = f"{d:+4d} "
    for a, b in wins:
        m = (X >= a) & (X < b) & (-LY >= d - .5) & (-LY < d + .5) & (Ln > .02)
        row += f"  {Ln[m].mean():.3f}/{Lo[m].mean():.3f}" if m.sum() > 15 else "    --/--  "
    print(row)

print("\namplitudes against each station's own plateaus:")
for a, b in wins:
    w = (X >= a) & (X < b) & (Ln > .02)
    tp = Ln[w & (-LY >= 20) & (-LY <= 34)].mean()
    up = Ln[w & (-LY <= -20) & (-LY >= -34)].mean()
    tro = Ln[w & (-LY >= 2.5) & (-LY <= 4.5)].mean()
    arr = Ln[w & (-LY >= 7.2) & (-LY <= 8.8)].mean()
    cre = Ln[w & (-LY <= -1.2) & (-LY >= -2.8)].mean()
    otro = Lo[w & (-LY >= 2.5) & (-LY <= 4.5)].mean()
    oarr = Lo[w & (-LY >= 7.2) & (-LY <= 8.8)].mean()
    ocre = Lo[w & (-LY <= -1.2) & (-LY >= -2.8)].mean()
    print(f"  x{a}-{b} (local x {LXc[w&(np.abs(LY)<3)].mean():+7.1f}) trued {tp:.3f} un-planed {up:.3f}")
    print(f"      crest {100*(cre/up-1):+5.1f}% (was {100*(ocre/up-1):+5.1f})   "
          f"riser {100*(tro/tp-1):+6.1f}% (was {100*(otro/tp-1):+5.1f})   "
          f"arris {100*(arr/tp-1):+6.1f}% (was {100*(oarr/tp-1):+5.1f})")
print("  C2 target: crest +7.8%, riser -18.6%, arris +17.7% at full swell")

# what the swell mask should be doing at each station
lo = UX * (0 - AX) + UY * ((AY - NX * (0 - AX) / NY) - AY)
print(f"\nswell endpoints: local x at canvas x=0 -> {lo:.1f}")
key = (UX * (75 - AX) + UY * (25 - AY))
print(f"key local x {key:.1f}")

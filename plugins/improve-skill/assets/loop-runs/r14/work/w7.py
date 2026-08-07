import numpy as np
from PIL import Image

R = "loop-runs/r13/"
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")).astype(np.float32) / 255.
lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
Lc, Lr = lum(cand), lum(ref)
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)

t = np.radians(34.0)
s = Y * np.cos(t) + X * np.sin(t) - 791.9   # our own cut: 0 on the line, + into trued

print("signed residual (ref - cand) binned by OUR OWN distance from the cut,")
print("in the block-free left strip, three x windows:")
wins = [(20, 130), (130, 240), (240, 350)]
print("   d " + "".join(f"   x{a}-{b}" for a, b in wins) + "     all")
for d in range(-20, 25):
    row = f"{d:+4d} "
    for a, b in wins + [(20, 350)]:
        m = (X >= a) & (X < b) & (s >= d - 0.5) & (s < d + 0.5) & (Lc > 0.02)
        row += f"  {np.mean(Lr[m]-Lc[m]):+.4f}" if m.sum() > 20 else "        --"
    print(row)

m_all = (X >= 20) & (X < 350) & (Lc > 0.02)
for nm, sel in (("d in [+1,+6] (would darken)", (s >= 1) & (s <= 6)),
                ("d in [+6,+11] (would brighten)", (s >= 6) & (s <= 11)),
                ("d in [-6,-1]", (s >= -6) & (s <= -1)),
                ("trued far, d>+20", s > 20)):
    m = m_all & sel
    print(f"{nm:32s} n={m.sum():6d}  mean(ref-cand) {np.mean(Lr[m]-Lc[m]):+.4f}   cand {Lc[m].mean():.4f}  ref {Lr[m].mean():.4f}")

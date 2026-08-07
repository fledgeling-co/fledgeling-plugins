import numpy as np
from PIL import Image

cand = np.asarray(Image.open("icon.png").convert("RGB")).astype(np.float32) / 255.
old = np.asarray(Image.open("loop-runs/r13/candidate-1024.png").convert("RGB")).astype(np.float32) / 255.
ref = np.asarray(Image.open("loop-runs/r13/reference-1024.png").convert("RGB")).astype(np.float32) / 255.
lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
Lc, Lo, Lr = lum(cand), lum(old), lum(ref)
Y, X = np.mgrid[0:1024, 0:1024].astype(np.float32)
tc = np.radians(34.0)
sc = Y * np.cos(tc) + X * np.sin(tc) - 791.9
tr = np.radians(41.0)
sr = Y * np.cos(tr) + X * np.sin(tr) - 763.5

wins = [(20, 130), (130, 240), (240, 350)]
print("achieved cross-profile, by station.  new / old (ours), and C2 on its own cut")
print("   d " + "".join(f"      x{a}-{b}" for a, b in wins) + "        C2 all")
for d in range(-8, 16):
    row = f"{d:+4d} "
    for a, b in wins:
        m = (X >= a) & (X < b) & (sc >= d - .5) & (sc < d + .5) & (Lc > .02)
        row += f"  {Lc[m].mean():.3f}/{Lo[m].mean():.3f}" if m.sum() > 20 else "     --/--  "
    m = (X >= 20) & (X < 350) & (sr >= d - .5) & (sr < d + .5) & (Lr > .02)
    row += f"    {Lr[m].mean():.4f}" if m.sum() > 20 else "       --"
    print(row)

print("\nrelative to each station's own trued plateau (d in [+20,+30]):")
for a, b in wins:
    pl = (X >= a) & (X < b) & (sc >= 20) & (sc <= 30) & (Lc > .02)
    base = Lc[pl].mean()
    tro = (X >= a) & (X < b) & (sc >= 2) & (sc <= 5) & (Lc > .02)
    pk = (X >= a) & (X < b) & (sc >= 7) & (sc <= 9) & (Lc > .02)
    up = (X >= a) & (X < b) & (sc >= -3) & (sc <= -1) & (Lc > .02)
    upb = (X >= a) & (X < b) & (sc >= -30) & (sc <= -20) & (Lc > .02)
    print(f"  x{a}-{b}: trued plateau {base:.3f}  trough {100*(Lc[tro].mean()/base-1):+5.1f}%  "
          f"arris {100*(Lc[pk].mean()/base-1):+5.1f}%   crest {100*(Lc[up].mean()/Lc[upb].mean()-1):+5.1f}% of un-planed {Lc[upb].mean():.3f}")
print("  C2 measured:            trough -15.6/-18.1/-22.2%   arris +11.9/+17.2/+24.1%   crest +5.6/+12.1/+5.6%")

print("\nsaturation check at the riser (should rise, not fall):")
for nm, img, s in (("new", cand, sc), ("old", old, sc), ("C2", ref, sr)):
    L = lum(img)
    r1 = (X >= 20) & (X < 350) & (s >= 2) & (s <= 5) & (L > .02)
    r2 = (X >= 20) & (X < 350) & (s >= 20) & (s <= 30) & (L > .02)
    c1, c2 = img[r1].mean(0), img[r2].mean(0)
    f = lambda c: (c.max() - c.min()) / c.max()
    print(f"  {nm:4s} riser RGB {c1[0]:.3f} {c1[1]:.3f} {c1[2]:.3f} sat {f(c1):.3f}   "
          f"plateau sat {f(c2):.3f}   delta {f(c1)-f(c2):+.3f}")

# 256/128 survival
for size in (256, 128):
    k = size / 1024.
    a = np.asarray(Image.open("icon.png").convert("RGB").resize((size, size), Image.LANCZOS)).astype(np.float32) / 255.
    b = np.asarray(Image.open("loop-runs/r13/candidate-1024.png").convert("RGB").resize((size, size), Image.LANCZOS)).astype(np.float32) / 255.
    La, Lb = lum(a), lum(b)
    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    s = yy * np.cos(tc) + xx * np.sin(tc) - 791.9 * k
    sel = lambda L, d0, d1: L[(xx >= 20 * k) & (xx < 350 * k) & (s >= d0) & (s <= d1) & (L > .02)].mean()
    pa, pb = sel(La, 5 * k * 4, 8), sel(Lb, 5 * k * 4, 8)
    print(f"{size}px: arris peak/plateau  new {sel(La,1.2*k*4,2.2*k*4)/pa:.4f}  old {sel(Lb,1.2*k*4,2.2*k*4)/pb:.4f}   (C2 1.108 at 256, 1.054 at 128)")

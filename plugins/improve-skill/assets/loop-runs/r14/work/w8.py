import numpy as np
from PIL import Image

R = "loop-runs/r13/"
for size in (256, 128):
    ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB")
                     .resize((size, size), Image.LANCZOS)).astype(np.float32) / 255.
    cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB")
                      .resize((size, size), Image.LANCZOS)).astype(np.float32) / 255.
    lum = lambda a: 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    Lr, Lc = lum(ref), lum(cand)
    Y, X = np.mgrid[0:size, 0:size].astype(np.float32)
    k = size / 1024.
    tr, tc = np.radians(41.0), np.radians(34.0)
    sr = Y * np.cos(tr) + X * np.sin(tr) - 763.5 * k
    sc = Y * np.cos(tc) + X * np.sin(tc) - 791.9 * k
    print(f"\n=== {size}px, distance in {size}px pixels (1 px = {1024/size:.0f} at 1024) ===")
    print("   d      ref     cand")
    for d in np.arange(-5, 6.5, 0.5):
        mr = (X >= 20 * k) & (X < 350 * k) & (sr >= d - 0.25) & (sr < d + 0.25) & (Lr > 0.02)
        mc = (X >= 20 * k) & (X < 350 * k) & (sc >= d - 0.25) & (sc < d + 0.25) & (Lc > 0.02)
        a = f"{Lr[mr].mean():.4f}" if mr.sum() > 8 else "  --  "
        b = f"{Lc[mc].mean():.4f}" if mc.sum() > 8 else "  --  "
        print(f"{d:+5.1f}   {a}   {b}")

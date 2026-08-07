"""r04: the vermilion hone line in both images -> cutting-edge angle, midpoint, length."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
imgs = {
    "REF ": np.asarray(Image.open(R + "reference-1024.png").convert("RGBA"), float) / 255.,
    "CAND": np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), float) / 255.,
}

for tag, a in imgs.items():
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    warm = (r - np.maximum(g, b))
    for t in (0.18, 0.25, 0.32):
        m = (warm > t) & (a[..., 3] > 0.5)
        ys, xs = np.nonzero(m)
        if len(xs) < 50:
            print(f"{tag} warm>{t}: n={len(xs)}")
            continue
        A = np.polyfit(xs.astype(float), ys.astype(float), 1)
        ang = np.degrees(np.arctan(-A[0]))
        # endpoints along the fit
        print(f"{tag} warm>{t:.2f}: n={len(xs):6d} x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] "
              f"angle={ang:.2f}deg mid=({xs.mean():.0f},{ys.mean():.0f}) "
              f"len={np.hypot(xs.max()-xs.min(), ys.max()-ys.min()):.0f}")
    print()

# also: peak-warmth spine per column, robust
for tag, a in imgs.items():
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    warm = r - np.maximum(g, b)
    pts = []
    for x in range(0, 1024, 8):
        col = warm[:, x]
        y = int(np.argmax(col))
        if col[y] > 0.20:
            pts.append((x, y))
    if len(pts) > 6:
        px = np.array([p[0] for p in pts], float)
        py = np.array([p[1] for p in pts], float)
        A = np.polyfit(px, py, 1)
        print(f"{tag} spine: n={len(pts)} x[{px.min():.0f},{px.max():.0f}] "
              f"angle={np.degrees(np.arctan(-A[0])):.2f}deg "
              f"y@x0={A[1]:.0f} mid=({px.mean():.0f},{A[0]*px.mean()+A[1]:.0f})")

"""r04 coarse-structure analysis: measure the reference's structure, not assume it."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGB"), dtype=np.float64) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGB"), dtype=np.float64) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


Lr, Lc = lum(ref), lum(cand)

for name, L in (("REF ", Lr), ("CAND", Lc)):
    h, _ = np.histogram(L[60:964, 60:964], bins=20, range=(0, 1))
    print(name, "hist/1k:", " ".join(f"{v/1000:5.1f}" for v in h))

print()
# block mask: dark pixels inside the tile
for name, L in (("REF ", Lr), ("CAND", Lc)):
    for thr in (0.30, 0.35, 0.40, 0.45):
        m = np.zeros(L.shape, bool)
        m[50:974, 50:974] = L[50:974, 50:974] < thr
        ys, xs = np.nonzero(m)
        if len(xs) == 0:
            continue
        print(f"{name} thr={thr:.2f} n={len(xs):6d} ({100*len(xs)/1024**2:5.2f}%) "
              f"x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] "
              f"cx={xs.mean():.0f} cy={ys.mean():.0f}")
    print()

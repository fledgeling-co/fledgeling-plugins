"""r04 coarse-structure measurement: block silhouette, boundary line, curl, fields."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGBA"), dtype=np.float64) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), dtype=np.float64) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def erode(m, n):
    for _ in range(n):
        e = m.copy()
        e[1:, :] &= m[:-1, :]
        e[:-1, :] &= m[1:, :]
        e[:, 1:] &= m[:, :-1]
        e[:, :-1] &= m[:, 1:]
        m = e
    return m


Lr, Lc = lum(ref), lum(cand)
inr = erode(ref[..., 3] > 0.99, 14)
inc = erode(cand[..., 3] > 0.99, 14)
print("inside px: ref %d cand %d" % (inr.sum(), inc.sum()))


def report(tag, L, inside, thrs):
    for thr in thrs:
        m = inside & (L < thr)
        ys, xs = np.nonzero(m)
        if len(xs) < 100:
            continue
        print(f"  {tag} thr={thr:.2f} n={len(xs):6d} ({100*len(xs)/inside.sum():5.2f}% of tile) "
              f"x[{xs.min()},{xs.max()}] y[{ys.min()},{ys.max()}] "
              f"w={xs.max()-xs.min()} h={ys.max()-ys.min()} cx={xs.mean():.0f} cy={ys.mean():.0f}")


print("\n== dark-object (block) mask ==")
report("REF ", Lr, inr, (0.28, 0.32, 0.36, 0.40))
report("CAND", Lc, inc, (0.28, 0.32, 0.36, 0.40))

print("\n== per-row extent of the block (thr) ==")
for tag, L, inside, thr in (("REF ", Lr, inr, 0.34), ("CAND", Lc, inc, 0.34)):
    m = inside & (L < thr)
    print(f"  {tag}")
    for y in range(150, 800, 50):
        xs = np.nonzero(m[y])[0]
        if len(xs):
            print(f"    y={y:4d} x[{xs.min():4d},{xs.max():4d}] span={xs.max()-xs.min():4d}")

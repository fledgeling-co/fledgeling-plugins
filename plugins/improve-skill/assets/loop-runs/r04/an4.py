"""r04: PCA + support-function corners of the reference block; same for the master."""
import numpy as np
from PIL import Image

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref = np.asarray(Image.open(R + "reference-1024.png").convert("RGBA"), dtype=np.float64) / 255.
cand = np.asarray(Image.open(R + "candidate-1024.png").convert("RGBA"), dtype=np.float64) / 255.


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def largest_blob(m):
    """flood fill from the biggest row-run; pure numpy label via iterative dilation"""
    lab = np.zeros(m.shape, np.int32)
    ys, xs = np.nonzero(m)
    seed = (int(np.median(ys)), int(np.median(xs)))
    if not m[seed]:
        seed = (ys[len(ys) // 2], xs[len(xs) // 2])
    cur = np.zeros(m.shape, bool)
    cur[seed] = True
    while True:
        nxt = cur.copy()
        nxt[1:, :] |= cur[:-1, :]
        nxt[:-1, :] |= cur[1:, :]
        nxt[:, 1:] |= cur[:, :-1]
        nxt[:, :-1] |= cur[:, 1:]
        nxt &= m
        if nxt.sum() == cur.sum():
            return cur
        cur = nxt


def analyse(tag, m):
    m = largest_blob(m)
    ys, xs = np.nonzero(m)
    pts = np.stack([xs, ys], 1).astype(float)
    c = pts.mean(0)
    q = pts - c
    cov = q.T @ q / len(q)
    w, v = np.linalg.eigh(cov)
    ax = v[:, np.argmax(w)]
    if ax[0] < 0:
        ax = -ax
    ang = np.degrees(np.arctan2(-ax[1], ax[0]))
    per = np.array([-ax[1], ax[0]])
    a = q @ ax
    b = q @ per
    print(f"{tag}: n={len(q)} ({100*len(q)/1024**2:.2f}%) centroid=({c[0]:.0f},{c[1]:.0f}) "
          f"pca_angle={ang:.2f}deg  along[{a.min():.0f},{a.max():.0f}] len={a.max()-a.min():.0f}  "
          f"across[{b.min():.0f},{b.max():.0f}] wid={b.max()-b.min():.0f}")
    # corners: extreme of a+/-b combos
    for sa, sb, name in ((-1, 1, "lead-lo "), (-1, -1, "lead-hi "),
                         (1, 1, "trail-lo"), (1, -1, "trail-hi")):
        s = sa * a + sb * b
        i = int(np.argmax(s))
        print(f"    {name} corner ({pts[i,0]:.0f},{pts[i,1]:.0f})")
    return m, c, ax, per


Lr, Lc = lum(ref), lum(cand)
print("== reference block ==")
analyse("REF ", Lr < 0.30)
print("\n== master block (curl excluded by hand: curl lives x<450,y<470) ==")
mc = (Lc < 0.50) & (cand[..., 3] > 0.99)
analyse("CAND", mc)

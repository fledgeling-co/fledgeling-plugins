"""Mark LENGTH, mark COUNT, and where in scale-space each image keeps its relief.

r11 closed by saying amplitude is solved and the next detail round belongs to mark
length and count. Three instruments, all on clean patches of each plane:

 1. scale decomposition - rms of the 1-3px, 3-13px and 13-40px band-passes. A field
    of long ruled lines and a field of short flecks over a granular substrate can
    carry the SAME 3-13px rms (which is all r10/r11 measured) and look nothing alike.
 2. connected-component geometry of the thresholded relief - per-mark length (major
    axis), width (minor axis), count per 10k px, and area coverage.
 3. run-length along the dominant bearing - the duty cycle of a single ridge.
"""
import math, sys, numpy as np

W = 1024
h = np.load("h1024.npy")
g = np.load((sys.argv[1] if len(sys.argv) > 1 else "g") + "1024.npy")
rough = np.load("rough.npy"); trued = np.load("trued.npy")
yy, xx = np.mgrid[0:W, 0:W].astype(float)


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[:x.shape[0], :x.shape[1]]


BANDS = (("1-3px", 1, 3), ("3-13px", 3, 13), ("13-40px", 13, 40))
print("scale decomposition, rms of each band-pass")
print(f"{'region':16s} " + " ".join(f"{n:>22s}" for n, _, _ in BANDS))
print(f"{'':16s} " + " ".join(f"{'ref':>7s}{'ours':>8s}{'r/o':>7s}" for _ in BANDS))
for name, m in (("un-planed", rough), ("trued", trued),
                ("un-planed band", rough & (yy > 384)),
                ("un-planed above", rough & (yy <= 384))):
    cells = []
    for _, lo, hi in BANDS:
        a = (box(h, lo) - box(h, hi))[m].std()
        b = (box(g, lo) - box(g, hi))[m].std()
        cells.append(f"{a:7.4f}{b:8.4f}{a/max(b,1e-6):7.2f}")
    print(f"{name:16s} " + " ".join(f"{c:>22s}" for c in cells))


# ---- connected components of the thresholded relief, pure numpy union-find
def components(mask):
    lab = np.zeros(mask.shape, np.int32)
    idx = np.argwhere(mask)
    order = {tuple(p): i + 1 for i, p in enumerate(idx)}
    parent = list(range(len(idx) + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for (y, x) in idx:
        i = order[(y, x)]
        lab[y, x] = i
        for dy, dx in ((-1, 0), (-1, -1), (-1, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx]:
                union(i, order[(ny, nx)])
    groups = {}
    for (y, x) in idx:
        groups.setdefault(find(order[(y, x)]), []).append((y, x))
    return list(groups.values())


def marks(img, x0, y0, n=200, tag=""):
    p = img[y0:y0+n, x0:x0+n]
    hp = (box(p, 3) - box(p, 13))
    thr = 1.1 * hp.std()
    out = []
    for sign in (1, -1):
        for comp in components(sign * hp > thr):
            if len(comp) < 3:
                continue
            a = np.array(comp, float)
            a -= a.mean(0)
            ev = np.linalg.eigvalsh(a.T @ a / len(a))
            L, Wd = 3.46 * math.sqrt(max(ev[1], 0)), 3.46 * math.sqrt(max(ev[0], 0))
            out.append((L, max(Wd, 0.7), len(comp)))
    if not out:
        return
    L = np.array([o[0] for o in out]); Wd = np.array([o[1] for o in out])
    ar = np.array([o[2] for o in out])
    cov = 100.0 * ar.sum() / (n * n)
    print(f"{tag:20s} n={len(out):5d} ({10000*len(out)/(n*n):5.1f}/10k px)  "
          f"len med {np.median(L):5.1f} p90 {np.quantile(L, .9):6.1f} max {L.max():6.1f}"
          f"  wid med {np.median(Wd):4.1f}  aspect {np.median(L/Wd):5.1f}  cov {cov:5.1f}%")


print("\nmarks (connected components of the 3-13px relief, |hp| > 1.1 sd)")
for name, (x0, y0) in {"un-planed left": (20, 520), "un-planed mid": (150, 400),
                       "un-planed low": (110, 700), "above-band A": (230, 120),
                       "above-band B": (430, 30), "trued": (700, 640),
                       "trued near": (560, 470)}.items():
    for lbl, img in (("ref", h), ("ours", g)):
        marks(img, x0, y0, 200, f"{name} {lbl}")
    print()

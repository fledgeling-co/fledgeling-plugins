"""Lattice or field: the two numbers the eye is reading in `v-band-left.png`.

r14 closed by saying the remaining distance on the un-planed plane is a
lattice-vs-field problem rather than a density one, and named ridge placement as
the next round's target. Neither of the instruments already in the fixture can see
that fault: coverage, count, mark length, aspect and band rms are all statistics of
the marks THEMSELVES and are blind to how those marks are arranged. Two that aren't:

 1. VOID - the distance from each un-marked pixel to the nearest mark, over the
    thresholded 3-13px relief. A lattice of dashed tracks leaves closed cells of
    bare ground between the tracks; a field does not. p90 and max of that distance
    are the size of the largest hole in the texture.
 2. BEARING SCATTER - each mark's own PCA bearing, binned to 15 canvas degrees.
    Two families of ruled lines put every mark in two bins; a torn field spreads
    them. Reported as normalised entropy (1.0 = uniform over bearings) and as the
    share held by the two fullest bins.
"""
import math, sys, numpy as np
from w3helpers import box, components, STATIONS

g = np.load((sys.argv[1] if len(sys.argv) > 1 else "g") + "1024.npy")
h = np.load("h1024.npy")


def dist_to_mark(mask, cap=40):
    """Chebyshev-ish distance transform by repeated 8-neighbour dilation. Small
    patches, so the loop is cheaper than importing anything."""
    d = np.zeros(mask.shape, float)
    cur = mask.copy()
    for k in range(1, cap + 1):
        nxt = cur.copy()
        nxt[1:] |= cur[:-1]; nxt[:-1] |= cur[1:]
        nxt[:, 1:] |= cur[:, :-1]; nxt[:, :-1] |= cur[:, 1:]
        nxt[1:, 1:] |= cur[:-1, :-1]; nxt[:-1, :-1] |= cur[1:, 1:]
        nxt[1:, :-1] |= cur[:-1, 1:]; nxt[:-1, 1:] |= cur[1:, :-1]
        d[nxt & ~cur] = k
        if nxt.all():
            break
        cur = nxt
    d[~cur] = cap
    return d


def stats(img, x0, y0, n=200):
    p = img[y0:y0+n, x0:x0+n]
    hp = box(p, 3) - box(p, 13)
    mask = np.abs(hp) > 1.1 * hp.std()
    d = dist_to_mark(mask)
    void = d[~mask]
    bins = np.zeros(12)
    for sign in (1, -1):
        for comp in components(sign * hp > 1.1 * hp.std()):
            if len(comp) < 3:
                continue
            a = np.array(comp, float); a -= a.mean(0)
            ev, evec = np.linalg.eigh(a.T @ a / len(a))
            if ev[1] < 1e-9:
                continue
            vy, vx = evec[:, 1]
            th = (math.degrees(math.atan2(vy, vx))) % 180
            bins[min(11, int(th / 15))] += math.sqrt(ev[1]) * len(comp)
    bins /= max(bins.sum(), 1e-9)
    ent = -(bins[bins > 0] * np.log(bins[bins > 0])).sum() / math.log(12)
    top2 = np.sort(bins)[::-1][:2].sum()
    return (float(np.quantile(void, .9)), float(void.max()), float(void.mean()),
            ent, top2, np.argsort(bins)[::-1][:2])


print(f"{'station':16s} {'void p90':>13s} {'void max':>13s} {'void mean':>13s} "
      f"{'bearing ent':>13s} {'top-2 share':>13s}   ref / ours")
for name, (x0, y0) in STATIONS.items():
    r = stats(h, x0, y0); o = stats(g, x0, y0)
    print(f"{name:16s} {r[0]:6.1f}/{o[0]:6.1f} {r[1]:6.1f}/{o[1]:6.1f} "
          f"{r[2]:6.2f}/{o[2]:6.2f} {r[3]:6.3f}/{o[3]:6.3f} {r[4]:6.3f}/{o[4]:6.3f}"
          f"   peaks ref {r[5][0]*15:3d}/{r[5][1]*15:3d}  ours {o[5][0]*15:3d}/{o[5][1]*15:3d}")

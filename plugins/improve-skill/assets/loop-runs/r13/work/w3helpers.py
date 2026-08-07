"""The mark instrument from w3.py, callable, so a sweep can print one row per take."""
import math, numpy as np

STATIONS = {"un-planed left": (20, 520), "un-planed mid": (150, 400),
            "un-planed low": (110, 700), "above-band": (230, 120),
            "trued": (700, 640)}
REF = {"un-planed left": (199.0, 3.9, 8.6, 2.0, 1.9, 23.5),
       "un-planed mid": (108.0, 3.8, 9.2, 2.2, 1.9, 18.8),
       "un-planed low": (105.2, 4.5, 10.8, 2.4, 1.7, 20.4),
       "above-band": (82.8, 4.4, 13.1, 2.2, 2.0, 17.0),
       "trued": (191.5, 3.8, 8.3, 2.2, 1.8, 22.8)}


def box(x, w):
    pad = w // 2
    xp = np.pad(x.astype(float), pad, mode="edge")
    c = np.cumsum(np.cumsum(xp, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    return (s / (w * w))[:x.shape[0], :x.shape[1]]


def components(mask):
    idx = np.argwhere(mask)
    order = {tuple(p): i + 1 for i, p in enumerate(idx)}
    parent = list(range(len(idx) + 1))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]
            a = parent[a]
        return a

    for (y, x) in idx:
        i = order[(y, x)]
        for dy, dx in ((-1, 0), (-1, -1), (-1, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx]:
                ra, rb = find(i), find(order[(ny, nx)])
                if ra != rb:
                    parent[max(ra, rb)] = min(ra, rb)
    groups = {}
    for (y, x) in idx:
        groups.setdefault(find(order[(y, x)]), []).append((y, x))
    return list(groups.values())


def marks(img, x0, y0, n=200):
    p = img[y0:y0+n, x0:x0+n]
    hp = box(p, 3) - box(p, 13)
    thr = 1.1 * hp.std()
    out = []
    for sign in (1, -1):
        for comp in components(sign * hp > thr):
            if len(comp) < 3:
                continue
            a = np.array(comp, float)
            a -= a.mean(0)
            ev = np.linalg.eigvalsh(a.T @ a / len(a))
            out.append((3.46 * math.sqrt(max(ev[1], 0)),
                        max(3.46 * math.sqrt(max(ev[0], 0)), 0.7), len(comp)))
    L = np.array([o[0] for o in out]); Wd = np.array([o[1] for o in out])
    ar = np.array([o[2] for o in out])
    return (10000 * len(out) / (n * n), float(np.median(L)), float(np.quantile(L, .9)),
            float(np.median(Wd)), float(np.median(L / Wd)), 100.0 * ar.sum() / (n * n))


def report(h, g, label=""):
    print(f"{'station':16s} {'n/10k':>13s} {'med len':>13s} {'p90':>13s} "
          f"{'wid':>11s} {'aspect':>11s} {'cov%':>13s}   (ref / ours)")
    for name, (x0, y0) in STATIONS.items():
        o = marks(g, x0, y0)
        r = REF[name]
        cells = "".join(f"{a:6.1f}/{b:6.1f}" if i in (0, 5) else f"{a:5.1f}/{b:5.1f}"
                        for i, (a, b) in enumerate(zip(r, o)))
        print(f"{name:16s} {cells}")

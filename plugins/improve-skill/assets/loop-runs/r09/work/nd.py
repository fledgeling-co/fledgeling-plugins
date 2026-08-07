"""numpy-only morphology + exact Euclidean distance transform (Felzenszwalb/Huttenlocher)."""
import numpy as np
from PIL import Image, ImageFilter

def _mf(mask, size, mode):
    im = Image.fromarray((mask*255).astype(np.uint8))
    f = ImageFilter.MinFilter(size) if mode == 'erode' else ImageFilter.MaxFilter(size)
    return np.asarray(im.filter(f)) > 127

def erode(m, k=3):  return _mf(m, k, 'erode')
def dilate(m, k=3): return _mf(m, k, 'dilate')
def opening(m, k=3): return dilate(erode(m, k), k)
def closing(m, k=3): return erode(dilate(m, k), k)

def convex_fill(m):
    """Row-span fill AND column-span fill. Exact for convex shapes; the block is one."""
    def span(a):
        out = np.zeros_like(a)
        for i in range(a.shape[0]):
            w = np.flatnonzero(a[i])
            if w.size: out[i, w[0]:w[-1]+1] = True
        return out
    return span(m) & span(m.T).T

def _dt1d(f):
    """1-D squared distance transform of sampled function f (Felzenszwalb & Huttenlocher)."""
    n = f.shape[-1]
    d = np.empty_like(f)
    for row in range(f.shape[0]):
        fr = f[row]
        v = np.zeros(n, dtype=np.int64); z = np.empty(n+1); k = 0
        v[0] = 0; z[0] = -np.inf; z[1] = np.inf
        for q in range(1, n):
            while True:
                s = ((fr[q] + q*q) - (fr[v[k]] + v[k]*v[k])) / (2.0*q - 2.0*v[k])
                if s <= z[k]: k -= 1
                else: break
            k += 1; v[k] = q; z[k] = s; z[k+1] = np.inf
        k = 0
        for q in range(n):
            while z[k+1] < q: k += 1
            d[row, q] = (q - v[k])**2 + fr[v[k]]
    return d

def edt(mask):
    """Euclidean distance from every pixel to the nearest True pixel of `mask`."""
    INF = 1e12
    f = np.where(mask, 0.0, INF)
    f = _dt1d(f)
    f = _dt1d(np.ascontiguousarray(f.T)).T
    return np.sqrt(f)

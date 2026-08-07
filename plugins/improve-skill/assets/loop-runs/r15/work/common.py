"""Shared loaders + the icon's local frame, for r15 measurement."""
import math
import numpy as np
from PIL import Image

R14 = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r14"

ANGLE = math.radians(33.0)
UX, UY = math.cos(ANGLE), -math.sin(ANGLE)
NX, NY = -math.sin(ANGLE), -math.cos(ANGLE)
BLADE_LEN = 640.0
BLADE_THICK = 204.0
EDGE_MID = (543.0, 604.0)
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2
RISE_NEAR, RISE_FAR = 48.0, 132.0
K_RISE = (RISE_FAR - RISE_NEAR) / BLADE_LEN


def rise_at(lx):
    return RISE_NEAR + K_RISE * lx


def to_canvas(lx, ly):
    return (AX + UX * lx + NX * ly, AY + UY * lx + NY * ly)


def to_top(lx, ly):
    x, y = to_canvas(lx, ly)
    return (x, y - rise_at(lx))


def to_local(px, py):
    dx, dy = px - AX, py - AY
    return (UX * dx + UY * dy, NX * dx + NY * dy)


def to_local_top(px, py):
    """Invert the sheared top-face frame."""
    a, b, c, d = UX, UY - K_RISE, NX, NY
    e, f = AX, AY - RISE_NEAR
    det = a * d - c * b
    dx, dy = px - e, py - f
    return ((d * dx - c * dy) / det, (-b * dx + a * dy) / det)


def load(path):
    im = Image.open(path).convert("RGB")
    return np.asarray(im).astype(np.float64) / 255.0


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def sat(a):
    mx = a.max(-1)
    mn = a.min(-1)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)


def cand():
    return load(f"{R14}/candidate-1024.png")


def ref():
    return load(f"{R14}/reference-1024.png")


def boxblur(a, k):
    """Separable box blur, radius k (odd window 2k+1), reflect edges."""
    if k <= 0:
        return a.copy()
    pad = np.pad(a, ((k, k), (k, k)), mode="reflect")
    cs = np.cumsum(pad, axis=0)
    cs = np.vstack([np.zeros((1, cs.shape[1])), cs])
    out = (cs[2 * k + 1:, :] - cs[:-(2 * k + 1), :]) / (2 * k + 1)
    cs = np.cumsum(out, axis=1)
    cs = np.hstack([np.zeros((cs.shape[0], 1)), cs])
    out = (cs[:, 2 * k + 1:] - cs[:, :-(2 * k + 1)]) / (2 * k + 1)
    return out


def highpass(L, k=6):
    return L - boxblur(L, k)


def grid(shape):
    ys, xs = np.mgrid[0:shape[0], 0:shape[1]]
    return xs.astype(np.float64), ys.astype(np.float64)

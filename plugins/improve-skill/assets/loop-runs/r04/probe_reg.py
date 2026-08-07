"""r04 probe: how much of the 1024/256 SSIM gap is pure misregistration of the diagonal?

Warps the CURRENT candidate render by the rigid map that carries the master's hone
frame onto the reference's measured one, and rescores ssim/edge_f1 with fidelity.py's
own formulas. Diagnostic only - tells us whether the measured 5.9deg / 35px offset is
what the metric is seeing.
"""
import numpy as np
from PIL import Image
import sys

sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F  # noqa

R = "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets/loop-runs/r01/"
ref_im = Image.open(R + "reference-1024.png").convert("RGBA")
cand_im = Image.open(R + "candidate-1024.png").convert("RGBA")

# frames
A_ANG, A_ORG = 33.00, (274.6, 778.3)      # master
B_ANG, B_ORG = 38.92, (382.0, 688.0)      # reference, measured


def uv(deg):
    a = np.radians(deg)
    return (np.cos(a), -np.sin(a)), (-np.sin(a), -np.cos(a))


def warp(im, ang_b, org_b, scale=1.0):
    """PIL affine: dst(x,y) = src(a x + b y + c, d x + e y + f)."""
    ua, na = uv(A_ANG)
    ub, nb = uv(ang_b)
    # dst is candidate placed in frame B; so for a dst pixel, find its (lx,ly) in B, then
    # read src at A's canvas position of that (lx,ly).
    M = np.array([[ub[0], nb[0]], [ub[1], nb[1]]]) * scale
    Minv = np.linalg.inv(M)
    N = np.array([[ua[0], na[0]], [ua[1], na[1]]])
    T = N @ Minv
    c = np.array(A_ORG) - T @ np.array(org_b)
    return im.transform((1024, 1024), Image.AFFINE,
                        (T[0, 0], T[0, 1], c[0], T[1, 0], T[1, 1], c[1]),
                        resample=Image.BICUBIC)


def score(cim, size):
    ci = cim.resize((size, size), Image.LANCZOS)
    ri = ref_im.resize((size, size), Image.LANCZOS)
    gc, gr = F.to_gray(ci), F.to_gray(ri)
    m = {"lum_delta": round(abs(gc.mean() - gr.mean()), 4),
         "ssim": round(F.ssim(gc, gr), 4),
         "edge_f1": round(F.edge_f1(gc, gr), 4),
         "mask_iou": F.mask_iou(ci, ri)}
    m["composite"] = F.composite_for(size, m)
    return m


print("variant                       1024                          256")
for name, im in [("as-is", cand_im),
                 ("rot->38.92 only", warp(cand_im, 38.92, A_ORG)),
                 ("rot+move (measured)", warp(cand_im, 38.92, B_ORG)),
                 ("move only (33deg)", warp(cand_im, 33.00, B_ORG)),
                 ("rot+move+1.05x", warp(cand_im, 38.92, B_ORG, 1.05)),
                 ("rot+move+0.95x", warp(cand_im, 38.92, B_ORG, 0.95)),
                 ("36deg+move", warp(cand_im, 36.00, B_ORG))]:
    a, b = score(im, 1024), score(im, 256)
    print(f"{name:22s} ssim {a['ssim']:.4f} e{a['edge_f1']:.4f} c{a['composite']:.4f}   "
          f"ssim {b['ssim']:.4f} e{b['edge_f1']:.4f} c{b['composite']:.4f}")

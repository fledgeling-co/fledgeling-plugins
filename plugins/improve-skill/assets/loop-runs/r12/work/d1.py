"""r12 diagnostic 1: where do the 1024 edge FP/FN and the SSIM deficit actually live?

Regions are built in the master's own local frame (the r08 idiom) and the reference is
read through the SAME masks, so every number below compares like for like on a region
whose identity the two images agree on (block silhouette IoU is 0.95).
"""
import sys, pathlib, math, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = 1024
g = F.to_gray(F.render_candidate(A / "icon.svg", W))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", W))
np.save("d_g.npy", g); np.save("d_h.npy", h)

# ---- local frame (matches build_icon.py) -------------------------------------
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
BLADE_LEN, BLADE_THICK = 640.0, 204.0
RISE_NEAR, RISE_FAR = 48.0, 132.0
K_RISE = (RISE_FAR - RISE_NEAR) / BLADE_LEN
AX = 543.0 - UX * BLADE_LEN / 2
AY = 604.0 - UY * BLADE_LEN / 2
yy, xx = np.mgrid[0:W, 0:W].astype(float)

def inv(a, b, c, d, e, f):
    det = a * d - b * c
    return (d / det, -b / det, -c / det, a / det,
            (c * f - d * e) / det, (b * e - a * f) / det)

# top-face frame: matrix(UX, UY-K_RISE, NX, NY, AX, AY-RISE_NEAR)
ia, ib, ic, idd, ie, if_ = inv(UX, UY - K_RISE, NX, NY, AX, AY - RISE_NEAR)
tx = ia * xx + ic * yy + ie
ty = ib * xx + idd * yy + if_
# ground frame
ja, jb, jc, jd, je, jf = inv(UX, UY, NX, NY, AX, AY)
gx = ja * xx + jc * yy + je
gy = jb * xx + jd * yy + jf
np.save("d_tx.npy", tx); np.save("d_ty.npy", ty)
np.save("d_gx.npy", gx); np.save("d_gy.npy", gy)

# ---- regions ------------------------------------------------------------------
inner = 14.0
TOPFACE = (tx > inner) & (tx < BLADE_LEN - inner) & (ty > inner) & (ty < BLADE_THICK - inner)
# front face: below the top face's lower chain, above the ground contact, in ground frame
FRONT = (gx > inner) & (gx < BLADE_LEN - inner) & (gy > 6.0) & (gy < 40.0)
CURL = (np.hypot(xx - 308.0, yy - 278.0) < 150.0) & ~TOPFACE
bound_y = 604.0 - math.tan(ANG) * (xx - 543.0)     # the cut, rising to the right
ROUGH = (yy < bound_y - 30) & ~TOPFACE & ~FRONT & ~CURL
TRUED = (yy > bound_y + 30) & ~TOPFACE & ~FRONT & ~CURL
sq = (np.abs((xx - 511.5) / 511.5) ** 5 + np.abs((yy - 511.5) / 511.5) ** 5) ** 0.2
TILE = sq < 0.86
np.save("d_topface.npy", TOPFACE); np.save("d_front.npy", FRONT)
np.save("d_curl.npy", CURL); np.save("d_rough.npy", ROUGH & TILE); np.save("d_trued.npy", TRUED & TILE)

REG = [("topface", TOPFACE & TILE), ("frontface", FRONT & TILE), ("curl", CURL & TILE),
       ("rough-gnd", ROUGH & TILE), ("trued-gnd", TRUED & TILE)]

# ---- edge accounting -----------------------------------------------------------
ec, er = F.sobel_edges(g), F.sobel_edges(h)
keep = ~F.rim_mask(W)
ec &= keep; er &= keep
FP = ec & ~F.dilate(er)          # candidate edge with no reference edge nearby
FN = er & ~F.dilate(ec)          # reference edge the candidate misses
print("1024 edges: cand %d  ref %d   FP %d (%.1f%% of cand)  FN %d (%.1f%% of ref)"
      % (ec.sum(), er.sum(), FP.sum(), 100 * FP.sum() / ec.sum(),
         FN.sum(), 100 * FN.sum() / er.sum()))
print()
print("%-11s %7s | %6s %6s | %6s %6s | %6s %6s | %7s %7s"
      % ("region", "px", "cEdg%", "rEdg%", "cSd", "rSd", "cMean", "rMean", "FP", "FN"))
for name, m in REG:
    n = m.sum()
    if n < 500:
        continue
    print("%-11s %7d | %5.1f%% %5.1f%% | %.4f %.4f | %.4f %.4f | %7d %7d"
          % (name, n, 100 * ec[m].mean(), 100 * er[m].mean(),
             g[m].std(), h[m].std(), g[m].mean(), h[m].mean(),
             FP[m].sum(), FN[m].sum()))

# ---- high-pass texture energy (lighting ramp removed) --------------------------
print()
print("high-pass (minus 12px box mean) sd, and gradient density above 4/255:")
gh = g - F.box_mean(g, 13); hh = h - F.box_mean(h, 13)
def graddens(x):
    p = np.pad(x, 1, mode="edge")
    gx_ = p[1:-1, 2:] - p[1:-1, :-2]; gy_ = p[2:, 1:-1] - p[:-2, 1:-1]
    return np.hypot(gx_, gy_) > 4 / 255
dc, dr = graddens(g), graddens(h)
for name, m in REG:
    if m.sum() < 500:
        continue
    print("  %-11s cand sd %.4f  ref sd %.4f   |  cand %.1f%%  ref %.1f%%"
          % (name, gh[m].std(), hh[m].std(), 100 * dc[m].mean(), 100 * dr[m].mean()))

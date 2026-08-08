"""r12 diagnostic 5: are C2's iron-face Sobel edges ON the face, or at the mask rim?

The FN pool on the top face did not move when the grit landed. Either the metric's
threshold (a 0.10 L step) is far above the grit's amplitude, or those reference edges
are not on the face at all - they are the reference's own block silhouette falling
inside a mask cut from OURS, which is ~1.5 cells out of register. Erode and see.
"""
import sys, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

g = np.load("d_g.npy"); h = np.load("d_h.npy")
TOP = np.load("d_topface.npy")
ec, er = F.sobel_edges(g), F.sobel_edges(h)

def erode(m, r):
    return ~F.dilate(~m, r)

print("%-10s %8s | %8s %8s | %8s %8s" % ("erode", "px", "cEdg%", "rEdg%", "cHP-sd", "rHP-sd"))
gh = g - F.box_mean(g, 13); hh = h - F.box_mean(h, 13)
for r in (0, 6, 14, 26, 40):
    m = erode(TOP, r) if r else TOP
    if m.sum() < 400:
        break
    print("%-10d %8d | %7.2f%% %7.2f%% | %8.4f %8.4f"
          % (r, m.sum(), 100 * ec[m].mean(), 100 * er[m].mean(), gh[m].std(), hh[m].std()))

# how big a step does the metric's threshold actually ask for?
core = erode(TOP, 26)
for nm, x in (("cand", g), ("ref ", h)):
    p = np.pad(x, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    mag = np.hypot(gx, gy)[core]
    print("%s face-core sobel mag: mean %.4f  p90 %.4f  p99 %.4f  p99.9 %.4f  >0.40 %.2f%%"
          % (nm, mag.mean(), np.percentile(mag, 90), np.percentile(mag, 99),
             np.percentile(mag, 99.9), 100 * (mag > 0.40).mean()))

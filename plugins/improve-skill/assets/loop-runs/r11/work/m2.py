"""Proper masks, then the same partition. m1's block mask was the union of two
dark-thresholds dilated, which conflates the two blocks' silhouette mismatch with
each block's own interior. Split them: each image's own block by flood fill from a
seed inside it, the overlap, and the mismatch collar.
"""
import sys, pathlib, math, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

W = 1024
g = np.load("g1024.npy"); h = np.load("h1024.npy")


def flood(dark, seed):
    m = np.zeros_like(dark)
    m[seed[1], seed[0]] = True
    while True:
        n = F.dilate(m, 1) & dark
        if n.sum() == m.sum():
            return m
        m = n


bg = flood(g < 0.45, (500, 400))
bh = flood(h < 0.45, (500, 400))
np.save("bg.npy", bg); np.save("bh.npy", bh)
print(f"cand block {100*bg.mean():.2f}% of tile   ref block {100*bh.mean():.2f}%   "
      f"IoU {(bg & bh).sum() / (bg | bh).sum():.3f}")

ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
AX = 543.0 - UX * 320.0
AY = 604.0 - UY * 320.0
yy, xx = np.mgrid[0:W, 0:W].astype(float)
ly = NX * (xx - AX) + NY * (yy - AY)
r_key = np.hypot(xx - 75.0, yy - 25.0)
np.save("ly.npy", ly); np.save("rkey.npy", r_key)

rim = F.rim_mask(W)
subj = F.dilate(bg | bh, 6)                 # either block, plus a 6px collar
band = np.abs(ly) < 34
rough = (ly > 0) & ~subj & ~rim & ~band
trued = (ly < 0) & ~subj & ~rim & ~band
np.save("rough.npy", rough); np.save("trued.npy", trued)

ec, er = F.sobel_edges(g) & ~rim, F.sobel_edges(h) & ~rim
mc, mr = ec & F.dilate(er), er & F.dilate(ec)
REG = {"rough ground": rough, "trued ground": trued,
       "both blocks": bg & bh & ~rim, "cand block only": bg & ~bh & ~rim,
       "ref block only": bh & ~bg & ~rim, "hone band": band & ~rim & ~subj,
       "collar": subj & ~(bg | bh) & ~rim}
print(f"\n{'region':17s} {'px%':>5s} {'cand e':>7s} {'ref e':>7s} {'cand d%':>8s} {'ref d%':>8s}")
for name, m in REG.items():
    n = max(m.sum(), 1)
    print(f"{name:17s} {100*n/W/W:5.1f} {(ec&m).sum():7d} {(er&m).sum():7d} "
          f"{100*(ec&m).sum()/n:8.2f} {100*(er&m).sum()/n:8.2f}")
print(f"{'TOTAL':17s} {'':5s} {ec.sum():7d} {er.sum():7d}")
print(f"prec {mc.sum()/ec.sum():.4f}  rec {mr.sum()/er.sum():.4f}  "
      f"f1 {2*(mc.sum()/ec.sum())*(mr.sum()/er.sum())/((mc.sum()/ec.sum())+(mr.sum()/er.sum())):.4f}")

print("\nrough ground by radius from key (75,25):")
print(f"{'r':>9s} {'px':>7s} {'cand d%':>8s} {'ref d%':>8s} {'cand L':>7s} {'ref L':>7s}")
for lo in range(0, 1200, 100):
    m = rough & (r_key >= lo) & (r_key < lo + 100)
    if m.sum() < 500: continue
    print(f"{lo:4d}-{lo+100:4d} {m.sum():7d} {100*(ec&m).sum()/m.sum():8.2f} "
          f"{100*(er&m).sum()/m.sum():8.2f} {g[m].mean():7.3f} {h[m].mean():7.3f}")

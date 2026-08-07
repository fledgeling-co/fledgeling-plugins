"""Where do the edges live, region by region, in each image?

The r10 gate bought edge_f1 0.0746 -> 0.1574 with the grain round, but precision
is still 0.063 and recall 0.042: 94% of our marks are nowhere near one of the
reference's, and 96% of the reference's are unmatched. Partition both edge sets by
region (rough ground / trued ground / block / curl / hone band) and by radius from
the fitted key at (75, 25), so the round knows whether the fault is missing marks,
misplaced marks, or marks on a plane that should be bare.
"""
import sys, pathlib, math, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
g = F.to_gray(F.render_candidate(A / "icon.svg", 1024))
h = F.to_gray(F.normalise_reference(A / "icon-engineC-f5665d-2.png", 1024))
np.save("g1024.npy", g); np.save("h1024.npy", h)

W = 1024
ANG = math.radians(33.0)
UX, UY = math.cos(ANG), -math.sin(ANG)
NX, NY = -math.sin(ANG), -math.cos(ANG)
EDGE_MID = (543.0, 604.0); BLADE_LEN = 640.0
AX = EDGE_MID[0] - UX * BLADE_LEN / 2
AY = EDGE_MID[1] - UY * BLADE_LEN / 2
yy, xx = np.mgrid[0:W, 0:W].astype(float)
ly = NX * (xx - AX) + NY * (yy - AY)
lx = UX * (xx - AX) + UY * (yy - AY)
r_key = np.hypot(xx - 75.0, yy - 25.0)

# block: dark in the candidate; C2's block is dark too. Use each image's own dark
# pixels dilated, so a mask fault cannot leak the block into a ground statistic.
def block_mask(img):
    m = img < 0.42
    return F.dilate(m, 4)
bm_g, bm_h = block_mask(g), block_mask(h)
block = bm_g | bm_h
rim = F.rim_mask(W)
band = np.abs(ly) < 34            # the hone band: not in scope, masked out everywhere
rough = (ly > 0) & ~block & ~rim & ~band
trued = (ly < 0) & ~block & ~rim & ~band

ec, er = F.sobel_edges(g) & ~rim, F.sobel_edges(h) & ~rim
mc, mr = ec & F.dilate(er), er & F.dilate(ec)     # matched, exactly as edge_f1 counts

print(f"cand edges {ec.sum():6d}  matched {mc.sum():5d}  prec {mc.sum()/ec.sum():.4f}")
print(f"ref  edges {er.sum():6d}  matched {mr.sum():5d}  rec  {mr.sum()/er.sum():.4f}")
print()
REG = {"rough ground": rough, "trued ground": trued, "block(+4px)": block & ~rim,
       "hone band": band & ~rim}
print(f"{'region':14s} {'px%':>5s} {'cand e':>7s} {'ref e':>7s} "
      f"{'cand d%':>8s} {'ref d%':>8s} {'unmatched cand':>15s} {'unmatched ref':>14s}")
for name, m in REG.items():
    n = m.sum()
    print(f"{name:14s} {100*n/W/W:5.1f} {(ec&m).sum():7d} {(er&m).sum():7d} "
          f"{100*(ec&m).sum()/n:8.2f} {100*(er&m).sum()/n:8.2f} "
          f"{(ec&m&~mc).sum():15d} {(er&m&~mr).sum():14d}")

print("\nrough ground, by radius from the key at (75,25):")
print(f"{'r':>9s} {'px':>7s} {'cand d%':>8s} {'ref d%':>8s} {'cand |g|':>9s} {'ref |g|':>9s}")
def gradmag(img):
    p = np.pad(img, 1, mode="edge")
    gx = (p[:-2, 2:] + 2*p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2*p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2*p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0
Gc, Gh = gradmag(g), gradmag(h)
for lo in range(0, 1100, 100):
    m = rough & (r_key >= lo) & (r_key < lo + 100)
    if m.sum() < 400: continue
    print(f"{lo:4d}-{lo+100:4d} {m.sum():7d} {100*(ec&m).sum()/m.sum():8.2f} "
          f"{100*(er&m).sum()/m.sum():8.2f} {Gc[m].mean():9.4f} {Gh[m].mean():9.4f}")
print("\ntrued ground, by radius:")
for lo in range(0, 1600, 150):
    m = trued & (r_key >= lo) & (r_key < lo + 150)
    if m.sum() < 400: continue
    print(f"{lo:4d}-{lo+150:4d} {m.sum():7d} {100*(ec&m).sum()/m.sum():8.2f} "
          f"{100*(er&m).sum()/m.sum():8.2f} {Gc[m].mean():9.4f} {Gh[m].mean():9.4f}")

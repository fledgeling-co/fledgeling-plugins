"""What kind of thing is C2's curl, materially - opaque sheet or translucent one?

r18 fixed the curl's BRIGHT end (p90/p99 above its own board now match C2 to 0.006)
and left the mid-tone open: inside the footprint C2's median sits +0.033 above its
board where ours sits -0.038 below. w1 says the same feature still owns the only
in-class 32px artefact left - 4 FP cells on the roll's upper-left rim, |grad|
0.106-0.120 against C2's 0.046-0.082, cleared entirely by SHAVING=0.

Peak brightness is therefore not what is making that rim an edge. Two candidates:
  (a) the silhouette is too abrupt - C2's rim transition is spread over more px;
  (b) the body is opaque where C2's is a thin translucent sheet, so C2's inside
      luminance is the board's, modulated, and never steps away from it.
Both are measurable. C2's rims were FITTED in round 8 (near centre (294,253) R 115,
far centre (359,186) R 121), so C2's own footprint can be built analytically rather
than borrowed from our registration.
"""
import subprocess
import tempfile
import pathlib
import math
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def nat(svg, s=1024):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


def bilinear(g, x, y):
    x0, y0 = int(math.floor(x)), int(math.floor(y))
    if x0 < 0 or y0 < 0 or x0 + 1 >= g.shape[1] or y0 + 1 >= g.shape[0]:
        return float("nan")
    fx, fy = x - x0, y - y0
    return float((g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx) * (1 - fy)
                 + (g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx) * fy)


ref = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
ours = nat("icon.svg")

# --- 1. rim profiles, each in its OWN roll's frame ---------------------------
# ours: CURL_C (308,278) R 115.  C2: near rim (294,253) R 115 (round-8 fit).
CASES = (("ours", ours, (308.0, 278.0), 115.0), ("C2  ", ref, (294.0, 253.0), 115.0))
print("radial profiles across the roll's upper-left rim, sampled every 3px")
print("(r is distance from the roll's own centre; the rim is at r=R)")
for bearing in (200, 215, 230, 245):   # screen degrees, up-left quadrant
    th = math.radians(bearing)
    dx, dy = math.cos(th), math.sin(th)
    print("\n  bearing %d deg" % bearing)
    for nm, g, c, R in CASES:
        vals = []
        for k in range(-16, 17):
            r = R + k * 3.0
            vals.append(bilinear(g, c[0] + dx * r, c[1] + dy * r))
        inside = [v for v in vals[:14] if v == v]      # r < R-6
        outside = [v for v in vals[19:] if v == v]     # r > R+9
        step = max(vals[10:23]) - min(vals[10:23])
        print("    %s in %.3f  out %.3f  |step across rim| %.3f  worst 3px jump %.3f"
              % (nm, np.mean(inside), np.mean(outside), step,
                 max(abs(vals[i + 1] - vals[i]) for i in range(10, 22))))


# --- 2. footprint statistics, each image's own roll -------------------------
def disc(c, R, shape=(1024, 1024)):
    y, x = np.mgrid[0:shape[0], 0:shape[1]]
    return (x - c[0]) ** 2 + (y - c[1]) ** 2 <= R * R


def swept(c0, R0, c1, R1):
    """union of the two rim discs and the band between them: a hoop seen near end-on"""
    m = disc(c0, R0) | disc(c1, R1)
    n = 24
    for i in range(1, n):
        t = i / n
        m |= disc((c0[0] + (c1[0] - c0[0]) * t, c0[1] + (c1[1] - c0[1]) * t), R0 + (R1 - R0) * t)
    return m


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def grow(m, px, step=5):
    out = m.copy()
    for _ in range(px // step):
        out = dilate(out, step)
    return out


def local_sd(g, w=9):
    pad = w // 2
    p = np.pad(g, pad, mode="edge")
    c = np.cumsum(np.cumsum(p, 0), 1)
    c = np.pad(c, ((1, 0), (1, 0)))
    s = c[w:, w:] - c[:-w, w:] - c[w:, :-w] + c[:-w, :-w]
    m1 = (s / (w * w))[:g.shape[0], :g.shape[1]]
    c2 = np.cumsum(np.cumsum(p * p, 0), 1)
    c2 = np.pad(c2, ((1, 0), (1, 0)))
    s2 = c2[w:, w:] - c2[:-w, w:] - c2[w:, :-w] + c2[:-w, :-w]
    m2 = (s2 / (w * w))[:g.shape[0], :g.shape[1]]
    return np.sqrt(np.maximum(m2 - m1 * m1, 0))


M_ref = swept((294.0, 253.0), 115.0, (359.0, 186.0), 121.0)
# ours, from the SHAVING=0 twin, which is the honest footprint for our own build
import os
env = dict(os.environ, SHAVING="0")
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True, env=env)
off = WORK / "var_noshaving.svg"
off.write_bytes(pathlib.Path("icon.svg").read_bytes())
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
g_off = nat(str(off))
M_ours = np.abs(ours - g_off) > 0.02

print("\nfootprint statistics (each image's own roll, its own annulus 10-40px out)")
for nm, g, M in (("ours", ours, M_ours), ("C2  ", ref, M_ref)):
    ring = grow(M, 40) & ~grow(M, 10)
    base = np.median(g[ring])
    sd_in = np.median(local_sd(g)[M])
    sd_out = np.median(local_sd(g)[ring])
    print("  %s  footprint %6d px  annulus median %.4f" % (nm, M.sum(), base))
    print("        inside - board:  p10 %+.4f  p50 %+.4f  p90 %+.4f  p99 %+.4f"
          % tuple(np.percentile(g[M], p) - base for p in (10, 50, 90, 99)))
    print("        local sd (9px):  inside %.4f  annulus %.4f   ratio %.2f"
          % (sd_in, sd_out, sd_in / max(sd_out, 1e-9)))

np.save(WORK / "M_ours.npy", M_ours)
np.save(WORK / "M_ref.npy", M_ref)

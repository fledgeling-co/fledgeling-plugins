"""Re-measure the near shadow off the landmark both images share, not off the mass.

w6's fit is only worth acting on if its profile origin is honest. w5/w6 marched from the
dark mass's CENTROID, so at the block's end caps a ray leaves the silhouette travelling
along the shadow rather than across it, and C2's block is a different size and place, so
the two fans do not sample the same edge. Round 17's note is explicit that this is where
a shadow measurement goes wrong, and it reports contact AGREEING (0.670 vs 0.662 in the
first 8px) where w6 has us 0.068 darker. One of the two is wrong.

So: recover the contact line in each image from the hone - the vermilion line both
images carry along the block's lower-right edge - by fitting its principal axis, march
perpendicular to THAT, and take u=0 where each ray leaves its own dark mass. Rays are
started only from the hone's own extent, so every ray in both fans crosses the long
lower-right edge and none crosses an end cap.
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


def rgbgray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return c, 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def nat(svg, s=1024):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return rgbgray(Image.open(t).convert("RGBA"))


def bil(g, x, y):
    x0, y0 = int(x), int(y)
    if x0 < 1 or y0 < 1 or x0 + 2 >= g.shape[1] or y0 + 2 >= g.shape[0]:
        return float("nan")
    fx, fy = x - x0, y - y0
    return float((g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx) * (1 - fy)
                 + (g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx) * fy)


def hone_axis(c):
    # both grounds are warm - C2's r-b runs to 0.20 at p99 over open board - so the
    # hone has to be picked out by SATURATION, not warmth: r-b > 0.30 AND r-g > 0.15
    # isolates 4.5k px in C2 on a 39.0 deg axis and 13.6k in ours on 33.4, which are
    # each image's own ground line to a tenth of a degree.
    warm = (c[..., 0] - c[..., 2] > 0.30) & (c[..., 0] - c[..., 1] > 0.15)
    ys, xs = np.nonzero(warm)
    x0, y0 = xs.mean(), ys.mean()
    u = np.stack([xs - x0, ys - y0])
    w, v = np.linalg.eigh(u @ u.T / len(xs))
    ax, ay = v[:, np.argmax(w)]
    if ax < 0:
        ax, ay = -ax, -ay
    return (x0, y0), (ax, ay), warm.sum(), math.degrees(math.atan2(-ay, ax))


def profile(c, g, reach=260, dark=0.45):
    (x0, y0), (ax, ay), n, deg = hone_axis(c)
    dx, dy = -ay, ax                     # perpendicular; +y is down-screen
    if dy < 0:
        dx, dy = -dx, -dy                # point down-right, away from the block
    D = g < dark
    rows = []
    for k in range(-22, 23):
        sx, sy = x0 + ax * k * 9.0, y0 + ay * k * 9.0
        # step back onto the block, then march out across the contact line
        bx, by = sx - dx * 40.0, sy - dy * 40.0
        if not (0 <= int(bx) < 1024 and 0 <= int(by) < 1024) or not D[int(by), int(bx)]:
            continue
        t = 0.0
        while t < 300 and D[int(min(1023, max(0, by + dy * t))), int(min(1023, max(0, bx + dx * t)))]:
            t += 1.0
        row = [bil(g, bx + dx * (t + u), by + dy * (t + u)) for u in range(reach)]
        if any(v != v for v in row):
            continue
        rows.append(row)
    m = np.median(np.array(rows), axis=0)
    return m / np.median(m[200:260]), len(rows), deg, n


BANDS = ((0, 8), (8, 16), (16, 32), (32, 64), (64, 96), (96, 128), (128, 192))
REFC, REFG = rgbgray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
OURC, OURG = nat("icon.svg")
NCC, NCG = nat(str(WORK / "var_nocast.svg"))

res = {}
for nm, c, g in (("ours", OURC, OURG), ("nocast", NCC, NCG), ("C2", REFC, REFG)):
    p, nr, deg, nw = profile(c, g)
    res[nm] = p
    print("%-7s hone %6d px, axis %.1f deg, %d rays" % (nm, nw, deg, nr))

print("\nnormalised by own far field, u = px out from where the ray leaves the block")
print("   u      ours   nocast     C2    ours-C2")
for u in list(range(0, 40, 4)) + list(range(40, 200, 8)):
    print("  %3d   %6.3f  %6.3f  %6.3f   %+.3f"
          % (u, res["ours"][u], res["nocast"][u], res["C2"][u], res["ours"][u] - res["C2"][u]))

print("\n32px bands (what a cell sees) and the step into each")
print("   band      ours   step  |    C2    step  |  ours-C2")
prev = {}
for a, b in BANDS:
    line = "  %3d-%3d" % (a, b)
    for n in ("ours", "C2"):
        v = res[n][a:b].mean()
        line += "   %6.3f %+.3f |" % (v, 0.0 if n not in prev else v - prev[n])
        prev[n] = v
    print(line + "   %+.3f" % (res["ours"][a:b].mean() - res["C2"][a:b].mean()))
for n in ("ours", "nocast", "C2"):
    integ = sum((1 - res[n][a:b].mean()) * (b - a) for a, b in BANDS)
    print("  %-7s deficit integral over 0-192px: %.1f" % (n, integ))
np.save(WORK / "prof_ours.npy", res["ours"])
np.save(WORK / "prof_ref.npy", res["C2"])

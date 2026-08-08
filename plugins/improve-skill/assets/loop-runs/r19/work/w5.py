"""The block's shadow profile, perpendicular to its contact line, at 32px SCALE.

w4 isolated the cast layer at 32px and it is a one-cell dark stripe: -0.115 at (10,24),
-0.129 at (11,23), -0.121 at (14,21), -0.132 at (19,18), and under -0.03 one cell either
side. A 26px sigma is 0.8 of a 32px cell, so the whole layer lives inside one cell. C2's
grid over the same ground ramps monotonically over four or five cells.

r17 measured contact (agrees) and far field (agrees, after the halo). This asks the
question those two miss: what does the profile do in between, and what does a 32px cell
see of it. Rays are marched perpendicular to each image's OWN contact line - ours at the
blade's 33 deg, C2's at the 41 deg r17 recovered - starting where each ray leaves that
image's own dark mask, so the comparison never touches registration. Each profile is
normalised by its own far field, which is what lets it survive the 0.18 palette offset.
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


def bil(g, x, y):
    x0, y0 = int(x), int(y)
    if x0 < 0 or y0 < 0 or x0 + 1 >= g.shape[1] or y0 + 1 >= g.shape[0]:
        return float("nan")
    fx, fy = x - x0, y - y0
    return float((g[y0, x0] * (1 - fx) + g[y0, x0 + 1] * fx) * (1 - fy)
                 + (g[y0 + 1, x0] * (1 - fx) + g[y0 + 1, x0 + 1] * fx) * fy)


def profile(g, deg, dark=0.45, rays=41, reach=260):
    """march down-right from inside the dark mass, perpendicular to the contact line"""
    th = math.radians(deg)
    ax, ay = math.cos(th), -math.sin(th)           # along the block
    dx, dy = -ay, ax                               # perpendicular, down-right
    D = g < dark
    ys, xs = np.nonzero(D)
    cx, cy = xs.mean(), ys.mean()
    out = []
    for k in range(-(rays // 2), rays // 2 + 1):
        sx, sy = cx + ax * k * 9.0, cy + ay * k * 9.0
        if not (0 <= int(sx) < 1024 and 0 <= int(sy) < 1024) or not D[int(sy), int(sx)]:
            continue
        t = 0.0
        while t < 400 and D[int(min(1023, max(0, sy + dy * t))), int(min(1023, max(0, sx + dx * t)))]:
            t += 1.0
        if t >= 400:
            continue
        row = [bil(g, sx + dx * (t + u), sy + dy * (t + u)) for u in range(0, reach)]
        if any(v != v for v in row):
            continue
        out.append(row)
    return np.array(out)


REF = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
OURS = nat("icon.svg")
NOCAST = nat(str(WORK / "var_nocast.svg"))

CASES = (("ours", OURS, 33.0), ("nocast", NOCAST, 33.0), ("C2", REF, 41.0))
prof = {}
for nm, g, deg in CASES:
    p = profile(g, deg)
    m = np.median(p, axis=0)
    far = np.median(m[200:260])
    prof[nm] = m / far
    print("%-7s %2d rays, far field %.4f" % (nm, p.shape[0], far))

print("\nnormalised profile, own far field = 1.000 (u = px out from the silhouette)")
print("   u    " + "".join("%9s" % n for n, _, _ in CASES))
for u in range(0, 200, 8):
    print("  %3d  " % u + "".join("%9.3f" % prof[n][u] for n, _, _ in CASES))

print("\nwhat a 32px cell sees: each row is one 32px band, mean of the profile over it,")
print("and the step from the band before it (the quantity the 32px Sobel reads)")
print("  band(px)      ours     step |    C2      step |   nocast   step")
prev = {n: None for n in prof}
for b in range(0, 6):
    lo, hi = b * 32, b * 32 + 32
    line = "  %3d-%3d  " % (lo, hi)
    for n in ("ours", "C2", "nocast"):
        v = prof[n][lo:hi].mean()
        s = 0.0 if prev[n] is None else v - prev[n]
        prev[n] = v
        line += "  %6.3f  %+.3f |" % (v, s)
    print(line)

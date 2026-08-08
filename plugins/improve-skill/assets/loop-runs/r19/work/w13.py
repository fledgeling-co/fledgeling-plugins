"""Does C2 carry a lit arris along the plane's top-back edge, and do we?

The 1024 crops show one difference that is a material relationship rather than a placement:
along the top-back edge of C2's plane there is a continuous bright thread, near-white,
running the full length and separating the dark body from the board. Ours has no such line -
our block's back edge is a plain antialiased step from board to dark.

An arris catches the light because it is the one place on the body whose normal sweeps
through every orientation between the top face and the back face, so it must pass through
the mirror angle. It is also exactly the feature that keeps a dark mass legible when it is
four cells wide: a one-px lip at 1024 is a quarter-cell at 32 and an eighth at 16, and it
lands on the boundary cell as a brightening that sharpens the step rather than blurring it.

Measure it the same way as w7 - off the hone axis each image owns, marching perpendicular,
u=0 where the ray enters that image's own dark mass, normalised by that image's own board -
but marching from the OTHER side, up-left, so the profile crosses the back edge.
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


def axis(c):
    warm = (c[..., 0] - c[..., 2] > 0.30) & (c[..., 0] - c[..., 1] > 0.15)
    ys, xs = np.nonzero(warm)
    x0, y0 = xs.mean(), ys.mean()
    u = np.stack([xs - x0, ys - y0])
    w, v = np.linalg.eigh(u @ u.T / len(xs))
    ax, ay = v[:, np.argmax(w)]
    if ax < 0:
        ax, ay = -ax, -ay
    return (x0, y0), (ax, ay), math.degrees(math.atan2(-ay, ax))


def backedge(c, g, out=90, dark=0.45):
    """profile across the plane's TOP-BACK edge; u=0 is the last board px before the mass"""
    (x0, y0), (ax, ay), deg = axis(c)
    dx, dy = -ay, ax
    if dy > 0:
        dx, dy = -dx, -dy            # point up-LEFT, across the back edge
    D = g < dark
    rows = []
    for k in range(-24, 25):
        # the hone is a BRIGHT line, so it is not in D; step 40px up-left off it, onto the
        # top face, and only then march - otherwise the ray never enters the mass at all
        sx, sy = x0 + ax * k * 9.0 + dx * 40.0, y0 + ay * k * 9.0 + dy * 40.0
        if not (0 <= int(sx) < 1024 and 0 <= int(sy) < 1024) or not D[int(sy), int(sx)]:
            continue
        t = 0.0
        # walk up-left out of the mass until the ray is clear of it
        while t < 420 and (not (0 <= int(sy + dy * t) < 1024 and 0 <= int(sx + dx * t) < 1024)
                           or D[int(sy + dy * t), int(sx + dx * t)]):
            t += 1.0
        if t >= 420:
            continue
        bx, by = sx + dx * t, sy + dy * t           # first clear px = u 0
        row = [bil(g, bx + dx * u, by + dy * u) for u in range(out)]
        deep = bil(g, bx - dx * 14.0, by - dy * 14.0)   # 14px inside the mass
        if any(v != v for v in row) or deep != deep:
            continue
        rows.append(row + [deep])
    a = np.array(rows)
    m = np.median(a, axis=0)
    return m[:-1] / np.median(m[60:88]), m[-1] / np.median(m[60:88]), len(rows), deg


REFC, REFG = rgbgray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((1024, 1024), Image.LANCZOS))
OURC, OURG = nat("icon.svg")

res = {}
for nm, c, g in (("ours", OURC, OURG), ("C2", REFC, REFG)):
    p, deep, n, deg = backedge(c, g)
    res[nm] = p
    print("%-5s %2d rays on a %.1f deg axis; body 14px inside the edge sits at %.3f of board"
          % (nm, n, deg, deep))

print("\nu = px OUT from the plane's back edge, normalised by each image's own board at 60-88px")
print("   u      ours      C2    ours-C2")
for u in list(range(0, 16)) + list(range(16, 60, 4)):
    print("  %3d   %6.3f  %6.3f   %+.3f" % (u, res["ours"][u], res["C2"][u], res["ours"][u] - res["C2"][u]))
for nm in ("ours", "C2"):
    p = res[nm]
    i = int(np.argmax(p[:24]))
    print("  %-5s peak within 24px of the edge: %.3f at u=%d;  board level %.3f;  lip %+.3f"
          % (nm, p[i], i, p[40:60].mean(), p[i] - p[40:60].mean()))
np.save(WORK / "back_ours.npy", res["ours"])
np.save(WORK / "back_ref.npy", res["C2"])

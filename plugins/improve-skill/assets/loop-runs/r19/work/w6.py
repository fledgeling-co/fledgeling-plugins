"""Fit the near shadow's DISTRIBUTION to C2's, holding its total roughly constant.

w5's finding, in the only frame that matters for a 32px false edge: what a 32px cell
sees. Normalised to each image's own far field,

    band     ours    C2      ours-C2
    0- 32   0.633   0.652    -0.019
   32- 64   0.816   0.780    +0.036
   64- 96   0.900   0.873    +0.027
   96-128   0.952   0.933    +0.019

so the first step ours +0.183 against C2's +0.128, 1.43x, and every later step already
agrees to 0.01. Our near shadow is too CONCENTRATED, not too dark and not too short:
density piled into the first cell and missing from the second and third. That is a
sub-cell-wide trench, and at 32px a trench is an edge.

The two layers that own those bands are separable - CONTACT (sigma 9, 15px out along the
perpendicular, op 0.42) owns 0-32, CAST (sigma 26, 45px out, op 0.35) owns 32-96 - so the
repair is a redistribution between them, not more shadow. Sweep both and fit the BAND
PROFILE, not the score. Total integral is reported for every point: if it moves much,
the edit has stopped being a redistribution and started dimming the plane, which is the
palette's job and not this round's.
"""
import subprocess
import tempfile
import pathlib
import math
import re
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")
SRC = pathlib.Path("build_icon.py").read_text()
BANDS = ((0, 8), (8, 16), (16, 32), (32, 64), (64, 96), (96, 128), (128, 192))


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
    th = math.radians(deg)
    ax, ay = math.cos(th), -math.sin(th)
    dx, dy = -ay, ax
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
    m = np.median(np.array(out), axis=0)
    return m / np.median(m[200:260])


def bandvec(p):
    return np.array([p[a:b].mean() for a, b in BANDS])


def build(name, subs):
    src = SRC
    for pat, rep in subs:
        src, n = re.subn(pat, rep, src, count=1)
        assert n == 1, (name, pat)
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                      "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".")
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return str(out)


ref_b = bandvec(profile(gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
                             .resize((1024, 1024), Image.LANCZOS)), 41.0))
print("C2 bands:      " + " ".join("%.3f" % v for v in ref_b))
print("               " + " ".join("%7s" % ("%d-%d" % b) for b in BANDS))


def report(tag, svg):
    b = bandvec(profile(nat(svg), 33.0))
    resid = np.abs(b - ref_b).sum()
    # deficit integral: how much light the whole shadow removes, 0-192px
    integ = (1.0 - np.array([b[i] for i in range(len(BANDS))])) @ np.array([e - s for s, e in BANDS])
    print("  %-18s " % tag + " ".join("%.3f" % v for v in b)
          + "   |resid| %.3f  step1 %+.3f  integral %.1f" % (resid, b[3] - b[2], integ))
    return resid


print("\nbaseline and the redistribution grid (CONTACT_OP owns 0-32, CAST_OP owns 32-96):")
report("baseline", "icon.svg")
best = []
for cop in (0.42, 0.34, 0.26):
    for kop in (0.35, 0.44, 0.52):
        if (cop, kop) == (0.42, 0.35):
            continue
        tag = "c%02d_k%02d" % (cop * 100, kop * 100)
        svg = build(tag, [(r"CONTACT_OP = 0\.42", "CONTACT_OP = %.2f" % cop),
                          (r"CAST_OP = 0\.35", "CAST_OP = %.2f" % kop)])
        best.append((report(tag, svg), tag))
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)
print("\nbest by band residual: " + ", ".join("%s %.3f" % (t, r) for r, t in sorted(best)[:4]))

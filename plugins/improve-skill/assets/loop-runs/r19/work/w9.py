"""Is the roll's own 32px contrast too strong, or only in the wrong place?

w1 says the roll owns 4 of the 20 FP cells - (7,7) (8,7) (9,7) (6,8), ours 0.106-0.120
against C2's 0.046-0.082 in the SAME cells - and 6 of the 13 FN cells, all of them at
canvas y 96-192, above our roll entirely. Both sets are consistent with a displacement
rather than a material fault: C2's fitted rims put its roll at (294,253) and (359,186),
ours are at (308,278) and (243,345), so ours sits about 50px left and 98px low - three
32px cells of it - and is drawn to a shorter sweep.

If that is all it is, then our roll's OWN internal contrast, measured in its own frame,
should sit at or under C2's, and there is nothing in this class to repair on it. If ours
runs hotter than C2's on its own ground, there is.
"""
import subprocess
import tempfile
import pathlib
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


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def disc(c, R, n=32):
    y, x = np.mgrid[0:n, 0:n]
    return ((x + 0.5) * (1024 / n) - c[0]) ** 2 + ((y + 0.5) * (1024 / n) - c[1]) ** 2 <= R * R


def hoop(c0, R0, c1, R1, n=32):
    m = disc(c0, R0, n) | disc(c1, R1, n)
    for i in range(1, 25):
        t = i / 25
        m |= disc((c0[0] + (c1[0] - c0[0]) * t, c0[1] + (c1[1] - c0[1]) * t), R0 + (R1 - R0) * t, n)
    return m


REF = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")
for s in (32, 16):
    ours = nat("icon.svg", s)
    off = nat(str(WORK / "var_noshaving.svg"), s)
    ref = gray(REF.resize((s, s), Image.LANCZOS))
    M_ours = np.abs(ours - off) > 0.004                        # our roll, from its own twin
    M_ref = hoop((294.0, 253.0), 115.0, (359.0, 186.0), 121.0, s)   # C2's, from the round-8 rim fit
    print("\n%dpx   our roll %d cells, C2's %d cells" % (s, M_ours.sum(), M_ref.sum()))
    for nm, g, M in (("ours", ours, M_ours), ("C2  ", ref, M_ref)):
        sg = sobel(g)[M]
        v = g[M]
        print("   %s |grad| in its own roll: p50 %.3f  p90 %.3f  max %.3f   cells over 0.10: %d"
              % (nm, np.percentile(sg, 50), np.percentile(sg, 90), sg.max(), (sg > 0.10).sum()))
        print("        luminance in its own roll: p10 %.3f  p50 %.3f  p90 %.3f  range %.3f"
              % (np.percentile(v, 10), np.percentile(v, 50), np.percentile(v, 90),
                 np.percentile(v, 90) - np.percentile(v, 10)))

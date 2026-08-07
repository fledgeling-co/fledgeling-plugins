"""Which layer owns each 32px false positive, by building the tile without it.

Attribution by eye or by coordinate has cost this loop rounds before (r17's
"the grain aliases" hypothesis died to a re-measure). So each candidate layer is
switched off in a COPY of the generator, the tile is rebuilt, and the FP set is
recomputed: an FP that survives with the layer gone was never that layer's.
"""
import subprocess
import tempfile
import pathlib
import re
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r18/work")
SRC = pathlib.Path("build_icon.py").read_text()


def gray(im):
    a = np.asarray(im.convert("RGBA"), float) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + NEUTRAL * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


def sobel(g):
    p = np.pad(g, 1, mode="edge")
    gx = (p[:-2, 2:] + 2 * p[1:-1, 2:] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[1:-1, :-2] + p[2:, :-2])
    gy = (p[2:, :-2] + 2 * p[2:, 1:-1] + p[2:, 2:]) - (p[:-2, :-2] + 2 * p[:-2, 1:-1] + p[:-2, 2:])
    return np.hypot(gx, gy) / 4.0


def dilate(m, r=1):
    out = m.copy()
    for dy in range(-r, r + 1):
        for dx in range(-r, r + 1):
            out |= np.roll(np.roll(m, dy, 0), dx, 1)
    return out


def rim_mask(n, thresh=0.86):
    y, x = np.mgrid[0:n, 0:n]
    u = (x - (n - 1) / 2) / max((n - 1) / 2, 1)
    v = (y - (n - 1) / 2) / max((n - 1) / 2, 1)
    return (np.abs(u) ** 5 + np.abs(v) ** 5) ** 0.2 > thresh


def build(name, subs):
    src = SRC
    for pat, rep in subs:
        new, n = re.subn(pat, rep, src, count=1)
        assert n == 1, (name, pat)
        src = new
    # the copy lives in work/, so point it back at the real asset directory
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                      "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".")
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return out


def edges32(svg):
    t = TMP / (pathlib.Path(svg).stem + "-32.png")
    subprocess.run(["rsvg-convert", "-w", "32", "-h", "32", str(svg), "-o", str(t)], check=True)
    return sobel(gray(Image.open(t).convert("RGBA")))


ref = gray(Image.open("icon-engineC-f5665d-2.png").convert("RGBA").resize((32, 32), Image.LANCZOS))
gb = sobel(ref)
keep = ~rim_mask(32)
eb = (gb > 0.10) & keep
deb = dilate(eb)

base = edges32("icon.svg")
ea = (base > 0.10) & keep
fp = ea & ~deb
print("baseline FP %d" % fp.sum())

VARIANTS = {
    "nograin": [(r"GRAIN_AMP_A = 0\.055", "GRAIN_AMP_A = 0.0001"),
                (r"GRAIN_AMP_B = 0\.055", "GRAIN_AMP_B = 0.0001")],
    "nocurl": [(r'SHAVING = os\.environ\.get\("SHAVING", "1"\) == "1"', "SHAVING = False")],
    "nocast": [(r"CAST_OP = 0\.35", "CAST_OP = 0.0")],
    "nohalo": [(r"HALO_OP = 0\.30", "HALO_OP = 0.0")],
    "nofibre": [(r"FIBRE_SCALE = 0\.80", "FIBRE_SCALE = 0.0001")],
}

ys, xs = np.nonzero(fp)
cells = list(zip(xs, ys))
table = {}
for name, subs in VARIANTS.items():
    svg = build(name, subs)
    g = edges32(svg)
    table[name] = g
    ea2 = (g > 0.10) & keep
    fp2 = ea2 & ~deb
    gone = fp & ~fp2
    print("  %-8s FP %2d  (removes %2d of the baseline's, adds %2d)"
          % (name, fp2.sum(), gone.sum(), (fp2 & ~fp).sum()))

print("\nper-cell |grad| under each variant (baseline first, ref last):")
hdr = "  cell    base  " + "  ".join("%-8s" % n for n in VARIANTS) + "   ref"
print(hdr)
for x, y in cells:
    print("  (%2d,%2d)  %.3f  " % (x, y, base[y, x])
          + "  ".join("%-8.3f" % table[n][y, x] for n in VARIANTS)
          + "   %.3f" % gb[y, x])
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

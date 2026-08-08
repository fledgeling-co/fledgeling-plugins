"""Where the 32 and 16px error lives NOW, by attribution rather than by eye.

r18 moved OUT_LIT and traded 32px edge_f1 0.9336 -> 0.9171: FP count unchanged at 20,
recall 0.9628 -> 0.9309. So the FP/FN sets have to be rebuilt on the CURRENT master
before anything is authored. Each candidate layer is switched off in a copy of the
generator: an artefact that survives a layer's removal was never that layer's.
"""
import subprocess
import tempfile
import pathlib
import re
import numpy as np
from PIL import Image

NEUTRAL = 128 / 255.0
TMP = pathlib.Path(tempfile.mkdtemp())
WORK = pathlib.Path("loop-runs/r19/work")
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
    src = src.replace("ASSETS = pathlib.Path(__file__).resolve().parent",
                      "ASSETS = pathlib.Path(__file__).resolve().parent.parent.parent.parent")
    p = WORK / ("gen_%s.py" % name)
    p.write_text(src)
    subprocess.run(["python3", str(p)], check=True, capture_output=True, cwd=".")
    out = WORK / ("var_%s.svg" % name)
    out.write_bytes(pathlib.Path("icon.svg").read_bytes())
    return out


def nat(svg, s):
    t = TMP / ("%s-%d.png" % (pathlib.Path(svg).stem, s))
    subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s), str(svg), "-o", str(t)], check=True)
    return gray(Image.open(t).convert("RGBA"))


REF = Image.open("icon-engineC-f5665d-2.png").convert("RGBA")

VARIANTS = {
    "nocurl": [(r'SHAVING = os\.environ\.get\("SHAVING", "1"\) == "1"', "SHAVING = False")],
    "nocast": [(r"CAST_OP = 0\.35", "CAST_OP = 0.0")],
    "nograin": [(r"GRAIN_AMP_A = 0\.055", "GRAIN_AMP_A = 0.0001"),
                (r"GRAIN_AMP_B = 0\.055", "GRAIN_AMP_B = 0.0001")],
    "nofibre": [(r"FIBRE_SCALE = 0\.80", "FIBRE_SCALE = 0.0001")],
    "nostep":  [(r"STEP_CREST = 0\.114", "STEP_CREST = 0.0001")],
}

svgs = {n: str(build(n, s)) for n, s in VARIANTS.items()}
subprocess.run(["python3", "build_icon.py"], check=True, capture_output=True)

for s in (32, 16):
    gb = sobel(gray(REF.resize((s, s), Image.LANCZOS)))
    keep = ~rim_mask(s)
    eb = (gb > 0.10) & keep
    deb = dilate(eb)
    base = nat("icon.svg", s)
    ga = sobel(base)
    ea = (ga > 0.10) & keep
    dea = dilate(ea)
    fp = ea & ~deb
    fn = eb & ~dea
    prec = (ea & deb).sum() / max(ea.sum(), 1)
    rec = (eb & dea).sum() / max(eb.sum(), 1)
    print("\n=== %dpx ===  edges ours %d  ref %d   prec %.4f  rec %.4f  f1 %.4f"
          % (s, ea.sum(), eb.sum(), prec, rec, 2 * prec * rec / max(prec + rec, 1e-9)))
    print("  FP %d   FN %d" % (fp.sum(), fn.sum()))

    tab = {}
    for n, p in svgs.items():
        g2 = sobel(nat(p, s))
        tab[n] = g2
        ea2 = (g2 > 0.10) & keep
        fp2 = ea2 & ~deb
        fn2 = eb & ~dilate(ea2)
        print("   %-8s FP %2d (clears %2d, adds %2d)   FN %2d" %
              (n, fp2.sum(), (fp & ~fp2).sum(), (fp2 & ~fp).sum(), fn2.sum()))

    ys, xs = np.nonzero(fp)
    print("  FP cells: |grad| ours / " + " / ".join(VARIANTS) + " / ref")
    for y, x in zip(ys, xs):
        print("   (%2d,%2d) %.3f  " % (x, y, ga[y, x])
              + " ".join("%.3f" % tab[n][y, x] for n in VARIANTS)
              + "   ref %.3f" % gb[y, x])
    ys, xs = np.nonzero(fn)
    print("  FN cells: ref |grad| / ours")
    for y, x in zip(ys, xs):
        print("   (%2d,%2d) ref %.3f  ours %.3f" % (x, y, gb[y, x], ga[y, x]))

"""Fit the shaving's transmission constants to the reference's measured interior.

Targets, measured on C2 in w12 (its own boxes, its own ground):
    bore seen through the loop      L p10 0.672  med 0.737
    far wall's inner face           L p10 0.625  med 0.673
    the most turned-away passage    L p10 0.668  med 0.700
    ground beside the loop          L p10 0.727  med 0.776
So C2's ribbon interior sits 0.05-0.11 under the ground beside it. Our ground
there measures 0.731, which puts the target at L ~0.63-0.67 median with a floor
near 0.60. Ours currently runs 0.338 median, 0.310 floor.

The inner-face mask is geometry, not colour, so it is captured once from the
shipped build and reused for every trial.
"""
import itertools, pathlib, re, subprocess, sys, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r16/work"
NEUTRAL = 128


def render_svg(path, size=1024):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


def rgb_of(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    if a.shape[2] == 4:
        r, al = a[..., :3], a[..., 3:4]
        a = r * al + (NEUTRAL / 255.0) * (1 - al)
    return a


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


fl = rgb_of(render_svg(W / "flag.svg"))
inner = (fl[..., 0] > 0.85) & (fl[..., 1] < 0.25) & (fl[..., 2] > 0.85)
base = rgb_of(render_svg(A / "icon.svg"))
nocurl = rgb_of(render_svg(W / "no-curl.svg"))
ribbon = np.abs(lum(base) - lum(nocurl)) > 0.004
outer = ribbon & ~inner
np.save(W / "inner.npy", inner)
np.save(W / "ribbon.npy", ribbon)

SRC = (A / "build_icon.py").read_text()


def trial(transmit, bore, ao):
    s = SRC
    s = s.replace("""        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            op = tap""",
                  f"""        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            col = _lerp(col, TRANSMIT, {transmit} * max(0.0, -lam))
            op = tap""")
    s = s.replace("            ao = 1.0 - 0.74 * depth", f"            ao = 1.0 - {ao} * depth")
    s = s.replace("            col = _lerp(col, TRANSMIT, max(0.0, lam) * 0.12)",
                  f"            col = _lerp(col, TRANSMIT, {bore} + {transmit} * max(0.0, lam))")
    p = A / "_trial_build.py"
    p.write_text(s)
    keep = (A / "icon.svg").read_bytes()
    try:
        subprocess.run(["python3", str(p)], cwd=A, check=True, capture_output=True)
        out = W / "trial.svg"
        out.write_bytes((A / "icon.svg").read_bytes())
    finally:
        (A / "icon.svg").write_bytes(keep)
        p.unlink(missing_ok=True)
    g = lum(rgb_of(render_svg(out)))
    return g


print(f"{'T':>5} {'bore':>5} {'ao':>5} | {'inner p10':>9} {'inner med':>9} | "
      f"{'outer p10':>9} {'outer med':>9} | {'ribbon p10':>10} {'ribbon med':>10}")
g = lum(base)
print(f"{'base':>5} {'':>5} {'':>5} | {np.percentile(g[inner],10):9.3f} {np.median(g[inner]):9.3f} | "
      f"{np.percentile(g[outer],10):9.3f} {np.median(g[outer]):9.3f} | "
      f"{np.percentile(g[ribbon],10):10.3f} {np.median(g[ribbon]):10.3f}")
print(f"{'C2':>5} {'':>5} {'':>5} | {0.655:9.3f} {0.703:9.3f} | {'':>9} {'':>9} | "
      f"{0.590:10.3f} {0.702:10.3f}   <- targets")

for T, bore, ao in itertools.product((0.30, 0.42), (0.30, 0.42, 0.54), (0.30, 0.45)):
    g = trial(T, bore, ao)
    print(f"{T:5.2f} {bore:5.2f} {ao:5.2f} | {np.percentile(g[inner],10):9.3f} {np.median(g[inner]):9.3f} | "
          f"{np.percentile(g[outer],10):9.3f} {np.median(g[outer]):9.3f} | "
          f"{np.percentile(g[ribbon],10):10.3f} {np.median(g[ribbon]):10.3f}")

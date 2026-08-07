"""Second pass: the outer face's floor.

The interior is fitted (T 0.42, bore 0.54 -> inner p10 0.649 med 0.698 against C2's
0.655 / 0.703). What is left is the outer face's dark tail: p10 0.512 against C2's
ribbon p10 0.590, median 0.652 against 0.702.

Physically the missing term is the sheet's ambient transmission - the light the
environment pushes through one thickness of shaving regardless of where the key
is. It is a floor, not a lambert, so it is swept on its own with the interior
constants held.
"""
import pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r16/work"
NEUTRAL = 128
T, BORE = 0.42, 0.54


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


inner = np.load(W / "inner.npy")
ribbon = np.load(W / "ribbon.npy")
outer = ribbon & ~inner
ground = lum(rgb_of(render_svg(W / "no-curl.svg")))
SRC = (A / "build_icon.py").read_text()


def trial(sheen):
    s = SRC.replace("""        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            op = tap""",
                    f"""        if outer:
            sh = max(0.0, min(1.0, (lam + 0.18) / 1.16)) ** 1.35
            col = _lerp(OUT_DARK, OUT_LIT, sh)
            col = _lerp(col, TRANSMIT, {sheen} + {T} * max(0.0, -lam))
            op = tap""")
    s = s.replace("            col = _lerp(col, TRANSMIT, max(0.0, lam) * 0.12)",
                  f"            col = _lerp(col, TRANSMIT, {BORE} + {T} * max(0.0, lam))")
    p = A / "_trial_build.py"
    p.write_text(s)
    keep = (A / "icon.svg").read_bytes()
    try:
        subprocess.run(["python3", str(p)], cwd=A, check=True, capture_output=True)
        (W / "trial.svg").write_bytes((A / "icon.svg").read_bytes())
    finally:
        (A / "icon.svg").write_bytes(keep)
        p.unlink(missing_ok=True)
    return lum(rgb_of(render_svg(W / "trial.svg")))


def row(tag, g):
    o, r = g[outer], g[ribbon]
    d = r - ground[ribbon]
    print(f"{tag:>6} | {np.percentile(o,10):6.3f} {np.median(o):6.3f} {np.percentile(o,90):6.3f} "
          f"| {np.percentile(r,10):6.3f} {np.median(r):6.3f} {np.percentile(r,90):6.3f} "
          f"| {(d<-0.15).mean()*100:5.1f}% {(d<-0.25).mean()*100:5.1f}% {(d<-0.35).mean()*100:5.1f}%")


print(f"{'sheen':>6} | {'out p10':>6} {'out med':>6} {'out p90':>6} "
      f"| {'rib p10':>6} {'rib med':>6} {'rib p90':>6} | below ground >.15  >.25  >.35")
row("base", lum(rgb_of(render_svg(A / "icon.svg"))))
print(f"{'C2':>6} | {'':>6} {'':>6} {'':>6} | {0.590:6.3f} {0.702:6.3f} {0.821:6.3f} "
      f"|   2.9%   1.3%   0.0%   <- targets")
for sheen in (0.0, 0.10, 0.18, 0.26):
    row(f"{sheen:.2f}", trial(sheen))

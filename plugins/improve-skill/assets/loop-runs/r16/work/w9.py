"""Does the curl survive to 32 and 16px, and does the reference's?

The curl's exact footprint is recovered by building the tile twice, with and
without it (SHAVING=0), and differencing - no hand-drawn mask. The reference's
is taken from its own visible loop, boxed by hand and checked against the
render.

The question a small-size repair has to answer is not "is the curl there" but
"how many luminance counts separate it from the ground it sits on, at 32 and
16px", because that difference IS the read.
"""
import os, pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r16/work"
REF = A / "icon-engineC-f5665d-2.png"
NEUTRAL = 128


def build(svg_out, shaving="0"):
    """build_icon.py always writes assets/icon.svg, so stash it, build the
    variant, move it aside and rebuild the real one."""
    keep = (A / "icon.svg").read_bytes()
    try:
        subprocess.run(["python3", str(A / "build_icon.py")], cwd=A,
                       env=dict(os.environ, SHAVING=shaving), check=True, capture_output=True)
        svg_out.write_bytes((A / "icon.svg").read_bytes())
    finally:
        (A / "icon.svg").write_bytes(keep)


def render_svg(path, size):
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
        tmp = pathlib.Path(t.name)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), str(path), "-o", str(tmp)], check=True)
    im = Image.open(tmp).convert("RGBA"); tmp.unlink(missing_ok=True); return im


def gray(im):
    a = np.asarray(im, dtype=np.float64) / 255.0
    rgb, al = a[..., :3], a[..., 3:4]
    c = rgb * al + (NEUTRAL / 255.0) * (1 - al)
    return 0.2126 * c[..., 0] + 0.7152 * c[..., 1] + 0.0722 * c[..., 2]


noc = W / "no-curl.svg"
if not noc.exists():
    build(noc, "0")
print("built no-curl.svg" if noc.exists() else "FAILED")

for size in (1024, 32, 16):
    with_ = gray(render_svg(A / "icon.svg", size))
    without = gray(render_svg(noc, size))
    d = with_ - without
    m = np.abs(d) > 0.004
    print(f"== {size}px  curl footprint {m.sum()} px ({m.mean()*100:.2f}% of tile)")
    if m.any():
        print(f"   curl mean L {with_[m].mean():.4f}   the ground it covers {without[m].mean():.4f}"
              f"   delta {(with_[m]-without[m]).mean():+.4f}")
        print(f"   curl L range {with_[m].min():.3f}-{with_[m].max():.3f}"
              f"   |dL| mean {np.abs(d[m]).mean():.4f}  max {np.abs(d[m]).max():.4f}")
        ys, xs = np.nonzero(m)
        print(f"   bbox x[{xs.min()}-{xs.max()}] y[{ys.min()}-{ys.max()}]")
        if size <= 32:
            print("   per-pixel dL (x100):")
            sub = (d[ys.min():ys.max()+1, xs.min():xs.max()+1] * 100).round().astype(int)
            for row in sub:
                print("     " + " ".join(f"{v:4d}" for v in row))

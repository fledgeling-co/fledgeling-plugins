"""The interior floor, sampled directly on both images.

Ours: the bands where the roll's INNER face is what the viewer sees - recovered
exactly, by rebuilding with the interior forced to a flag colour, so no box is
guessed. Reference: the same part of its loop, boxed on its own render.
"""
import pathlib, subprocess, tempfile
import numpy as np
from PIL import Image

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
W = A / "loop-runs/r16/work"
REF = A / "icon-engineC-f5665d-2.png"
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


def sat(a):
    mx, mn = a.max(-1), a.min(-1)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)


# --- our inner face, flagged ---------------------------------------------
src = (A / "build_icon.py").read_text()
flag = src.replace('col = _lerp(col, TRANSMIT, max(0.0, lam) * 0.12)',
                   'col = (255, 0, 255)')
assert flag != src
tmp_py = A / "_flag_build.py"
tmp_py.write_text(flag)
keep = (A / "icon.svg").read_bytes()
try:
    subprocess.run(["python3", str(tmp_py)], cwd=A, check=True, capture_output=True)
    (W / "flag.svg").write_bytes((A / "icon.svg").read_bytes())
finally:
    (A / "icon.svg").write_bytes(keep)
    tmp_py.unlink(missing_ok=True)

fl = rgb_of(render_svg(W / "flag.svg"))
inner = (fl[..., 0] > 0.85) & (fl[..., 1] < 0.25) & (fl[..., 2] > 0.85)
cand = rgb_of(render_svg(A / "icon.svg"))
nocurl = rgb_of(render_svg(W / "no-curl.svg"))
ribbon = np.abs(lum(cand) - lum(nocurl)) > 0.004
outer = ribbon & ~inner
print(f"ribbon {ribbon.sum()} px = inner {inner.sum()} ({inner.sum()/ribbon.sum()*100:.1f}%) "
      f"+ outer {outer.sum()}")

for tag, m in (("MASTER inner face", inner), ("MASTER outer face", outer)):
    L = lum(cand)[m]
    g = lum(nocurl)[m]
    print(f"  {tag}: L min {L.min():.3f} p10 {np.percentile(L,10):.3f} med {np.median(L):.3f} "
          f"p90 {np.percentile(L,90):.3f} | ground under it {g.mean():.3f} | mean d {(L-g).mean():+.3f}")
    px = cand[m][L <= np.percentile(L, 10)]
    print(f"        darkest decile rgb ({px.mean(0)[0]:.3f},{px.mean(0)[1]:.3f},{px.mean(0)[2]:.3f}) "
          f"sat {sat(px).mean():.3f}")

# --- the reference's interior --------------------------------------------
ref = rgb_of(Image.open(REF).convert("RGB").resize((1024, 1024), Image.LANCZOS))
Lr = lum(ref)
# boxes read off reference-1024: the bore (seen through the loop) and the
# ribbon's most turned-away passage, the lower-left of the loop.
for tag, (y0, y1, x0, x1) in (("ref bore (through the loop)", (150, 260, 240, 350)),
                              ("ref lower-left ribbon", (250, 330, 185, 235)),
                              ("ref far wall inside top", (110, 175, 260, 400)),
                              ("ref ground beside the loop", (150, 300, 90, 160))):
    p = ref[y0:y1, x0:x1].reshape(-1, 3)
    L = lum(ref[y0:y1, x0:x1]).ravel()
    print(f"  {tag:30s} L min {L.min():.3f} p10 {np.percentile(L,10):.3f} "
          f"med {np.median(L):.3f} max {L.max():.3f}  sat {sat(p).mean():.3f}")

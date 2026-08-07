"""Post-edit verification.

1. Did the ribbon land on the numbers measured off C2 in w11/w12?
2. The rubric's three vetoes: figure-ground at 16, the 16px read, one light model.
"""
import pathlib, subprocess, tempfile
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


def sat(a):
    mx, mn = a.max(-1), a.min(-1)
    return np.where(mx > 1e-6, (mx - mn) / np.maximum(mx, 1e-6), 0.0)


inner = np.load(W / "inner.npy")
ribbon = np.load(W / "ribbon.npy")
outer = ribbon & ~inner
now = rgb_of(render_svg(A / "icon.svg"))
ground = lum(rgb_of(render_svg(W / "no-curl.svg")))
L = lum(now)

print("== 1. the ribbon, against C2's measured numbers")
d = L[ribbon] - ground[ribbon]
print(f"   ribbon  L p10 {np.percentile(L[ribbon],10):.3f} med {np.median(L[ribbon]):.3f} "
      f"p90 {np.percentile(L[ribbon],90):.3f}   (C2: 0.590 / 0.702 / 0.821)")
print(f"   below its ground by >0.15 {(d<-0.15).mean()*100:4.1f}%  >0.25 {(d<-0.25).mean()*100:4.1f}%  "
      f">0.35 {(d<-0.35).mean()*100:4.1f}%   (C2: 2.9 / 1.3 / 0.0)")
print(f"   inner face L min {L[inner].min():.3f} p10 {np.percentile(L[inner],10):.3f} "
      f"med {np.median(L[inner]):.3f}   (C2 bore p10 0.672 med 0.737; far wall p10 0.625 med 0.673)")
print(f"   outer face L p10 {np.percentile(L[outer],10):.3f} med {np.median(L[outer]):.3f} "
      f"p90 {np.percentile(L[outer],90):.3f}")
dk = now[ribbon][L[ribbon] <= np.percentile(L[ribbon], 5)]
print(f"   darkest 5% sat {sat(dk).mean():.3f}  rgb ({dk.mean(0)[0]:.3f},{dk.mean(0)[1]:.3f},"
      f"{dk.mean(0)[2]:.3f})   (C2 darkest 5% sat 0.203)")
print(f"   the roll still models: inner p10->p90 spread {np.percentile(L[inner],90)-np.percentile(L[inner],10):.3f}, "
      f"ribbon p10->p90 {np.percentile(L[ribbon],90)-np.percentile(L[ribbon],10):.3f}")

print("\n== 2. rubric vetoes")
g16 = lum(rgb_of(render_svg(A / "icon.svg", 16)))
print("   16px read (L x100):")
for row in (g16 * 100).round().astype(int):
    print("     " + " ".join(f"{v:3d}" for v in row))
print(f"   figure-ground at 16: tile L range {g16.min():.3f}-{g16.max():.3f}, "
      f"p90-p10 {np.percentile(g16,90)-np.percentile(g16,10):.3f}")

# one light model: is the ribbon's brightest side still the side the key is on?
ys, xs = np.nonzero(ribbon)
cy, cx = ys.mean(), xs.mean()
up = ribbon.copy(); up[int(cy):, :] = False
dn = ribbon.copy(); dn[:int(cy), :] = False
lf = ribbon.copy(); lf[:, int(cx):] = False
rt = ribbon.copy(); rt[:, :int(cx)] = False
print(f"   one light (key is up-and-left, LIGHT=(-0.36,-0.93)):")
print(f"     upper half L {L[up].mean():.3f}  vs lower half {L[dn].mean():.3f}   "
      f"{'OK top-lit' if L[up].mean() > L[dn].mean() else 'BROKEN'}")
print(f"     left  half L {L[lf].mean():.3f}  vs right half {L[rt].mean():.3f}")

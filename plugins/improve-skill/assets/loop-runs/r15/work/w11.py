"""Did the shipped render get the material that was measured off the reference?

before = r14's own candidate render, i.e. this round's baseline.
"""
import numpy as np
from PIL import Image
import common as C

r = C.ref()
c = np.asarray(Image.open("../../../icon.png").convert("RGB")).astype(float) / 255
prev = np.asarray(Image.open("../../r14/candidate-1024.png").convert("RGB")).astype(float)[..., :3] / 255

xs, ys = C.grid((1024, 1024))
lx, ly = C.to_local_top(xs, ys)
face = (lx > 30) & (lx < C.BLADE_LEN - 30) & (ly > 14) & (ly < C.BLADE_THICK - 14)
lxf, lyf = C.to_local(xs, ys)
trued = (lyf < -80) & (lyf > -400)
unplaned = (lyf > 90) & (lyf < 420)


def bands(L, m):
    out = {}
    for tag, (k1, k2) in [("1-3", (0, 1)), ("3-5", (1, 2)), ("5-9", (2, 4)), ("9-17", (4, 8))]:
        b = (C.boxblur(L, k1) if k1 else L) - C.boxblur(L, k2)
        out[tag] = b[m].std()
    return out


def report(name, img, m):
    L = C.lum(img)
    hp = L - C.boxblur(L, 6)
    d = hp[m] - hp[m].mean()
    print("%-7s mean %.4f  hp sd %.4f  skew %+.2f  bands %s"
          % (name, L[m].mean(), hp[m].std(), float((d ** 3).mean() / d.std() ** 3),
             " ".join("%s=%.4f" % kv for kv in bands(L, m).items())))


print("=== iron's top face (co-masked, interior) ===")
report("before", prev, face)
report("after", c, face)
report("ref", r, face)

print("\n=== means that must not move (polarity / figure-ground) ===")
for tag, m in (("face", face), ("trued", trued), ("unplaned", unplaned)):
    print("  %-9s before %.4f  after %.4f  (%+.4f)"
          % (tag, C.lum(prev)[m].mean(), C.lum(c)[m].mean(),
             C.lum(c)[m].mean() - C.lum(prev)[m].mean()))

print("\n=== does it survive downsampling ===")
for size in (256, 128):
    m2 = np.asarray(Image.fromarray((face * 255).astype(np.uint8)).resize((size, size), Image.NEAREST)) > 127
    for name, img in (("after", c), ("ref", r)):
        s = np.asarray(Image.fromarray((img * 255).astype(np.uint8)).resize((size, size), Image.LANCZOS)).astype(float) / 255
        L = C.lum(s)
        print("  %d %-5s hp sd %.4f" % (size, name, (L - C.boxblur(L, 2))[m2].std()))

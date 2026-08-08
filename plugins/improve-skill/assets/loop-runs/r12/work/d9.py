"""r12 rubric checks: figure-ground, the 16px read, and the single light model.

The gate is not the authority; these are. Run before/after on the same renders.
"""
import sys, pathlib, tempfile, math, numpy as np
sys.path.insert(0, "/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/scripts")
import fidelity as F

A = pathlib.Path("/Users/lukerhodes/Dev/fledgeling-plugins/plugins/improve-skill/assets")
svg = (A / "icon.svg").read_text()
ctl = pathlib.Path(tempfile.mkdtemp()) / "control.svg"
ctl.write_text(svg.replace('filter="url(#ironGrit)"', ""))

BLOCK = np.load("d_topface.npy") | np.load("d_front.npy")
ROUGH = np.load("d_rough.npy"); TRUED = np.load("d_trued.npy")

for size, lab in ((128, "128px"),):
    step = 1024 // size
    b = BLOCK[::step, ::step][:size, :size]
    r = ROUGH[::step, ::step][:size, :size]
    t = TRUED[::step, ::step][:size, :size]
    print(lab + " figure-ground (ground L : block L)")
    for nm, p in (("before", ctl), ("after ", A / "icon.svg")):
        g = F.to_gray(F.render_candidate(p, size))
        print("   %s  block %.4f | vs un-planed %.4f = %.2f:1 | vs trued %.4f = %.2f:1"
              % (nm, g[b].mean(), g[r].mean(), g[r].mean() / g[b].mean(),
                 g[t].mean(), g[t].mean() / g[b].mean()))

print()
print("16px read: p90-p10 spread, and the darkest/brightest cells")
for nm, p in (("before", ctl), ("after ", A / "icon.svg")):
    g = F.to_gray(F.render_candidate(p, 16))
    print("   %s  spread %.4f   min %.4f  max %.4f" % (nm, np.percentile(g, 90) - np.percentile(g, 10), g.min(), g.max()))

print()
print("single light: each corner's own ground mean as a ratio of that plane's mean")
for nm, p in (("before", ctl), ("after ", A / "icon.svg")):
    g = F.to_gray(F.render_candidate(p, 1024))
    tl = g[60:260, 60:260][ROUGH[60:260, 60:260]]
    bl = g[560:760, 60:260][ROUGH[560:760, 60:260]]
    br = g[760:960, 760:960][TRUED[760:960, 760:960]]
    print("   %s  TL %.3fx  BL %.3fx  (of un-planed mean %.4f)   BR %.3fx of trued %.4f"
          % (nm, tl.mean() / g[ROUGH].mean(), bl.mean() / g[ROUGH].mean(), g[ROUGH].mean(),
             br.mean() / g[TRUED].mean(), g[TRUED].mean()))
